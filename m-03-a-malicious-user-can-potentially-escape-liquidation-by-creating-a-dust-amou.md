---
# Core Classification
protocol: Mochi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 937
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-mochi-contest
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/127

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

protocol_categories:
  - dexes
  - cdp
  - cross_chain
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WatchPug
  - jonah1005
---

## Vulnerability Title

[M-03] A malicious user can potentially escape liquidation by creating a dust amount position and trigger the liquidation by themself

### Overview


This bug report is about a vulnerability in the current implementation of the WatchPug system. The vulnerability allows a malicious user to potentially escape liquidation by creating a dust amount position which triggers the liquidation. The liquidator may confuse the current dust auction with the ‘liquidatable’ position or be unable to proceed with such a complex liquidation. The recommendation is to consider making liquidated positions unable to be used (for depositing and borrowing) again.

### Original Finding Content

_Submitted by WatchPug, also found by jonah1005_

In the current implementation, a liquidated position can be used for depositing and borrowing again.

However, if there is a liquidation auction ongoing, even if the position is now `liquidatable`, the call of `triggerLiquidation()` will still fail.

The liquidator must `settleLiquidation` first.

If the current auction is not profitable for the liquidator, say the value of the collateral can not even cover the gas cost, the liquidator may be tricked and not liquidate the new loan at all.

Considering if the liquidator bot is not as small to handle this situation (take the profit of the new liquidation and the gas cost loss of the current auction into consideration), a malicious user can create a dust amount position trigger the liquidation by themself.

Since the collateral of this position is so small that it can not even cover the gas cost, liquidators will most certainly ignore this auction.

The malicious user will then deposit borrow the actual loan.

When this loan becomes `liquidatable`, liquidators may:

1.  confuse the current dust auction with the `liquidatable` position;
2.  unable to proceed with such a complex liquidation.

As a result, the malicious user can potentially escape liquidation.

##### Recommendation
Consider making liquidated positions unable to be used (for depositing and borrowing) again.

**[ryuheimat (Mochi) confirmed](https://github.com/code-423n4/2021-10-mochi-findings/issues/127)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | WatchPug, jonah1005 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/127
- **Contest**: https://code4rena.com/contests/2021-10-mochi-contest

### Keywords for Search

`vulnerability`

