---
# Core Classification
protocol: Curve Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40999
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Lending/README.md#2-the-use-of-txorigin
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

The use of `tx.origin`

### Overview


The report highlights a bug in the code for a liquidity gauge manager. The issue is that the code sets the manager as a "tx.origin" in the gauge deploy transaction. This is not recommended because some DeFi users may be using Multisigs or Account Abstraction wallets, which means that "tx.origin" may not accurately identify the final user. The recommendation is to make the manager a customizable input for the "factory.deploy_gauge()" function.

### Original Finding Content

##### Description
Liquidity gauge `manager` is set as a `tx.origin` of the gauge deploy transaction.
- https://github.com/curvefi/curve-stablecoin/blob/c3f7040960627f023a2098232658c49e74400d03/contracts/lending/LiquidityGauge.vy#L176

It is not recommended to have `tx.origin` in access control logic.
Some DeFi users are Multisigs or Account Abstraction wallets. 
In such cases, `tx.origin` is not correct final user identification.

##### Recommendation
We recommend having `manager` as a customizable input for `factory.deploy_gauge()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Curve Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Lending/README.md#2-the-use-of-txorigin
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

