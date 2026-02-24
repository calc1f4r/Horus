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
solodit_id: 53591
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Checkpoint_Proofs_Security_Assessment_Report_v2.0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Checkpoint_Proofs_Security_Assessment_Report_v2.0.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

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

Lack Of Support For Compounding Withdrawal Credentials After Electra Upgrade

### Overview


The EigenPod, a system that helps manage cryptocurrency, is currently unable to verify a new type of withdrawal credential called the compounding withdrawal credential. This means that validators with this type of credential cannot have their ETH counted in EigenPod after a recent upgrade. The team has identified the issue and plans to fix it in the future, but for now, users can still recover their funds by exiting the validator and performing a checkpoint. However, this may result in lost rewards during the downtime. The team has suggested adding a new function and updating the system to support the new type of withdrawal credential.

### Original Finding Content

## Description

The EigenPod does not support verifying compounding withdrawal credentials, preventing ETH in validators with compounding withdrawal credentials from being counted in EigenPod after Electra. EIP-7251 included in the Electra upgrade introduces the compounding withdrawal credential represented by a `0x02` prefix. This new type of withdrawal credential allows validators to have an effective balance of up to 2048 ETH.

The `_verifyWithdrawalCredentials()` function has a check to ensure that the validator's withdrawal credentials are pointed to the EigenPod:

```solidity
// Ensure the validator's withdrawal credentials are pointed at this pod
require(
    validatorFields.getWithdrawalCredentials() == bytes32(_podWithdrawalCredentials()),
    "EigenPod._verifyWithdrawalCredentials: proof is not for this EigenPod"
);
```

However, EigenPod only supports Eth1 (`0x01` prefixed) withdrawal credentials, and not compounding (`0x02` prefixed) credentials:

```solidity
function _podWithdrawalCredentials() internal view returns (bytes memory) {
    // @audit `bytes1(uint8(1))` corresponds to the `0x01` prefix
    return abi.encodePacked(bytes1(uint8(1)), bytes11(0), address(this));
}
```

Hence, validators with compounding withdrawal credentials cannot be verified on the EigenPod, preventing the ETH in compounding validators from being restaked on EigenLayer. 

Note that funds can still be recovered by exiting the validator and performing a checkpoint to record the new EigenPod balance. However, potential AVS rewards during this downtime are lost.

## Recommendations

Consider adding a new function `_podCompoundingWithdrawalCredentials()` and add support for the `0x02` prefix in `_verifyWithdrawalCredentials()`.

## Resolution

The EigenLayer team has acknowledged the issue with the following comment:

"We are comfortable deploying to mainnet without the fix and will upgrade the EigenPod beacon in the future to support compounding withdrawal credentials."

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Checkpoint_Proofs_Security_Assessment_Report_v2.0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Checkpoint_Proofs_Security_Assessment_Report_v2.0.pdf

### Keywords for Search

`vulnerability`

