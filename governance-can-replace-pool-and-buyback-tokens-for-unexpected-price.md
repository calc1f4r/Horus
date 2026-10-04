---
# Core Classification
protocol: Polars
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56023
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-07-Polars.md
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

Governance can replace pool and buyBack tokens for unexpected price

### Overview


The report highlights a potential issue with the contracts CollateralizationERC20.sol and PrimaryCollateralizationERC20.sol. These contracts have four functions that can only be called by the pool: buy, buySeparately, buyBack, and buyBackSeparately. These functions accept both tokens and payment, but do not check if the price is fair. However, there is a possibility for the pool to be updated and for a large amount of collateral tokens to be withdrawn for a small payment. The recommendation is to either remove the function that allows for pool updates or add a comment explaining how all funds are secured, such as requiring a vote for pool updates. The report suggests skipping a re-audit.

### Original Finding Content

**Description**

At contracts CollateralizationERC20.sol, PrimaryCollateralizationERC20.sol there are 4
functions that can be called only by pool: buy, buySeparately, buyBack, buyBackSeparately.
This is good, since the functions accept both amounts: tokensAmount and payment (and don’t
check if price is fair).
At the same time, there is possibility of updating the pool (by governance, function
changePoolAddress), and withdraw lots of collateral token for very small payment.

**Recommendation**:

Remove changePoolAddress function (if possible). If not, add a comment that briefly explains
how all funds are secured. For example: governance address will be a contract that requires
voting for pool update.

**Re-audit**:

Skipped.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Polars |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-07-07-Polars.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

