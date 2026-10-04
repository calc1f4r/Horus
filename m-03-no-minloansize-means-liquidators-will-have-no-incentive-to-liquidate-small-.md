---
# Core Classification
protocol: Revert Lend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32269
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-revert-lend
source_link: https://code4rena.com/reports/2024-03-revert-lend
github_link: https://github.com/code-423n4/2024-03-revert-lend-findings/issues/455

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - grearlake
  - falconhoof
---

## Vulnerability Title

[M-03] No `minLoanSize` means liquidators will have no incentive to liquidate small positions

### Overview


The bug report warns that setting the `minLoanSize` to 0 in the protocol can cause serious problems. This is because there will be no incentive for liquidators to pay off small loans that are underwater, which means they would not receive any reward for doing so. This could lead to a cheap attack where someone could borrow many small loans, let them accrue interest and become underwater, without being liquidated. This could result in the entire protocol becoming underwater, and the responsibility of cleaning up the bad debt would fall on the protocol and lenders. The recommended solution is to set a realistic `minLoanSize` to incentivize liquidators to clean up bad debt. The team has acknowledged this issue and plans to implement a reasonable `minLoanSize` before deployment. The judge has marked this as a medium issue due to its potential impact on the protocol.

### Original Finding Content


No `minLoanSize` can destabilise the protocol.

### Vulnerability Details

According to protocol team, they plan to roll out the protocol with `minLoanSize = 0` and adjust that number if needs be. This can be a big issue because there will be no incentive for liquidators to liquidate small underwater positions given the gas cost. To do so would not make economic sense based on the incentive they would receive.

It also opens up a cheap attack path for would be attackers where they can borrow many small loans, which will go underwater as they accrue interest, but will not be liquidated.

### Impact

Can push the entire protocol into an underwater state. Underwater debt would first be covered by Protocol reserves and where they aren't sufficient, lenders will bear the responsibility of the uneconomical clean up of bad debt, so both the protocol and lenders stand to lose out.

### Recommended Mitigation Steps

Close the vulnerability by implementing a realistic `minLoanSize`, which will incentivise liquidators to clean up bad debt.

**[kalinbas (Revert) acknowledged and commented](https://github.com/code-423n4/2024-03-revert-lend-findings/issues/455#issuecomment-2021465002):**
 > Will do the deployment with a reasonable `minLoanSize`.

**[ronnyx2017 (judge) commented](https://github.com/code-423n4/2024-03-revert-lend-findings/issues/455#issuecomment-2028742056):**
 > Normally, I would mark such issues as Low. But given that this issue provides a substantial reminder to the sponsor, I am retaining it as Medium.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Code4rena |
| Protocol | Revert Lend |
| Report Date | N/A |
| Finders | grearlake, falconhoof |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-revert-lend
- **GitHub**: https://github.com/code-423n4/2024-03-revert-lend-findings/issues/455
- **Contest**: https://code4rena.com/reports/2024-03-revert-lend

### Keywords for Search

`vulnerability`

