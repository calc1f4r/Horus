---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: token
vulnerability_type: token_handling_vulnerabilities

# Attack Vector Details
attack_type: economic_exploit
affected_component: staking_module

# Technical Primitives
primitives:
  - fee_on_transfer_error
  - rebasing_token_error
  - token_approval_error
  - mint_unlimited
  - burn_error
  - token_transfer_hook
  - nft_handling_error
  - token_decimal_handling

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - cosmos_sdk
  - token
  - token_handling
  - fee_on_transfer
  - rebasing
  - token_approval
  - unlimited_mint
  - NFT
  - ERC20
  - ERC721
  
language: go
version: all
---

## References
- [bypassing-of-nft-collection-integrity-checks.md](../../../../reports/cosmos_cometbft_findings/bypassing-of-nft-collection-integrity-checks.md)
- [c-01-user-can-deny-opponent-nft-rewards-by-marking-safe-post-battle.md](../../../../reports/cosmos_cometbft_findings/c-01-user-can-deny-opponent-nft-rewards-by-marking-safe-post-battle.md)
- [h-02-protocoldao-lacks-a-method-to-take-out-ggp.md](../../../../reports/cosmos_cometbft_findings/h-02-protocoldao-lacks-a-method-to-take-out-ggp.md)
- [h-03-mishandling-of-receiving-hype-in-the-stakingmanager-user-cant-confirm-withd.md](../../../../reports/cosmos_cometbft_findings/h-03-mishandling-of-receiving-hype-in-the-stakingmanager-user-cant-confirm-withd.md)
- [h-05-failure-to-update-dirty-flag-in-transfertounoccupiedplot-prevents-reward-ac.md](../../../../reports/cosmos_cometbft_findings/h-05-failure-to-update-dirty-flag-in-transfertounoccupiedplot-prevents-reward-ac.md)
- [h-05-transferring-nativevault-tokens-can-break-some-functionalities.md](../../../../reports/cosmos_cometbft_findings/h-05-transferring-nativevault-tokens-can-break-some-functionalities.md)
- [h-1-stakingrewardsmanagertopup-misallocates-funds-to-stakingrewards-contracts.md](../../../../reports/cosmos_cometbft_findings/h-1-stakingrewardsmanagertopup-misallocates-funds-to-stakingrewards-contracts.md)
- [h-11-rewardsmanager-fails-to-validate-pool_-when-updating-exchange-rates-allowin.md](../../../../reports/cosmos_cometbft_findings/h-11-rewardsmanager-fails-to-validate-pool_-when-updating-exchange-rates-allowin.md)
- [h-2-yt-holder-are-unable-to-claim-their-interest.md](../../../../reports/cosmos_cometbft_findings/h-2-yt-holder-are-unable-to-claim-their-interest.md)
- [h-3-buyoutlien-will-cause-the-vault-to-fail-to-processepoch.md](../../../../reports/cosmos_cometbft_findings/h-3-buyoutlien-will-cause-the-vault-to-fail-to-processepoch.md)
- [missing-message-type-registrations-in-regulation-module.md](../../../../reports/cosmos_cometbft_findings/missing-message-type-registrations-in-regulation-module.md)
- [staked-tokens-can-be-destroyed-through-a-failed-challenge.md](../../../../reports/cosmos_cometbft_findings/staked-tokens-can-be-destroyed-through-a-failed-challenge.md)
- [m-10-minting-public-vault-shares-while-the-protocol-is-paused-can-lead-to-lp-fun.md](../../../../reports/cosmos_cometbft_findings/m-10-minting-public-vault-shares-while-the-protocol-is-paused-can-lead-to-lp-fun.md)
- [m-01-setbeforesendhook-can-never-delete-an-existing-store-due-to-vulnerable-vali.md](../../../../reports/cosmos_cometbft_findings/m-01-setbeforesendhook-can-never-delete-an-existing-store-due-to-vulnerable-vali.md)
- [m-17-the-gauge-status-wasnt-checked-before-reducing-the-users-gauge-weight.md](../../../../reports/cosmos_cometbft_findings/m-17-the-gauge-status-wasnt-checked-before-reducing-the-users-gauge-weight.md)
- [m-3-attacker-will-dos-lidovault-up-to-36-days-which-will-ruin-expected-apr-for-a.md](../../../../reports/cosmos_cometbft_findings/m-3-attacker-will-dos-lidovault-up-to-36-days-which-will-ruin-expected-apr-for-a.md)
- [registry-owner-can-be-set-as-appchain-owner.md](../../../../reports/cosmos_cometbft_findings/registry-owner-can-be-set-as-appchain-owner.md)
- [m-2-converter-cannot-be-changed-in-redeemer.md](../../../../reports/cosmos_cometbft_findings/m-2-converter-cannot-be-changed-in-redeemer.md)
- [m-8-the-pendle-version-of-lend-uses-the-wrong-function-for-swapping-fee-on-trans.md](../../../../reports/cosmos_cometbft_findings/m-8-the-pendle-version-of-lend-uses-the-wrong-function-for-swapping-fee-on-trans.md)
- [violations-of-erc-7562-rules.md](../../../../reports/cosmos_cometbft_findings/violations-of-erc-7562-rules.md)

