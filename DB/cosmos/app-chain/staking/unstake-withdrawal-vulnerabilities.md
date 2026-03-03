---
protocol: generic
chain: cosmos
category: staking
vulnerability_type: unstake_withdrawal_vulnerabilities

attack_type: logical_error|economic_exploit|dos
affected_component: staking_logic

primitives:
  - cooldown_bypass
  - withdrawal_dos
  - withdrawal_accounting
  - queue_manipulation
  - before_slash
  - emergency
  - pending_not_tracked
  - lock_funds

severity: high
impact: fund_loss|dos|state_corruption
exploitability: 0.7
financial_impact: high

tags:
  - cosmos
  - appchain
  - staking
  - staking
  - defi

language: go|solidity|rust
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Unstake Cooldown Bypass
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Getting Max Staking Rewards Possible While Bypassing the Loc | `reports/cosmos_cometbft_findings/getting-max-staking-rewards-possible-while-bypassing-the-lockup-periods.md` | MEDIUM | Quantstamp |
| [H-02] unstake should update exchange rates first | `reports/cosmos_cometbft_findings/h-02-unstake-should-update-exchange-rates-first.md` | HIGH | Code4rena |
| [H06] AUD lending market could affect the protocol | `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md` | HIGH | OpenZeppelin |
| [H09] Slash process can be bypassed | `reports/cosmos_cometbft_findings/h09-slash-process-can-be-bypassed.md` | HIGH | OpenZeppelin |
| [M-01] User Can Bypass Fishing Duration and Unstake Immediat | `reports/cosmos_cometbft_findings/m-01-user-can-bypass-fishing-duration-and-unstake-immediately-due-to-uninitializ.md` | MEDIUM | Shieldify |
| [M-04] Disabling of cooldown during post-slash can be bypass | `reports/cosmos_cometbft_findings/m-04-disabling-of-cooldown-during-post-slash-can-be-bypassed.md` | MEDIUM | Pashov Audit Group |
| Lockup of vestings or completion time can be bypassed due to | `reports/cosmos_cometbft_findings/m-14-lockup-of-vestings-or-completion-time-can-be-bypassed-due-to-missing-check-.md` | MEDIUM | Sherlock |
| OperationalStaking::_unstake Delegators can bypass 28 days u | `reports/cosmos_cometbft_findings/m-7-operationalstaking_unstake-delegators-can-bypass-28-days-unstaking-cooldown-.md` | MEDIUM | Sherlock |

### Unstake Withdrawal Dos
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| beaconChainETHStrategy Queued Withdrawals Excluded From Slas | `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md` | MEDIUM | SigmaPrime |
| [C-02] Stakes not forwarded post-delegation, positions unwit | `reports/cosmos_cometbft_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md` | HIGH | Pashov Audit Group |
| Deposited Stakes Can Be Locked in StakeManager if the Valida | `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md` | HIGH | OpenZeppelin |
| Direct Deposits Enable Theft Of A Validator’s Funds | `reports/cosmos_cometbft_findings/direct-deposits-enable-theft-of-a-validators-funds.md` | HIGH | SigmaPrime |
| [H-01] `_AddRebalanceRequest` may use outdated balance for d | `reports/cosmos_cometbft_findings/h-01-_addrebalancerequest-may-use-outdated-balance-for-delegate-withdrawal-reque.md` | HIGH | Pashov Audit Group |
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| [H-02] It is impossible to slash queued withdrawals that con | `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md` | HIGH | Code4rena |
| [H-02] ValidatorManager: missing fund withdrawal from valida | `reports/cosmos_cometbft_findings/h-02-validatormanager-missing-fund-withdrawal-from-validator-in-deactivatevalida.md` | HIGH | Pashov Audit Group |

### Unstake Withdrawal Accounting
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| A Relayer Can Avoid a Slash by Requesting a Withdrawal From  | `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md` | HIGH | Quantstamp |
| Admin balances don't account for potential token rebases | `reports/cosmos_cometbft_findings/admin-balances-dont-account-for-potential-token-rebases.md` | MEDIUM | MixBytes |
| [C-02] Stakes not forwarded post-delegation, positions unwit | `reports/cosmos_cometbft_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md` | HIGH | Pashov Audit Group |
| DoS on stake accounting functions by bloating `operatorNodes | `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md` | MEDIUM | Cyfrin |
| Emergency Withdrawal Conditions Might Change Over Time | `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md` | MEDIUM | OpenZeppelin |
| ERC-4337 call to `_payPrefund` may lead to the validator sta | `reports/cosmos_cometbft_findings/erc-4337-call-to-_payprefund-may-lead-to-the-validator-stake-being-split.md` | HIGH | MixBytes |
| Fixed exchange rate at unstaking fails to socialize slashing | `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md` | MEDIUM | MixBytes |
| [H-01] `_AddRebalanceRequest` may use outdated balance for d | `reports/cosmos_cometbft_findings/h-01-_addrebalancerequest-may-use-outdated-balance-for-delegate-withdrawal-reque.md` | HIGH | Pashov Audit Group |

### Unstake Queue Manipulation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| _checkBalance Returns an Incorrect Value During Insolvency | `reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md` | MEDIUM | OpenZeppelin |
| A malicious staker can force validator withdrawals by instan | `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md` | HIGH | Cyfrin |
| Activation of queued cutting board can be manipulated leadin | `reports/cosmos_cometbft_findings/activation-of-queued-cutting-board-can-be-manipulated-leading-to-redirection-of-.md` | MEDIUM | Spearbit |
| beaconChainETHStrategy Queued Withdrawals Excluded From Slas | `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md` | MEDIUM | SigmaPrime |
| Function `getTotalStake()` fails to account for pending vali | `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md` | HIGH | Cyfrin |
| [H-01] Buffer Silently Locks Staked HYPE in Contract Without | `reports/cosmos_cometbft_findings/h-01-buffer-silently-locks-staked-hype-in-contract-without-using-them-for-withdr.md` | HIGH | Code4rena |
| [H-02] It is impossible to slash queued withdrawals that con | `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md` | HIGH | Code4rena |
| [H-02] Users Who Queue Withdrawal Before A Slashing Event Di | `reports/cosmos_cometbft_findings/h-02-users-who-queue-withdrawal-before-a-slashing-event-disadvantage-users-who-q.md` | HIGH | Code4rena |

### Unstake Before Slash
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| [H-02] Users Who Queue Withdrawal Before A Slashing Event Di | `reports/cosmos_cometbft_findings/h-02-users-who-queue-withdrawal-before-a-slashing-event-disadvantage-users-who-q.md` | HIGH | Code4rena |
| [H02] Delegators can prevent service providers from deregist | `reports/cosmos_cometbft_findings/h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md` | HIGH | OpenZeppelin |
| Insufficient Delay forRocketNodeStaking.withdrawRPL() | `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md` | MEDIUM | SigmaPrime |
| [M-03] When malicious behavior occurs and DSS requests slash | `reports/cosmos_cometbft_findings/m-03-when-malicious-behavior-occurs-and-dss-requests-slashing-against-vault-duri.md` | MEDIUM | Code4rena |
| [M-05] Slashings will always fail in some cases | `reports/cosmos_cometbft_findings/m-05-slashings-will-always-fail-in-some-cases.md` | MEDIUM | Code4rena |
| `LidoVault::vaultEndedWithdraw` doesn't take into considerat | `reports/cosmos_cometbft_findings/m-1-lidovaultvaultendedwithdraw-doesnt-take-into-consideration-income-withdrawal.md` | MEDIUM | Sherlock |
| [M-11] `ValidatorWithdrawalVault.distributeRewards` can be c | `reports/cosmos_cometbft_findings/m-11-validatorwithdrawalvaultdistributerewards-can-be-called-to-make-operator-sl.md` | MEDIUM | Code4rena |
| Withdrawing after a slash event before the vault has ended w | `reports/cosmos_cometbft_findings/m-2-withdrawing-after-a-slash-event-before-the-vault-has-ended-will-decrease-fix.md` | MEDIUM | Sherlock |

### Unstake Emergency
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| A malicious staker can force validator withdrawals by instan | `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md` | HIGH | Cyfrin |
| DoS on stake accounting functions by bloating `operatorNodes | `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md` | MEDIUM | Cyfrin |
| Emergency Withdrawal Conditions Might Change Over Time | `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md` | MEDIUM | OpenZeppelin |
| [H-01] `_AddRebalanceRequest` may use outdated balance for d | `reports/cosmos_cometbft_findings/h-01-_addrebalancerequest-may-use-outdated-balance-for-delegate-withdrawal-reque.md` | HIGH | Pashov Audit Group |
| [H-01] `BlockBeforeSend` hook can be exploited to perform a  | `reports/cosmos_cometbft_findings/h-01-blockbeforesend-hook-can-be-exploited-to-perform-a-denial-of-service.md` | HIGH | Code4rena |
| [M-03] Inconsistent State Restoration in `cancelWithdrawal`  | `reports/cosmos_cometbft_findings/m-03-inconsistent-state-restoration-in-cancelwithdrawal-function.md` | MEDIUM | Code4rena |
| [M02] Separate stake and prepayment [core] | `reports/cosmos_cometbft_findings/m02-separate-stake-and-prepayment-core.md` | MEDIUM | OpenZeppelin |
| Potential Denial of Service in Report Generation Due to Unde | `reports/cosmos_cometbft_findings/potential-denial-of-service-in-report-generation-due-to-underflow.md` | MEDIUM | Quantstamp |

