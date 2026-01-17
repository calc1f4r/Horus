---
# Core Classification
protocol: generic
chain: cosmos
category: module-accounting
vulnerability_type: fund_accounting_error

# Attack Vector Details
attack_type: economic_exploit
affected_component: cosmos_sdk_modules

# Technical Primitives
primitives:
  - module_account
  - bank_keeper
  - SendCoins
  - MintCoins
  - BurnCoins
  - community_pool
  - token_supply
  - escrow_account

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos-sdk
  - module-account
  - bank
  - mint
  - burn
  - supply
  - accounting
  - escrow
  - fund-transfer

# Version Info
language: go
version: all
---

## References
- [ref-1]: reports/cosmos_cometbft_findings/h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md
- [ref-2]: reports/cosmos_cometbft_findings/m-26-zeta-token-supply-keeps-growing-on-failed-onreceive-contract-calls.md
- [ref-3]: reports/cosmos_cometbft_findings/m-11-attacker-can-freeze-users-first-rewards.md
- [ref-4]: reports/cosmos_cometbft_findings/m-1-pushing-same-tranchid-to-the-tokenidtotranches-will-inflate-stakednxm-accoun.md
- [ref-5]: reports/cosmos_cometbft_findings/h-7-removestakes-and-removedelegatestakes-silently-handle-errors-in-endblocker.md
- [ref-6]: reports/cosmos_cometbft_findings/linear-iteration-over-undelegations-with-unmetered-token-transfers-expose-a-perm.md

## Vulnerability Title

**Cross-Module Fund Transfer and Token Supply Accounting Vulnerabilities**

### Overview

Cosmos SDK applications use module accounts and bank keeper functions (`SendCoins`, `MintCoins`, `BurnCoins`) for token management across modules. Critical vulnerabilities arise when fund transfers between module accounts have incorrect accounting logic, temporary contexts are not properly committed/rolled back, or token supply invariants are violated during cross-chain and cross-module operations.

### Root Cause Statement

This vulnerability exists because **incorrect fund transfer logic or missing atomicity guarantees** in cross-module operations allows **token supply inflation, accounting mismatches, or stuck funds** leading to **permanent fund loss, protocol insolvency, or DoS attacks**.

### Vulnerability Description

#### Root Cause

The fundamental issues are:

1. **Incorrect iteration over coin amounts** - Processing entire `sdk.Coins` instead of individual `sdk.Coin` in loops
2. **Non-atomic operations with temporary contexts** - Minting tokens before EVM calls without rollback on failure
3. **Missing withdrawal address configuration** - Rewards sent to contract addresses that cannot retrieve them
4. **Duplicate accounting entries** - Same IDs pushed multiple times inflating tracked balances
5. **Silent error handling in fund transfers** - Errors swallowed during `SendCoinsFromModuleToAccount`

#### Attack Scenario

**Scenario 1: Double Fund Transfer via Iteration Bug (HIGH) [[ref-1]]**

1. ERC20Keeper receives multiple coins to burn via `BurnCoins()`
2. Loop iterates over `amount sdk.Coins` but sends entire `amount` on first match
3. If first coin is ERC20Denom, entire `amount` sent to community pool
4. Subsequent iterations process remaining coins normally
5. Result: double the funds transferred - coins duplicated or lost

```go
// VULNERABLE: Sends entire 'amount' instead of 'coin'
func (k ERC20Keeper) BurnCoins(ctx context.Context, addr sdk.AccAddress, amount sdk.Coins) error {
    for _, coin := range amount {
        if types.IsERC20Denom(coin.Denom) {
            // BUG: Sends all coins, not just the matching one
            if err := k.communityPoolKeeper.FundCommunityPool(ctx, amount, evmAddr.Bytes()); err != nil {
                return err
            }
            continue
        }
        // Other processing...
    }
    return nil
}
```

**Scenario 2: Token Supply Inflation via Failed EVM Call (MEDIUM) [[ref-2]]**

1. Cross-chain message triggers ZETA token mint to fungible module
2. Temporary context used for subsequent `onReceive()` EVM call
3. EVM call reverts but mint is committed to fungible module
4. Tokens minted without corresponding deposit on source chain
5. Attacker repeats 185 times to hit 1.85B ZETA cap causing DoS

```go
// VULNERABLE: Mint committed even if onReceive fails
func CallOnReceiveZevmConnector() {
    // Mint tokens to module account
    DepositCoinsToFungibleModule(ctx, amount)  // Committed!
    
    // EVM call may fail but mint already committed
    _, err := k.CallEVM(ctx, onReceiveParams...)
    if err != nil {
        return err  // Tokens remain minted!
    }
}
```

**Scenario 3: Rewards Frozen via Withdrawal Address Attack (MEDIUM) [[ref-3]]**

1. User deploys validator-staking contract
2. Contract stakes tokens and accrues rewards
3. Attacker front-runs first claim with small stake on behalf of user
4. Cosmos SDK distributes rewards to contract address (default)
5. Rewards stuck permanently - contract has no retrieve function

**Scenario 4: Duplicate ID Accounting Inflation (MEDIUM) [[ref-4]]**

