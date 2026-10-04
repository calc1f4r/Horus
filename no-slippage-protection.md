---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44899
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-30-Vaultka.md
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
  - Zokyo
---

## Vulnerability Title

No slippage protection

### Overview


The bug report describes a medium severity issue that has been resolved. It involves the SakeVaultV2.sol function _swap(), which is used by external functions openPosition() and fulfilledRequestSwap(). When _swap() interacts with a decentralized exchange (DEX), there is a risk of price slippage, meaning the output amount received may be less than the desired amount. The report recommends adding an argument for the desired output amount in the openPosition() and fulfilledRequestSwap() functions. The issue has been resolved by passing information about the slippage through the calldata.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

SakeVaultV2.sol - In function _swap() which is invoked by external functions: openPosition() and fulfilledRequestSwap(). As _swap() interacts with an external Decentralized Exchange (DEX), it can be exposed to price slippage on execution. The functions mentioned do not consider requiring the output amount to be greater than the desired minimum amount.
For instance, velaShares is the output amount received of vlp after staking USDC that resulted from _swap. velaShares can end up being less than the desirable amount that the user had in mind at the beginning of the execution of openPosition(). The same should be considered in fulfilledRequestSwap().

**Recommendation** 

Add an argument in openPosition() and fulfilledRequestSwap() that represents the desirable output amount to be set by the user. 
Fix: Client acknowledges that slippage amount of swap is to be handled via Kyberswap by passing information about it through the calldata.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-30-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