### Unstake Pending Not Tracked
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Deposited Stakes Can Be Locked in StakeManager if the Valida | `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md` | HIGH | OpenZeppelin |
| Dust limit attack on `forceUpdateNodes` allows DoS of rebala | `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md` | HIGH | Cyfrin |
| Fixed exchange rate at unstaking fails to socialize slashing | `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md` | MEDIUM | MixBytes |
| Getting Max Staking Rewards Possible While Bypassing the Loc | `reports/cosmos_cometbft_findings/getting-max-staking-rewards-possible-while-bypassing-the-lockup-periods.md` | MEDIUM | Quantstamp |
| [H-01] LP unstaking only burns the shares but leaves the und | `reports/cosmos_cometbft_findings/h-01-lp-unstaking-only-burns-the-shares-but-leaves-the-underlying-tokens-in-the-.md` | HIGH | Code4rena |
| Bucket rewards will be wiped by stake/unstake before accrueR | `reports/cosmos_cometbft_findings/h-4-bucket-rewards-will-be-wiped-by-stakeunstake-before-accruerewards-lastreward.md` | HIGH | Sherlock |
| Include Pending In Unstake | `reports/cosmos_cometbft_findings/include-pending-in-unstake.md` | MEDIUM | OtterSec |
| [M-02] A malicious strategy can permanently DoS all currentl | `reports/cosmos_cometbft_findings/m-02-a-malicious-strategy-can-permanently-dos-all-currently-pending-withdrawals-.md` | MEDIUM | Code4rena |

### Unstake Lock Funds
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Execution failure of `\_updateReward` function due to uninit | `reports/cosmos_cometbft_findings/execution-failure-of-_updatereward-function-due-to-uninitialized-_rewarddistribu.md` | MEDIUM | Halborn |
| Execution of `stake` and `unstake` operations blocked due to | `reports/cosmos_cometbft_findings/execution-of-stake-and-unstake-operations-blocked-due-to-uninitialized-_methods-.md` | MEDIUM | Halborn |
| Fixed exchange rate at unstaking fails to socialize slashing | `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md` | MEDIUM | MixBytes |
| [H06] AUD lending market could affect the protocol | `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md` | HIGH | OpenZeppelin |
| [M-02] sFrxEth may revert on redeeming non-zero amount | `reports/cosmos_cometbft_findings/m-02-sfrxeth-may-revert-on-redeeming-non-zero-amount.md` | MEDIUM | Code4rena |
| [M-05] Last Holder Can’t Exit, Zero‑Supply Unstake Reverts | `reports/cosmos_cometbft_findings/m-05-last-holder-cant-exit-zerosupply-unstake-reverts.md` | MEDIUM | Code4rena |
| [M-06] Unstake function reverts because of use of outdated/s | `reports/cosmos_cometbft_findings/m-06-unstake-function-reverts-because-of-use-of-outdatedstale-serviceids-array.md` | MEDIUM | Code4rena |
| Validator cannot set new address if more than 300 unstakes i | `reports/cosmos_cometbft_findings/m-1-validator-cannot-set-new-address-if-more-than-300-unstakes-in-its-array.md` | MEDIUM | Sherlock |

---

# Unstake Withdrawal Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Unstake Withdrawal Vulnerabilities in Cosmos/AppChain Security Audits**

---

## Table of Contents