1. Staking contract tracks tranche IDs in array
2. Same tranche ID pushed multiple times without uniqueness check
3. `stakedNxm` calculation iterates array, counting duplicates
4. Total assets inflated leading to incorrect mint/redeem ratios
5. Users receive more tokens than entitled during redemption

### Vulnerable Pattern Examples

#### Example 1: Incorrect Amount in Loop Iteration [[ref-1]]

```go
// SEVERITY: HIGH
// Sends entire amount instead of individual coin
for _, coin := range amount {
    if types.IsERC20Denom(coin.Denom) {
        // Should be: sdk.Coins{coin}
        k.communityPoolKeeper.FundCommunityPool(ctx, amount, addr)
        continue
    }
}
```

#### Example 2: Non-Atomic Mint and Call [[ref-2]]

```go
// SEVERITY: MEDIUM
// Mint happens before EVM call, not rolled back on failure
func (k Keeper) DepositAndCall(ctx context.Context, amount sdk.Coin) error {
    // Mint committed immediately
    err := k.bankKeeper.MintCoins(ctx, types.ModuleName, sdk.NewCoins(amount))
    if err != nil {
        return err
    }
    
    // If this fails, mint is still committed!
    _, err = k.evmKeeper.CallContract(ctx, params...)
    return err
}
```

#### Example 3: Silent Error in Module Fund Transfer [[ref-5]]

```go
// SEVERITY: HIGH
// Error swallowed, state corruption occurs silently
func RemoveStakes(ctx sdk.Context, stakeRemoval types.StakeRemoval) {
    coins := sdk.NewCoins(sdk.NewCoin(types.DefaultBondDenom, stakeRemoval.Amount))
    
    err = k.SendCoinsFromModuleToAccount(ctx, types.ModuleName, stakeRemoval.Reputer, coins)
    if err != nil {
        // BUG: Only logs error, continues execution!
        sdkCtx.Logger().Error("failed to send coins", "error", err)
        return  // State already modified, funds not transferred
    }
}
```

#### Example 4: Rewards Sent to Wrong Address [[ref-3]]

```rust
// SEVERITY: MEDIUM
// No withdrawal address set, rewards go to contract
fn execute_stake(deps: DepsMut, info: MessageInfo) -> Result<Response, ContractError> {
    let msg = StakingMsg::Delegate {
        validator: validator_addr.clone(),
        amount: coin,
    };
    
    // BUG: No SetWithdrawAddress message sent!
    // Rewards will go to this contract, not owner
    Ok(Response::new().add_message(msg))
}
```

#### Example 5: Duplicate Entry Inflation [[ref-4]]

```solidity
// SEVERITY: MEDIUM
// Same trancheId can be pushed multiple times
function stake(uint256 tokenId, uint256 _trancheId) external {
    // BUG: No check if _trancheId already exists!
    tokenIdToTranches[tokenId].push(_trancheId);
}

function stakedNxm() public view returns (uint256 assets) {
    uint256[] memory trancheIds = tokenIdToTranches[tokenId];
    for (uint256 j = 0; j < trancheIds.length; j++) {
        // Duplicate IDs counted multiple times!
        assets += getDepositValue(trancheIds[j]);
    }
}
```

### Secure Implementation Examples

#### Secure Pattern 1: Correct Coin Iteration

```go
// SECURE: Process each coin individually
for _, coin := range amount {
    if types.IsERC20Denom(coin.Denom) {
        // Send only this specific coin
        if err := k.communityPoolKeeper.FundCommunityPool(
            ctx, 
            sdk.NewCoins(coin),  // Single coin, not entire amount
            evmAddr.Bytes(),
        ); err != nil {
            return err
        }
        continue
    }
    // Process non-ERC20 coins
    if err := k.sudoBurn(ctx, coin); err != nil {
        return err
    }
}
```

#### Secure Pattern 2: Atomic Context with Rollback

```go
// SECURE: Use temporary context for atomicity
func (k Keeper) DepositAndCall(ctx context.Context, amount sdk.Coin) error {
    // Create temporary context
    cacheCtx, commit := ctx.CacheContext()
    
    // Mint in temporary context
    err := k.bankKeeper.MintCoins(cacheCtx, types.ModuleName, sdk.NewCoins(amount))
    if err != nil {
        return err
    }
    
    // Call contract in temporary context
    _, err = k.evmKeeper.CallContract(cacheCtx, params...)
    if err != nil {
        // Don't commit - both operations rolled back
        return err
    }
    
    // Only commit if both operations succeed
    commit()
    return nil
}
```

#### Secure Pattern 3: Error Handling with State Rollback

```go
// SECURE: Use cache context and rollback on errors
func RemoveStakes(ctx sdk.Context, stakeRemoval types.StakeRemoval) error {
    cacheSdkCtx, write := ctx.CacheContext()
    
    coins := sdk.NewCoins(sdk.NewCoin(types.DefaultBondDenom, stakeRemoval.Amount))
    
    err := k.SendCoinsFromModuleToAccount(cacheSdkCtx, types.ModuleName, stakeRemoval.Reputer, coins)
    if err != nil {
        // Cache context discarded, state unchanged
        return errors.Wrap(err, "failed to send coins")
    }
    
    // Only write if transfer succeeded
    write()
    return nil
}
```

