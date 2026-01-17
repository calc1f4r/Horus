---
# Core Classification
protocol: Ethereum Reserve Dollar (ERD)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60118
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
source_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Ibrahim Abouzied
  - Rabib Islam
  - Hytham Farah
---

## Vulnerability Title

Liquidations Are Not Proportionally Funded by All Troves

### Overview


The bug report discusses an issue with the `TroveManager.sol` file where active troves that are liquidating other troves may cause disproportionate liquidation of assets. This means that troves with less popular collateral types may end up with a lot of liquidated debt, leading to potential liquidation cascades. In extreme cases, this could result in unclaimed debt. The recommendation is to either fund liquidations with all troves, regardless of collateral type, or to clearly document this design decision and its consequences. Additionally, a function could be inserted to prevent the last trove of a certain collateral type from being liquidated, and there should be a trove that holds all collateral types and cannot be closed. 

### Original Finding Content

**File(s) affected:**`TroveManager.sol`

**Description:** When active troves are liquidating other troves, assets are liquidated with respect to proportions of collateralized asset types. For example, for a trove that only holds rETH that gets liquidated, all of its rewards (collateral and debt) will go towards only troves that hold rETH. This could lead to scenarios where some troves take on a disproportionate amount of liquidated debt if they use a less popular collateral type. In the case of a particular collateral type taking a steep dive in price, this could lead to liquidation cascades. **At its most extreme, liquidating the last trove that holds a given collateral type may result in perpetually unclaimed debt.**

**Recommendation:** Consider funding liquidations with all troves, regardless of collateral type. Otherwise, explicate in documentation that this is an intentional design decision and discuss the above consequences. If maintaining this logic for liquidation, consider inserting a function that prevents the last trove of a given collateral type from being liquidated. Moreover, consider enforcing the existence of a trove that holds all collateral types and that cannot be closed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethereum Reserve Dollar (ERD) |
| Report Date | N/A |
| Finders | Ibrahim Abouzied, Rabib Islam, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html

### Keywords for Search

`vulnerability`

