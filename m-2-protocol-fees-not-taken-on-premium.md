---
# Core Classification
protocol: Illuminate Round 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6234
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/35
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-illuminate-judging/issues/22

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - IllIllI
---

## Vulnerability Title

M-2: Protocol fees not taken on premium

### Overview


This bug report is about a vulnerability found in the Swivel version of the `lend()` function in the Illuminate protocol. The vulnerability allows users to use any extra underlying premium from their Swivel orders to buy more iPTs without paying a fee. This means that Illuminate misses out on fees. The fee is calculated based on the amount listed in the orders, but the premium is the balance change after the orders have executed. No fee is charged on this premium, either when swapping in the yield pool or when minting iPTs directly. The tool used to discover this vulnerability was Manual Review. The recommendation is to calculate the fee after the order on the full balance change, which is similar to a finding from the previous contest.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-illuminate-judging/issues/22 

## Found by 
IllIllI

## Summary

Protocol fees not taken on premium


## Vulnerability Detail
The Swivel version of `lend()` allows the user to use any extra underlying premium from their Swivel orders, to buy more iPTs via a swap or minting directly, but no fee is taken from this premium.


## Impact
Rather than using the Illuminate version of `lend()`, which charges a fee, users could use the Swivel version, and ensure the fee portion is small, and the premium non-fee portion is large, so that Illuminate misses out on fees.


## Code Snippet
The fee is calculated based on the amount listed in the orders:
```solidity
// File: src/Lender.sol : Lender.lend()   #1

488            // Lent represents the total amount of underlying to be lent
489 @>         uint256 lent = swivelAmount(a);
490    
491            // Get the underlying balance prior to calling initiate
492            uint256 starting = IERC20(u).balanceOf(address(this));
493    
494            // Transfer underlying token from user to Illuminate
495            Safe.transferFrom(IERC20(u), msg.sender, address(this), lent);
496    
497            // Calculate fee for the total amount to be lent
498:@>         uint256 fee = lent / feenominator;
```
https://github.com/sherlock-audit/2023-01-illuminate/blob/main/src/Lender.sol#L488-L498

But the premium is the balance change after the orders have executed (can be thought of as positive slippage):
```solidity
// File: src/Lender.sol : Lender.lend()   #2
525                // Calculate the premium
526 @>             uint256 premium = (IERC20(u).balanceOf(address(this)) - starting) -
527:                   fee;
```
https://github.com/sherlock-audit/2023-01-illuminate/blob/main/src/Lender.sol#L525-L527

And no fee is charged on this premium, either when swapping in the yield pool, or when minting iPTs directly.

## Tool used

Manual Review


## Recommendation
Calculate the fee after the order, on the full balance change

This is similar to a [finding](https://github.com/sherlock-audit/2022-10-illuminate-judging/issues/45) from the previous contest, but the mitigation was to remove the amount fee from the premium, but didn't address the fee for the premium itself

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Illuminate Round 2 |
| Report Date | N/A |
| Finders | IllIllI |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-illuminate-judging/issues/22
- **Contest**: https://app.sherlock.xyz/audits/contests/35

### Keywords for Search

`vulnerability`

