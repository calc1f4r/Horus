---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28190
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Anchor%20Collateral%20stETH/README.md#4-an-unfavorable-exchange-may-occur
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
  - MixBytes
---

## Vulnerability Title

An unfavorable exchange may occur

### Overview


This bug report is about a potential issue in the RewardsLiquidator.vy contract, which could cause an unfavorable swap if the initial balance of USDC or UST plus the exchanged tokens are bigger than the minimum required swap amount. The issue is not considered a risk to the project, however, it is recommended to calculate the swapped amount with the difference of the balance before and after the transaction. This is not a planned behavior that needs to be handled.

### Original Finding Content

##### Description
At the lines: 
https://github.com/lidofinance/anchor-collateral-steth/blob/8d52ce72cb42d48dff1851222e3b624c941ddb30/contracts/RewardsLiquidator.vy#L306-L308 
and 
https://github.com/lidofinance/anchor-collateral-steth/blob/8d52ce72cb42d48dff1851222e3b624c941ddb30/contracts/RewardsLiquidator.vy#L329-L331 
if the initial USDC or UST balance + exchanged tokens are bigger than min required swap amount then an unfavorable swap may occur.
Actually, it is safe for the project.
##### Recommendation
It is recommended to calc swapped amount with difference balance from and balance after.
This is not a planned behavior that needs to be handled.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Anchor%20Collateral%20stETH/README.md#4-an-unfavorable-exchange-may-occur
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

