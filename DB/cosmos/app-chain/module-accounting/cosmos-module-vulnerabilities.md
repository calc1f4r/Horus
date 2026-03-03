---
protocol: generic
chain: cosmos
category: module_accounting
vulnerability_type: cosmos_module_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: module_accounting_logic

primitives:
  - bank_error
  - auth_error
  - distribution
  - staking_specific
  - slashing_specific
  - evidence
  - crisis
  - capability

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - module_accounting
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Module Bank Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-03] Unlimited Nibi could be minted because evm and bank b | `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md` | HIGH | Code4rena |
| [H-06] Hardcoded gas used in ERC20 queries allows for block  | `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md` | HIGH | Code4rena |
| Integer Overflow in AddExternalIncentive Function | `reports/cosmos_cometbft_findings/integer-overflow-in-addexternalincentive-function.md` | HIGH | Halborn |
| [PRST-4] Unbonding of validators does not give priority to i | `reports/cosmos_cometbft_findings/prst-4-unbonding-of-validators-does-not-give-priority-to-inactive-validators.md` | MEDIUM | Hexens |
| [PRST-6] First depositor can steal assets due to missing sli | `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md` | HIGH | Hexens |
| Risk of token/uToken exchange rate manipulation | `reports/cosmos_cometbft_findings/risk-of-tokenutoken-exchange-rate-manipulation.md` | HIGH | TrailOfBits |

### Module Auth Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-03] Unlimited Nibi could be minted because evm and bank b | `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md` | HIGH | Code4rena |
| Integer Overflow in AddExternalIncentive Function | `reports/cosmos_cometbft_findings/integer-overflow-in-addexternalincentive-function.md` | HIGH | Halborn |
| [M-01] Reentrancy Check in `lock_staking::reentry_check` Cau | `reports/cosmos_cometbft_findings/m-01-reentrancy-check-in-lock_stakingreentry_check-causes-concurrent-init-deposi.md` | MEDIUM | Code4rena |
| [M-02] Deposits might fail if staking module account is not  | `reports/cosmos_cometbft_findings/m-02-deposits-might-fail-if-staking-module-account-is-not-activated.md` | MEDIUM | Pashov Audit Group |
| [M-05] Last Holder Can’t Exit, Zero‑Supply Unstake Reverts | `reports/cosmos_cometbft_findings/m-05-last-holder-cant-exit-zerosupply-unstake-reverts.md` | MEDIUM | Code4rena |
| Lockup of vestings or completion time can be bypassed due to | `reports/cosmos_cometbft_findings/m-14-lockup-of-vestings-or-completion-time-can-be-bypassed-due-to-missing-check-.md` | MEDIUM | Sherlock |
| [M-26] ZRC20 Token Pause Check Bypass | `reports/cosmos_cometbft_findings/m-26-zrc20-token-pause-check-bypass.md` | MEDIUM | Code4rena |
| [PRST-4] Unbonding of validators does not give priority to i | `reports/cosmos_cometbft_findings/prst-4-unbonding-of-validators-does-not-give-priority-to-inactive-validators.md` | MEDIUM | Hexens |

