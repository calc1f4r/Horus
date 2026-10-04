---
# Core Classification
protocol: Ion Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32705
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ion-protocol-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Liquidations Use Inaccurate rate Values

### Overview


The `liquidate` function in the `Liquidation` contract does not calculate interest before liquidating a vault, leading to incorrect calculations of the amount of collateral and debt to be repaid. This results in the health ratio of the vault being lower than expected and the liquidator receiving less collateral than they should. Additionally, the function may mistakenly determine that a vault is "dusty" and pay off all debt when it is not necessary. To fix this issue, interest should be accrued within the `liquidate` function. This bug has been resolved in a recent pull request.

### Original Finding Content

The [`liquidate` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/Liquidation.sol#L162) of the `Liquidation` contract does not accrue interest prior to liquidating a vault. Instead, interest is accrued within the call to [`confiscateVault` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L797) which determines the amount sent to the liquidator. Therefore, the [`rate`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/Liquidation.sol#L170) at which the amount of collateral and debt to repay for a vault is calculated will be lower than what is sent to the liquidator. This would result in the health ratio of a vault being less than the `TARGET_HEALTH` value after liquidation when it is expected to be no less than this value. Furthermore, the liquidator will receive the collateral at a lower discount than if interest had been accrued prior to liquidation.


Moreover, the `liquidate` function could [determine that a vault will be dusty after being liquidated](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/Liquidation.sol#L221) and pay off all debt when in fact the vault would not have dust after liquidation if using an accurate value for the `rate`. As a result, all of the debt within a vault would be paid off when not required.


Consider accruing interest within the `liquidate` function to ensure that all computations are done with an accurate `rate`.


***Update:** Resolved in [pull request #30](https://github.com/Ion-Protocol/ion-protocol/pull/30).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Ion Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ion-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

