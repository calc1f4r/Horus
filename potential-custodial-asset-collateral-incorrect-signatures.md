---
# Core Classification
protocol: Bond Appetit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28581
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Bond%20Appetit/README.md#7-potential-custodial-asset-collateral-incorrect-signatures
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
  - MixBytes
---

## Vulnerability Title

Potential custodial asset collateral incorrect signatures

### Overview


This bug report is about the lack of signature correctness checks in the RealAssetDepositaryBalanceView data structure in a GitHub repository. The signatures in question are not specified in the report, but it is recommended to implement additional checks and add comments about the nature of the signatures. This would help to ensure that the signatures are formed correctly and can be verified.

### Original Finding Content

##### Description
This warning is about absent signature correctness checks in Proof data structure in RealAssetDepositaryBalanceView in here: https://github.com/bondappetit/bondappetit-protocol/blob/355180f0aca0b29d60d808f761052956b7a3a159/contracts/depositary/RealAssetDepositaryBalanceView.sol#L88.

What kind of signatures are these? How do they get formed? Were they formed correctly and how to check that?

##### Recommendation
It is recommended to implement additional signature correctness checks, append comments about the nature of those signatures.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Bond Appetit |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Bond%20Appetit/README.md#7-potential-custodial-asset-collateral-incorrect-signatures
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

