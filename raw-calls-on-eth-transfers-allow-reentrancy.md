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
solodit_id: 27856
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Stablecoin%20(crvUSD)/README.md#1-raw-calls-on-eth-transfers-allow-reentrancy
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

Raw calls on ETH transfers allow reentrancy

### Overview


This bug report is about a vulnerability in the Curvefi Stablecoin Controller contract. If WETH is used as collateral, users can choose to receive native ETH when it is sent to them. This breaks the Checks-Effects-Interactions pattern, meaning a call to an arbitrary address can be made in the middle of functions `repay()` and `_liquidate()`. This means an attacker can reenter some other smart contract (excluding the Controller) and call `rate_write()` in `AggMonetaryPolicy`, and the rate will be updated using old `total_debt` (not affected by ongoing `repay` or `liquidate`). The recommendation is to limit gas on native ETH transfers in order to prevent this vulnerability.

### Original Finding Content

##### Description

If WETH is used as collateral, users can choose to receive native ETH when it is sent to users. It happens in function `_withdraw_collateral()`.

- https://github.com/curvefi/curve-stablecoin/blob/0d9265cc2dbd221b0f27f880fac1c590e1f12d28/contracts/Controller.vy#L514-L521

It breaks Checks-Effects-Interactions pattern. So, a call to an arbitrary address can be made in the middle of functions `repay()` and `_liquidate()`.

- https://github.com/curvefi/curve-stablecoin/blob/0d9265cc2dbd221b0f27f880fac1c590e1f12d28/contracts/Controller.vy#L731
- https://github.com/curvefi/curve-stablecoin/blob/0d9265cc2dbd221b0f27f880fac1c590e1f12d28/contracts/Controller.vy#L795
- https://github.com/curvefi/curve-stablecoin/blob/0d9265cc2dbd221b0f27f880fac1c590e1f12d28/contracts/Controller.vy#L1054
- https://github.com/curvefi/curve-stablecoin/blob/0d9265cc2dbd221b0f27f880fac1c590e1f12d28/contracts/Controller.vy#L1069

Thus, an attacker can reenter some other smart contract (excluding this Controller). For example, this attacker can call`rate_write()` in `AggMonetaryPolicy`, and the rate will be updated using old `total_debt` (not affected by ongoing `repay` or `liquidate`).

##### Recommendation

We recommend limiting gas on native ETH transfers.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Curve%20Finance/Curve%20Stablecoin%20(crvUSD)/README.md#1-raw-calls-on-eth-transfers-allow-reentrancy
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

