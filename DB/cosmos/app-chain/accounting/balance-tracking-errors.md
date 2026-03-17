---
protocol: generic
chain: cosmos
category: accounting
vulnerability_type: balance_tracking_errors

attack_type: logical_error|economic_exploit|dos
affected_component: accounting_logic

primitives:
  - balance_not_updated
  - double_counting
  - tvl_error
  - state_corruption
  - missing_deduction
  - cross_module
  - pending_tracking
  - negative_value
  - fee_deduction

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - accounting
  - staking
  - defi

language: go|solidity|rust
version: all

# Pattern Identity (Required)
root_cause_family: denial_of_service
pattern_key: denial_of_service | accounting_logic | balance_tracking_errors

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - AddBTCDelegationInclusionProof
  - SyncStateDBWithAccount
  - a
  - balance
  - balanceOf
  - balance_not_updated
  - changeManagers
  - cross_module
  - double_counting
  - fee_deduction
  - for
  - getTotalAssetTVL
  - getTotalStake
  - handleSlashing
  - happens
  - mint
  - missing_deduction
  - msg.sender
  - negative_value
  - of
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Accounting Balance Not Updated
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-01] User can prevent balance updates by withdrawing | `reports/cosmos_cometbft_findings/h-01-user-can-prevent-balance-updates-by-withdrawing.md` | HIGH | Pashov Audit Group |
| [H-02] Broken balance update if a slash event happens | `reports/cosmos_cometbft_findings/h-02-broken-balance-update-if-a-slash-event-happens.md` | HIGH | Pashov Audit Group |
| [H-03] Unlimited Nibi could be minted because evm and bank b | `reports/cosmos_cometbft_findings/h-03-unlimited-nibi-could-be-minted-because-evm-and-bank-balance-are-not-synced-.md` | HIGH | Code4rena |
| Lack of rebasable tokens support | `reports/cosmos_cometbft_findings/lack-of-rebasable-tokens-support.md` | HIGH | MixBytes |
| [M-04] Preventing balance updates by adding a new validator  | `reports/cosmos_cometbft_findings/m-04-preventing-balance-updates-by-adding-a-new-validator-in-the-current-block.md` | MEDIUM | Pashov Audit Group |
| Missing Balance Deduction in Unstaking Functions Allows Cont | `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md` | HIGH | Quantstamp |
| Oracle’s _sanityCheck for prices will not work with slashing | `reports/cosmos_cometbft_findings/oracles-_sanitycheck-for-prices-will-not-work-with-slashing.md` | HIGH | ConsenSys |
| Potential Stake Lock and Inconsistency Due to Validator Stat | `reports/cosmos_cometbft_findings/potential-stake-lock-and-inconsistency-due-to-validator-state-transitions.md` | MEDIUM | OpenZeppelin |

### Accounting Double Counting
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Accounting for `rewardStakeRatioSum` is incorrect when a del | `reports/cosmos_cometbft_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md` | HIGH | Cyfrin |
| Duplicate Request Rewards | `reports/cosmos_cometbft_findings/duplicate-request-rewards.md` | HIGH | OpenZeppelin |
| Dirty EVM state changes are not committed before precompile  | `reports/cosmos_cometbft_findings/h-2-dirty-evm-state-changes-are-not-committed-before-precompile-calls-resulting-.md` | HIGH | Sherlock |
| External PT redeem functions can be reentered to double coun | `reports/cosmos_cometbft_findings/h-2-external-pt-redeem-functions-can-be-reentered-to-double-count-the-received-u.md` | HIGH | Sherlock |
| Incorrect Withdrawable Shares Reduction After AVS And Beacon | `reports/cosmos_cometbft_findings/incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md` | HIGH | SigmaPrime |
| Operator can over allocate the same stake to unlimited nodes | `reports/cosmos_cometbft_findings/operator-can-over-allocate-the-same-stake-to-unlimited-nodes-within-one-epoch-ca.md` | MEDIUM | Cyfrin |
| Risk of double-spend attacks due to use of single-node Cliqu | `reports/cosmos_cometbft_findings/risk-of-double-spend-attacks-due-to-use-of-single-node-clique-consensus-without-.md` | MEDIUM | TrailOfBits |
| RocketMinipoolDelegateOld - Node operator may reenter finali | `reports/cosmos_cometbft_findings/rocketminipooldelegateold-node-operator-may-reenter-finalise-to-manipulate-accou.md` | HIGH | ConsenSys |

### Accounting Tvl Error
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Function `getTotalStake()` fails to account for pending vali | `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md` | HIGH | Cyfrin |
| [H-04] Strategy allocation tracking errors affect TVL calcul | `reports/cosmos_cometbft_findings/h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md` | HIGH | Pashov Audit Group |
| [M-04] Delayed slashing window and lack of transparency for  | `reports/cosmos_cometbft_findings/m-04-delayed-slashing-window-and-lack-of-transparency-for-pending-slashes-could-.md` | MEDIUM | Code4rena |

### Accounting State Corruption
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Any decrease in slashed or rewarded amounts reported will ma | `reports/cosmos_cometbft_findings/any-decrease-in-slashed-or-rewarded-amounts-reported-will-make-validatormanager-.md` | MEDIUM | Spearbit |
| Incorrect accounting in LockingController.applyLosses functi | `reports/cosmos_cometbft_findings/incorrect-accounting-in-lockingcontrollerapplylosses-function.md` | HIGH | Spearbit |

