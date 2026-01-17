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
solodit_id: 53718
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/eigenlayer-3.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/eigenlayer-3.pdf
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

Verifying Beacon Chain Withdrawals Break After Deneb

### Overview


The `BeaconChainProofs.verifyWithdrawal()` function has a bug that causes withdrawals to be stuck or falsely created in the EigenPod contract after the Ethereum Deneb upgrade. This is because the upgrade added two new fields, increasing the tree height from 4 to 5, but the function assumes a constant height of 4. This leads to valid withdrawals being marked as invalid and makes the function vulnerable to attacks. To fix this, the function needs to account for the change in tree height after Deneb and distinguish between pre and post-Deneb withdrawals. This has been addressed in PRs #395 and #416.

### Original Finding Content

## Description

The `BeaconChainProofs.verifyWithdrawal()` function does not support withdrawals that occur after the Ethereum Deneb upgrade, resulting in withdrawals being stuck or maliciously fabricated inside the EigenPod contract. The Deneb upgrade adds two new fields to the `ExecutionPayload` container to account for blobs, increasing the number of fields from 15 to 17, which results in a tree height increase from 4 to 5. However, the `BeaconChainProofs` library assumes a constant tree height of 4, resulting in the following:

1. Valid withdrawal proofs that occur after Deneb are incorrectly verified to be invalid - normal users cannot withdraw their ETH from the EigenPod contract.
2. The `BeaconChainProofs.verifyWithdrawal()` function is now susceptible to a second pre-image attack, where a malicious attacker can pose an intermediate node as a leaf to successfully verify withdrawals that don’t exist on the beacon chain.

## Recommendations

Account for the change in tree height after Deneb. The fixed logic will need to also still account for withdrawals that have occurred before Deneb, so consider adding logic that determines if a withdrawal is pre or post-Deneb.

## Resolution

Both pre and post-Deneb tree heights are now stored as constants. The tree height value used for every beacon chain withdrawal is determined by checking the timestamp of the withdrawal against the timestamp of the Deneb fork. This issue has been addressed in PRs #395 and #416.

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

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/eigenlayer-3.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/eigenlayer-3.pdf

### Keywords for Search

`vulnerability`