### Module Distribution
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| CVGT Staking Pool State Manipulation | `reports/cosmos_cometbft_findings/cvgt-staking-pool-state-manipulation.md` | HIGH | OtterSec |
| Delegated Boost Persists Even If veRAAC Is Withdrawn/Reduced | `reports/cosmos_cometbft_findings/delegated-boost-persists-even-if-veraac-is-withdrawnreduced.md` | MEDIUM | Codehawks |
| [H-01] Wrong handling of ERC20 denoms in `ERC20Keeper::BurnC | `reports/cosmos_cometbft_findings/h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md` | HIGH | Code4rena |
| Owner is able to withdraw staking token. | `reports/cosmos_cometbft_findings/owner-is-able-to-withdraw-staking-token.md` | HIGH | Zokyo |
| Staking and withdrawal operations might be blocked. | `reports/cosmos_cometbft_findings/staking-and-withdrawal-operations-might-be-blocked.md` | MEDIUM | Zokyo |

### Module Staking Specific
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| [H-03] Unlimited Nibi could be minted because evm and bank b | `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md` | HIGH | Code4rena |
| Inconsistencies in Slash Redelegation | `reports/cosmos_cometbft_findings/inconsistencies-in-slash-redelegation.md` | MEDIUM | OtterSec |
| [M-07] `Vested CSX` to `Regular CSX` Conversion Process Enab | `reports/cosmos_cometbft_findings/m-07-vested-csx-to-regular-csx-conversion-process-enables-potential-unauthorized.md` | MEDIUM | Shieldify |
| [M-26] ZRC20 Token Pause Check Bypass | `reports/cosmos_cometbft_findings/m-26-zrc20-token-pause-check-bypass.md` | MEDIUM | Code4rena |
| Missing _grantRole for KEEPER_ROLE will prevent calling of c | `reports/cosmos_cometbft_findings/missing-_grantrole-for-keeper_role-will-prevent-calling-of-critical-keeper-funct.md` | HIGH | Spearbit |
| [PRST-4] Unbonding of validators does not give priority to i | `reports/cosmos_cometbft_findings/prst-4-unbonding-of-validators-does-not-give-priority-to-inactive-validators.md` | MEDIUM | Hexens |
| [PRST-6] First depositor can steal assets due to missing sli | `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md` | HIGH | Hexens |

### Module Slashing Specific
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Bond Curve is Not Reset Inside the `submitInitialSlashing` F | `reports/cosmos_cometbft_findings/bond-curve-is-not-reset-inside-the-submitinitialslashing-function.md` | MEDIUM | MixBytes |
| Message is indexed as refundable even if the signature was o | `reports/cosmos_cometbft_findings/m-2-message-is-indexed-as-refundable-even-if-the-signature-was-over-a-fork.md` | MEDIUM | Sherlock |
| `slash` calls can be blocked, allowing malicious users to by | `reports/cosmos_cometbft_findings/m-2-slash-calls-can-be-blocked-allowing-malicious-users-to-bypass-the-slashing-m.md` | MEDIUM | Sherlock |
| Slashing fails if claims revert | `reports/cosmos_cometbft_findings/m-6-slashing-fails-if-claims-revert.md` | MEDIUM | Sherlock |
| Slashing of re-delegated stake is computed incorrectly | `reports/cosmos_cometbft_findings/slashing-of-re-delegated-stake-is-computed-incorrectly.md` | MEDIUM | TrailOfBits |

### Module Evidence
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Fund Distribution May Not Incentivize Users to Participate | `reports/cosmos_cometbft_findings/fund-distribution-may-not-incentivize-users-to-participate.md` | MEDIUM | Quantstamp |
| Relayer Can Submit Undisputable Evidence for L2->L1 Trades | `reports/cosmos_cometbft_findings/relayer-can-submit-undisputable-evidence-for-l2-l1-trades.md` | HIGH | Quantstamp |
| Relayer Can Use Valid Evidence of One Trade to Avoid Getting | `reports/cosmos_cometbft_findings/relayer-can-use-valid-evidence-of-one-trade-to-avoid-getting-slashed-for-another.md` | HIGH | Quantstamp |
| Using `abi.encodePacked()`can Lead to Hash Collisions | `reports/cosmos_cometbft_findings/using-abiencodepackedcan-lead-to-hash-collisions.md` | HIGH | Quantstamp |

### Module Crisis
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| DoS in Cosmos SDK Crisis Module (github.com/cosmos/cosmos-sd | `reports/cosmos_cometbft_findings/dos-in-cosmos-sdk-crisis-module-githubcomcosmoscosmos-sdkxcrisis.md` | MEDIUM | Zokyo |

### Module Capability
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-03] Attacker Can Desynchronize Supply Snapshot During Sam | `reports/cosmos_cometbft_findings/m-03-attacker-can-desynchronize-supply-snapshot-during-same-block-unstake-reduci.md` | MEDIUM | Code4rena |

---

# Cosmos Module Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Cosmos Module Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Module Bank Error](#1-module-bank-error)
2. [Module Auth Error](#2-module-auth-error)
3. [Module Distribution](#3-module-distribution)
4. [Module Staking Specific](#4-module-staking-specific)
5. [Module Slashing Specific](#5-module-slashing-specific)
6. [Module Evidence](#6-module-evidence)
7. [Module Crisis](#7-module-crisis)
8. [Module Capability](#8-module-capability)

---

## 1. Module Bank Error

### Overview

Implementation flaw in module bank error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 6 audit reports with severity distribution: HIGH: 5, MEDIUM: 1.

> **Key Finding**: The `NibiruBankKeeper.SyncStateDBWithAccount` function in `bank_extension.go` is responsible for keeping the EVM state database (`StateDB`) in sync with bank account balances. However, this function is not being called by all operations that modify bank balances. This means that the EVM state databa

### Vulnerability Description

#### Root Cause

Implementation flaw in module bank error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies module bank error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to module operations

### Vulnerable Pattern Examples

**Example 1: [H-03] Unlimited Nibi could be minted because evm and bank balance are not synce** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md`
```go
func (bk *NibiruBankKeeper) SyncStateDBWithAccount(
	ctx sdk.Context, acc sdk.AccAddress,
) {
	// If there's no StateDB set, it means we're not in an EthereumTx.
	if bk.StateDB == nil {
		return
	}
	balanceWei := evm.NativeToWei(
		bk.GetBalance(ctx, acc, evm.EVMBankDenom).Amount.BigInt(),
	)
	bk.StateDB.SetBalanceWei(eth.NibiruAddrToEthAddr(acc), balanceWei)
}
```

