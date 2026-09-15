---
# Core Classification
protocol: Alpha Finance Homora V2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10872
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/alpha-homora-v2/
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

protocol_categories:
  - dexes
  - yield
  - services
  - liquidity_manager
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H01] Users can force other users to pay their fees

### Overview


The bug report is related to the HomoraBank system, which is a platform for users to borrow tokens. When users borrow tokens using HomoraBank, the bank takes on debt from CREAM and must account for each user’s share of that debt. As CREAM adds interest to the borrowed amount, the totalDebt for the corresponding token increases, resulting in an increase in the amount owed by each HomoraBank user with debt in that token.

In addition to paying interest, users also pay a fee to the governor of HomoraBank. This fee is a percentage of the interest earned by CREAM and is calculated every time interest is accrued. The fee amount is then recorded as a pendingReserve in the bank structure. However, the fee is not added to the totalDebt owed by users, and it is only when the governor calls the resolveReserve function that the pendingReserve “resolves” and the fee is actually added to the totalDebt.

This means that if a user repays their debt before the governor next calls resolveReserve, they will avoid paying fees on their debt. This could result in malicious users passing off huge amounts of fees to other users, leading to those other users getting liquidated as a result. To avoid these issues, the code should be updated to increment totalDebt every time fees are accrued to ensure that all fees are charged to users fairly according to their share of borrows. This bug was fixed in PR#94.

### Original Finding Content

When users [`borrow` tokens](https://github.com/AlphaFinanceLab/homora-v2/blob/5efa332f2ecf8e9705c326cffda5305bc6f752f7/contracts/HomoraBank.sol#L456) using `HomoraBank`, the bank performs a [borrow from `CREAM`](https://github.com/AlphaFinanceLab/homora-v2/blob/5efa332f2ecf8e9705c326cffda5305bc6f752f7/contracts/HomoraBank.sol#L570). As `HomoraBank` takes on the debt from `CREAM`, it must account internally for each user’s proportionate share of that debt. As `CREAM` adds interest to the borrowed amount, the [`totalDebt` for the corresponding token increases](https://github.com/AlphaFinanceLab/homora-v2/blob/5efa332f2ecf8e9705c326cffda5305bc6f752f7/contracts/HomoraBank.sol#L190), which in turn increases the amount owed by each `HomoraBank` user who has debt in that token.


In addition to paying interest, users also pay a fee to the governor of `HomoraBank`. This [fee is a percentage](https://github.com/AlphaFinanceLab/homora-v2/blob/5efa332f2ecf8e9705c326cffda5305bc6f752f7/contracts/HomoraBank.sol#L189) of the interest earned by `CREAM`. However, while the `CREAM` interest is [accrued automatically](https://github.com/AlphaFinanceLab/homora-v2/blob/5efa332f2ecf8e9705c326cffda5305bc6f752f7/contracts/HomoraBank.sol#L112) on many calls to the bank – so that the interest earned is always up to date at the time of a withdrawal – the same is not true of the fee.


The fee is calculated every time interest is accrued, in the [`accrue` function](https://github.com/AlphaFinanceLab/homora-v2/blob/5efa332f2ecf8e9705c326cffda5305bc6f752f7/contracts/HomoraBank.sol#L183). The fee amount is then merely recorded as a `pendingReserve` in the bank struct; it is not yet added to the `totalDebt` owed by users (which is required to effectively “charge” the fee). Only when the governor calls the function [`resolveReserve`](https://github.com/AlphaFinanceLab/homora-v2/blob/5efa332f2ecf8e9705c326cffda5305bc6f752f7/contracts/HomoraBank.sol#L211), does the `pendingReserve` “resolve” and the fee actually get added to the `totalDebt`.


This means that if a user repays their debt before the governor next calls `resolveReserve`, they will avoid paying fees on their debt. The economic incentive is then for users to front-run the governor’s calls to `resolveReserve`. Importantly, although a user could avoid paying fees in this manner, the fees would still be accrued to the bank, and they would instead be charged to the other users who have debt associated with the same token.


In extreme cases, especially if `resolveReserve` were not called regularly by governance, malicious users could pass off huge amounts of fees to other users, which could lead to those other users getting liquidated as a result.


To avoid these issues and to align the code with the intent of the system, consider incrementing `totalDebt` every time fees are accrued to ensure that all fees are charged to users fairly according to their share of borrows.


***Update:** Fixed in [PR#94](https://github.com/AlphaFinanceLab/homora-v2/pull/94).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Alpha Finance Homora V2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/alpha-homora-v2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

