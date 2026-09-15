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
solodit_id: 44378
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/641
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-oku-judging/issues/789

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
finders_count: 37
finders:
  - tobi0x18
  - iamreiski
  - xiaoming90
  - Tri-pathi
  - whitehair0330
---

## Vulnerability Title

H-8: Insecure calls to `safeTransferFrom` leads to users tokens steal by attacker

### Overview


This bug report discusses an issue with the function `safeTransferFrom()` in the protocol contract. This function is used to transfer tokens from a user to the protocol contract. However, it has been found that this function can be abused by an attacker to create unfair orders and steal tokens from users. The root cause of this issue is identified in the code and it is recommended to use `msg.sender` instead of the recipient address for the `safeTransferFrom()` function call. The protocol team has already fixed this issue in their code.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-oku-judging/issues/789 

## Found by 
0x37, 0xaxaxa, 0xc0ffEE, Bigsam, Boy2000, BugPull, ChinmayF, John44, KungFuPanda, Laksmana, LonWof-Demon, PoeAudits, Ragnarok, Tri-pathi, Xcrypt, Z3R0, bughuntoor, c-n-o-t-e, covey0x07, future2\_22, gajiknownnothing, hals, iamandreiski, joshuajee, lanrebayode77, nikhil840096, phoenixv110, rahim7x, silver\_eth, t.aksoy, tobi0x18, vinica\_boy, whitehair0330, xiaoming90, y51r, zhoo, zxriptor
### Summary

The function `safeTransferFrom()` is used to transfer tokens from user to the protocol contract. This function is used in `modifyOrder` and `createOrder` with the recipent address as the `owner` form who the tokens will be transfered from. An attacker can abuse this functionnality to create unfaire orders for a protocol user that approve more tokens than needed to the protocol contract the fill the order immediatly and gain instant profit while the victim lost his tokens.

### Root Cause

In `OracleLess.sol::procureTokens():280`
https://github.com/sherlock-audit/2024-11-oku/blob/main/oku-custom-order-types/contracts/automatedTrigger/OracleLess.sol#L280
`procureTokens()` implement tokens transfer from an owner address to the protocol contract

In `StopLimit.sol::createOrder():171`
https://github.com/sherlock-audit/2024-11-oku/blob/main/oku-custom-order-types/contracts/automatedTrigger/StopLimit.sol#L171

In `StopLimit.sol::modifyOrder():226-230`
https://github.com/sherlock-audit/2024-11-oku/blob/main/oku-custom-order-types/contracts/automatedTrigger/StopLimit.sol#L226-L230

In `Bracket.sol::modifyOrder():250-254`
https://github.com/sherlock-audit/2024-11-oku/blob/main/oku-custom-order-types/contracts/automatedTrigger/Bracket.sol#L250-L254

### Internal pre-conditions

_No response_

### External pre-conditions

1. A user should have approve more tokens than needed for a trade that whould result in some residual allowance to the protocole contract

### Attack Path

1. The attacker create/modify an unfaire order with the victim as recipent with an amounIn <= residual allowance
2. The prococol then transfer the tokens from the user to create the order
3. The attacker fill the order an gain instant profit

### Impact

_No response_

### PoC

_No response_

### Mitigation

It would be better to use `msg.sender` to ensure that the `recipient/owner` of the order is the order creator or juste use `msg.sender` as parameter to the `safeTransferFrom()` function call instead of order recipient



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/gfx-labs/oku-custom-order-types/pull/1

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Oku's New Order Types Contract Contest |
| Report Date | N/A |
| Finders | tobi0x18, iamreiski, xiaoming90, Tri-pathi, whitehair0330, silver\_eth, covey0x07, zxriptor, future2\_22, lanrebayode77, phoenixv110, Z3R0, 0xaxaxa, Xcrypt, joshuajee, gajiknownnothing, nikhil840096, KungFuPa, Boy2000, LonWof-Demon, y51r, 0x37, John44, vinica\_boy, BugPull, Ragnarok, t.aksoy, Bigsam, ChinmayF, rahim7x, bughuntoor, c-n-o-t-e, Laksmana, zhoo, 0xc0ffEE, PoeAudits, hals |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-oku-judging/issues/789
- **Contest**: https://app.sherlock.xyz/audits/contests/641

### Keywords for Search

`vulnerability`

