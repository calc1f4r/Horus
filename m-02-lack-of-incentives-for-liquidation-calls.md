---
# Core Classification
protocol: Sharwafinance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36482
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] Lack of incentives for Liquidation calls

### Overview


This report describes a bug in the `liquidation` process of a financial system that could have a high impact. The liquidation process is important for maintaining the system's financial health, but there is currently no incentive for users to initiate it. This could lead to delayed liquidation, which increases the risk of financial losses and could even threaten the solvency of the system. The report recommends implementing incentives for liquidators to improve the liquidation process and manage systemic risk effectively.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

The `liquidation` operates as follows:

1. All collateral balances owned by the `marginAccount` are retrieved in the code line `MarginAccount#L221-L231`.
2. Assets are liquidated for USDC through the `ModularSwapRouter::liquidate` function, converting the account's holdings into a more liquid form. Code line `MarginAccount#L233`.
3. Debts in corresponding `LiquidityPools` are cleared in the code line `MarginAccount#L237`, using the USDC acquired from liquidation (step 2). If debts exceed the liquidation proceeds, additional funds are drawn from the `insurancePool` to cover the shortfall (`MarginAccount#L293`).

The problem is that there is no incentive for calling the `MarginTrading::liquidate` function, which is crucial for maintaining the financial health of the system. The lack of incentives for initiating liquidation poses several risks:

1. If the value of collateral within a margin account sharply declines, and liquidation is not triggered in a timely manner, the account may become insolvent, **threatening the solvency of the `InsurancePool` contract**.
2. Delayed liquidation increases exposure to financial risk, particularly as market conditions fluctuate, potentially degrading the collateral's value further.
3. Simultaneous insolvencies across multiple accounts could destabilize the entire system, highlighting the critical nature of proactive liquidation management.

**Recommendations**

It is advisable to implement incentives for liquidators. This could involve adjusting the liquidation process to offer a percentage of the liquidated assets to the caller, ensuring debts are covered while also providing a reward for managing systemic risk effectively.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Sharwafinance |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/SharwaFinance-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

