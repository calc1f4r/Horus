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
solodit_id: 19591
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/sushi/auction-maker-furo/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/sushi/auction-maker-furo/review.pdf
github_link: none

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

Non-standard ERC20 Tokens Are Not Supported And Locked in the Contract

### Overview


This bug report is about non-ERC20 compliant tokens not being supported by a contract. Specifically, when the transfer() function does not correctly implement the IERC20 interface, an error is thrown when trying to call the end() function for a related auction. This is because the call to IERC20(token).transfer() does not return the expected value, and the tokens cannot be reclaimed. To resolve this issue, the development team has implemented the OpenZeppelin’s SafeERC20 library. This library is a vetted library used to handle non-standard ERC20 contracts, and it allows these tokens to be supported.

### Original Finding Content

## Description

Non-ERC20 compliant tokens might not be supported by the contract. Specifically, this is true when the `transfer()` function does not correctly implement to the `IERC20` interface. One prominent example for such tokens is the stablecoin USDT.

When trying to call `end()` for a related auction, the transaction reverts. This is because the call to `IERC20(token).transfer()` does not match the expected return value of `transfer()` on the target contract. In the case of USDT, the function does not return any value which causes an execution error as it attempts to decode a `bool`. There is no other way to reclaim these tokens, so they would be locked in the contract.

## Recommendations

Appropriate handling of non-standard ERC20 contracts is necessary if these tokens are to be supported. A common way to handle this is by using a vetted library such as OpenZeppelin’s SafeERC20.

## Resolution

The development team has addressed this issue in PR 1 by using the OpenZeppelin’s SafeERC20 library.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Sushi |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/sushi/auction-maker-furo/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/sushi/auction-maker-furo/review.pdf

### Keywords for Search

`vulnerability`

