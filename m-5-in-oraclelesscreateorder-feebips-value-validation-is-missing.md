---
# Core Classification
protocol: Oku's New Order Types Contract Contest
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44383
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/641
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-oku-judging/issues/277

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
  - phoenixv110
---

## Vulnerability Title

M-5: In OracleLess.createOrder() feeBips value validation is missing

### Overview


This bug report discusses an issue, M-5, found in the code for the OracleLess contract. The problem is that there is no validation for the maximum value of the `feeBips` input, which should be less than or equal to 10000. This means that a malicious user can create orders with a `feeBips` value greater than 10000, causing them to fail in the `execute()` method. This can be abused by creating multiple orders that cannot be executed or cancelled, leading to a denial of service for other orders. The root cause of this issue is the lack of validation in the `createOrder()` function. The impact of this bug is that these orders will remain in the queue and potentially cause the queue to exceed its maximum gas usage limit, causing a denial of service for other orders. To fix this issue, the validation for `feeBips` should be added to the `createOrder()` function in the OracleLess contract.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-oku-judging/issues/277 

## Found by 
phoenixv110
### Summary

The max value of `feeBips` should be ***<=10000***. But this validation is missing in `createOrder()`. All such orders where feeBips is > 10000 will revert in `execute()` method. A malicious user can create 100s of such orders which never execute even if the price conditions are met. It can use `USDC` as tokenIn and blacklist itself so that `_cancelOrder()` also reverts. As `_cancelOrder()` tries to transfer tokenIn to the user. If the receiver is blacklisted user then transfer will fail. This was the malicious user can create 1 wei orders will can neither execute nor cancellable. 

https://github.com/sherlock-audit/2024-11-oku/blob/main/oku-custom-order-types/contracts/automatedTrigger/OracleLess.sol#L38C5-L67C6

### Root Cause

Missing feeBips input validation in `createOrder()`

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

_No response_

### Impact

Such orders will exist in the `pendingOrderIds` which can not be deleted from the queue. These orders can increase the queue size until the max gas usage limit is reached. Which will DoS all other orders.

### PoC

_No response_

### Mitigation

Add the check `feeBips <= 10000` in `createOrder()` of `OracelLess.sol`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Oku's New Order Types Contract Contest |
| Report Date | N/A |
| Finders | phoenixv110 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-oku-judging/issues/277
- **Contest**: https://app.sherlock.xyz/audits/contests/641

### Keywords for Search

`vulnerability`

