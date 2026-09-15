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
solodit_id: 53593
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Checkpoint_Proofs_Security_Assessment_Report_v2.0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Checkpoint_Proofs_Security_Assessment_Report_v2.0.pdf
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

Double-Counting ETH From Consolidations After Electra Upgrade

### Overview

See description below for full details.

### Original Finding Content

## Description

EIP-7251 consolidations, when implemented, open the EigenPod to a potential attack vector where ETH from a consolidated validator can be double-counted when verifying withdrawal credentials.

EIP-7251, included in the upcoming Electra upgrade, allows validators to consolidate by specifying a source and target validator. The source validator's ETH balance is sent to the target validator as the source validator initiates an exit from the beacon chain.

This opens the EigenPod to a timing attack where a source validator is verified on the EigenPod before it consolidates to a target validator, which is later verified on the EigenPod to have both validators' balances. This results in the source validator's balance being double-counted.

Fortunately, EIP-7251 consolidations are initiated by a request from the withdrawal credentials of the source validator; hence, only the EigenPod is capable of submitting valid consolidation requests. It is possible to take precautionary measures when implementing consolidations to protect against this attack vector.

*Note:* This issue is categorized as having informational severity as the in-scope EigenPod code currently does not implement consolidations and hence is not vulnerable to the attack described above.

## Recommendations

When implementing consolidations on the EigenPod, ensure **ValidatorInfo::restakedBalanceGwei** accounting is properly adjusted once the consolidation has occurred. It is important to verify that the consolidation has actually occurred on the beacon chain before making the adjustment, as it is possible for consolidation requests to be rejected on the consensus layer.

Some notable reasons for consolidation requests to be rejected on the consensus layer are if:

- Either the source or target validator is not registered on the beacon chain
- The source and target validators are the same
- The withdrawal credentials of the source or target validators are not **0x01** or **0x02** prefixed
- The source or target validators are not active or are exiting the beacon chain

Note that the consensus layer does not require the source and target validators to have the same withdrawal address, so this must be checked on the EigenPod. A consolidation to a target validator with a different withdrawal address will result in unbacked pod owner shares if the source validator's restaked balance is not checkpointed after consolidation.

A more simple solution may be to use a checkpoint proof to update the balances of both the source and target validators in the same checkpoint. This requires both validators to be verified on the EigenPod before the consolidation request is made, such that the target validator cannot be verified on the EigenPod after it receives the balance from consolidation.

## Resolution

The EigenLayer team has acknowledged the issue with the following comment:

> "We will carefully consider the recommendations provided when upgrading the EigenPod beacon in the future to support consolidations."

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

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Checkpoint_Proofs_Security_Assessment_Report_v2.0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Eigen_Labs_EigenLayer_Checkpoint_Proofs_Security_Assessment_Report_v2.0.pdf

### Keywords for Search

`vulnerability`

