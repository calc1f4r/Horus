---
# Core Classification
protocol: dForce
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34261
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#4-tokens-in-segregated-mode-cannot-be-fully-repaid-by-borrowers
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
  - MixBytes
---

## Vulnerability Title

Tokens in Segregated mode cannot be fully repaid by borrowers

### Overview


The bug report states that there is an issue with the `MarketV2.currentDebt` value for tokens with Segregated mode activated. The `currentDebt` value is supposed to prevent the debt from exceeding the `debtCeiling`, but it is not taking into account the increasing debt over time due to the `InterestRateModel` associated with the `iToken`. This causes borrowers to be unable to fully repay their debt until the contract's owner updates the `ControllerV2ExtraExplicit` implementation. The bug is labeled as `high` because it can potentially block certain `repayBorrow` transactions. The recommendation is to reset the `currentDebt` value to `zero` when it is less than the amount being repaid.

### Original Finding Content

##### Description
Tokens that have the Segregated mode activated possess a designated `MarketV2.currentDebt` value. This value is prevented from surpassing the `debtCeiling` through borrow functions. Notably, the `ControllerV2ExtraExplicit.afterRepayBorrow` function employs the `SafeMath.sub` function to subtract the amount of repaid underlying assets from the `currentDebt` value. This function is designed to revert any underflow errors. However, the `currentDebt` value does not consider that the debt is increasing over time with `InterestRateModel`, associated with the `iToken`. Consequently, the repaid amount always exceeds the borrowed sum, causing borrowers unable to fully repay their debt until the contract's owner updates the `ControllerV2ExtraExplicit` implementation. 

This issue is labeled as `high`, since it imposes the potential to temporarily block specific `repayBorrow` transactions.

Related code - `beforeBorrow` for Segregated mode: https://github.com/dforce-network/LendingContracts/blob/6f3a7b6946d8226b38e7f0d67a50e68a28fe5165/contracts/ControllerV2ExtraExplicit.sol#L200
##### Recommendation
We recommend reseting the `currentDebt` value to `zero` in cases where `currentDebt` is less than `repayAmount`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | dForce |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/dForce/Lending%20v2/README.md#4-tokens-in-segregated-mode-cannot-be-fully-repaid-by-borrowers
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

