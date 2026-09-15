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
solodit_id: 53592
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

Validator Status Incorrectly Set To WITHDRAWN After Electra Upgrade

### Overview


The Electra upgrade has caused a bug where validator status is incorrectly set to WITHDRAWN in a checkpoint due to changes in how deposits are credited. This is because the upgrade introduces pending balance deposits, which can result in newly-registered validators having a zero balance. This issue can be avoided by not verifying validators on the EigenPod until the pending balance deposit has been processed. The EigenLayer team is aware of the issue and will make changes closer to the upgrade's deployment. 

### Original Finding Content

## Description

The Electra upgrade changes how deposits are credited to validator balances, resulting in validator status being incorrectly set to **WITHDRAWN** in a checkpoint.

Currently, deposits on the beacon chain are credited to validators at the same time that they are processed. If the deposit belongs to a new validator, they get registered onto the beacon chain along with their deposit balance. 

EIP-7251 included in Electra changes how deposits are applied on the beacon chain by introducing **pending balance deposits**. Due to this change, processed deposits now register new validators onto the beacon chain with a zero balance and create a pending balance deposit, which gets processed once per epoch to credit the deposit amount to the validator's balance. This means that there is now a period of time (an epoch or longer due to the churn limit) when newly-registered validators will have a zero balance.

A newly-registered validator with a zero balance can have its withdrawal credentials verified on the **EigenPod**. If this validator is checkpointed, then it will be marked as **WITHDRAWN** even though the validator has not exited the beacon chain.

This issue can be prevented if the pod owner does not verify their validator on the EigenPod and starts a checkpoint until the pending balance deposit has been processed. Furthermore, no funds are lost since the validator can exit the beacon chain to recover the ETH, which can be withdrawn from the EigenPod after the checkpoint. However, the pod owner will lose out on potential **AVS** rewards during this downtime.

## Recommendations

Prevent pod owners from verifying newly-registered validators with zero balances on the EigenPod by checking that the validator's effective balance is greater than zero.

## Resolution

The EigenLayer team has acknowledged the issue with the following comment:

> "We’ll make the appropriate changes closer to the fork when the scope and timeline of the Electra upgrade are clearer. Since this isn’t an issue for the current beacon chain spec, we’re comfortable deploying to mainnet without the fix."

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