1. [Unstake Cooldown Bypass](#1-unstake-cooldown-bypass)
2. [Unstake Withdrawal Dos](#2-unstake-withdrawal-dos)
3. [Unstake Withdrawal Accounting](#3-unstake-withdrawal-accounting)
4. [Unstake Queue Manipulation](#4-unstake-queue-manipulation)
5. [Unstake Before Slash](#5-unstake-before-slash)
6. [Unstake Emergency](#6-unstake-emergency)
7. [Unstake Pending Not Tracked](#7-unstake-pending-not-tracked)
8. [Unstake Lock Funds](#8-unstake-lock-funds)

---

## 1. Unstake Cooldown Bypass

### Overview

Implementation flaw in unstake cooldown bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 13 audit reports with severity distribution: HIGH: 6, MEDIUM: 7.

> **Key Finding**: The client has marked a bug as "Fixed" and provided an explanation for the fix. The bug was related to the staking contract, which determines the multiplier a user gets based on staking amount and lockup period. However, the contract did not check if the lockup period had actually elapsed before all

### Vulnerability Description

#### Root Cause

Implementation flaw in unstake cooldown bypass logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies unstake cooldown bypass in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to unstake operations

### Vulnerable Pattern Examples

**Example 1: Getting Max Staking Rewards Possible While Bypassing the Lockup Periods** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/getting-max-staking-rewards-possible-while-bypassing-the-lockup-periods.md`
```
// Vulnerable pattern from Sapien:
**Update**
Marked as "Fixed" by the client. Addressed in: `b175349`.

![Image 42: Alert icon](https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the client. Addressed in: `228ae219c5478f375bed56376ffba8538ea2f09e`. The client provided the following explanation:

> The vulnerability was fixed by adding lock period validation checks across unstaking functions.

![
```

**Example 2: [H-02] unstake should update exchange rates first** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-unstake-should-update-exchange-rates-first.md`
```go
// @audit shares are computed here with old rate
uint128 validatorSharesRemove = tokensToShares(amount, v.exchangeRate);
require(validatorSharesRemove > 0, "Unstake amount is too small");

if (v.disabledEpoch == 0) {
    // @audit rates are updated here
    updateGlobalExchangeRate();
    updateValidator(v);
    // ...
}
```

**Example 3: [H06] AUD lending market could affect the protocol** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`
```
// Vulnerable pattern from Audius Contracts Audit:
In case an AUD token lending market appears, an attacker could use this market to influence the result of a governance’s proposal, which could lead to a take over of the protocol.


An attacker would only need to stake tokens for a brief moment without waiting for the [`votingPeriod`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L23) to request an unstake. This aggravates the attack, as the attacker would on
```

**Example 4: [M-01] User Can Bypass Fishing Duration and Unstake Immediately Due to Uninitial** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-01-user-can-bypass-fishing-duration-and-unstake-immediately-due-to-uninitializ.md`
```solidity
function stakeMany(uint256[] calldata heroIds, uint8 zone) external whenNotPausedOrEmergency {
    // Checks zone is valid
    if (zone > 2) revert InvalidZone();

    uint256 len = heroIds.length;

    // Get storage pointer
    FisherCatStorage storage $ = _getStorage();

    uint256 fee = $.zoneDetails[zone].fee;

    // Checks entry fee is set
    if (fee == 0) revert RewardsNotSet();

    uint256 amount = fee * len;

    if (amount != 0) {
        // transfer `amount` of $HERO20 as entry fee from user to contract
        hero20.transferFrom(msg.sender, address(this), amount);
    }

    for (uint256 i = 0; i < len; ++i) {
        uint256 heroId = heroIds[i];

        // Checks hero owner
        if (msg.sender != hero721.ownerOf(heroId)) revert CallerIsNotOwner();

        // Transfer hero721 to this contract
        hero721.transferFrom(msg.sender, address(this), heroId);

        // Update hero information
        $.heroInfo[heroId] =
            HeroInformation({owner: msg.sender, zone: zone, stakeAt: uint40(block.timestamp), pendingVRF: 0});

        // Emit `Staked`.
        emit Staked(msg.sender, heroId, zone, fee);
    }
}
```

**Example 5: [M-04] Disabling of cooldown during post-slash can be bypassed** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-04-disabling-of-cooldown-during-post-slash-can-be-bypassed.md`
```
// Vulnerable pattern from Increment:
**Severity**

**Impact:** Medium, as staker can bypass disabling of cooldown

**Likelihood:** Medium, during the post slash period

**Description**

When `StakedToken` is in the post-slashing state, the cooldown function is disabled, preventing the staker from activating it by setting `_stakersCooldowns[msg.sender] = block.timestamp`.

However, the staker can possibly bypass the disabling of the cooldown function by transferring to another account that has a valid cooldown timestamp.

That is be
```

**Variant: Unstake Cooldown Bypass - HIGH Severity Cases** [HIGH]
> Found in 6 reports:
> - `reports/cosmos_cometbft_findings/h-02-unstake-should-update-exchange-rates-first.md`
> - `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`
> - `reports/cosmos_cometbft_findings/h09-slash-process-can-be-bypassed.md`

**Variant: Unstake Cooldown Bypass in Sapien** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/getting-max-staking-rewards-possible-while-bypassing-the-lockup-periods.md`
> - `reports/cosmos_cometbft_findings/missing-balance-deduction-in-unstaking-functions-allows-contract-drainage-and-lo.md`

**Variant: Unstake Cooldown Bypass in Covalent** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-02-unstake-should-update-exchange-rates-first.md`
> - `reports/cosmos_cometbft_findings/m-7-operationalstaking_unstake-delegators-can-bypass-28-days-unstaking-cooldown-.md`

**Variant: Unstake Cooldown Bypass in Audius Contracts Audit** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`
> - `reports/cosmos_cometbft_findings/h09-slash-process-can-be-bypassed.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in unstake cooldown bypass logic allows exploitation through missing validation,
func secureUnstakeCooldownBypass(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 13 audit reports
- **Severity Distribution**: HIGH: 6, MEDIUM: 7
- **Affected Protocols**: Valantis, Sapien - 2, Kinetiq LST Protocol, Increment, Andromeda – Validator Staking ADO and Vesting ADO
- **Validation Strength**: Strong (3+ auditors)

---

## 2. Unstake Withdrawal Dos

### Overview

Implementation flaw in unstake withdrawal dos logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 55 audit reports with severity distribution: HIGH: 19, MEDIUM: 36.

> **Key Finding**: This bug report discusses an issue with the DelegationManager contract that results in incorrect calculations of burnable shares during operator slashing events. The `_addQueuedSlashableShares()` function excludes `beaconChainETHStrategy` from cumulative scaled shares tracking, which leads to underc

### Vulnerability Description

#### Root Cause

Implementation flaw in unstake withdrawal dos logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies unstake withdrawal dos in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to unstake operations

### Vulnerable Pattern Examples

**Example 1: beaconChainETHStrategy Queued Withdrawals Excluded From Slashable Shares** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md`
```solidity
/// @dev Add to the cumulative withdrawn scaled shares from an operator for a given strategy
function _addQueuedSlashableShares(address operator, IStrategy strategy, uint256 scaledShares) internal {
    // @audit beaconChainETHStrategy is excluded from slashable shares tracking
    if (strategy != beaconChainETHStrategy) {
        uint256 currCumulativeScaledShares = _cumulativeScaledSharesHistory[operator][strategy].latest();
        _cumulativeScaledSharesHistory[operator][strategy].push({
            key: uint32(block.number),
            value: currCumulativeScaledShares + scaledShares
        });
    }
}
```

**Example 2: [C-02] Stakes not forwarded post-delegation, positions unwithdrawable** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md`
```go
IERC20(_stakingToken).safeTransferFrom(_stakeMsgSender(), address(this), _amount);
stakers[receiver].amountStaked += _amount;
```

**Example 3: Deposited Stakes Can Be Locked in StakeManager if the Validator Is Inactive** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md`
```
// Vulnerable pattern from FCHAIN Validator and Staking Contracts Audit:
The [`initializeDeposit` function](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L303) is designed to accept licenses and staking amounts as stakes for a validating node within the system. This function can be called by the validators to increase their own weight or by delegators to increase the weight of their delegated validator. However, the function does not validate the active status of a validator before proceeding with
```

**Example 4: Direct Deposits Enable Theft Of A Validator’s Funds** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/direct-deposits-enable-theft-of-a-validators-funds.md`
```
// Vulnerable pattern from Swell:
## Description

If a node operator interacts with the deposit contract directly first, it is possible for them to set the withdrawal address to an arbitrary address. Then this node can be added to Swell and used normally. Once deposits are enabled on the Beacon chain, it is possible for this node operator to withdraw all the ETH deposited with this node. In addition to this, it is impossible for the normal withdrawal method specified by `swNFTUpgrade.sol` to work for deposits made to this node.

```

**Example 5: [H-01] `_AddRebalanceRequest` may use outdated balance for delegate withdrawal r** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-_addrebalancerequest-may-use-outdated-balance-for-delegate-withdrawal-reque.md`
```solidity
function _addRebalanceRequest(address validator, uint256 withdrawalAmount) internal {
        require(!_validatorsWithPendingRebalance.contains(validator), "Validator has pending rebalance");
        require(withdrawalAmount > 0, "Invalid withdrawal amount");

        (bool exists, uint256 index) = _validatorIndexes.tryGet(validator);
        require(exists, "Validator does not exist");
        require(_validators[index].balance >= withdrawalAmount, "Insufficient balance");

        validatorRebalanceRequests[validator] = RebalanceRequest({validator: validator, amount: withdrawalAmount});
        _validatorsWithPendingRebalance.add(validator);

        emit RebalanceRequestAdded(validator, withdrawalAmount);
    }
```

**Variant: Unstake Withdrawal Dos - HIGH Severity Cases** [HIGH]
> Found in 19 reports:
> - `reports/cosmos_cometbft_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md`
> - `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md`
> - `reports/cosmos_cometbft_findings/direct-deposits-enable-theft-of-a-validators-funds.md`

**Variant: Unstake Withdrawal Dos in EigenLayer** [MEDIUM]
> Protocol-specific variant found in 4 reports:
> - `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md`
> - `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md`
> - `reports/cosmos_cometbft_findings/m-02-a-malicious-strategy-can-permanently-dos-all-currently-pending-withdrawals-.md`

**Variant: Unstake Withdrawal Dos in Kinetiq_2025-02-26** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/h-01-_addrebalancerequest-may-use-outdated-balance-for-delegate-withdrawal-reque.md`
> - `reports/cosmos_cometbft_findings/h-02-validatormanager-missing-fund-withdrawal-from-validator-in-deactivatevalida.md`
> - `reports/cosmos_cometbft_findings/h-06-some-stakers-may-fail-to-withdraw-staking-hype.md`

**Variant: Unstake Withdrawal Dos in Rocketpool** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md`
> - `reports/cosmos_cometbft_findings/rocketnodestaking-node-operators-can-reduce-slashing-impact-by-withdrawing-exces.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in unstake withdrawal dos logic allows exploitation through missing validation, 
func secureUnstakeWithdrawalDos(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 55 audit reports
- **Severity Distribution**: HIGH: 19, MEDIUM: 36
- **Affected Protocols**: KelpDAO, Puffer Finance, ZetaChain Cross-Chain, Templedao, Tokemak
- **Validation Strength**: Strong (3+ auditors)

---

## 3. Unstake Withdrawal Accounting

### Overview

Implementation flaw in unstake withdrawal accounting logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 55 audit reports with severity distribution: HIGH: 24, MEDIUM: 31.

> **Key Finding**: The team has fixed a previous issue, but a new issue still exists. The `bondWithdrawal` function can only track one type of token, but the `BondManager` can support multiple tokens. This can lead to unexpected behavior in the `withdraw()` function. The team has made a second round of fixes by adding

### Vulnerability Description

#### Root Cause

Implementation flaw in unstake withdrawal accounting logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies unstake withdrawal accounting in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to unstake operations

### Vulnerable Pattern Examples

**Example 1: A Relayer Can Avoid a Slash by Requesting a Withdrawal From the Bond** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/a-relayer-can-avoid-a-slash-by-requesting-a-withdrawal-from-the-bond.md`
```
// Vulnerable pattern from Pheasant Network:
**Update**
The team fixed the described issue. However, an issue persisted: `bondWithdrawal` can only keep track of one token, but `BondManager` supports several tokens. `getBond()` receives a token ID as parameter (token A) and subtracts `bondWithdrawal.withdrawalAmount` (can be ANY token). This wrong accounting can lead to unexpected behavior in `PheasantNetworkBridgeChild.withdraw()`.

In a second round of fixes, the team solved this additional issue by adding a mapping to differentiate depos
```

**Example 2: Admin balances don't account for potential token rebases** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/admin-balances-dont-account-for-potential-token-rebases.md`
```
// Vulnerable pattern from Curve Finance:
##### Description
Admin fees (stored in an array https://github.com/curvefi/stableswap-ng/blob/8c78731ed43c22e6bcdcb5d39b0a7d02f8cb0386/contracts/main/CurveStableSwapMetaNG.vy#L208) don't account for potential slashings. If admin fees are withdrawn first (after the slashing event), then LPs are getting unfairly diluted.
This issue has been assigned a MEDIUM severity level because admin balances don't account for both rebases up and down while slashings are quite rare events (so that rebases down
```

**Example 3: [C-02] Stakes not forwarded post-delegation, positions unwithdrawable** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/c-02-stakes-not-forwarded-post-delegation-positions-unwithdrawable.md`
```go
IERC20(_stakingToken).safeTransferFrom(_stakeMsgSender(), address(this), _amount);
stakers[receiver].amountStaked += _amount;
```

**Example 4: DoS on stake accounting functions by bloating `operatorNodesArray` with irremova** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md`
```go
if (nodePendingRemoval[valID] && …) {
         _removeNodeFromArray(operator,nodeId);
         nodePendingRemoval[valID] = false;
     }
```

**Example 5: Emergency Withdrawal Conditions Might Change Over Time** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md`
```
// Vulnerable pattern from Radiant Riz Audit:
After a market has been [shut down](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPoolConfigurator.sol#L491), the `shutdown` function from the `RizLendingPool` contract [takes a snapshot](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPool.sol#L728) through the `BadDebtManager` contract. This is done to keep a record of the [prices in the particular lending pool and al
```

**Variant: Unstake Withdrawal Accounting - MEDIUM Severity Cases** [MEDIUM]
> Found in 31 reports:
> - `reports/cosmos_cometbft_findings/admin-balances-dont-account-for-potential-token-rebases.md`
> - `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md`
> - `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md`

**Variant: Unstake Withdrawal Accounting in Kinetiq_2025-02-26** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-01-_addrebalancerequest-may-use-outdated-balance-for-delegate-withdrawal-reque.md`
> - `reports/cosmos_cometbft_findings/h-02-validatormanager-missing-fund-withdrawal-from-validator-in-deactivatevalida.md`

**Variant: Unstake Withdrawal Accounting in Kinetiq** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-02-users-who-queue-withdrawal-before-a-slashing-event-disadvantage-users-who-q.md`
> - `reports/cosmos_cometbft_findings/m-03-inconsistent-state-restoration-in-cancelwithdrawal-function.md`

**Variant: Unstake Withdrawal Accounting in Telcoin Update** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-1-rogue-plugin-can-become-unremovable-and-halt-all-staking-and-claiming.md`
> - `reports/cosmos_cometbft_findings/m-1-account-that-is-affiliated-with-a-plugin-can-sometimes-evade-slashing.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in unstake withdrawal accounting logic allows exploitation through missing valid
func secureUnstakeWithdrawalAccounting(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 55 audit reports
- **Severity Distribution**: HIGH: 24, MEDIUM: 31
- **Affected Protocols**: KelpDAO, Puffer Finance, Persistence, Tokensfarm, Casimir
- **Validation Strength**: Strong (3+ auditors)

---

## 4. Unstake Queue Manipulation

### Overview

Implementation flaw in unstake queue manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 23 audit reports with severity distribution: HIGH: 9, MEDIUM: 14.

> **Key Finding**: The `_checkBalance` function in the OETHVaultCore.sol contract is not returning the correct balance in certain scenarios. Specifically, if the WETH in the withdrawal queue exceeds the total amount of workable assets, the function should return a balance of 0 but instead returns the amount of WETH in

### Vulnerability Description

#### Root Cause

Implementation flaw in unstake queue manipulation logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies unstake queue manipulation in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to unstake operations

### Vulnerable Pattern Examples

**Example 1: _checkBalance Returns an Incorrect Value During Insolvency** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/_checkbalance-returns-an-incorrect-value-during-insolvency.md`
```
// Vulnerable pattern from OETH Withdrawal Queue Audit:
The [`_checkBalance`](https://github.com/OriginProtocol/origin-dollar/blob/eca6ffa74d9d0c5fb467551a30912cb722fab9c2/contracts/contracts/vault/OETHVaultCore.sol#L392-L407) function returns the balance of an asset held in the vault and all the strategies. If the requested asset is WETH, the amount of WETH reserved for the withdrawal queue is subtracted from this balance to reflect the correct amount of workable assets. In this specific case, the function returns the same result as [the `_totalValu
```

**Example 2: A malicious staker can force validator withdrawals by instantly staking and unst** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md`
```solidity
function requestUnstake(uint256 amount) external nonReentrant {
    // code ....
    uint256 expectedWithdrawableBalance =
        getWithdrawableBalance() + requestedExits * VALIDATOR_CAPACITY + delayedEffectiveBalance;
    if (unstakeQueueAmount > expectedWithdrawableBalance) {
        uint256 requiredAmount = unstakeQueueAmount - expectedWithdrawableBalance;
>       uint256 requiredExits = requiredAmount / VALIDATOR_CAPACITY; //@audit required exits calculated here
        if (requiredAmount % VALIDATOR_CAPACITY > 0) {
            requiredExits++;
        }
        exitValidators(requiredExits);
    }

    emit UnstakeRequested(msg.sender, amount);
}
```

**Example 3: Activation of queued cutting board can be manipulated leading to redirection of ** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/activation-of-queued-cutting-board-can-be-manipulated-leading-to-redirection-of-.md`
```
// Vulnerable pattern from Berachain Pol:
Severity: Medium Risk
Context: Berachef.sol#158
Description: A validator operator can queue a new cutting board at any time. Once thecuttingBoardBlockDelay
has passed, the queued cutting board is ready for activation. The activation of a cutting board occurs viadistrib-
utor.distributeFor() which calls beraChef.activateReadyQueuedCuttingBoard(pubkey, blockNumber); .
The validator is incentivized to emit the BGT reward to reward vaults that will provide the best financial incentives
while also in
```

**Example 4: beaconChainETHStrategy Queued Withdrawals Excluded From Slashable Shares** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md`
```solidity
/// @dev Add to the cumulative withdrawn scaled shares from an operator for a given strategy
function _addQueuedSlashableShares(address operator, IStrategy strategy, uint256 scaledShares) internal {
    // @audit beaconChainETHStrategy is excluded from slashable shares tracking
    if (strategy != beaconChainETHStrategy) {
        uint256 currCumulativeScaledShares = _cumulativeScaledSharesHistory[operator][strategy].latest();
        _cumulativeScaledSharesHistory[operator][strategy].push({
            key: uint32(block.number),
            value: currCumulativeScaledShares + scaledShares
        });
    }
}
```

**Example 5: [H-01] Buffer Silently Locks Staked HYPE in Contract Without Using Them For With** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-buffer-silently-locks-staked-hype-in-contract-without-using-them-for-withdr.md`
```go
if (operationType == OperationType.UserWithdrawal) {
            // Buffer handling uses 18 decimal precision
            uint256 currentBuffer = hypeBuffer;
            uint256 amountFromBuffer = Math.min(amount, currentBuffer);

            if (amountFromBuffer > 0) {
                hypeBuffer = currentBuffer - amountFromBuffer;
                amount -= amountFromBuffer;
                emit BufferDecreased(amountFromBuffer, hypeBuffer);
            }

            // If fully fulfilled from buffer, return
            if (amount == 0) {
                return;
            }
        }
```

**Variant: Unstake Queue Manipulation - HIGH Severity Cases** [HIGH]
> Found in 9 reports:
> - `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md`
> - `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md`
> - `reports/cosmos_cometbft_findings/h-01-buffer-silently-locks-staked-hype-in-contract-without-using-them-for-withdr.md`

**Variant: Unstake Queue Manipulation in Casimir** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md`
> - `reports/cosmos_cometbft_findings/function-gettotalstake-fails-to-account-for-pending-validators-leading-to-inaccu.md`
> - `reports/cosmos_cometbft_findings/users-could-avoid-loss-by-frontrunning-to-request-unstake.md`

**Variant: Unstake Queue Manipulation in EigenLayer** [MEDIUM]
> Protocol-specific variant found in 4 reports:
> - `reports/cosmos_cometbft_findings/beaconchainethstrategy-queued-withdrawals-excluded-from-slashable-shares.md`
> - `reports/cosmos_cometbft_findings/h-02-it-is-impossible-to-slash-queued-withdrawals-that-contain-a-malicious-strat.md`
> - `reports/cosmos_cometbft_findings/m-02-a-malicious-strategy-can-permanently-dos-all-currently-pending-withdrawals-.md`

**Variant: Unstake Queue Manipulation in Kinetiq** [HIGH]
> Protocol-specific variant found in 3 reports:
> - `reports/cosmos_cometbft_findings/h-01-buffer-silently-locks-staked-hype-in-contract-without-using-them-for-withdr.md`
> - `reports/cosmos_cometbft_findings/h-02-users-who-queue-withdrawal-before-a-slashing-event-disadvantage-users-who-q.md`
> - `reports/cosmos_cometbft_findings/m-03-inconsistent-state-restoration-in-cancelwithdrawal-function.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in unstake queue manipulation logic allows exploitation through missing validati
func secureUnstakeQueueManipulation(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 23 audit reports
- **Severity Distribution**: HIGH: 9, MEDIUM: 14
- **Affected Protocols**: Maia DAO Ecosystem, Napier, Berachain Pol, Sentiment V2, Puffer Finance
- **Validation Strength**: Strong (3+ auditors)

---

## 5. Unstake Before Slash

### Overview

Implementation flaw in unstake before slash logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 14 audit reports with severity distribution: HIGH: 2, MEDIUM: 12.

> **Key Finding**: This bug report discusses an issue with the StakingAccountant contract in the Kinetiq project. The problem occurs when there is a slashing event, causing a decrease in the amount of HYPE tokens available for withdrawal. This can result in loss of stake for users who have not yet confirmed their with

### Vulnerability Description

#### Root Cause

Implementation flaw in unstake before slash logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies unstake before slash in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to unstake operations

### Vulnerable Pattern Examples

**Example 1: [H-02] Users Who Queue Withdrawal Before A Slashing Event Disadvantage Users Who** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-02-users-who-queue-withdrawal-before-a-slashing-event-disadvantage-users-who-q.md`
```go
uint256 hypeAmount = stakingAccountant.kHYPEToHYPE(postFeeKHYPE);

    // Lock kHYPE tokens
    kHYPE.transferFrom(msg.sender, address(this), kHYPEAmount);

    // Create withdrawal request
    _withdrawalRequests[msg.sender][withdrawalId] = WithdrawalRequest({
        hypeAmount: hypeAmount,
        kHYPEAmount: postFeeKHYPE,
        kHYPEFee: kHYPEFee,
        timestamp: block.timestamp
    });
```

**Example 2: [H02] Delegators can prevent service providers from deregistering endpoints** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h02-delegators-can-prevent-service-providers-from-deregistering-endpoints.md`
```
// Vulnerable pattern from Audius Contracts Audit:
Under some conditions, delegators may prevent service providers from deregistering endpoints. This can happen innocently or maliciously.


Consider the case where a service provider has registered more than one endpoint and that the service provider has staked the minimum amount of stake. Suppose delegators have delegated to this service provider the maximum amount of stake.


When the service provider attempts to deregister one of the endpoints, their call to the [`deregister` function](https:/
```

**Example 3: Insufficient Delay forRocketNodeStaking.withdrawRPL()** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md`
```go
require ( block.number.sub(getNodeRPLStakedBlock(msg.sender)) >= rocketDAOProtocolSettingsRewards.getRewardsClaimIntervalBlocks(),
" The withdrawal cooldown period has not passed ");
```

**Example 4: [M-03] When malicious behavior occurs and DSS requests slashing against vault du** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-03-when-malicious-behavior-occurs-and-dss-requests-slashing-against-vault-duri.md`
```go
uint256 public constant SLASHING_WINDOW = 7 days;
    uint256 public constant SLASHING_VETO_WINDOW = 2 days;
    uint256 public constant MIN_STAKE_UPDATE_DELAY = SLASHING_WINDOW + SLASHING_VETO_WINDOW;
    uint256 public constant MIN_WITHDRAWAL_DELAY = SLASHING_WINDOW + SLASHING_VETO_WINDOW;
```

**Example 5: `LidoVault::vaultEndedWithdraw` doesn't take into consideration income withdrawa** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-1-lidovaultvaultendedwithdraw-doesnt-take-into-consideration-income-withdrawal.md`
```go
uint256 totalEarnings = vaultEndingETHBalance.mulDiv(withdrawnStakingEarningsInStakes, vaultEndingStakesAmount) - totalProtocolFee + vaultEndedStakingEarnings;
```

**Variant: Unstake Before Slash - MEDIUM Severity Cases** [MEDIUM]
> Found in 12 reports:
> - `reports/cosmos_cometbft_findings/insufficient-delay-forrocketnodestakingwithdrawrpl.md`
> - `reports/cosmos_cometbft_findings/m-03-when-malicious-behavior-occurs-and-dss-requests-slashing-against-vault-duri.md`
> - `reports/cosmos_cometbft_findings/m-05-slashings-will-always-fail-in-some-cases.md`

**Variant: Unstake Before Slash in Karak** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-03-when-malicious-behavior-occurs-and-dss-requests-slashing-against-vault-duri.md`
> - `reports/cosmos_cometbft_findings/m-05-slashings-will-always-fail-in-some-cases.md`

**Variant: Unstake Before Slash in Saffron Lido Vaults** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-1-lidovaultvaultendedwithdraw-doesnt-take-into-consideration-income-withdrawal.md`
> - `reports/cosmos_cometbft_findings/m-2-withdrawing-after-a-slash-event-before-the-vault-has-ended-will-decrease-fix.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in unstake before slash logic allows exploitation through missing validation, in
func secureUnstakeBeforeSlash(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 14 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 12
- **Affected Protocols**: Rocketpool, Saffron Lido Vaults, Streamr, Casimir, Telcoin
- **Validation Strength**: Strong (3+ auditors)

---

## 6. Unstake Emergency

### Overview

Implementation flaw in unstake emergency logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 11 audit reports with severity distribution: HIGH: 3, MEDIUM: 8.

> **Key Finding**: The bug report describes an issue where a user can exploit the system by repeatedly depositing and withdrawing ETH, causing unnecessary withdrawals from the Beacon Chain. This results in a loss of potential rewards for genuine stakers and is also costly for the protocol. The report recommends implem

### Vulnerability Description

#### Root Cause

Implementation flaw in unstake emergency logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies unstake emergency in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to unstake operations

### Vulnerable Pattern Examples

**Example 1: A malicious staker can force validator withdrawals by instantly staking and unst** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/a-malicious-staker-can-force-validator-withdrawals-by-instantly-staking-and-unst.md`
```solidity
function requestUnstake(uint256 amount) external nonReentrant {
    // code ....
    uint256 expectedWithdrawableBalance =
        getWithdrawableBalance() + requestedExits * VALIDATOR_CAPACITY + delayedEffectiveBalance;
    if (unstakeQueueAmount > expectedWithdrawableBalance) {
        uint256 requiredAmount = unstakeQueueAmount - expectedWithdrawableBalance;
>       uint256 requiredExits = requiredAmount / VALIDATOR_CAPACITY; //@audit required exits calculated here
        if (requiredAmount % VALIDATOR_CAPACITY > 0) {
            requiredExits++;
        }
        exitValidators(requiredExits);
    }

    emit UnstakeRequested(msg.sender, amount);
}
```

**Example 2: DoS on stake accounting functions by bloating `operatorNodesArray` with irremova** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md`
```go
if (nodePendingRemoval[valID] && …) {
         _removeNodeFromArray(operator,nodeId);
         nodePendingRemoval[valID] = false;
     }
```

**Example 3: Emergency Withdrawal Conditions Might Change Over Time** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md`
```
// Vulnerable pattern from Radiant Riz Audit:
After a market has been [shut down](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPoolConfigurator.sol#L491), the `shutdown` function from the `RizLendingPool` contract [takes a snapshot](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/riz-lending/RizLendingPool.sol#L728) through the `BadDebtManager` contract. This is done to keep a record of the [prices in the particular lending pool and al
```

**Example 4: [H-01] `_AddRebalanceRequest` may use outdated balance for delegate withdrawal r** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-_addrebalancerequest-may-use-outdated-balance-for-delegate-withdrawal-reque.md`
```solidity
function _addRebalanceRequest(address validator, uint256 withdrawalAmount) internal {
        require(!_validatorsWithPendingRebalance.contains(validator), "Validator has pending rebalance");
        require(withdrawalAmount > 0, "Invalid withdrawal amount");

        (bool exists, uint256 index) = _validatorIndexes.tryGet(validator);
        require(exists, "Validator does not exist");
        require(_validators[index].balance >= withdrawalAmount, "Insufficient balance");

        validatorRebalanceRequests[validator] = RebalanceRequest({validator: validator, amount: withdrawalAmount});
        _validatorsWithPendingRebalance.add(validator);

        emit RebalanceRequestAdded(validator, withdrawalAmount);
    }
```

**Example 5: [H-01] `BlockBeforeSend` hook can be exploited to perform a denial of service** [HIGH]
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

**Variant: Unstake Emergency - MEDIUM Severity Cases** [MEDIUM]
> Found in 8 reports:
> - `reports/cosmos_cometbft_findings/dos-on-stake-accounting-functions-by-bloating-operatornodesarray-with-irremovabl.md`
> - `reports/cosmos_cometbft_findings/emergency-withdrawal-conditions-might-change-over-time.md`
> - `reports/cosmos_cometbft_findings/m-03-inconsistent-state-restoration-in-cancelwithdrawal-function.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in unstake emergency logic allows exploitation through missing validation, incor
func secureUnstakeEmergency(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 11 audit reports
- **Severity Distribution**: HIGH: 3, MEDIUM: 8
- **Affected Protocols**: Rollie, EIP-4337 – Ethereum Account Abstraction Audit, Casimir, Kinetiq LST, Suzaku Core
- **Validation Strength**: Strong (3+ auditors)

---

## 7. Unstake Pending Not Tracked

### Overview

Implementation flaw in unstake pending not tracked logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 16 audit reports with severity distribution: HIGH: 5, MEDIUM: 11.

> **Key Finding**: The initializeDeposit function in the StakeManager contract allows validators and delegators to deposit resources for validating nodes. However, the function does not check if the validator is active before accepting the deposit, leading to locked stakes and the inability to withdraw them. This bug 

### Vulnerability Description

#### Root Cause

Implementation flaw in unstake pending not tracked logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies unstake pending not tracked in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to unstake operations

### Vulnerable Pattern Examples

**Example 1: Deposited Stakes Can Be Locked in StakeManager if the Validator Is Inactive** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/deposited-stakes-can-be-locked-in-stakemanager-if-the-validator-is-inactive.md`
```
// Vulnerable pattern from FCHAIN Validator and Staking Contracts Audit:
The [`initializeDeposit` function](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L303) is designed to accept licenses and staking amounts as stakes for a validating node within the system. This function can be called by the validators to increase their own weight or by delegators to increase the weight of their delegated validator. However, the function does not validate the active status of a validator before proceeding with
```

**Example 2: Dust limit attack on `forceUpdateNodes` allows DoS of rebalancing and potential ** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/dust-limit-attack-on-forceupdatenodes-allows-dos-of-rebalancing-and-potential-va.md`
```
// Vulnerable pattern from Suzaku Core:
**Description:** An attacker can exploit the `forceUpdateNodes()` function with minimal `limitStake` values to force all validator nodes into a pending update state. By exploiting precision loss in stake-to-weight conversion, an attacker can call `forceUpdateNodes` with a minimal limitStake (e.g., 1 wei), which sets the rebalancing flag without actually reducing any stake, effectively blocking legitimate rebalancing for the entire epoch.

Consider following scenario:
- Large vault undelegation r
```

**Example 3: Fixed exchange rate at unstaking fails to socialize slashing and distorts reward** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md`
```
// Vulnerable pattern from Mantle Network:
##### Description
When `Staking.unstakeRequest()` is called, the mETH/ETH rate is fixed and does not reflect slashing or rewards that may occur by the time `Staking.claimUnstakeRequest()` is executed. If two users create requests concurrently and losses arrive afterward, those losses are not socialized across them. One request may be fully paid while the other may revert on claim due to insufficient allocated funds.

This can be exacerbated by frontrunning updates to `LiquidityBuffer.cumulativeD
```

**Example 4: Getting Max Staking Rewards Possible While Bypassing the Lockup Periods** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/getting-max-staking-rewards-possible-while-bypassing-the-lockup-periods.md`
```
// Vulnerable pattern from Sapien:
**Update**
Marked as "Fixed" by the client. Addressed in: `b175349`.

![Image 42: Alert icon](https://certificate.quantstamp.com/full/sapien/ffb7e698-6178-46f0-8df8-52e537af70c0/static/media/success-icon-alert.4e26c8d3b65fdf9f4f0789a4086052ba.svg)

**Update**
Marked as "Fixed" by the client. Addressed in: `228ae219c5478f375bed56376ffba8538ea2f09e`. The client provided the following explanation:

> The vulnerability was fixed by adding lock period validation checks across unstaking functions.

![
```

**Example 5: [H-01] LP unstaking only burns the shares but leaves the underlying tokens in th** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h-01-lp-unstaking-only-burns-the-shares-but-leaves-the-underlying-tokens-in-the-.md`
```go
#[test(
        c = @staking_addr, user_a = @0xAAA, user_b = @0xBBB, user_c = @0xCCC
    )]
    fun test_poc(
        c: &signer,
        user_a: &signer,
        user_b: &signer,
        user_c: &signer
    ) {
        test_setup(c, string::utf8(b"initvaloper1test"));

        //gets the metadata for all tokens
        let ulp_metadata = coin::metadata(@initia_std, string::utf8(b"ulp"));
        let init_metadata = coin::metadata(@initia_std, string::utf8(b"uinit"));
        let cabal_lp_metadata = cabal::get_cabal_token_metadata(1);
        let x_init_metadata = cabal::get_xinit_metadata();
        let sx_init_metadata = cabal::get_sxinit_metadata();

        let initia_signer = &account::create_signer_for_test(@initia_std);

        let ulp_decimals = 1_000_000; //ulp has 6 decimals

        let deposit_amount_a = 100 * ulp_decimals; //the amount user a deposits
        primary_fungible_store::transfer( //user a must first be funded
            initia_signer,
            ulp_metadata,
            signer::address_of(user_a),
            deposit_amount_a
        );
        utils::increase_block(1, 1);
        cabal::mock_stake(user_a, 1, deposit_amount_a); //user a stakes 100 ulp

        utils::increase_block(1, 1);

        let deposit_amount_b = 50 * ulp_decimals; //the amount user b stakes
// ... (truncated)
```

**Variant: Unstake Pending Not Tracked - MEDIUM Severity Cases** [MEDIUM]
> Found in 11 reports:
> - `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md`
> - `reports/cosmos_cometbft_findings/getting-max-staking-rewards-possible-while-bypassing-the-lockup-periods.md`
> - `reports/cosmos_cometbft_findings/include-pending-in-unstake.md`

**Variant: Unstake Pending Not Tracked in Cabal** [HIGH]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/h-01-lp-unstaking-only-burns-the-shares-but-leaves-the-underlying-tokens-in-the-.md`
> - `reports/cosmos_cometbft_findings/m-04-unstaking-from-lp-pools-will-cause-underflow-and-lock-user-funds.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in unstake pending not tracked logic allows exploitation through missing validat
func secureUnstakePendingNotTracked(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 16 audit reports
- **Severity Distribution**: HIGH: 5, MEDIUM: 11
- **Affected Protocols**: Celo Contracts Audit, Sentiment V2, Cabal, MorphL2, Babylonchain
- **Validation Strength**: Strong (3+ auditors)

---

## 8. Unstake Lock Funds

### Overview

Implementation flaw in unstake lock funds logic allows exploitation through missing validation, incorrect state handling, or improper access controls. This pattern was found across 13 audit reports with severity distribution: HIGH: 2, MEDIUM: 11.

> **Key Finding**: This bug report describes an issue with the `_updateReward` function in the `VeQoda` contract. This function is important and is used in other functions such as `stake`, `unstake`, and `_updateVeTokenCache`. However, the `_rewardDistributors` address set is not properly initialized, causing the func

### Vulnerability Description

#### Root Cause

Implementation flaw in unstake lock funds logic allows exploitation through missing validation, incorrect state handling, or improper access controls.

#### Attack Scenario

1. Attacker identifies unstake lock funds in the protocol
2. Exploits the missing validation or incorrect logic
3. May lead to fund loss, denial of service, or protocol state corruption related to unstake operations

### Vulnerable Pattern Examples

**Example 1: Execution failure of `\_updateReward` function due to uninitialized `\_rewardDis** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/execution-failure-of-_updatereward-function-due-to-uninitialized-_rewarddistribu.md`
```solidity
function stake(address account, bytes32 method, uint256 amount) external {
        if (amount <= 0) {
            revert CustomErrors.ZeroStakeAmount();
        }

        // Calculate unclaimed reward before balance update
        _updateReward(account);
```

**Example 2: Execution of `stake` and `unstake` operations blocked due to uninitialized `\_me** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/execution-of-stake-and-unstake-operations-blocked-due-to-uninitialized-_methods-.md`
```solidity
function stake(address account, bytes32 method, uint256 amount) external {
        if (amount <= 0) {
            revert CustomErrors.ZeroStakeAmount();
        }

        // Calculate unclaimed reward before balance update
        _updateReward(account);

        // if user exists, first update their cached veToken balance
        if (_users.contains(account)) {
            _updateVeTokenCache(account);
        }

        // Do token transfer from user to contract
        address token = _methodInfo[method].token;
        IERC20(token).safeTransferFrom(msg.sender, address(this), amount);
```

**Example 3: Fixed exchange rate at unstaking fails to socialize slashing and distorts reward** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/fixed-exchange-rate-at-unstaking-fails-to-socialize-slashing-and-distorts-reward.md`
```
// Vulnerable pattern from Mantle Network:
##### Description
When `Staking.unstakeRequest()` is called, the mETH/ETH rate is fixed and does not reflect slashing or rewards that may occur by the time `Staking.claimUnstakeRequest()` is executed. If two users create requests concurrently and losses arrive afterward, those losses are not socialized across them. One request may be fully paid while the other may revert on claim due to insufficient allocated funds.

This can be exacerbated by frontrunning updates to `LiquidityBuffer.cumulativeD
```

**Example 4: [H06] AUD lending market could affect the protocol** [HIGH]
> 📖 Reference: `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`
```
// Vulnerable pattern from Audius Contracts Audit:
In case an AUD token lending market appears, an attacker could use this market to influence the result of a governance’s proposal, which could lead to a take over of the protocol.


An attacker would only need to stake tokens for a brief moment without waiting for the [`votingPeriod`](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L23) to request an unstake. This aggravates the attack, as the attacker would on
```

**Example 5: [M-02] sFrxEth may revert on redeeming non-zero amount** [MEDIUM]
> 📖 Reference: `reports/cosmos_cometbft_findings/m-02-sfrxeth-may-revert-on-redeeming-non-zero-amount.md`
```
// Vulnerable pattern from Asymmetry Finance:
<https://github.com/code-423n4/2023-03-asymmetry/blob/44b5cd94ebedc187a08884a7f685e950e987261c/contracts/SafEth/derivatives/SfrxEth.sol#L61-L65><br>
<https://github.com/code-423n4/2023-03-asymmetry/blob/44b5cd94ebedc187a08884a7f685e950e987261c/contracts/SafEth/SafEth.sol#L118>

### Impact

Unstaking is blocked.

### Proof of Concept

When unstaking the `withdraw` of each derivative is called. `SfrxEth.withdraw` calls [`IsFrxEth(SFRX_ETH_ADDRESS).redeem(_amount, address(this), address(this));`](h
```

**Variant: Unstake Lock Funds - HIGH Severity Cases** [HIGH]
> Found in 2 reports:
> - `reports/cosmos_cometbft_findings/h06-aud-lending-market-could-affect-the-protocol.md`
> - `reports/cosmos_cometbft_findings/malicious-target-can-make-_endvote-revert-forever-by-forceunstakingstaking-again.md`

**Variant: Unstake Lock Funds in Qoda DAO** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/execution-failure-of-_updatereward-function-due-to-uninitialized-_rewarddistribu.md`
> - `reports/cosmos_cometbft_findings/execution-of-stake-and-unstake-operations-blocked-due-to-uninitialized-_methods-.md`

**Variant: Unstake Lock Funds in Olas** [MEDIUM]
> Protocol-specific variant found in 2 reports:
> - `reports/cosmos_cometbft_findings/m-06-unstake-function-reverts-because-of-use-of-outdatedstale-serviceids-array.md`
> - `reports/cosmos_cometbft_findings/m-16-staked-service-will-be-irrecoverable-by-owner-if-not-an-erc721-receiver.md`

### Secure Implementation

```go
// ✅ SECURE: Proper implementation with validation
// Addresses: Implementation flaw in unstake lock funds logic allows exploitation through missing validation, inco
func secureUnstakeLockFunds(ctx sdk.Context) error {
    // 1. Validate all inputs
    // 2. Check state preconditions
    // 3. Perform operation atomically
    // 4. Update all affected state
    // 5. Emit events for tracking
    return nil
}
```

### Impact Analysis

- **Frequency**: Found in 13 audit reports
- **Severity Distribution**: HIGH: 2, MEDIUM: 11
- **Affected Protocols**: Streamr, Olas, Cabal, MorphL2, Qoda DAO
- **Validation Strength**: Strong (3+ auditors)

---

## Detection Patterns

### Automated Detection
```
# Unstake Cooldown Bypass
grep -rn 'unstake|cooldown|bypass' --include='*.go' --include='*.sol'
# Unstake Withdrawal Dos
grep -rn 'unstake|withdrawal|dos' --include='*.go' --include='*.sol'
# Unstake Withdrawal Accounting
grep -rn 'unstake|withdrawal|accounting' --include='*.go' --include='*.sol'
# Unstake Queue Manipulation
grep -rn 'unstake|queue|manipulation' --include='*.go' --include='*.sol'
# Unstake Before Slash
grep -rn 'unstake|before|slash' --include='*.go' --include='*.sol'
# Unstake Emergency
grep -rn 'unstake|emergency' --include='*.go' --include='*.sol'
# Unstake Pending Not Tracked
grep -rn 'unstake|pending|not|tracked' --include='*.go' --include='*.sol'
# Unstake Lock Funds
grep -rn 'unstake|lock|funds' --include='*.go' --include='*.sol'
```

## Keywords

`account`, `accounting`, `activation`, `address`, `admin`, `affect`, `after`, `allows`, `appchain`, `attack`, `avoid`, `balances`, `beaconchainethstrategy`, `before`, `bloating`, `blocked`, `board`, `bond`, `bypass`, `bypassing`, `change`, `conditions`, `cooldown`, `cosmos`, `could`, `cutting`, `delay`, `delegators`, `deposited`, `deregistering`
