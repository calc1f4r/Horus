---
# Core Classification
protocol: Possumadapters
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44150
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PossumAdapters-Security-Review.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[L-01] Remaining Tokens Should Be Sent to `_swap.recevier()` Instead of `msg.sender` in `swapOneInch()` Function

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Reported By

[EgisSec](https://twitter.com/EgisSec)

## Description

When calling `swapOneInch()` we specify `swapData()` and `_forLiquidity()`. Inside `swapData()` we specify a `receiver` who will receive the tokens.

There is a case when if `_forLiquidity = false` we check if there are any remaining PSM tokens by subtracting `spentAmount_` from `_swap.psmAmount`.

If there are any remaining tokens, they are sent to `msg.sender`. Considering we are specifying a `swapData.receiver`, if there are any remaining PSM tokens, they should be sent to `swapData.receiver`.

## Impact

Inconvenience and potential gas costs, as `msg.sender` has to transfer the tokens to `swapData.receiver`.

## Location of Affected Code

File: [AdapterV1.sol#L599](https://github.com/shieldify-security/SPP-Adapters/blob/335351b51a87ce3d20ea471d0f686776ce7d2393/src/AdapterV1.sol#L599)

## Recommendation

Consider implementing the following change:

```solidity
- if (remainAmount > 0) PSM.safeTransfer(msg.sender, remainAmount);
+ if (remainAmount > 0) PSM.safeTransfer(_swap.recevier, remainAmount);
```

## Team Response

Fixed as proposed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Possumadapters |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PossumAdapters-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

