---
# Core Classification
protocol: Secured Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59974
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
source_link: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
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
finders_count: 3
finders:
  - Mustafa Hasan
  - Valerian Callens
  - Guillermo Escobero
---

## Vulnerability Title

Modifying System Parameters Can Lead To Dangerous Behavior

### Overview


This bug report discusses potential issues with the Secured Finance protocol that could lead to user liquidations and market instability. The report highlights three specific areas where updates to system parameters could have unintended consequences. These include modifying the list of accepted collateral currencies, updating haircut values, and the potential for draining funds from the ReserveFund contract. The report recommends that the Secured Finance team carefully consider the impact of any parameter updates and only make changes when absolutely necessary.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> _We will notify users & community about system parameter updates before we execute them. Also, we will use multi-sig wallet as our contract owner, so nobody can update them alone._

**File(s) affected:**`TokenVault.sol`

**Description:** Administrators of the Secured Finance protocol can modify a set of parameters that can lead to liquidations and market instability:

1.   `TokenVaultStorage.slot().collateralCurrencies` set is queried when calculating the available collateral of users. This set can be modified by the owner of `TokenVault`, calling `TokenVault.updateCurrency()`. If this administrator removes a currency from the set, this currency will not be used in the collateral calculation, and it will be worth zero (in user positions and deposited funds), potentially leading to a cascade of user liquidations.
2.   Updating haircut values can uncover the positions of some users.
3.   If the contract `ReserveFund` is not paused and the liquidated user is insolvent, `ReserveFund` can cover in some conditions a portion of the amount transferred to the liquidator. If replicable, this process could lead to draining funds from the contract `ReserveFund`. This is expected to be protected by the Circuit Breaker and minimum debt price modules, and rapid liquidation executions. Protocol operators should be careful when updating the threshold and minimum debt price values. Still, adding more tests of that specific process would help to make sure it is not possible to execute this scenario, by considering several edge cases and extreme conditions.

**Recommendation:** Before removing a collateral currency from the system, updating the haircut rate of a currency, or modifying any other critical parameter, the Secured Finance team should consider the side effects of it, based on the users' positions at that point, and the collateral deposited in the system. This operation should be performed only when it is strictly necessary.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Secured Finance |
| Report Date | N/A |
| Finders | Mustafa Hasan, Valerian Callens, Guillermo Escobero |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/secured-finance/20cad24f-5901-4107-9509-e3d5ad3acc7c/index.html

### Keywords for Search

`vulnerability`

