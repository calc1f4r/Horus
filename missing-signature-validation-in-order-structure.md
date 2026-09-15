---
# Core Classification
protocol: Liquorice
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49450
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#10-missing-signature-validation-in-order-structure
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

Missing signature validation in `Order` structure

### Overview


The bug report is about a contract called `Signing` and an issue with the `Order` structure. The fields `baseTokenData.toRecipient` and `quoteTokenData.toTrader` are not included in the signature verification process, which means they can be changed without affecting the signature. The recommendation is to include these fields in the signature and to explicitly pass them as arguments when calling the `LiquoriceSettlement.settle` method.

### Original Finding Content

##### Description

In the `Signing` contract, the `Order` structure includes the fields `baseTokenData.toRecipient` and `quoteTokenData.toTrader`. These fields are currently ignored in the signature verification process. They are not included in the data that is signed, meaning they can be altered without invalidating the signature.

##### Recommendation

We recommend including `baseTokenData.toRecipient` and `quoteTokenData.toTrader` in the order's signature. If these fields are intended to be specified at the time of calling `LiquoriceSettlement.settle`, it is advisable to explicitly pass them as arguments to the method.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Liquorice |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Liquorice/README.md#10-missing-signature-validation-in-order-structure
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

