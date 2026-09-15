---
# Core Classification
protocol: Uniswap V3 Limit Orders
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48912
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
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
  - Hans
  - Alex Roan
  - Giovanni Di Siena
---

## Vulnerability Title

Malicious validators can prevent orders from being created or cancelled

### Overview


The bug report discusses an issue with using `block.timestamp` as the deadline for certain functions in the Uniswap v3 limit orders code. This means that a transaction could be considered valid whenever the validator decides to include it, which could result in orders being fulfilled when they were meant to be cancelled or not being created at all. The report recommends adding deadline arguments to all functions that interact with Uniswap v3 to prevent this issue. The bug has been fixed by adding these arguments in a recent commit by GFX Labs. Cyfrin has acknowledged the issue.

### Original Finding Content

**Description:** Use of `block.timestamp` as the deadline for [`MintParams`](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L1056), [`IncreaseLiquidityParams`](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L1099) and [`DecreaseLiquidityParams`](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L1207) means that a given transaction interfacing with Uniswap v3 will be valid whenever the validator decides to include it. This could result in orders prevented from being created or cancelled if a malicious validator holds these transactions until after the tick price for the given pool has moved such that the deadline is valid but order status is no longer valid.

**Impact:** Whenever the validator decides to include the transaction in a block, it will be valid at that time, since `block.timestamp` will be the current timestamp. This could result in forcing an order to be fulfilled when it was the sender's intention to have it cancelled, by holding until price exceeds the target tick as ITM orders can't be cancelled, or never creating the order at all, by similar reasoning as it is not allowed to create orders that are immediately ITM.

**Recommended Mitigation:** Add deadline arguments to all functions that interact with Uniswap v3 via the `NonFungiblePositionManager`, and pass it along to the associated calls.

**GFX Labs:** Fixed by adding deadline arguments to all Position Manager calls in commit [f05cdfc](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/f05cdfce4762d980235fe4d726800d2b0a112d2d).

**Cyfrin:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Uniswap V3 Limit Orders |
| Report Date | N/A |
| Finders | Hans, Alex Roan, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

