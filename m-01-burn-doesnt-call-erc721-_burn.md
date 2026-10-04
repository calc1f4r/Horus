---
# Core Classification
protocol: Timeswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25638
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-timeswap
source_link: https://code4rena.com/reports/2022-01-timeswap
github_link: https://github.com/code-423n4/2022-01-timeswap-findings/issues/111

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
  - liquid_staking
  - yield
  - services
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-01] `burn()` doesn't call ERC721 `_burn()`

### Overview


This bug report is about the `burn()` function in the CollateralizedDebt.sol contract, which is an ERC721 token. The `burn()` function should reverse the actions of the `mint()` function by burning the ERC721 token, but the `_burn()` function is never called. This means a user can continue to hold their ERC721 token representing their position after receiving their funds, unlike the `burn()` functions found in other Timeswap Convenience contracts. To fix this bug, the `burn()` function should include the line `_burn(id);`. The bug has been acknowledged by Mathepreneur (Timeswap).

### Original Finding Content

_Submitted by sirhashalot_

The CollateralizedDebt.sol contract is a ERC721 token. It has a `mint()` function, which uses the underlying `safeMint()` function to create an ERC721 token representing a collateral position. The `burn()` function in CollateralizedDebt.sol should reverse the actions of `mint()` by burning the ERC721 token, but the ERC721 `_burn()` function is never called. This means a user can continue to hold their ERC721 token representing their position after receiving their funds. This is unlike the `burn()` function found in Bond.sol, Insurance.sol, and Liquidity.sol, which all call the `_burn()` function (though note the `_burn()` function in these other Timeswap Convenience contracts is the ERC20 `_burn()`).

#### Proof of Concept

The problematic `burn()` function is found in CollareralizedDebt.sol
<https://github.com/code-423n4/2022-01-timeswap/blob/bf50d2a8bb93a5571f35f96bd74af54d9c92a210/Timeswap/Timeswap-V1-Convenience/contracts/CollateralizedDebt.sol#L80-L88>

Compare this function to the `burn()` functions defined in the other Timeswap Convenience contracts, which contain calls to `_burn()`

#### Recommended Mitigation Steps

Include the following line in the `burn()` function
`_burn(id);`

**[Mathepreneur (Timeswap) acknowledged](https://github.com/code-423n4/2022-01-timeswap-findings/issues/111):**
 > If decided not to burn the ERC721 token at all. The burn in this context is burning the debt and collateral locked balance in the ERC721 token.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Timeswap |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-timeswap
- **GitHub**: https://github.com/code-423n4/2022-01-timeswap-findings/issues/111
- **Contest**: https://code4rena.com/reports/2022-01-timeswap

### Keywords for Search

`vulnerability`

