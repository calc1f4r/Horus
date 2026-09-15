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
solodit_id: 28588
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Bond%20Appetit/README.md#4-potential-collateralization-imbalance
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
  - MixBytes
---

## Vulnerability Title

Potential collateralization imbalance

### Overview

See description below for full details.

### Original Finding Content

##### Description
In function `balance` defined at https://github.com/bondappetit/bondappetit-protocol/blob/88680691fe8d872c5fc26e9500d19cf7caaa9861/contracts/depositary/StableTokenDepositaryBalanceView.sol#L81 contract aggregates balances through different tokens, so function return sum of collateral assets. However, as we known price of some stable coins can be changed(especially algorithmic stable coins), so we can't simply calculate sum of tokens to get real assets value.

##### Recommendation
We recommend to use oracles to fetch real assets price

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Bond Appetit |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Bond%20Appetit/README.md#4-potential-collateralization-imbalance
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