#### Secure Pattern 4: Set Withdrawal Address Before Staking

```rust
// SECURE: Set withdrawal address before any staking
fn execute_stake(deps: DepsMut, info: MessageInfo) -> Result<Response, ContractError> {
    let config = CONFIG.load(deps.storage)?;
    
    // First set withdrawal address
    let set_withdraw_msg = DistributionMsg::SetWithdrawAddress {
        address: config.owner.to_string(),
    };
    
    // Then delegate
    let delegate_msg = StakingMsg::Delegate {
        validator: validator_addr.clone(),
        amount: coin,
    };
    
    Ok(Response::new()
        .add_message(set_withdraw_msg)
        .add_message(delegate_msg))
}
```

#### Secure Pattern 5: Uniqueness Check Before Push

```solidity
// SECURE: Check for duplicates before adding
function stake(uint256 tokenId, uint256 _trancheId) external {
    // Check if trancheId already exists
    uint256[] storage tranches = tokenIdToTranches[tokenId];
    for (uint256 i = 0; i < tranches.length; i++) {
        if (tranches[i] == _trancheId) {
            revert TrancheIdAlreadyExists();
        }
    }
    
    tranches.push(_trancheId);
}

// Alternative: Use mapping for O(1) lookup
mapping(uint256 => mapping(uint256 => bool)) private trancheExists;

function stake(uint256 tokenId, uint256 _trancheId) external {
    if (trancheExists[tokenId][_trancheId]) {
        return; // Already tracked
    }
    trancheExists[tokenId][_trancheId] = true;
    tokenIdToTranches[tokenId].push(_trancheId);
}
```

### Impact Analysis

| Impact Category | Description | Severity |
|-----------------|-------------|----------|
| **Token Supply Inflation** | Minting without corresponding deposit breaks supply invariant | HIGH |
| **Permanent Fund Loss** | Tokens sent to wrong address or contract without retrieve capability | HIGH |
| **Protocol Insolvency** | Accounting inflation leads to more claims than assets | HIGH |
| **Chain DoS** | Supply cap reached prevents all deposits | MEDIUM |
| **Unfair Distribution** | Duplicate entries give some users more than entitled | MEDIUM |

### Affected Scenarios

1. **Cross-Chain Bridges**: Token mint/burn with EVM calls requiring atomicity
2. **Staking Rewards Distribution**: Withdrawal address configuration
3. **Token Factory Operations**: MintCoins/BurnCoins in custom keepers
4. **Module Account Transfers**: SendCoinsFromModuleToAccount error handling
5. **Accounting Arrays**: Tracking deposits, tranches, or delegations

### Detection Patterns

```go
// Pattern 1: Check for amount vs coin in loops
for _, coin := range amount {
    // Look for uses of 'amount' instead of 'coin'
    FundCommunityPool(ctx, amount, ...)  // VULNERABLE
}

// Pattern 2: Check for atomicity in multi-step operations
k.bankKeeper.MintCoins(ctx, ...)
k.evmKeeper.CallContract(ctx, ...)  // If this fails, mint persists

// Pattern 3: Check for swallowed errors
err = k.SendCoinsFromModuleToAccount(...)
if err != nil {
    logger.Error(err)
    return  // Not returning error, state corrupted
}

// Pattern 4: Check for missing withdrawal address
StakingMsg::Delegate { validator, amount }
// Missing: DistributionMsg::SetWithdrawAddress
```

### Audit Checklist

- [ ] Bank keeper operations in loops use correct coin vs amount
- [ ] Multi-step operations use CacheContext with proper commit/rollback
- [ ] Error handling in module fund transfers propagates errors correctly
- [ ] Withdrawal addresses set before staking operations
- [ ] Array tracking operations check for duplicate entries
- [ ] Token supply invariants maintained after all operations
- [ ] Silent error handling in EndBlocker fund operations reviewed
- [ ] Cross-module fund flows have proper atomicity guarantees

### Real-World Examples

| Protocol | Vulnerability | Severity | Auditor |
|----------|--------------|----------|---------|
| Initia MiniEVM | BurnCoins sends entire amount instead of single coin | HIGH | Code4rena |
| ZetaChain | ZETA supply grows on failed onReceive calls | MEDIUM | Sherlock |
| Andromeda | Rewards frozen via front-run staking attack | MEDIUM | Sherlock |
| stNXM | Duplicate tranche IDs inflate staked accounting | MEDIUM | Sherlock |
| Allora | RemoveStakes silently swallows SendCoins errors | HIGH | Sherlock |
| MilkyWay | Unmetered SendCoins in undelegation batches | HIGH | Sherlock |

### Keywords

cross-module fund transfer, module account, bank keeper, SendCoins, MintCoins, BurnCoins, token supply inflation, accounting error, community pool, escrow account, cache context, atomicity, withdrawal address, duplicate entries, silent error, fund loss, supply invariant, cosmos-sdk modules
