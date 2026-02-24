---
# Core Classification
protocol: MCDEX Mai Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11402
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/mcdex-mai-protocol-audit/
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

protocol_categories:
  - dexes
  - services
  - derivatives
  - rwa
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H01] Incorrect social loss

### Overview


This bug report is about a bug in the code of the Mcdex.io platform. The bug occurs when a bankrupt position is liquidated and the insurance fund is empty. In this case, the losses are attributed to positions on the same side, which can lead to the contract being underfunded. This means that some profits will not be redeemable. To fix this issue, the code should be updated to assign losses to the opposite side of the liquidation. The bug has now been fixed.

### Original Finding Content

When a bankrupt position is liquidated and the insurance fund is empty, the [opponent position holders should cover the loss](https://mcdex.io/references/#/en/perpetual?id=auto-liquidation). In this way, the profits on one side are garnished to fund the loss on the other side. This ensures the system as a whole cannot become insolvent. However, the loss is [actually attributed to positions on the same side](https://github.com/mcdexio/mai-protocol-v2/blob/4b198083ec4ae2d6851e101fc44ea333eaa3cd92/contracts/perpetual/Position.sol#L290). In the worst case, none of the positions on the same side will be able to cover the loss, which means the contract will be underfunded and some profits will not be redeemable. Consider updating the code to assign losses to the opposite side of the liquidation.


**Update:** *Fixed.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | MCDEX Mai Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/mcdex-mai-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

