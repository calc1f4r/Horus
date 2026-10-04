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
solodit_id: 53561
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Rounding Of slashingFactor Can Result In Complete Loss Of Withdrawable Shares

### Overview

See description below for full details.

### Original Finding Content

## Description

Due to rounding, it is possible for the `slashingFactor` to be rounded down to zero, even when both `operatorMaxMagnitude` and `beaconChainSlashingFactor` are non-zero. This can result in incorrect `withdrawableShares` being calculated for the `beaconChainETHStrategy`.

The `slashingFactor` for the `beaconChainETHStrategy` is calculated as:

```solidity
DelegationManager.sol::_getSlashingFactor()
if (strategy == beaconChainETHStrategy) {
    uint64 beaconChainSlashingFactor = eigenPodManager.beaconChainSlashingFactor(staker);
    return operatorMaxMagnitude.mulWad(beaconChainSlashingFactor);
}
```

Due to the rounding of the `mulWad()` function, it is possible for the `slashingFactor` to be rounded down to 0, even when both `operatorMaxMagnitude` and `beaconChainSlashingFactor` are non-zero.

An operator can exploit this rounding to burn their stakers’ withdrawable shares by doing the following:

1. The operator creates a malicious AVS and registers and allocates to it.
2. The operator slashes themself through their AVS by a large amount such that their `maxMagnitude` is reduced to a very small value (e.g. 1).
3. A staker verifies a validator on their EigenPod and delegates to the operator.
4. The staker gets penalised on the beacon chain by a very small amount (e.g. 1 gwei).

Once the staker’s `beaconChainSlashingFactor` is reduced below WAD in step 4, their `slashingFactor` becomes 0 and they lose all their withdrawable shares.

Though the impact of this issue can be extremely severe, this issue has an informational severity rating as it is very unlikely that an operator would grief their stakers without any potential upside. Furthermore, it is assumed that stakers will perform due diligence on the operators they delegate to.

## Recommendations

Consider informing users on this particular edge case in the documentation. Furthermore, provide plenty of warning to stakers on the front-end when operators may be considered malicious and have an extremely low `maxMagnitude`.

## Resolution

The EigenLayer team has added a Natspec comment to the `_getSlashingFactor()` function to inform users of this particular edge case. This issue has been resolved in PR #1089.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

