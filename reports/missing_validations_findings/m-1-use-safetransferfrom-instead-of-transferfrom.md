---
# Core Classification
protocol: DODO
chain: everychain
category: uncategorized
vulnerability_type: safetransfer

# Attack Vector Details
attack_type: safetransfer
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3519
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/21
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-dodo-judging/issues/47

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 2.9958817230870607
rarity_score: 0.010295692282349065

# Context Tags
tags:
  - safetransfer
  - erc20

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - yixxas
  - Nyx
  - sach1r0
  - Tomo
  - 0x4non
---

## Vulnerability Title

M-1: Use safeTransferFrom() instead of transferFrom().

### Overview


This bug report is about a vulnerability in some tokens that do not correctly implement the EIP20 standard. These tokens do not correctly handle the return value of the transfer and transferFrom functions, which should be checked for success. This means that some tokens (like USDT) do not actually perform the transfer and return false, while others revert the transaction due to the missing return value. This can cause issues with the protocol as the tokens that don't correctly implement the EIP20 spec will be unusable. To solve this issue, OpenZeppelin's SafeERC20 versions with the safeTransfer and safeTransferFrom functions are recommended, as they handle the return value check as well as non-standard-compliant tokens. This bug was found by sach1r0, Nyx, yixxas, 0x4non, and Tomo using manual review. Although no direct loss of funds was found, Evert0x suggested that a failed token transfer should still be caught.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-dodo-judging/issues/47 

## Found by 
sach1r0, Nyx, yixxas, 0x4non, Tomo

## Summary

The ERC20.transfer() and ERC20.transferFrom() functions return a boolean value indicating success. This parameter needs to be checked for success. Some tokens do not revert if the transfer failed but return false instead.

## Vulnerability Detail
Some tokens (like USDT) don't correctly implement the EIP20 standard and their transfer/ transferFrom function return void instead of a success boolean. Calling these functions with the correct EIP20 function signatures will always revert.
## Impact
Tokens that don't actually perform the transfer and return false are still counted as a correct transfer and tokens that don't correctly implement the latest EIP20 spec, like USDT, will be unusable in the protocol as they revert the transaction because of the missing return value.
## Code Snippet
https://github.com/sherlock-audit/2022-11-dodo/blob/main/contracts/SmartRoute/DODORouteProxy.sol#L420

https://github.com/sherlock-audit/2022-11-dodo/blob/main/contracts/SmartRoute/DODORouteProxy.sol#L423
## Tool used

Manual Review

## Recommendation
Recommend using OpenZeppelin's SafeERC20 versions with the safeTransfer and safeTransferFrom functions that handle the return value check as well as non-standard-compliant tokens.

## Discussion

**Evert0x**

We think a medium is still valid, although no direct loss of funds, a failed token transfer should be catched.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2.9958817230870607/5 |
| Rarity Score | 0.010295692282349065/5 |
| Audit Firm | Sherlock |
| Protocol | DODO |
| Report Date | N/A |
| Finders | yixxas, Nyx, sach1r0, Tomo, 0x4non |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-dodo-judging/issues/47
- **Contest**: https://app.sherlock.xyz/audits/contests/21

### Keywords for Search

`SafeTransfer, ERC20`