## Vulnerability Title

**Token Transfer and Handling Vulnerabilities**

### Overview

This entry documents 6 distinct vulnerability patterns extracted from 24 audit reports (15 HIGH, 9 MEDIUM severity) across 21 protocols by 8 independent audit firms. These patterns represent recurring security issues in Cosmos SDK appchains and related staking/infrastructure protocols, validated through cross-auditor analysis.

### Vulnerability Description

#### Root Cause

These vulnerabilities fundamentally stem from:

1. **Missing state transition guards**: Critical operations lack proper checks for concurrent or conflicting state changes
2. **Incomplete accounting**: Balance, share, or reward tracking fails to account for edge cases (slashing, rebasing, pending operations)
3. **Timing window exploitation**: Race conditions between mempool visibility and transaction execution enable frontrunning attacks
4. **Cross-module inconsistency**: State tracked independently across modules can become desynchronized
5. **Insufficient validation**: Input parameters, state preconditions, or return values not properly validated

#### Attack Scenarios

#### Pattern 1: Token Transfer Hook

**Frequency**: 14/24 reports | **Severity**: HIGH | **Validation**: Strong (5 auditors)
**Protocols affected**: Astaria, Napier, Octopus Network, Telcoin Platform Audit, GoGoPool

This bug report is about the ProtocolDAO implementation not having a method to take out GGP. This means that it cannot handle GGP unless it is updated. The proof of concept states that the slashGGP() function will be executed and the GGP will be transferred to ProtocolDAO. However, the current Proto

**Example 1.1** [HIGH] — GoGoPool
Source: `h-02-protocoldao-lacks-a-method-to-take-out-ggp.md`
```solidity
// ❌ VULNERABLE: Token Transfer Hook
function slashGGP(address stakerAddr, uint256 ggpAmt) public onlySpecificRegisteredContract("MinipoolManager", msg.sender) {
        Vault vault = Vault(getContractAddress("Vault"));
        decreaseGGPStake(stakerAddr, ggpAmt);
        vault.transferToken("ProtocolDAO", ggp, ggpAmt);
    }
```

**Example 1.2** [HIGH] — GoGoPool
Source: `h-02-protocoldao-lacks-a-method-to-take-out-ggp.md`
```solidity
// ❌ VULNERABLE: Token Transfer Hook
contract ProtocolDAO is Base {
...

+    function spend(
+        address recipientAddress,
+        uint256 amount
+    ) external onlyGuardian {
+        Vault vault = Vault(getContractAddress("Vault"));
+        TokenGGP ggpToken = TokenGGP(getContractAddress("TokenGGP"));
+
+        if (amount == 0 || amount > vault.balanceOfToken("ProtocolDAO", ggpToken)) {
+            revert InvalidAmount();
+        }
+
+        vault.withdrawToken(recipientAddress, ggpToken, amount);
+
+        emit GGPTokensSentByDAOProtocol(address(this), recipientAddress, amount);
+   }
```

#### Pattern 2: Fee On Transfer Error

**Frequency**: 4/24 reports | **Severity**: MEDIUM | **Validation**: Strong (3 auditors)
**Protocols affected**: Astaria, Illuminate, Pimlico ERC20 Paymaster, Stakehouse Protocol

This bug report is about a vulnerability in the code for the GiantMevAndFeesPool contract. This vulnerability can be exploited by an attacker to transfer real LPTokens out of the GiantMevAndFeesPool contract. The proof of concept is that the contract does not check the validity of the _stakingFundsV

