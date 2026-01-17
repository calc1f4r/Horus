---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3687
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/170

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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - 0xRajeev
---

## Vulnerability Title

M-12: Loan duration can exceed the end of the next epoch

### Overview


This bug report is about a vulnerability found in a protocol related to the Astaria platform. The vulnerability is that loan duration can exceed the end of the next epoch, which deviates from the protocol specification. This means that the implementation does not adhere to the spec and could lead to miscalculations and potential fund loss. The code snippet that was used to detect this vulnerability is available in the report. The recommendation is to either implement as per the specification or revisit the specification.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/170 

## Found by 
0xRajeev

## Summary

Loan duration can exceed the end of the next epoch, which deviates from the protocol specification.

## Vulnerability Detail

From the specs: "The duration of new loans is restricted to not exceed the end of the next epoch. For example, if a PublicVault is 15 days into a 30-day epoch, new loans must not be longer than 45 days."

However, there's no enforcement of this requirement. 

## Impact

The implementation does not adhere to the spec: Loan duration can exceed the end of the next epoch, which breaks protocol specification and therefore lead to miscalculations and potential fund loss.


## Code Snippet

1. https://docs.astaria.xyz/docs/protocol-mechanics/epochs
2. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/VaultImplementation.sol#L146-L228

## Tool used

Manual Review

## Recommendation

Implement as per specification or revisit the specification.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | 0xRajeev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/170
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