### Accounting Missing Deduction
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| _checkBalance Returns an Incorrect Value During Insolvency | `reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md` | MEDIUM | OpenZeppelin |
| Public vaults can become insolvent because of missing `yInte | `reports/cosmos_cometbft_findings/h-9-public-vaults-can-become-insolvent-because-of-missing-yintercept-update.md` | HIGH | Sherlock |
| Missing Balance Deduction in Unstaking Functions Allows Cont | `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md` | HIGH | Quantstamp |
| Missing validation that ensures unspent BTC is fully sent ba | `reports/cosmos_cometbft_findings/missing-validation-that-ensures-unspent-btc-is-fully-sent-back-as-change-in-lomb.md` | MEDIUM | Cantina |
| The delegator resetting self-delegation causes multiple issu | `reports/cosmos_cometbft_findings/the-delegator-resetting-self-delegation-causes-multiple-issues-in-the-protocol.md` | HIGH | Cyfrin |

### Accounting Cross Module
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [M-26] ZRC20 Token Pause Check Bypass | `reports/cosmos_cometbft_findings/m-26-zrc20-token-pause-check-bypass.md` | MEDIUM | Code4rena |

### Accounting Pending Tracking
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [C-01] Pending payouts excluded from total balance cause inc | `reports/cosmos_cometbft_findings/c-01-pending-payouts-excluded-from-total-balance-cause-incorrect-share-calculati.md` | HIGH | Pashov Audit Group |
| [C-02] Pending stake not accounted for in liquidity calculat | `reports/cosmos_cometbft_findings/c-02-pending-stake-not-accounted-for-in-liquidity-calculations.md` | HIGH | Pashov Audit Group |
| Function `getTotalStake()` fails to account for pending vali | `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md` | HIGH | Cyfrin |
| Include Pending In Unstake | `reports/cosmos_cometbft_findings/include-pending-in-unstake.md` | MEDIUM | OtterSec |
| [M-05] Changing VoteWeighting contract can result in lost st | `reports/cosmos_cometbft_findings/m-05-changing-voteweighting-contract-can-result-in-lost-staking-incentives.md` | MEDIUM | Code4rena |

### Accounting Negative Value
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Adversary can arbitrarily trigger a chain halt by sending `M | `reports/cosmos_cometbft_findings/h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md` | HIGH | Sherlock |
| If the Covenant signature does not pass , EXPIRED events it  | `reports/cosmos_cometbft_findings/h-3-if-the-covenant-signature-does-not-pass-expired-events-it-will-still-be-exec.md` | HIGH | Sherlock |
| Incorrect accounting in LockingController.applyLosses functi | `reports/cosmos_cometbft_findings/incorrect-accounting-in-lockingcontrollerapplylosses-function.md` | HIGH | Spearbit |
| Lack of rebasable tokens support | `reports/cosmos_cometbft_findings/lack-of-rebasable-tokens-support.md` | HIGH | MixBytes |
| Negative rebase of stETH could prevent a round from ending | `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md` | MEDIUM | OpenZeppelin |
| Refund can be over-credited in a negative yield event | `reports/cosmos_cometbft_findings/refund-can-be-over-credited-in-a-negative-yield-event.md` | MEDIUM | OpenZeppelin |
| Refunds will be over-credited in a negative yield event | `reports/cosmos_cometbft_findings/refunds-will-be-over-credited-in-a-negative-yield-event.md` | MEDIUM | OpenZeppelin |
| USERS MAY NOT BE ABLE TO UNSTAKE OR CLAIM REWARDS WHEN stake | `reports/cosmos_cometbft_findings/users-may-not-be-able-to-unstake-or-claim-rewards-when-stakedamountlimit-is-decr.md` | MEDIUM | Halborn |

### Accounting Fee Deduction
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Incorrect fees will be charged | `reports/cosmos_cometbft_findings/h-35-incorrect-fees-will-be-charged.md` | HIGH | Sherlock |
| Ignite fee is not returned for pre-validated `QI` stakes in  | `reports/cosmos_cometbft_findings/ignite-fee-is-not-returned-for-pre-validated-qi-stakes-in-the-event-of-registrat.md` | MEDIUM | Cyfrin |
| [M-04] Gas refunds use block gas instead of transaction gas, | `reports/cosmos_cometbft_findings/m-04-gas-refunds-use-block-gas-instead-of-transaction-gas-leading-to-incorrect-r.md` | MEDIUM | Code4rena |
| `msg_server_stake::AddStake` calculates the weight incorrect | `reports/cosmos_cometbft_findings/m-32-msg_server_stakeaddstake-calculates-the-weight-incorrectly-resulting-in-inc.md` | MEDIUM | Sherlock |

---

# Balance Tracking Errors - Comprehensive Database

