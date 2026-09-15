---
# Core Classification
protocol: Telcoin
chain: everychain
category: uncategorized
vulnerability_type: transferfrom_vs_safetransferfrom

# Attack Vector Details
attack_type: transferfrom_vs_safetransferfrom
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3634
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/25
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/82

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.40
financial_impact: medium

# Scoring
quality_score: 2
rarity_score: 5

# Context Tags
tags:
  - transferfrom_vs_safetransferfrom
  - weird_erc20

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - launchpad

# Audit Details
report_date: unknown
finders_count: 15
finders:
  - pashov
  - Deivitto
  - 0x4non
  - yixxas
  - rotcivegaf
---

## Vulnerability Title

M-2: Unsafe ERC20 methods

### Overview


This bug report is about unsafe ERC20 methods which can cause the transaction to revert for certain tokens. The issue was found by a group of people, including 0x4non, 0xAgro, yixxas, 0xheynacho, Bnke0x0, WATCHPUG, aphak5010, rotcivegaf, Mukund, hickuphh3, pashov, hyh, Deivitto, rvierdiiev, and eierina. The issue is related to certain tokens that do not conform to the standard IERC20 interface, such as when using `IERC20(token).transferFrom()` and `IERC20(token).transfer()`. This can cause the transaction to revert if the _aggregator does not always consume all the allowance given at Line 72, or when the current allowance is not zero (e.g. USDT). 

The impact of this issue is that the contract will malfunction for certain tokens. The code snippets related to this issue can be found at Lines 47-82 and 94-97 in the FeeBuyback.sol file. The issue was discovered through manual review. The recommendation is to consider using SafeERC20 for transferFrom, transfer, and approve. A discussion on the issue can be found in the telcoin-staking pull request #6.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/82 

## Found by 
0x4non, 0xAgro, yixxas, 0xheynacho, Bnke0x0, WATCHPUG, aphak5010, rotcivegaf, Mukund, hickuphh3, pashov, hyh, Deivitto, rvierdiiev, eierina

## Summary

Using unsafe ERC20 methods can revert the transaction for certain tokens.

## Vulnerability Detail

There are many [Weird ERC20 Tokens](https://www.hacknote.co/17c261f7d8fWbdml/doc/182a568ab5cUOpDM) that won't work correctly using the standard `IERC20` interface.

For example, `IERC20(token).transferFrom()` and `IERC20(token).transfer()` will fail for some tokens as they may not conform to the standard IERC20 interface. And if `_aggregator` does not always consume all the allowance given at L72, the transaction will also revert on the next call, because there are certain tokens that do not allow approval of a non-zero number when the current allowance is not zero (eg, USDT).

## Impact

The contract will malfunction for certain tokens.

## Code Snippet

https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/fee-buyback/FeeBuyback.sol#L94-L97

https://github.com/sherlock-audit/2022-11-telcoin/blob/main/contracts/fee-buyback/FeeBuyback.sol#L47-L82

## Tool used

Manual Review

## Recommendation

Consider using `SafeERC20` for `transferFrom`, `transfer` and `approve`.

## Discussion

**amshirif**

https://github.com/telcoin/telcoin-staking/pull/6

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 2/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Telcoin |
| Report Date | N/A |
| Finders | pashov, Deivitto, 0x4non, yixxas, rotcivegaf, hickuphh3, WATCHPUG, hyh, Bnke0x0, 0xheynacho, Mukund, rvierdiiev, 0xAgro, aphak5010, eierina |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-telcoin-judging/issues/82
- **Contest**: https://app.sherlock.xyz/audits/contests/25

### Keywords for Search

`transferFrom vs safeTransferFrom, Weird ERC20`

