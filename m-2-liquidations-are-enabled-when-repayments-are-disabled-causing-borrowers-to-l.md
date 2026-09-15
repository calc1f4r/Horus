---
# Core Classification
protocol: Blueberry
chain: everychain
category: uncategorized
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6649
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/41
source_link: none
github_link: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/290

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - liquidation

protocol_categories:
  - leveraged_farming
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Jeiwan
  - Nyx
---

## Vulnerability Title

M-2: Liquidations are enabled when repayments are disabled, causing borrowers to lose funds without a chance to repay

### Overview


This bug report is about an issue found in the BlueBerryBank contract. The issue is that when repayments are disabled by the admin, liquidations are still allowed. This means that borrowers cannot repay their debts and are forced to lose their collateral. This was found by Jeiwan and Nyx through manual review. The code snippet that is relevant to this issue is located at BlueBerryBank.sol#L740. The impact of this issue is that positions will be forced to liquidations while their owners won't be able to repay debts to avoid liquidations. The recommendation to fix this issue is to consider disallowing liquidations when repayments are disabled, or alternatively, to consider never disallowing repayments so that users could maintain their positions in a healthy risk range anytime.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/290 

## Found by 
Jeiwan, Nyx

## Summary
Debt repaying can be temporary disabled by the admin of `BlueBerryBank`, however liquidations are not disabled during this period. As a result, users' positions can accumulate more borrow interest, go above the liquidation threshold, and be liquidated, while users aren't able to repay the debts.
## Vulnerability Detail
The owner of [BlueBerryBank](https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L22) can disable different functions of the contract, [including repayments](https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L233-L235). However, while [repayments are disabled](https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L747) liquidations are still [allowed](https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L516-L517). As a result, when repayments are disabled, liquidator can liquidate any position, and borrowers won't be able to protect against that by repaying their debts. Thus, borrowers will be forced to lose their collateral.
## Impact
Positions will be forced to liquidations while their owners won't be able to repay debts to avoid liquidations.
## Code Snippet
[BlueBerryBank.sol#L740](https://github.com/sherlock-audit/2023-02-blueberry/blob/main/contracts/BlueBerryBank.sol#L740)
## Tool used
Manual Review
## Recommendation
Consider disallowing liquidations when repayments are disabled. Alternatively, consider never disallowing repayments so that users could maintain their positions in a healthy risk range anytime.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry |
| Report Date | N/A |
| Finders | Jeiwan, Nyx |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/290
- **Contest**: https://app.sherlock.xyz/audits/contests/41

### Keywords for Search

`Liquidation`