**Example 2: [H-06] Hardcoded gas used in ERC20 queries allows for block production halt from** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md`
```go
File: funtoken.go
265: func (p precompileFunToken) balance(
266: 	start OnRunStartResult,
267: 	contract *vm.Contract,
268: ) (bz []byte, err error) {
---
285: 	erc20Bal, err := p.evmKeeper.ERC20().BalanceOf(funtoken.Erc20Addr.Address, addrEth, ctx)
286: 	if err != nil {
287: 		return
288: 	}
```

**Example 3: Integer Overflow in AddExternalIncentive Function** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/integer-overflow-in-addexternalincentive-function.md`
```go
amount := msg.AmountPerBlock.Mul(sdk.NewInt(int64(msg.ToBlock - msg.FromBlock)))
```

**Example 4: [PRST-4] Unbonding of validators does not give priority to inactive validators** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/prst-4-unbonding-of-validators-does-not-give-priority-to-inactive-validators.md`
```
// Vulnerable pattern from Persistence:
**Severity:** Medium

**Path:** x/liquidstake/keeper/liquidstake.go:LiquidUnstake#L344-L459

**Description:**

When a user wants to withdraw their `stkXPRT` for `xprt`, they will call `LiquidUnstake`. In the function, the module will back out delegations for each validator according to their weight for a total of the unbonding amount. The module takes the whole set of validators and does not check their active status.

By not giving priority to unbonding inactive validators first, it will furthe
```

**Example 5: Risk of token/uToken exchange rate manipulation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/risk-of-tokenutoken-exchange-rate-manipulation.md`
```go
func (k Keeper) TotalUTokenSupply(ctx sdk.Context, uTokenDenom string) sdk.Coin {
    if k.IsAcceptedUToken(ctx, uTokenDenom) {
        return k.bankKeeper.GetSupply(ctx, uTokenDenom)
        // TODO - Question: Does bank module still track balances sent (locked) via IBC?
        // If it doesn't then the balance returned here would decrease when the tokens
        // are sent off, which is not what we want. In that case, the keeper should keep
        // an sdk.Int total supply for each uToken type.
    }
    return sdk.NewCoin(uTokenDenom, sdk.ZeroInt())
}
```

**Variant: Module Bank Error in Nibiru** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md`
> - `reports/cosmos_cometbft_findings/h-06-hardcoded-gas-used-in-erc20-queries-allows-for-block-production-halt-from-i.md`

**Variant: Module Bank Error in Persistence** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/prst-4-unbonding-of-validators-does-not-give-priority-to-inactive-validators.md`
> - `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in module bank error logic allows exploitation through missing validation, incor
func secureModuleBankError(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 6 audit reports
- **Severity Distribution**: HIGH: 5, MEDIUM: 1
- **Affected Protocols**: Cosmos Module, Nibiru, Umee, Persistence
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Module Auth Error

### Overview

Implementation flaw in module auth error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 8 audit reports with severity distribution: HIGH: 2, MEDIUM: 6.

> **Key Finding**: The `NibiruBankKeeper.SyncStateDBWithAccount` function in `bank_extension.go` is responsible for keeping the EVM state database (`StateDB`) in sync with bank account balances. However, this function is not being called by all operations that modify bank balances. This means that the EVM state databa

### Vulnerability Description

#### Root Cause

Implementation flaw in module auth error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies module auth error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to module operations

### Vulnerable Pattern Examples

**Example 1: [H-03] Unlimited Nibi could be minted because evm and bank balance are not synce** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md`
```go
func (bk *NibiruBankKeeper) SyncStateDBWithAccount(
	ctx sdk.Context, acc sdk.AccAddress,
) {
	// If there's no StateDB set, it means we're not in an EthereumTx.
	if bk.StateDB == nil {
		return
	}
	balanceWei := evm.NativeToWei(
		bk.GetBalance(ctx, acc, evm.EVMBankDenom).Amount.BigInt(),
	)
	bk.StateDB.SetBalanceWei(eth.NibiruAddrToEthAddr(acc), balanceWei)
}
```

**Example 2: Integer Overflow in AddExternalIncentive Function** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/integer-overflow-in-addexternalincentive-function.md`
```go
amount := msg.AmountPerBlock.Mul(sdk.NewInt(int64(msg.ToBlock - msg.FromBlock)))
```

**Example 3: [M-01] Reentrancy Check in `lock_staking::reentry_check` Causes Concurrent INIT ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-reentrancy-check-in-lock_stakingreentry_check-causes-concurrent-init-deposi.md`
```go
fun reentry_check(
    staking_account: &mut StakingAccount,
    with_update: bool
) {
    let (height, _) = block::get_block_info();
    assert!(staking_account.last_height != height, error::invalid_state(EREENTER));

    if (with_update) {
        staking_account.last_height = height;
    };
}
```

**Example 4: [M-02] Deposits might fail if staking module account is not activated** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-deposits-might-fail-if-staking-module-account-is-not-activated.md`
```
// Vulnerable pattern from stHYPE_2025-10-13:
_Resolved_
```

**Example 5: Lockup of vestings or completion time can be bypassed due to missing check for s** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-14-lockup-of-vestings-or-completion-time-can-be-bypassed-due-to-missing-check-.md`
```rust
pub struct Batch {
    /// The amount of tokens in the batch
    pub amount: Uint128,
    /// The amount of tokens that have been claimed.
    pub amount_claimed: Uint128,
    /// When the lockup ends.
    pub lockup_end: u64,
    /// How often releases occur.
    pub release_unit: u64,
    /// Specifies how much is to be released after each `release_unit`. If
    /// it is a percentage, it would be the percentage of the original amount.
    pub release_amount: WithdrawalType,
    /// The time at which the last claim took place in seconds.
    pub last_claimed_release_time: u64,
}
```

**Variant: Module Auth Error - MEDIUM Severity Cases** [MEDIUM]
> Found in 6 reports:
> - `reports/cosmos_cometbft_findings/m-01-reentrancy-check-in-lock_stakingreentry_check-causes-concurrent-init-deposi.md`
> - `reports/cosmos_cometbft_findings/m-02-deposits-might-fail-if-staking-module-account-is-not-activated.md`
> - `reports/cosmos_cometbft_findings/m-05-last-holder-cant-exit-zerosupply-unstake-reverts.md`

**Variant: Module Auth Error in Cabal** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-01-reentrancy-check-in-lock_stakingreentry_check-causes-concurrent-init-deposi.md`
> - `reports/cosmos_cometbft_findings/m-05-last-holder-cant-exit-zerosupply-unstake-reverts.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in module auth error logic allows exploitation through missing validation, incor
func secureModuleAuthError(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 8 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 6
- **Affected Protocols**: stHYPE_2025-10-13, Persistence, Cabal, Nibiru, Andromeda – Validator Staking ADO and Vesting ADO
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Module Distribution

### Overview

Implementation flaw in module distribution logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 3, MEDIUM: 2.

> **Key Finding**: The report highlights a potential vulnerability in the CVGT staking state that can be exploited by manipulating the CVGT mint and CVGTStakingPoolState accounts. This allows attackers to set any CVGT on a poolstate and stability_pool_state, as well as spoof the CVGTStakingPoolState, potentially enabl

### Vulnerability Description

#### Root Cause

Implementation flaw in module distribution logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies module distribution in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to module operations

### Vulnerable Pattern Examples

**Example 1: CVGT Staking Pool State Manipulation** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/cvgt-staking-pool-state-manipulation.md`
```rust
pub struct Initialize<'info> {
    #[account()]
    pub cvgt: Box<Account<'info, Mint>>,
}
```

**Example 2: Delegated Boost Persists Even If veRAAC Is Withdrawn/Reduced** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/delegated-boost-persists-even-if-veraac-is-withdrawnreduced.md`
```solidity
This sets `UserBoost` with `amount` and an `expiry`, effectively guaranteeing that “X” units of veRAAC are delegated for that duration.
2. **No Ongoing Balance Check**\
   Once set, the **BoostController** never re‑checks whether the user still has that many veRAAC tokens locked in veRAACToken. The contract only checks the user’s balance at the moment of delegation (via `if (userBalance < amount) revert InsufficientVeBalance()`).
3. **User Reduces or Withdraws veRAAC**\
   Right after delegating, the user calls:
```

**Example 3: [H-01] Wrong handling of ERC20 denoms in `ERC20Keeper::BurnCoins`** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-wrong-handling-of-erc20-denoms-in-erc20keeperburncoins.md`
```go
func (k ERC20Keeper) MintCoins(ctx context.Context, addr sdk.AccAddress, amount sdk.Coins) error {
	// ... snip ...

	for _, coin := range amount {
		denom := coin.Denom
		if types.IsERC20Denom(denom) {
			return moderrors.Wrapf(types.ErrInvalidRequest, "cannot mint erc20 coin: %s", coin.Denom)
		}

		// ... snip ...

		inputBz, err := k.ERC20ABI.Pack("sudoMint", evmAddr, coin.Amount.BigInt())
		if err != nil {
			return types.ErrFailedToPackABI.Wrap(err.Error())
		}

		// ... snip ...
	}

	// ... snip ...
}
```

**Example 4: Owner is able to withdraw staking token.** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/owner-is-able-to-withdraw-staking-token.md`
```
// Vulnerable pattern from Radiant Capital:
**Description**

MultiFee Distribution.sol: recoverERC20(). 
The owner can directly access users' funds and withdraw their tokens anytime since the owner can't recover only reward tokens. As a result, in the case of the private key exploit (of an owner account), users' funds can be withdrawn directly from the contract. That's why it is recommended to validate that the provided 'tokenAddress is not a staking token, in order to exclude a centralization risk. 

**Recommendation**: 

Validate that '
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in module distribution logic allows exploitation through missing validation, inc
func secureModuleDistribution(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 5 audit reports
- **Severity Distribution**: HIGH: 3, MEDIUM: 2
- **Affected Protocols**: Radiant Capital, Initia, Convergent, Core Contracts
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Module Staking Specific

### Overview

Implementation flaw in module staking specific logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 8 audit reports with severity distribution: HIGH: 4, MEDIUM: 4.

> **Key Finding**: The `MsgSetBeforeSendHook` in the `tokenfactory` module allows the creator of a token to set a custom logic for determining whether a transfer should succeed. However, a malicious token creator can set an invalid address as the hook, causing transfers to fail and potentially leading to a denial of s

### Vulnerability Description

#### Root Cause

Implementation flaw in module staking specific logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies module staking specific in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to module operations

### Vulnerable Pattern Examples

**Example 1: [H-01] `BlockBeforeSend` hook can be exploited to perform a denial of service** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md`
```go
poc: build
   	@echo "starting POC.."

   	# clear port 26657 if old process still running
   	@if lsof -i :26657; then \
   		kill -9 $$(lsof -t -i :26657) || echo "cannot kill process"; \
   	fi

   	# remove old setup and init new one
   	@rm -rf .mantrapoc
   	@mkdir -p .mantrapoc

   	./build/mantrachaind init poc-test --chain-id test-chain --home .mantrapoc
   	./build/mantrachaind keys add validator --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add validator2 --keyring-backend test --home .mantrapoc

   	# create alice and bob account
   	./build/mantrachaind keys add alice --keyring-backend test --home .mantrapoc
   	./build/mantrachaind keys add bob --keyring-backend test --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show validator2 -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show alice -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc
   	./build/mantrachaind genesis add-genesis-account $$(./build/mantrachaind keys show bob -a --keyring-backend test --home .mantrapoc) 500000000000stake --home .mantrapoc

   	./build/mantrachaind genesis gentx validator 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc
   	# ./build/mantrachaind genesis gentx validator2 100000000stake --chain-id test-chain --keyring-backend test --home .mantrapoc

   	./build/mantrachaind genesis collect-gentxs --home .mantrapoc

   	# start node
   	./build/mantrachaind start --home .mantrapoc --minimum-gas-prices 0stake
```

**Example 2: [H-03] Unlimited Nibi could be minted because evm and bank balance are not synce** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md`
```go
func (bk *NibiruBankKeeper) SyncStateDBWithAccount(
	ctx sdk.Context, acc sdk.AccAddress,
) {
	// If there's no StateDB set, it means we're not in an EthereumTx.
	if bk.StateDB == nil {
		return
	}
	balanceWei := evm.NativeToWei(
		bk.GetBalance(ctx, acc, evm.EVMBankDenom).Amount.BigInt(),
	)
	bk.StateDB.SetBalanceWei(eth.NibiruAddrToEthAddr(acc), balanceWei)
}
```

**Example 3: Inconsistencies in Slash Redelegation** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/inconsistencies-in-slash-redelegation.md`
```go
> func (k Keeper) SlashRedelegation(ctx context.Context, srcValidator types.Validator,
> redelegation types.Redelegation,
> infractionHeight int64, slashFactor math.LegacyDec,
> ) (totalSlashAmount math.Int, err error) {
> [...]
> tokensToBurn, err := k.Unbond(ctx, delegatorAddress, valDstAddr, sharesToUnbond)
> if err != nil {
> return math.ZeroInt(), err
> }
> [...]
> }
>
```

**Example 4: [M-07] `Vested CSX` to `Regular CSX` Conversion Process Enables Potential Unauth** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-07-vested-csx-to-regular-csx-conversion-process-enables-potential-unauthorized.md`
```solidity
/// @notice Executes a forced withdrawal of tokens from the contract.
/// @dev Can only be called by the council to mitigate against malicious vesters.
/// @param amount Specifies the amount of tokens to be withdrawn.
function cliff(uint256 amount) external onlyCouncil {
  if (amount > vesting.amount || amount == 0) {
    revert NotEnoughTokens();
  }
  vesting.amount -= amount;
  cliffedAmount += amount;
  sCsxToken.unStake(amount);
  csxToken.safeTransfer(msg.sender, amount);
  emit Cliff(msg.sender, amount, vesting.amount);
}
```

**Example 5: [M-26] ZRC20 Token Pause Check Bypass** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-26-zrc20-token-pause-check-bypass.md`
```go
go test ./x/crosschain/keeper/gas_payment_test.go -run TestZRC20PauseBypassTry2 -v
```

**Variant: Module Staking Specific - MEDIUM Severity Cases** [MEDIUM]
> Found in 4 reports:
> - `reports/cosmos_cometbft_findings/inconsistencies-in-slash-redelegation.md`
> - `reports/cosmos_cometbft_findings/m-07-vested-csx-to-regular-csx-conversion-process-enables-potential-unauthorized.md`
> - `reports/cosmos_cometbft_findings/m-26-zrc20-token-pause-check-bypass.md`

**Variant: Module Staking Specific in Persistence** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/prst-4-unbonding-of-validators-does-not-give-priority-to-inactive-validators.md`
> - `reports/cosmos_cometbft_findings/prst-6-first-depositor-can-steal-assets-due-to-missing-slippage-protection.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in module staking specific logic allows exploitation through missing validation,
func secureModuleStakingSpecific(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 8 audit reports
- **Severity Distribution**: HIGH: 4, MEDIUM: 4
- **Affected Protocols**: Csx, Persistence, Infrared Contracts, MANTRA, Cosmos LSM
- **Validation Strength**: Strong (3+ auditors)

---

## 5. Module Slashing Specific

### Overview

Implementation flaw in module slashing specific logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: MEDIUM: 5.

> **Key Finding**: The report describes a bug in the `submitInitialSlashing` function of the `CSModule` contract. This bug causes the bond curve for a Node Operator to not be reset to the default after being penalized. This could lead to incorrect counting of unbonded validator keys. The severity of this bug is classi

### Vulnerability Description

#### Root Cause

Implementation flaw in module slashing specific logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies module slashing specific in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to module operations

### Vulnerable Pattern Examples

**Example 1: Bond Curve is Not Reset Inside the `submitInitialSlashing` Function** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/bond-curve-is-not-reset-inside-the-submitinitialslashing-function.md`
```
// Vulnerable pattern from Lido:
##### Description
The issue is identified within the [`submitInitialSlashing`](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSModule.sol#L1174) function of the `CSModule` contract, where the initial slashing penalty is applied to the Node Operator bond. While this penalization occurs, the Bond Curve for that Node Operator is not reset to the default.

The issue is classified as **Medium** severity because it may lead to incorrect accou
```

**Example 2: Message is indexed as refundable even if the signature was over a fork** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-2-message-is-indexed-as-refundable-even-if-the-signature-was-over-a-fork.md`
```go
// if this finality provider has signed the canonical block before,
	// slash it via extracting its secret key, and emit an event
	if ms.HasEvidence(ctx, req.FpBtcPk, req.BlockHeight) {
		// the finality provider has voted for a fork before!
		// If this evidence is at the same height as this signature, slash this finality provider

		// get evidence
		evidence, err := ms.GetEvidence(ctx, req.FpBtcPk, req.BlockHeight)
		if err != nil {
			panic(fmt.Errorf("failed to get evidence despite HasEvidence returns true"))
		}

		// set canonical sig to this evidence
		evidence.CanonicalFinalitySig = req.FinalitySig
		ms.SetEvidence(ctx, evidence)

		// slash this finality provider, including setting its voting power to
		// zero, extracting its BTC SK, and emit an event
		ms.slashFinalityProvider(ctx, req.FpBtcPk, evidence)
	}

	// at this point, the finality signature is 1) valid, 2) over a canonical block,
	// and 3) not duplicated.
	// Thus, we can safely consider this message as refundable
	ms.IncentiveKeeper.IndexRefundableMsg(ctx, req)
```

**Example 3: `slash` calls can be blocked, allowing malicious users to bypass the slashing me** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-2-slash-calls-can-be-blocked-allowing-malicious-users-to-bypass-the-slashing-m.md`
```go
modifier checkpointProtection(address account) {
    uint256 numCheckpoints = _stakes[account]._checkpoints.length;
    require(numCheckpoints == 0 || _stakes[account]._checkpoints[numCheckpoints - 1]._blockNumber != block.number, "StakingModule: Cannot exit in the same block as another stake or exit");
    _;
}
```

**Example 4: Slashing fails if claims revert** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-6-slashing-fails-if-claims-revert.md`
```
// Vulnerable pattern from Telcoin:
Source: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/5
```

**Example 5: Slashing of re-delegated stake is computed incorrectly** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/slashing-of-re-delegated-stake-is-computed-incorrectly.md`
```go
let multiplier = (Decimal::one() - self.slash_fraction_double_sign)?;
for entry in redelegations.iter() {
    let del_address = entry.delegator_address;
    for redelegation in entry.outbound_redelegations.iter() {
        let mut validator = self.validators.get_mut(redelegation.address.into())?;
        let mut delegator = validator.get_mut(del_address.into())?;
        delegator.slash_redelegation((multiplier * redelegation.amount)?.amount()?)?;
    }
}
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in module slashing specific logic allows exploitation through missing validation
func secureModuleSlashingSpecific(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 5 audit reports
- **Severity Distribution**: MEDIUM: 5
- **Affected Protocols**: Lido, Babylon chain launch (phase-2), Telcoin, Telcoin Update, Orga and Merk
- **Validation Strength**: Strong (3+ auditors)

---

## 6. Module Evidence

### Overview

Implementation flaw in module evidence logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 3, MEDIUM: 1.

> **Key Finding**: The bug report discusses an issue in the code of the Pheasant Network Bridge Child, specifically in the `PheasantNetworkBridgeChild.sol` file. The problem occurs when there is a successful dispute for a trade of a certain number of tokens. The system is supposed to slash a portion of the bond manage

### Vulnerability Description

#### Root Cause

Implementation flaw in module evidence logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies module evidence in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to module operations

### Vulnerable Pattern Examples

**Example 1: Fund Distribution May Not Incentivize Users to Participate** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/fund-distribution-may-not-incentivize-users-to-participate.md`
```
// Vulnerable pattern from Pheasant Network:
**Update**
This issue is categorized as mitigated, given that the values are not hard-coded in the current implementation.

**File(s) affected:**`PheasantNetworkBridgeChild.sol`

**Description:** In case of a successful dispute for a trade of `n` tokens, the system will slash from the bond manager an amount of `tradableBondRatio * n / 100` and will distribute 50% to the initiator of the trade and 50% to the disputer. An integrity constraint in `PheasantNetworkBridgeChild.finalizeTradeParamUpdate
```

**Example 2: Relayer Can Submit Undisputable Evidence for L2->L1 Trades** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/relayer-can-submit-undisputable-evidence-for-l2-l1-trades.md`
```
// Vulnerable pattern from Pheasant Network:
**Update**
The issue is fixed due to a shift of responsibility. Now, the relayer has no reason to submit evidence with a wrong block hash because he will get slashed when he will have to defend himself.

![Image 63: Alert icon](https://certificate.quantstamp.com/full/pheasant-network/0b120935-78d1-45a1-88c4-f770c8e5fa52/static/media/info-icon-alert.3c9578483b1cf3181c9bfb6fec7dc641.svg)

**Update**
Addressed in: `64a96f0bec95007790f91ab71b054b38eb0e101a`. The client provided the following explana
```

**Example 3: Relayer Can Use Valid Evidence of One Trade to Avoid Getting Slashed for Another** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/relayer-can-use-valid-evidence-of-one-trade-to-avoid-getting-slashed-for-another.md`
```
// Vulnerable pattern from Pheasant Network:
**Update**
Addressed in: `0508a14eb93180ea7b313978248663a60ccb5faa`.

**File(s) affected:**`PheasantNetworkBridgeChild.sol`

**Description:** The evidence submitted by the Relayer is not checked at all in the function `withdraw()`. This may be explained by the fact that the system is an optimistic bridge and that if the evidence provided is incorrect, it will be detected, and the Relayer will get slashed.

However, the current system makes the following scenario possible:

1.   One user sends th
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in module evidence logic allows exploitation through missing validation, incorre
func secureModuleEvidence(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 4 audit reports
- **Severity Distribution**: HIGH: 3, MEDIUM: 1
- **Affected Protocols**: Pheasant Network
- **Validation Strength**: Single auditor

---

## 7. Module Crisis

### Overview

Implementation flaw in module crisis logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report is about a problem in the Cosmos SDK network where the chain does not stop when a certain check fails. This can be used by attackers to disrupt the network, which is called a denial-of-service attack. The chances of this happening are moderate, as it requires specific knowledge and s

### Vulnerability Description

#### Root Cause

Implementation flaw in module crisis logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies module crisis in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to module operations

### Vulnerable Pattern Examples

**Example 1: DoS in Cosmos SDK Crisis Module (github.com/cosmos/cosmos-sdk/x/crisis)** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/dos-in-cosmos-sdk-crisis-module-githubcomcosmoscosmos-sdkxcrisis.md`
```
// Vulnerable pattern from Shido:
**Severity:** Medium

**Status**: Acknowledged

**Description:** 

The chain does not halt when an invariant check fails on a Cosmos SDK network, and a transaction is sent to the x/crisis module.

**Impact**: 

This can lead to a denial-of-service (DoS) attack, in which an attacker repeatedly triggers invariant failures to disrupt the network.

**Likelihood:** 

Moderate, as it requires knowledge of the invariant checks and the ability to craft malicious transactions.

**Recommendation:** 

Ther
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in module crisis logic allows exploitation through missing validation, incorrect
func secureModuleCrisis(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: Shido
- **Validation Strength**: Single auditor

---

## 8. Module Capability

### Overview

Implementation flaw in module capability logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: This bug report discusses a vulnerability in the Cabal token contract that allows an attacker to manipulate the supply and reward distribution of the token. By initiating an unstake transaction in the same block as the manager's snapshot, the attacker can exploit flaws in the contract to artificiall

### Vulnerability Description

#### Root Cause

Implementation flaw in module capability logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies module capability in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to module operations

### Vulnerable Pattern Examples

**Example 1: [M-03] Attacker Can Desynchronize Supply Snapshot During Same-Block Unstake, Red** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-attacker-can-desynchronize-supply-snapshot-during-same-block-unstake-reduci.md`
```
// Vulnerable pattern from Cabal:
<https://github.com/code-423n4/2025-04-cabal/blob/5b5f92ab4f95e5f9f405bbfa252860472d164705/sources/cabal_token.move# L219-L227>

### Finding description and impact

An attacker holding Cabal LSTs (like sxINIT) can monitor the mempool for the manager’s `voting_reward::snapshot()` transaction. By submitting his own `cabal::initiate_unstake` transaction to execute in the *same block* (`H`) as the manager’s snapshot, the attacker can use two flaws:

1. `cabal_token::burn` (called by their unstake) d
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in module capability logic allows exploitation through missing validation, incor
func secureModuleCapability(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 1 audit reports
- **Severity Distribution**: MEDIUM: 1
- **Affected Protocols**: Cabal
- **Validation Strength**: Single auditor

---

## Detection Patterns

### Automated Detection
```
# Module Bank Error
grep -rn 'module|bank|error' --include='*.go' --include='*.sol'
# Module Auth Error
grep -rn 'module|auth|error' --include='*.go' --include='*.sol'
# Module Distribution
grep -rn 'module|distribution' --include='*.go' --include='*.sol'
# Module Staking Specific
grep -rn 'module|staking|specific' --include='*.go' --include='*.sol'
# Module Slashing Specific
grep -rn 'module|slashing|specific' --include='*.go' --include='*.sol'
# Module Evidence
grep -rn 'module|evidence' --include='*.go' --include='*.sol'
# Module Crisis
grep -rn 'module|crisis' --include='*.go' --include='*.sol'
# Module Capability
grep -rn 'module|capability' --include='*.go' --include='*.sol'
```

## Keywords

`addexternalincentive`, `allowing`, `allows`, `another`, `appchain`, `attacker`, `auth`, `avoid`, `balance`, `bank`, `because`, `block`, `bond`, `boost`, `bypass`, `calls`, `capability`, `causes`, `check`, `concurrent`, `cosmos`, `could`, `crisis`, `curve`, `cvgt`, `delegated`, `denial`, `denoms`, `deposit`, `desynchronize`
