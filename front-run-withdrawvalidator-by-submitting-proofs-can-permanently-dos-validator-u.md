---
# Core Classification
protocol: Casimir
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34997
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Hans
  - 0kage
---

## Vulnerability Title

Front-run withdrawValidator by submitting proofs can permanently DOS validator unstaking on EigenLayer

### Overview


The bug report describes a vulnerability in the CasimirManager contract, which allows an attacker to prevent validator withdrawals on the EigenLayer. This can create a risk for insolvency in the Casimir protocol. The recommended mitigation is to split the `withdrawValidator` function into two separate functions, listen to a specific event emission, and introduce a try-catch while verifying withdrawals. This issue has been fixed in the latest version of the Casimir contract. 

### Original Finding Content

**Description:** An attacker can observe the mempool and front-run the `CasimirManager::withdrawValidator` transaction by submitting the same proofs directly on Eigen Layer.

Since the proof is already verified, the `CasimirManager::withdrawValidator` transaction will revert when it tries to submit the same proofs. Submitting an empty proof to bypass proof verification also does not work because the `finalEffectiveBalance` will always be 0, preventing the queuing of withdrawals.

````solidity
function withdrawValidator(
    uint256 stakedValidatorIndex,
    WithdrawalProofs memory proofs,
    ISSVClusters.Cluster memory cluster
) external {
    onlyReporter();

   // ..code...

    uint256 initialDelayedRewardsLength = eigenWithdrawals.userWithdrawalsLength(address(this)); //@note this holds the rewards
    uint64 initialDelayedEffectiveBalanceGwei = eigenPod.withdrawableRestakedExecutionLayerGwei(); //@note this has the current ETH balance

>   eigenPod.verifyAndProcessWithdrawals(
        proofs.oracleTimestamp,
        proofs.stateRootProof,
        proofs.withdrawalProofs,
        proofs.validatorFieldsProofs,
        proofs.validatorFields,
        proofs.withdrawalFields
    ); //@audit reverts if proof is already verified

    {
        uint256 updatedDelayedRewardsLength = eigenWithdrawals.userWithdrawalsLength(address(this));
        if (updatedDelayedRewardsLength > initialDelayedRewardsLength) {
            IDelayedWithdrawalRouter.DelayedWithdrawal memory withdrawal =
                eigenWithdrawals.userDelayedWithdrawalByIndex(address(this), updatedDelayedRewardsLength - 1);
            if (withdrawal.blockCreated == block.number) {
                delayedRewards += withdrawal.amount;
                emit RewardsDelayed(withdrawal.amount);
            }
        }
    }

    uint64 updatedDelayedEffectiveBalanceGwei = eigenPod.withdrawableRestakedExecutionLayerGwei();
>   uint256 finalEffectiveBalance =
        (updatedDelayedEffectiveBalanceGwei - initialDelayedEffectiveBalanceGwei) * GWEI_TO_WEI; //@audit if no proofs submitted, this will be 0
    delayedEffectiveBalance += finalEffectiveBalance;
    reportWithdrawnEffectiveBalance += finalEffectiveBalance;
}

//... code
````

**Impact:** At a negligible cost, an attacker can prevent validator withdrawals on EigenLayer, creating an insolvency risk for Casimir.

**Recommended Mitigation:** Consider making the following changes to `CasimirManager::withdrawValidators`:

- Split the function into two separate functions, one for full-withdrawal verifications and another for queuing verified withdrawals.
- Listen to the following event emission in `EigenPod::_processFullWithdrawal` and filter the events emitted with the recipient as `CasimirManager`.
````solidity
event FullWithdrawalRedeemed(
    uint40 validatorIndex,
    uint64 withdrawalTimestamp,
    address indexed recipient,
    uint64 withdrawalAmountGwei
);
````
- Introduce a try-catch while verifying withdrawal for each applicable validator index. If a proof is already verified, update the `stakedValidatorIds` array and reduce `requestedExits` in the catch section.
- Once all withdrawals are verified, use the event emissions to create a `QueuedWithdrawalParams` array that will be sent to the second function that internally calls `eigenDelegationManager.queueWithdrawals(params)`.
- Update the `delayedEffectiveBalance` and `reportWithdrawnEffectiveBalance` at this stage.

Note: This assumes that the `reporter` is protocol-controlled.

**Casimir:**
Fixed in [eb31b43](https://github.com/casimirlabs/casimir-contracts/commit/eb31b4349e69eb401615e0eca253e9ab8cc0999d)

**Cyfrin:** Verified. Withdrawal proofs are decoupled from queuing withdrawals on EigenLayer. This successfully mitigates the Denial of Service risk reported in this issue. It is noted however that the effective balance is hardcoded as 32 ether.

It is recommended that the effective balance is passed as a parameter by monitoring the full withdrawal event on EigenLayer.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Casimir |
| Report Date | N/A |
| Finders | Hans, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