**Example 2.1** [HIGH] — Astaria
Source: `h-35-incorrect-fees-will-be-charged.md`
```solidity
// ❌ VULNERABLE: Fee On Transfer Error
uint256 initiatorPayment = transferAmount.mulDivDown(
      auction.initiatorFee,
      100
    );
```

**Example 2.2** [HIGH] — Astaria
Source: `h-35-incorrect-fees-will-be-charged.md`
```solidity
// ❌ VULNERABLE: Fee On Transfer Error
if (transferAmount >= lien.amount) {
          payment = lien.amount;
          transferAmount -= payment;
        } else {
          payment = transferAmount;
          transferAmount = 0;
        }

        if (payment > 0) {
          LIEN_TOKEN.makePayment(tokenId, payment, lien.position, payer);
        }
      }
```

#### Pattern 3: Mint Unlimited

**Frequency**: 2/24 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Astaria, Claynosaurz

The `staking_action::stake` function in the code has a vulnerability that allows an attacker to stake an invalid NFT. This is because the function only checks the `key` field of the collection structure, but not the `verified` field. This means that an attacker can create a fake NFT with the correct

**Example 3.1** [HIGH] — Claynosaurz
Source: `bypassing-of-nft-collection-integrity-checks.md`
```solidity
// ❌ VULNERABLE: Mint Unlimited
/// Stakes an NFT by delegating it to the global authority PDA.
pub fn stake(ctx: Context<StakingAction>) -> Result<()> {
    [...]
    // Deserialize Metadata to verify collection
    let nft_metadata = Metadata::safe_deserialize(&mut ctx.accounts.nft_metadata.to_account_info().data.borrow_mut()).unwrap();
    if let Some(collection) = nft_metadata.collection {
        if collection.key.to_string() != CLAYNO_COLLECTION_ADDRESS {
            return Err(error!(StakingError::WrongCollection));
        }
    } else {
        return Err(error!(StakingError::InvalidMetadata));
    };
    [...]
}
```

#### Pattern 4: Token Approval Error

**Frequency**: 2/24 reports | **Severity**: MEDIUM | **Validation**: Moderate (2 auditors)
**Protocols affected**: Coded Estate, Illuminate

This report describes a vulnerability in the Coded Estate contract that allows a malicious user to steal tokens without providing payment when the `auto_approve` feature is enabled. This is due to a lack of payment settlement logic in the `send_nft` function, which can be used to transfer tokens wit

**Example 4.1** [HIGH] — Coded Estate
Source: `h-08-adversary-can-use-send_nft-to-bypass-the-payment-and-steal-sellers-token-in.md`
```solidity
// ❌ VULNERABLE: Token Approval Error
File: contracts/codedestate/src/execute.rs
fn send_nft(
    &self,
    deps: DepsMut,
    env: Env,
    info: MessageInfo,
    contract: String,
    token_id: String,
    msg: Binary,
) -> Result<Response<C>, ContractError> {
    // Transfer token
    self._transfer_nft(deps, &env, &info, &contract, &token_id)?; // @c4-contest: just transfer token, no trade settlement logic

    let send = Cw721ReceiveMsg {
        sender: info.sender.to_string(),
        token_id: token_id.clone(),
        msg,
    };

    // Send message
    Ok(Response::new()
        .add_message(send.into_cosmos_msg(contract.clone())?)
        .add_attribute("action", "send_nft")
        .add_attribute("sender", info.sender)
        .add_attribute("recipient", contract)
        .add_attribute("token_id", token_id))
}


```

**Example 4.2** [MEDIUM] — Illuminate
Source: `m-2-converter-cannot-be-changed-in-redeemer.md`
```solidity
// ❌ VULNERABLE: Token Approval Error
/// @notice sets the converter address
    /// @param c address of the new converter
    /// @return bool true if successful
    function setConverter(address c) external authorized(admin) returns (bool) {
        converter = c;
        emit SetConverter(c);
        return true;
    }
```

#### Pattern 5: Nft Handling Error

**Frequency**: 1/24 reports | **Severity**: HIGH | **Validation**: Weak (1 auditors)
**Protocols affected**: Beetle

