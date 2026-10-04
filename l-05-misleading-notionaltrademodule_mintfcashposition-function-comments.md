---
# Core Classification
protocol: Notional
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25106
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-notional-coop
source_link: https://code4rena.com/reports/2022-06-notional-coop
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-05] Misleading `NotionalTradeModule._mintFCashPosition` function comments

### Overview

See description below for full details.

### Original Finding Content


The function comments imply that the given fCash position is redeemed. However, this function implements **minting** fCash tokens.

### Findings

[NotionalTradeModule.sol#L415](https://github.com/code-423n4/2022-06-notional-coop/blob/6f8c325f604e2576e2fe257b6b57892ca181509a/index-coop-notional-trade-module/contracts/protocol/modules/v1/NotionalTradeModule.sol#L415)

```solidity
* @dev Redeem a given fCash position from the specified send token (either underlying or asset token)
```

### Recommended Mitigation Steps

Fix the comments to mention minting instead of redeeming.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Notional |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-notional-coop
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2022-06-notional-coop

### Keywords for Search

`vulnerability`

