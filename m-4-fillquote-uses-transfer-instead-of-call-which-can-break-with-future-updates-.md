---
# Core Classification
protocol: Sense Update #1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8725
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/58
source_link: none
github_link: https://github.com/sherlock-audit/2023-03-sense-judging/issues/33

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

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
finders_count: 8
finders:
  - Bauer
  - 0x52
  - martin
  - tsvetanovv
  - Breeje
---

## Vulnerability Title

M-4: fillQuote uses transfer instead of call which can break with future updates to gas costs

### Overview


This bug report is about an issue with the `fillQuote()` function in the Sense smart contract. It was found by a group of people - sayan\_, Saeedalipoor01988, 0x52, tsvetanovv, martin, 0xAgro, Bauer, Breeje - who were manually reviewing the code. The problem is that the `fillQuote()` function uses the `transfer()` function instead of the `call()` function, which can cause issues if the gas costs change in the future. This could potentially break any integrations that use the contract. The code snippet can be found at https://github.com/sherlock-audit/2023-03-sense/blob/main/sense-v1/pkg/core/src/Periphery.sol#L902-L932. The recommendation is to use the `call()` function instead of the `transfer()` function, as this will help to prevent any issues with changing gas costs. The discussion concluded that this should be done and the bug report was accepted.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-03-sense-judging/issues/33 

## Found by 
sayan\_, Saeedalipoor01988, 0x52, tsvetanovv, martin, 0xAgro, Bauer, Breeje

## Summary

Transfer will always send ETH with a 2300 gas. This can be problematic for interacting smart contracts if gas cost change because their interaction may abruptly break.

## Vulnerability Detail

See summary.

## Impact

Changing gas costs may break integrations in the future

## Code Snippet

https://github.com/sherlock-audit/2023-03-sense/blob/main/sense-v1/pkg/core/src/Periphery.sol#L902-L932

## Tool used

Manual Review

## Recommendation

Use call instead of transfer. Reentrancy isn't a concern since the contract should only ever contain the callers funds. 

## Discussion

**jparklev**

Accepted: we should use .call instead of transfer when transferring ETH, specifically if the receiver is a contract that is integrating Sense.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Sense Update #1 |
| Report Date | N/A |
| Finders | Bauer, 0x52, martin, tsvetanovv, Breeje, sayan\_, 0xAgro, Saeedalipoor01988 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-03-sense-judging/issues/33
- **Contest**: https://app.sherlock.xyz/audits/contests/58

### Keywords for Search

`vulnerability`