This bug report is about a function called `markBeetleSafe()` that allows users to protect their in-game assets in a game called BeetleBattle. The function only checks if the user owns the asset, but doesn't consider when or how the function is being used. This means that a malicious user can wait u

**Example 5.1** [HIGH] — Beetle
Source: `c-01-user-can-deny-opponent-nft-rewards-by-marking-safe-post-battle.md`
```solidity
// ❌ VULNERABLE: Nft Handling Error
function markBeetleSafe(uint256 _tokenId) public {
  if (isStaked[_tokenId] != msg.sender) revert InvalidTokenOwner();
  safeBeetle[msg.sender] = _tokenId;

  emit SafeBeetleUpdated(msg.sender, _tokenId);
}
```

#### Pattern 6: Rebasing Token Error

**Frequency**: 1/24 reports | **Severity**: MEDIUM | **Validation**: Weak (1 auditors)
**Protocols affected**: Yieldy

A bug was discovered in the code for a contract called "Staking.sol" that can be found at the provided GitHub link. This bug creates a huge arbitrage opportunity for someone who deposits before the rebase. This person can then call the "instantUnstakeReserve" or "instantUnstakeCurve" to unstake the 

**Example 6.1** [MEDIUM] — Yieldy
Source: `m-04-arbitrage-on-stake.md`
```solidity
// ❌ VULNERABLE: Rebasing Token Error
File: Staking.sol
406:     function stake(uint256 _amount, address _recipient) public { // @audit-info [HIGH] 
407:         // if override staking, then don't allow stake
408:         require(!isStakingPaused, "Staking is paused");
409:         // amount must be non zero
410:         require(_amount > 0, "Must have valid amount");
411: 
412:         uint256 yieldyTotalSupply = IYieldy(YIELDY_TOKEN).totalSupply();
413: 
414:         // Don't rebase unless tokens are already staked or could get locked out of staking
415:         if (yieldyTotalSupply > 0) {
416:             rebase();
417:         }
418: 
419:         IERC20Upgradeable(STAKING_TOKEN).safeTransferFrom(
420:             msg.sender,
421:             address(this),
422:             _amount
423:         );
424: 
425:         Claim
```


### Impact Analysis

#### Technical Impact
- State corruption across staking/delegation modules
- Incorrect balance tracking leading to fund misallocation
- Protocol liveness degradation or complete halt
- Loss of economic security guarantees

#### Business Impact
- Direct financial loss for stakers/delegators: Documented in 15 HIGH severity findings
- Protocol insolvency risk due to accounting errors
- Erosion of trust in validator/operator incentive alignment
- Cascading effects across DeFi protocols built on affected infrastructure

#### Frequency Analysis
- Total reports analyzed: 24
- HIGH severity: 15 (62%)
- MEDIUM severity: 9 (37%)
- Unique protocols affected: 21
- Independent audit firms: 8
- Patterns with 3+ auditor validation (Strong): 2

### Detection Patterns

#### Code Patterns to Look For
```
- Missing balance update before/after token transfers
- Unchecked return values from staking/delegation operations
- State reads without freshness validation
- Arithmetic operations without overflow/precision checks
- Missing access control on state-modifying functions
- Linear iterations over unbounded collections
- Race condition windows in multi-step operations
```

#### Audit Checklist
- [ ] Verify all staking state transitions update balances atomically
- [ ] Check that slashing affects all relevant state (pending, queued, active)
- [ ] Ensure withdrawal requests cannot bypass cooldown periods
- [ ] Validate that reward calculations handle all edge cases (zero stake, partial periods)
- [ ] Confirm access control on all administrative and state-modifying functions
- [ ] Test for frontrunning vectors in all two-step operations
- [ ] Verify iteration bounds on all loops processing user-controlled data
- [ ] Check cross-module state consistency after complex operations

### Keywords for Search

> `token-handling`, `fee-on-transfer`, `rebasing`, `token-approval`, `unlimited-mint`, `NFT`, `ERC20`, `ERC721`, `decimal-handling`, `cosmos-sdk`, `appchain`, `CometBFT`, `staking-security`, `validator-security`

### Related Vulnerabilities

- Slashing evasion bypass patterns
- Epoch snapshot timing manipulation
- Chain halt DoS vectors
- EVM-Cosmos state synchronization issues
- IBC middleware vulnerabilities
