---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53547
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Over-Slashing Of Withdrawable beaconChainETHStrategy Shares

### Overview


The report describes a bug in the `_reduceSlashingFactor()` function in the `EigenPodManager` contract. This function incorrectly calculates the new beacon chain slashing factor, resulting in inconsistent withdrawable share calculations for validators. This bug is caused by not scaling the previous restaked balance by the deposit scaling factor. The report recommends modifying the function to incorporate the scaling factor and the EigenLayer team has acknowledged the issue and will update documentation to inform users of this edge case.

### Original Finding Content

## Description

The `_reduceSlashingFactor()` function in `EigenPodManager` incorrectly calculates the new beacon chain slashing factor by using unscaled balances, leading to inconsistent withdrawable share calculations depending on when validators are verified relative to checkpoints.

## EigenPodManager.sol::_reduceSlashingFactor()

```solidity
function _reduceSlashingFactor(
    address podOwner,
    uint256 prevRestakedBalanceWei,
    uint256 balanceDecreasedWei
) internal returns (uint64) {
    uint256 newRestakedBalanceWei = prevRestakedBalanceWei - balanceDecreasedWei;
    uint64 prevBeaconSlashingFactor = beaconChainSlashingFactor(podOwner);
    // newBeaconSlashingFactor is less than prevBeaconSlashingFactor because
    // newRestakedBalanceWei < prevRestakedBalanceWei
    uint64 newBeaconSlashingFactor =
        uint64(prevBeaconSlashingFactor.mulDiv(newRestakedBalanceWei, prevRestakedBalanceWei));
    uint64 beaconChainSlashingFactorDecrease = prevBeaconSlashingFactor - newBeaconSlashingFactor;
    _beaconChainSlashingFactor[podOwner] =
        BeaconChainSlashingFactor({slashingFactor: newBeaconSlashingFactor, isSet: true});
    emit BeaconChainSlashingFactorDecreased(podOwner, prevBeaconSlashingFactor, newBeaconSlashingFactor);
    return beaconChainSlashingFactorDecrease;
}
```

The `_reduceSlashingFactor()` function calculates the new beacon chain slashing factor (bcsf) without scaling `prevRestakedBalanceWei` by the deposit scaling factor (dsf). This causes the slashing factor to be reduced too aggressively when a validator is slashed.

Consider the following scenario where the 2nd validator is verified before the checkpoint is performed:

1. Stake and verify the first validator (withdrawableShares = 32 ETH)
2. Slash operator for 50% of allocation (withdrawableShares = 16 ETH, maxMagnitude = 0.5)
3. Stake and verify the second validator (withdrawableShares = 48 ETH, dsf = 1.5)
4. Slash the first validator for 16 ETH on the beacon chain
5. Perform an EigenPod checkpoint (withdrawableShares = 36 ETH, bcsf = 0.75)

Where:

- dsf = newWithdrawableShares
- newDepositShares × slashingFactorsteptwo = 48 / (64 × (0.5 × 1)) = 1.5
- finalWithdrawableShares = depositShares × dsf × slashingFactor = 64 × 1.5 × (0.5 × 0.75) = 36

The final withdrawable shares value is incorrectly calculated as 36 ETH, whereas the correct value is 40 ETH:

- expectedFinalWithdrawableShares = withdrawableSharesvalidatorOne + withdrawableSharesvalidatorTwo
- = (32 × 0.5 × 0.5) + 32
- = 8 + 32 = 40

## Recommendations

Modify `_reduceSlashingFactor()` to scale `prevRestakedBalanceWei` by the deposit scaling factor before calculating the new beacon chain slashing factor. To also incorporate the recommended change in EGSL-01, scale `prevRestakedBalanceWei` by `maxMagnitude * dsf`:

```solidity
EigenPodManager.sol::_reduceSlashingFactor()
prevRestakedBalanceWei = prevRestakedBalanceWei.mulWad(maxMagnitude).mulWad(dsf);
```

## Resolution

The EigenLayer team has acknowledged this issue in a response available as a Notion document. A summary of the response is as follows:

"Following the logic from EGSL-01, the attributable slashed amount when an AVS slashes decreases in the event of beacon chain slashing. The difference in end state between checkpointing before or after staking a validator is due to the asynchronous nature of the beacon chain proof system. A benefit of the system is that stakers are incentivized to immediately prove beacon chain slashes."

The EigenLayer team will also update documentation to inform users of this specific edge case.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf

### Keywords for Search

`vulnerability`

