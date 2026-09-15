---
# Core Classification
protocol: Sushi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19623
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

sgReceive Could Send Native Tokens to a Contract

### Overview


The development team identified an issue with the call by Stargate tosgReceive() which could result in tokens being left in the SushiXSwap contract on the destination chain, allowing any user to transfer them away freely. This could happen if the user puts a contract with no receive or fallback function as the toaddress on line 83, and line 98 would cause the entire transaction to revert. Another related situation would be if the receiving contract had a receive or fallback function that uses too much gas. 

The recommendation is to use addr.call{value: x}("") in place of transfer on line 98. This pattern is more generous with gas and also does not revert on failure, making it better suited for this section of code.

### Original Finding Content

## Description

The development team pointed out that, if the call by Stargate to `sgReceive()` were to revert, the tokens transferred from Stargate would be left in the SushiXSwap contract on the destination chain, where they could be transferred away freely by any user.

One possible condition under which this transaction could revert is if the user puts a contract with no receive or fallback function as the `to` address on line [83]. In this situation, if any native token balance is present in the SushiXSwap contract, then line [98] would cause the entire transaction to revert.

A related situation would be if the receiving contract had a receive or fallback function that uses too much gas, perhaps because of a change in gas fees on the destination chain, and so the transfer call would revert.

## Recommendations

Use `addr.call{value: x}("")` in place of `transfer` on line [98]. This pattern is more generous with gas and also does not revert on failure, which are both properties in line with what this section of code wishes to achieve.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/sushi/sushi-swap-stable-pool/review.pdf

### Keywords for Search

`vulnerability`