**A Complete Pattern-Matching Guide for Balance Tracking Errors in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Accounting Balance Not Updated](#1-accounting-balance-not-updated)
2. [Accounting Double Counting](#2-accounting-double-counting)
3. [Accounting Tvl Error](#3-accounting-tvl-error)
4. [Accounting State Corruption](#4-accounting-state-corruption)
5. [Accounting Missing Deduction](#5-accounting-missing-deduction)
6. [Accounting Cross Module](#6-accounting-cross-module)
7. [Accounting Pending Tracking](#7-accounting-pending-tracking)
8. [Accounting Negative Value](#8-accounting-negative-value)
9. [Accounting Fee Deduction](#9-accounting-fee-deduction)

---

## 1. Accounting Balance Not Updated

### Overview

Implementation flaw in accounting balance not updated logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 8 audit reports with severity distribution: HIGH: 6, MEDIUM: 2.

> **Key Finding**: This bug report describes a problem where the value of `creditedNodeETH` is not being updated correctly when the `finishWithdraw()` function is called. This can lead to an incorrect balance for users and can also be exploited by malicious users to prevent balance updates. The report recommends updat



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of denial_of_service"
- Pattern key: `denial_of_service | accounting_logic | balance_tracking_errors`
- Interaction scope: `multi_contract`
- Primary affected component(s): `accounting_logic`
- High-signal code keywords: `AddBTCDelegationInclusionProof`, `SyncStateDBWithAccount`, `a`, `balance`, `balanceOf`, `balance_not_updated`, `changeManagers`, `cross_module`
- Typical sink / impact: `fund_loss|dos|state_corruption`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `Safe.function -> address.function -> balance.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Unbounded loop over user-controlled array can exceed block gas limit
- Signal 2: External call failure causes entire transaction to revert
- Signal 3: Attacker can grief operations by manipulating state to cause reverts
- Signal 4: Resource exhaustion through repeated operations without rate limiting

#### False Positive Guards

- Not this bug when: Loop iterations are bounded by a reasonable constant
- Safe if: External call failures are handled gracefully (try/catch or pull pattern)
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting balance not updated logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting balance not updated in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: [H-01] User can prevent balance updates by withdrawing** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-user-can-prevent-balance-updates-by-withdrawing.md`
```go
// Calculate unattributed node balance
        uint256 nodeBalanceWei = node.nodeAddress.balance - node.creditedNodeETH;
```

**Example 2: [H-02] Broken balance update if a slash event happens** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-broken-balance-update-if-a-slash-event-happens.md`
```go
// Calculate unattributed node balance
        uint256 nodeBalanceWei = node.nodeAddress.balance - node.creditedNodeETH;
```

**Example 3: [H-03] Unlimited Nibi could be minted because evm and bank balance are not synce** [HIGH]
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

**Example 4: Lack of rebasable tokens support** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-rebasable-tokens-support.md`
```
// Vulnerable pattern from XPress:
##### Description
The issue is identified in the [`LOB`](https://github.com/longgammalabs/hanji-contracts/blob/09b6188e028650b9c1758010846080c5f8c80f8e/src/OnchainLOB.sol) contract.

For rebasable tokens, such as those that adjust their supply over time (e.g., Ampleforth), the LOB contract may keep all rewards in the contract balance. During a rebase (positive or negative), the recorded balances in the contract may not accurately reflect the true balances of the tokens held. This discrepancy can
```

**Example 5: Missing Balance Deduction in Unstaking Functions Allows Contract Drainage and Lo** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md`
```
// Vulnerable pattern from Sapien:
**Update**
Marked as "Fixed" by the client. Addressed in: `4a45a4a`.

![Image 26: Alert icon](https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the client. Addressed in: `f647099b7988fa4d01fac6a9f3481d25e748527a`. The client provided the following explanation:

> The vulnerability in the unstaking functions was fixed by implementing proper balance deduction and
```

**Variant: Accounting Balance Not Updated - MEDIUM Severity Cases** [MEDIUM]
> Found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-04-preventing-balance-updates-by-adding-a-new-validator-in-the-current-block.md`
> - `reports/cosmos_cometbft_findings/potential-stake-lock-and-inconsistency-due-to-validator-state-transitions.md`

**Variant: Accounting Balance Not Updated in Karak-June** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/h-01-user-can-prevent-balance-updates-by-withdrawing.md`
> - `reports/cosmos_cometbft_findings/h-02-broken-balance-update-if-a-slash-event-happens.md`
> - `reports/cosmos_cometbft_findings/m-04-preventing-balance-updates-by-adding-a-new-validator-in-the-current-block.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting balance not updated logic allows exploitation through missing vali
func secureAccountingBalanceNotUpdated(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 6, MEDIUM: 2
- **Affected Protocols**: Karak-June, Geodefi, Nibiru, XPress, Sapien
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Accounting Double Counting

### Overview

Implementation flaw in accounting double counting logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 9 audit reports with severity distribution: HIGH: 6, MEDIUM: 3.

> **Key Finding**: This bug report describes an issue with the accounting system in a software program. The program is incorrectly counting certain funds twice, which can lead to incorrect calculations and potentially give users more money than they should have. This issue has been fixed by the developers, but it is i

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting double counting logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting double counting in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: Accounting for `rewardStakeRatioSum` is incorrect when a delayed balance or rewa** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/accounting-for-rewardstakeratiosum-is-incorrect-when-a-delayed-balance-or-reward.md`
```go
// Before start
latestActiveBalanceAfterFee = 32 ETH
latestActiveRewards = 0

// startReport()
reportSweptBalance = 0 (rewards is in BeaconChain)

// syncValidators()
reportActiveBalance = 32.105 ETH

// finalizeReport()
rewards = 0.105 ETH
change = rewards - latestActiveRewards = 0.105 ETH
gainAfterFee = 0.1 ETH
=> rewardStakeRatioSum is increased
=> latestActiveBalanceAfterFee = 32.1

sweptRewards = 0
=> latestActiveRewards = 0.105
```

**Example 2: Duplicate Request Rewards** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/duplicate-request-rewards.md`
```go
deletedRequests[1] = 1
deletedRequests[2] = 2
```

**Example 3: Dirty EVM state changes are not committed before precompile calls, resulting in ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-2-dirty-evm-state-changes-are-not-committed-before-precompile-calls-resulting-.md`
```solidity
82: 	// if caller is not the same as origin it means call is coming through smart contract,
83: 	// and because state of smart contract calling precompile might be updated as well
84: 	// manually reduce amount in stateDB, so it is properly reflected in bank module
85: 	stateDB := evm.StateDB.(precompiletypes.ExtStateDB)
86: 	if contract.CallerAddress != evm.Origin {
87: 		stateDB.SubBalance(stakerAddress, amountUint256)
88: 	}
```

**Example 4: External PT redeem functions can be reentered to double count the received under** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-2-external-pt-redeem-functions-can-be-reentered-to-double-count-the-received-u.md`
```solidity
/// @notice redeem method signature for Sense
    /// @param p principal value according to the MarketPlace's Principals Enum
    /// @param u address of an underlying asset
    /// @param m maturity (timestamp) of the market
    /// @param s Sense's maturity is needed to extract the pt address
    /// @param a Sense's adapter for this market
    /// @return bool true if the redemption was successful
    function redeem(
        uint8 p,
        address u,
        uint256 m,
        uint256 s,
        address a
    ) external returns (bool) {
        // Check the principal is Sense
        if (p != uint8(MarketPlace.Principals.Sense)) {
            revert Exception(6, p, 0, address(0), address(0));
        }

        // Get Sense's principal token for this market
        IERC20 token = IERC20(IMarketPlace(marketPlace).token(u, m, p));

        // Cache the lender to save on SLOAD operations
        address cachedLender = lender;

        // Get the balance of tokens to be redeemed by the user
        uint256 amount = token.balanceOf(cachedLender);

        // Transfer the user's tokens to the redeem contract
        Safe.transferFrom(token, cachedLender, address(this), amount);

        // Get the starting balance to verify the amount received afterwards
        uint256 starting = IERC20(u).balanceOf(address(this));

        // Get the divider from the adapter
// ... (truncated)
```

**Example 5: Incorrect Withdrawable Shares Reduction After AVS And Beacon Chain Slashing** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/incorrect-withdrawable-shares-reduction-after-avs-and-beacon-chain-slashing.md`
```go
finalWithdrawableShares = depositShares × dsf × slashingFactor
                        = depositShares × dsf × (maxMagnitude × bcsf)
                        = 32 × 1 × (0.5 × 0.5)
                        = 8
```

**Variant: Accounting Double Counting - MEDIUM Severity Cases** [MEDIUM]
> Found in 3 reports:
> - `reports/cosmos_cometbft_findings/operator-can-over-allocate-the-same-stake-to-unlimited-nodes-within-one-epoch-ca.md`
> - `reports/cosmos_cometbft_findings/risk-of-double-spend-attacks-due-to-use-of-single-node-clique-consensus-without-.md`
> - `reports/cosmos_cometbft_findings/validators-array-length-has-to-be-updated-when-the-validator-is-alienated.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting double counting logic allows exploitation through missing validati
func secureAccountingDoubleCounting(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 9 audit reports
- **Severity Distribution**: HIGH: 6, MEDIUM: 3
- **Affected Protocols**: Scroll, l2geth, ZetaChain Cross-Chain, Casimir, Suzaku Core, Illuminate
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Accounting Tvl Error

### Overview

Implementation flaw in accounting tvl error logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 3 audit reports with severity distribution: HIGH: 2, MEDIUM: 1.

> **Key Finding**: The `getTotalStake()` function in the `CasimirManager` contract is used to calculate the total amount of ETH staked in the contract. However, it does not take into account the ETH staked by validators in the pending state. This means that the total stake calculated by the function is less than it sh

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting tvl error logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting tvl error in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: Function `getTotalStake()` fails to account for pending validators, leading to i** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md`
```solidity
function getTotalStake() public view returns (uint256 totalStake) {
  // @audit Validators in pending state is not accounted for
  totalStake = unassignedBalance + readyValidatorIds.length * VALIDATOR_CAPACITY + latestActiveBalanceAfterFee
      + delayedEffectiveBalance + withdrawnEffectiveBalance + subtractRewardFee(delayedRewards) - unstakeQueueAmount;
}
```

**Example 2: [H-04] Strategy allocation tracking errors affect TVL calculations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-04-strategy-allocation-tracking-errors-affect-tvl-calculations.md`
```solidity
function getTotalAssetTVL(address asset) public view returns (uint256 totalTVL) {
    uint256 poolBalance = IERC20(asset).balanceOf(address(this));
    uint256 strategyAllocated = assetsAllocatedToStrategies[asset];
    uint256 unstakingVaultBalance = _getUnstakingVaultBalance(asset);

    return poolBalance + strategyAllocated + unstakingVaultBalance;
}
```

**Example 3: [M-04] Delayed slashing window and lack of transparency for pending slashes coul** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-delayed-slashing-window-and-lack-of-transparency-for-pending-slashes-could-.md`
```solidity
function handleSlashing(IERC20 token, uint256 amount) external {
        if (amount == 0) revert ZeroAmount();
        if (!_config().supportedAssets[token]) revert UnsupportedAsset();

        SafeTransferLib.safeTransferFrom(address(token), msg.sender, address(this), amount);
        // Below is where custom logic for each asset lives
        SafeTransferLib.safeTransfer(address(token), address(0), amount);
    }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting tvl error logic allows exploitation through missing validation, in
func secureAccountingTvlError(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 3 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 1
- **Affected Protocols**: Karak, Elytra_2025-07-10, Casimir
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Accounting State Corruption

### Overview

Implementation flaw in accounting state corruption logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 2 audit reports with severity distribution: HIGH: 1, MEDIUM: 1.

> **Key Finding**: This bug report describes a problem in the code of a smart contract that could cause permanent corruption. The problem occurs when the oracle reports a decrease in the amount of rewards or penalties for a validator. This is not accounted for in the code, so the validator manager's accounting becomes

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting state corruption logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting state corruption in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: Any decrease in slashed or rewarded amounts reported will make validatorManager ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/any-decrease-in-slashed-or-rewarded-amounts-reported-will-make-validatormanager-.md`
```solidity
// ValidatorManager.sol#L469-L503

/// @notice Report a reward event for a validator
/// @param validator Address of the validator to be rewarded
/// @param amount Amount of rewards for the validator
function reportRewardEvent(address validator, uint256 amount) external onlyRole(ORACLE_ROLE) validatorActive(validator) {
    require(amount > 0, "Invalid reward amount");
    // Update reward amounts
    totalRewards += amount; // @audit has to follow Oracle updates
    validatorRewards[validator] += amount;
    emit RewardEventReported(validator, amount);
}

/* ========== SLASHING ========== */

/// @notice Report a slashing event for a validator
/// @param validator Address of the validator to be slashed
/// @param amount Amount to slash from the validator
function reportSlashingEvent(address validator, uint256 amount) external onlyRole(ORACLE_ROLE) validatorActive(validator) {
    require(amount > 0, "Invalid slash amount");
    // Update slashing amounts
    totalSlashing += amount; // @audit has to follow Oracle updates
    validatorSlashing[validator] += amount;
    emit SlashingEventReported(validator, amount);
}
```

**Example 2: Incorrect accounting in LockingController.applyLosses function** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/incorrect-accounting-in-lockingcontrollerapplylosses-function.md`
```go
uint256 allocation = epochTotalReceiptToken.mulDivUp(_amount, _globalReceiptToken);
_globalReceiptToken -= allocation;
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting state corruption logic allows exploitation through missing validat
func secureAccountingStateCorruption(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 2 audit reports
- **Severity Distribution**: HIGH: 1, MEDIUM: 1
- **Affected Protocols**: infiniFi contracts, Kinetiq LST
- **Validation Strength**: Single auditor

---

## 5. Accounting Missing Deduction

### Overview

Implementation flaw in accounting missing deduction logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 3, MEDIUM: 2.

> **Key Finding**: The `_checkBalance` function in the OETHVaultCore.sol contract is not returning the correct balance in certain scenarios. Specifically, if the WETH in the withdrawal queue exceeds the total amount of workable assets, the function should return a balance of 0 but instead returns the amount of WETH in

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting missing deduction logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting missing deduction in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: _checkBalance Returns an Incorrect Value During Insolvency** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md`
```
// Vulnerable pattern from OETH Withdrawal Queue Audit:
The [`_checkBalance`](https://github.com/OriginProtocol/origin-dollar/blob/eca6ffa74d9d0c5fb467551a30912cb722fab9c2/contracts/contracts/vault/OETHVaultCore.sol#L392-L407) function returns the balance of an asset held in the vault and all the strategies. If the requested asset is WETH, the amount of WETH reserved for the withdrawal queue is subtracted from this balance to reflect the correct amount of workable assets. In this specific case, the function returns the same result as [the `_totalValu
```

**Example 2: Public vaults can become insolvent because of missing `yIntercept` update** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-9-public-vaults-can-become-insolvent-because-of-missing-yintercept-update.md`
```go
/**
   * @notice Hook to update the slope and yIntercept of the PublicVault on payment.
   * The rate for the LienToken is subtracted from the total slope of the PublicVault, and recalculated in afterPayment().
   * @param lienId The ID of the lien.
   * @param amount The amount paid off to deduct from the yIntercept of the PublicVault.
   */
```

**Example 3: Missing Balance Deduction in Unstaking Functions Allows Contract Drainage and Lo** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md`
```
// Vulnerable pattern from Sapien:
**Update**
Marked as "Fixed" by the client. Addressed in: `4a45a4a`.

![Image 26: Alert icon](https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the client. Addressed in: `f647099b7988fa4d01fac6a9f3481d25e748527a`. The client provided the following explanation:

> The vulnerability in the unstaking functions was fixed by implementing proper balance deduction and
```

**Example 4: Missing validation that ensures unspent BTC is fully sent back as change in Lomb** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/missing-validation-that-ensures-unspent-btc-is-fully-sent-back-as-change-in-lomb.md`
```
// Vulnerable pattern from Lombard Finance:
## Lombard Transfer Signing Strategy
```

**Example 5: The delegator resetting self-delegation causes multiple issues in the protocol** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/the-delegator-resetting-self-delegation-causes-multiple-issues-in-the-protocol.md`
```
// Vulnerable pattern from Templedao:
**Description:** Whenever the vote power of delegators are changed, the validity of self-delegation of the delegator is not checked, which results in issues in multiple parts of the protocol.

- `unsetUserVoteDelegate`: It does not allow stakers to unset delegation through the function because it tries to subtract delegated balance from zero.
- `_withdrawFor`: It does not allow stakers to withdraw their assets because it tries to subtract delegated balance from zero.
- `_stakeFor`: It allows mal
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting missing deduction logic allows exploitation through missing valida
func secureAccountingMissingDeduction(ctx sdk.Context) error {
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
- **Affected Protocols**: Astaria, OETH Withdrawal Queue Audit, Templedao, Lombard Finance, Sapien
- **Validation Strength**: Strong (3+ auditors)

---

## 6. Accounting Cross Module

### Overview

Implementation flaw in accounting cross module logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 1 audit reports with severity distribution: MEDIUM: 1.

> **Key Finding**: The bug report discusses a vulnerability in the Zetachain setup where the Ethermint hooks are not triggered when calling into the zEVM from the crosschain module. This allows an attacker to bypass the pausing protection and withdraw funds that should not be accessible. The report suggests adding the

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting cross module logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting cross module in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: [M-26] ZRC20 Token Pause Check Bypass** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-26-zrc20-token-pause-check-bypass.md`
```go
go test ./x/crosschain/keeper/gas_payment_test.go -run TestZRC20PauseBypassTry2 -v
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting cross module logic allows exploitation through missing validation,
func secureAccountingCrossModule(ctx sdk.Context) error {
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
- **Affected Protocols**: ZetaChain
- **Validation Strength**: Single auditor

---

## 7. Accounting Pending Tracking

### Overview

Implementation flaw in accounting pending tracking logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 5 audit reports with severity distribution: HIGH: 3, MEDIUM: 2.

> **Key Finding**: This bug report discusses a problem with the staking protocol that can lead to overestimation of the staking balance. This occurs when a payout fails to transfer after a game is completed, causing the amount to be stored in a separate account. However, the protocol continues to include this amount i

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting pending tracking logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting pending tracking in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: [C-01] Pending payouts excluded from total balance cause incorrect share calcula** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-01-pending-payouts-excluded-from-total-balance-cause-incorrect-share-calculati.md`
```solidity
function transferPayout(address token, address recipient, uint256 amount) external {
    --- SNIPPED ---
    if (!callSucceeded) {
@<>     pendingPayouts[token][recipient] += amount;
        emit TransferFailed(token, recipient, amount);
        return false;
    }
    --- SNIPPED ---
}
```

**Example 2: [C-02] Pending stake not accounted for in liquidity calculations** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-02-pending-stake-not-accounted-for-in-liquidity-calculations.md`
```solidity
function requestStake(address token, uint256 amount) external nonReentrant {
    --- SNIPPED ---

    // Transfer the tokens from the user to this contract
@>  IERC20(token).safeTransferFrom(msg.sender, address(this), amount);

    --- SNIPPED ---
}
```

**Example 3: Function `getTotalStake()` fails to account for pending validators, leading to i** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md`
```solidity
function getTotalStake() public view returns (uint256 totalStake) {
  // @audit Validators in pending state is not accounted for
  totalStake = unassignedBalance + readyValidatorIds.length * VALIDATOR_CAPACITY + latestActiveBalanceAfterFee
      + delayedEffectiveBalance + withdrawnEffectiveBalance + subtractRewardFee(delayedRewards) - unstakeQueueAmount;
}
```

**Example 4: Include Pending In Unstake** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/include-pending-in-unstake.md`
```go
let validators = validator_set::get_validators(&self.validator_set);
let unstaked_sui = unstake_amount_from_validators(self, wrapper, amount, fee, validators, ctx);
// assert should never be reached because the pool is self-sufficient
assert!(coin::value(&unstaked_sui) == amount - fee, E_NOTHING_TO_UNSTAKE);
```

**Example 5: [M-05] Changing VoteWeighting contract can result in lost staking incentives** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-05-changing-voteweighting-contract-can-result-in-lost-staking-incentives.md`
```solidity
function changeManagers(address _tokenomics, address _treasury, address _voteWeighting) external {
        // Check for the contract ownership
        if (msg.sender != owner) {
            revert OwnerOnly(msg.sender, owner);
        }

        // Change Tokenomics contract address
        if (_tokenomics != address(0)) {
            tokenomics = _tokenomics;
            emit TokenomicsUpdated(_tokenomics);
        }

        // Change Treasury contract address
        if (_treasury != address(0)) {
            treasury = _treasury;
            emit TreasuryUpdated(_treasury);
        }

        // Change Vote Weighting contract address
        if (_voteWeighting != address(0)) {
            voteWeighting = _voteWeighting;
            emit VoteWeightingUpdated(_voteWeighting);
        }
    }
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting pending tracking logic allows exploitation through missing validat
func secureAccountingPendingTracking(ctx sdk.Context) error {
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
- **Affected Protocols**: Olas, Coinflip_2025-02-19, Casimir, Volo
- **Validation Strength**: Strong (3+ auditors)

---

## 8. Accounting Negative Value

### Overview

Implementation flaw in accounting negative value logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 9 audit reports with severity distribution: HIGH: 4, MEDIUM: 5.

> **Key Finding**: The bug report discusses an issue where an attacker can cause the chain to halt by sending a negative amount in the `MsgRemoveStake` or `MsgRemoveDelegateStake` messages. This is due to a lack of validation for the amount parameter in these messages. The bug can be triggered at any time and can caus

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting negative value logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting negative value in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: Adversary can arbitrarily trigger a chain halt by sending `MsgRemove{Delegate}St** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md`
```go
func RemoveStakes(
	sdkCtx sdk.Context,
	currentBlock int64,
	k emissionskeeper.Keeper,
) {
	removals, err := k.GetStakeRemovalsForBlock(sdkCtx, currentBlock)
	...
	for _, stakeRemoval := range removals {
		...
		coins := sdk.NewCoins(sdk.NewCoin(chainParams.DefaultBondDenom, stakeRemoval.Amount))
```

**Example 2: If the Covenant signature does not pass , EXPIRED events it will still be execut** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-3-if-the-covenant-signature-does-not-pass-expired-events-it-will-still-be-exec.md`
```go
func (ms msgServer) AddBTCDelegationInclusionProof(
	goCtx context.Context,
	req *types.MsgAddBTCDelegationInclusionProof,
) (*types.MsgAddBTCDelegationInclusionProofResponse, error) {
    ......
	activeEvent := types.NewEventPowerDistUpdateWithBTCDel(
		&types.EventBTCDelegationStateUpdate{
			StakingTxHash: stakingTxHash.String(),
			NewState:      types.BTCDelegationStatus_ACTIVE,
		},
	)

	ms.addPowerDistUpdateEvent(ctx, timeInfo.TipHeight, activeEvent)

	// record event that the BTC delegation will become unbonded at EndHeight-w
	expiredEvent := types.NewEventPowerDistUpdateWithBTCDel(&types.EventBTCDelegationStateUpdate{
		StakingTxHash: req.StakingTxHash,
		NewState:      types.BTCDelegationStatus_EXPIRED,
	})

	// NOTE: we should have verified that EndHeight > btcTip.Height + min_unbonding_time
	ms.addPowerDistUpdateEvent(ctx, btcDel.EndHeight-params.UnbondingTimeBlocks, expiredEvent)
......
}
```

**Example 3: Incorrect accounting in LockingController.applyLosses function** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/incorrect-accounting-in-lockingcontrollerapplylosses-function.md`
```go
uint256 allocation = epochTotalReceiptToken.mulDivUp(_amount, _globalReceiptToken);
_globalReceiptToken -= allocation;
```

**Example 4: Lack of rebasable tokens support** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/lack-of-rebasable-tokens-support.md`
```
// Vulnerable pattern from XPress:
##### Description
The issue is identified in the [`LOB`](https://github.com/longgammalabs/hanji-contracts/blob/09b6188e028650b9c1758010846080c5f8c80f8e/src/OnchainLOB.sol) contract.

For rebasable tokens, such as those that adjust their supply over time (e.g., Ampleforth), the LOB contract may keep all rewards in the contract balance. During a rebase (positive or negative), the recorded balances in the contract may not accurately reflect the true balances of the tokens held. This discrepancy can
```

**Example 5: Negative rebase of stETH could prevent a round from ending** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md`
```
// Vulnerable pattern from Pods Finance Ethereum Volatility Vault Audit:
When a round ends, the amount of underlying assets currently in the vault is [subtracted](https://github.com/pods-finance/yield-contracts/blob/c4b401ce674c24798de5f9d02c82e466ee0a2600/contracts/vaults/STETHVault.sol#L97) from the amount of assets the vault contained in the previous round. This calculation assumes a positive yield, but the underlying asset stETH is able to rebase in both a positive and negative direction due to the potential for slashing. In the case where Lido is slashed, `total
```

**Variant: Accounting Negative Value - MEDIUM Severity Cases** [MEDIUM]
> Found in 5 reports:
> - `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md`
> - `reports/cosmos_cometbft_findings/refund-can-be-over-credited-in-a-negative-yield-event.md`
> - `reports/cosmos_cometbft_findings/refunds-will-be-over-credited-in-a-negative-yield-event.md`

**Variant: Accounting Negative Value in Pods Finance Ethereum Volatility Vault Audit** [MEDIUM]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/negative-rebase-of-steth-could-prevent-a-round-from-ending.md`
> - `reports/cosmos_cometbft_findings/refund-can-be-over-credited-in-a-negative-yield-event.md`
> - `reports/cosmos_cometbft_findings/refunds-will-be-over-credited-in-a-negative-yield-event.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting negative value logic allows exploitation through missing validatio
func secureAccountingNegativeValue(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 9 audit reports
- **Severity Distribution**: HIGH: 4, MEDIUM: 5
- **Affected Protocols**: Superform, Pods Finance Ethereum Volatility Vault Audit, infiniFi contracts, LMCV part 2, Allora
- **Validation Strength**: Strong (3+ auditors)

---

## 9. Accounting Fee Deduction

### Overview

Implementation flaw in accounting fee deduction logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 4 audit reports with severity distribution: HIGH: 1, MEDIUM: 3.

> **Key Finding**: Issue H-35 is a bug found by csanuragjain in the handleIncomingPayment function of the AuctionHouse.sol code in the Astaria project. If the transferAmount is greater than the combined amount of all lien.amounts, then the initiatorPayment is calculated on the full transferAmount, even though only a p

### Vulnerability Description

#### Root Cause

Implementation flaw in accounting fee deduction logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies accounting fee deduction in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to accounting operations

### Vulnerable Pattern Examples

**Example 1: Incorrect fees will be charged** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-35-incorrect-fees-will-be-charged.md`
```go
uint256 initiatorPayment = transferAmount.mulDivDown(
      auction.initiatorFee,
      100
    );
```

**Example 2: Ignite fee is not returned for pre-validated `QI` stakes in the event of registr** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/ignite-fee-is-not-returned-for-pre-validated-qi-stakes-in-the-event-of-registrat.md`
```
// Vulnerable pattern from Benqi Ignite:
**Description:** The `1 AVAX` [Ignite fee](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L387) applied to pre-validated `QI` stakes is [paid to the fee recipient](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L388) at the time of registration. If this registration fails (e.g. due to off-chain BLS proof validation), the registration will be [marked as withdrawable](https://githu
```

**Example 3: [M-04] Gas refunds use block gas instead of transaction gas, leading to incorrec** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-gas-refunds-use-block-gas-instead-of-transaction-gas-leading-to-incorrect-r.md`
```go
// https://github.com/code-423n4/2024-11-nibiru/blob/84054a4f00fdfefaa8e5849c53eb66851a762319/app/evmante/evmante_gas_consume.go#L100-L105
		fees, err := keeper.VerifyFee(
			txData,
			evm.EVMBankDenom,
			baseFeeMicronibiPerGas,
			ctx.IsCheckTx(),
		)
```

**Example 4: `msg_server_stake::AddStake` calculates the weight incorrectly resulting in inco** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-32-msg_server_stakeaddstake-calculates-the-weight-incorrectly-resulting-in-inc.md`
```go
// Return the target weight of a topic
// ^w_{t,i} = S^{μ}_{t,i} * (P/C)^{ν}_{t,i}
// where S_{t,i} is the stake of of topic t in the last reward epoch i
// and (P/C)_{t,i} is the fee revenue collected for performing inference per topic epoch
// requests for topic t in the last reward epoch i
// μ, ν are global constants with fiduciary values of 0.5 and 0.5
```

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in accounting fee deduction logic allows exploitation through missing validation
func secureAccountingFeeDeduction(ctx sdk.Context) error {
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
- **Severity Distribution**: HIGH: 1, MEDIUM: 3
- **Affected Protocols**: Nibiru, Benqi Ignite, Astaria, Allora
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Accounting Balance Not Updated
grep -rn 'accounting|balance|not|updated' --include='*.go' --include='*.sol'
# Accounting Double Counting
grep -rn 'accounting|double|counting' --include='*.go' --include='*.sol'
# Accounting Tvl Error
grep -rn 'accounting|tvl|error' --include='*.go' --include='*.sol'
# Accounting State Corruption
grep -rn 'accounting|state|corruption' --include='*.go' --include='*.sol'
# Accounting Missing Deduction
grep -rn 'accounting|missing|deduction' --include='*.go' --include='*.sol'
# Accounting Cross Module
grep -rn 'accounting|cross|module' --include='*.go' --include='*.sol'
# Accounting Pending Tracking
grep -rn 'accounting|pending|tracking' --include='*.go' --include='*.sol'
# Accounting Negative Value
grep -rn 'accounting|negative|value' --include='*.go' --include='*.sol'
# Accounting Fee Deduction
grep -rn 'accounting|fee|deduction' --include='*.go' --include='*.sol'
```

## Keywords

`account`, `accounted`, `accounting`, `adversary`, `affect`, `allocation`, `allows`, `amount`, `amounts`, `appchain`, `arbitrarily`, `balance`, `bank`, `because`, `become`, `before`, `block`, `broken`, `bypass`, `calculations`, `cause`, `chain`, `changes`, `charged`, `check`, `committed`, `contract`, `corruption`, `cosmos`, `could`

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`AddBTCDelegationInclusionProof`, `SyncStateDBWithAccount`, `a`, `accounting`, `appchain`, `balance`, `balanceOf`, `balance_not_updated`, `balance_tracking_errors`, `changeManagers`, `cosmos`, `cross_module`, `defi`, `double_counting`, `fee_deduction`, `for`, `getTotalAssetTVL`, `getTotalStake`, `handleSlashing`, `happens`, `mint`, `missing_deduction`, `msg.sender`, `negative_value`, `of`, `pending_tracking`, `staking`, `state_corruption`, `tvl_error`
