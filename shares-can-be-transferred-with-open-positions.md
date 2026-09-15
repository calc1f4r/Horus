---
# Core Classification
protocol: Panoptic Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33813
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/panoptic-audit
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
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Shares Can Be Transferred With Open Positions

### Overview


This bug report discusses an issue where shares can be transferred or redeemed from an owner's account even if they have open positions. This is due to the incorrect use of `msg.sender` instead of `from` or `owner` in certain functions such as `transferFrom`, `withdraw`, and `redeem`. This means that an owner can transfer or redeem all of their shares, even if they have not exercised their positions. This can potentially lead to losses for the Panoptic pool if the owner transfers out their shares, leaving under collateralized positions in the pool. The owner can also profit unfairly by minting more shares and then redeeming them. The report suggests correcting the logic of these functions to check the number of open positions for the correct account. The bug has since been resolved.

### Original Finding Content

Shares can be transferred or redeemed from an owner's account while they have open positions. In several cases, `msg.sender` is used where it should be `from` or `owner`:


* `transferFrom`
* `maxWithdraw` used in `withdraw`
* `maxRedeem` used in `redeem`


By approving a second account with no open positions, the owner can thus transfer/redeem their entire share balance with unexercised positions.


* This can expose the Panoptic pool to potential losses when the owner transfers out the shares, leaving under collateralized positions in the pool.
* The owner can collect an undue profit by, for example, minting an ITM position where more shares are minted and then redeeming them.


Consider correcting the logic of the previously mentioned functions to check the number of open positions for the right account.


***Update:** Resolved.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Panoptic Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/panoptic-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

