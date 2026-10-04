---
# Core Classification
protocol: Noodles_2025-03-11
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62520
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Noodles-security-review_2025-03-11.md
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

[M-02] Missing slippage protection on sellCredits()

### Overview


The report states that users who trade credit tokens are experiencing an issue with bots causing slippage. This is because the price of credit tokens changes as the total supply changes. The report also explains that this issue can occur when a user submits a transaction to sell credit tokens and another transaction is executed before theirs, causing them to receive less native tokens than intended. To prevent this, the report suggests adding an option for users to specify a minimum amount they want to receive when selling credit tokens. This will help ensure that users receive the amount they intended.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

Users trading credit tokens are prone to slippage by bots. Since VisibilityCredits.sol utilises a bonding curve, the price of credit tokens increase and decrease as the total supply increases and decreases. 


**Slippage on sell:**
 - Alice submits sellCredits() transaction.
 - The transaction remains the mempool for sometime.
 - During this period, another sellCredits() transaction executes (unintentionally by other users or intentionally by bots), thus decreasing the trading cost.
 - Alice's transaction goes through but receives lesser native tokens than intended.

## Recommendations

Provide the users with the option to pass in a `minAmountOut` parameter on sells. Check the trading cost against this parameter to ensure the user receives what they intended to.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Noodles_2025-03-11 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Noodles-security-review_2025-03-11.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

