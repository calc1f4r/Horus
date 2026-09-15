---
# Core Classification
protocol: Yearn Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28458
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/Yfi%20Maker/README.md#1-losses-are-not-taken-into-account-in-the-strategy
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
---

## Vulnerability Title

Losses are not taken into account in the strategy

### Overview


The bug report states that the function `liquidatePosition()` in the file Strategy.sol does not take into account the value of the `_loss` variable accounting in `prepareReturn()` function. This means that the `liquidatePosition()` function will always return `_liquidatedAmount = _amountNeeded` excluding losses. This implementation may lead to a revert when the Vault calls the `withdraw` function due to an insufficient balance. Furthermore, the withdrawer from the Vault should incur the losses from liquidation caused by their own withdrawal, but the `liquidatePosition()` function is ignoring any losses from the underlying DAI vault, which could result in improper accounting of user balances and possible locking of the Vault withdrawals. 

The recommendation is to rewrite the logic of `liquidatePosition()` so that it takes into account the losses.

### Original Finding Content

##### Description
At line: https://github.com/orbxball/yfi-maker/blob/63af6fcfa536073f00d652f49befd18e429b5500/contracts/Strategy.sol#L264-L277
the `liquidatePosition()` function does not take into account the value of the`_loss` variable accounting in `prepareReturn()` function. In this case the `liquidatePosition()` function will always return `_liquidatedAmount = _amountNeeded` excluding losses.
This implementation may lead to revert when the Vault call the function `withdraw` function (at line https://github.com/yearn/yearn-vaults/blob/952b767fcd597fac8aa2cf5d023532d150bb9236/contracts/BaseStrategy.sol#L681) by reason of the insufficient balance. 
  
Also the withdrawer from vault should incur the losses from liquidation caused by his own withdrawal. However, the [liquidatePosition()](https://github.com/orbxball/yfi-maker/blob/63af6fcfa536073f00d652f49befd18e429b5500/contracts/Strategy.sol#L264) is ignoring any losses from underlying DAI vault. This may lead to improper accounting of user balances and possible locking of vault withdrawals.  
  
##### Recommendation
It is recommended to rewrite logic of `liquidatePosition()`  considering the losses.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | MixBytes |
| Protocol | Yearn Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/Yfi%20Maker/README.md#1-losses-are-not-taken-into-account-in-the-strategy
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

