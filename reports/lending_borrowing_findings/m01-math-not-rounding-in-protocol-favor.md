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
solodit_id: 10873
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/alpha-homora-v2/
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

[M01] Math not rounding in protocol favor

### Overview


A bug was recently found in the code of HomoraBank, a protocol used to calculate the amount of debt owed by a position. The calculation used to determine the debt owed was truncating the debt owed in the user’s favor - rounding down even when x.99999 was owed. This could lead to a situation where the protocol becomes undercollateralized without detection, as users are not paying off the full amount of debt. As a result, the extra debt is passed on to other users. To prevent this from happening, it is recommended to always round divisions in the protocol’s favor to help mitigate the risk of users abusing their advantage in the system. This bug has now been fixed in PR#95.

### Original Finding Content

Throughout [`HomoraBank`](https://github.com/AlphaFinanceLab/homora-v2/blob/5efa332f2ecf8e9705c326cffda5305bc6f752f7/contracts/HomoraBank.sol), the amount of debt owed by a position is calculated proportionally to the number of debt shares that position holds. The exact calculation performed is `debtOwed = totalDebt * positionsShare / totalShare`. However, this calculation truncates the debt owed in the user’s favor – rounding down even when `x.99999` is owed.


This means that at any given time, a significant amount of debt can be unaccounted for. Say `n` users each owe `100.9` to the protocol, the sum of their `debtOwed` calculated with truncation is `0.9n` less than the `totalDebt` of the protocol. In an extreme situation, this could lead the protocol to become `0.9n` undercollateralized without detection. If users start paying off this truncated debt, then the extra amount of debt is passed on to other users.


In some situations, a truncation in the user’s favor can have catastrophic consequences for a protocol. While we have not found that to be true of this situation, consider always rounding all divisions in the protocol’s favor to help mitigate the risk of users abusing their advantage in the system.


***Update:** Fixed in [PR#95](https://github.com/AlphaFinanceLab/homora-v2/pull/95).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

