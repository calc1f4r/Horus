---
# Core Classification
protocol: Rocketpool
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19442
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/rocket-pool/rocket-pool-4-feedistributor-fix/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/rocket-pool/rocket-pool-4-feedistributor-fix/review.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Unsafe Arithmetic and Casting

### Overview

See description below for full details.

### Original Finding Content

## Description

The `RocketHotfixNodeFee` contract’s `execute()` function contains unsafe arithmetic and type conversions that do not perform bounds checking. For valid values used in practice, this should never overflow and cause problems. However, it remains an advisable practice to use bounds-checked arithmetic and type conversions except in very unusual circumstances. It also avoids potentially complicated edge cases when verifying off-chain that the errors are correct and non-malicious.

The identified issue occurs at line [64] (below):

```solidity
63 uint256 currentValue = getUint(key);
uint256 newValue = uint256(int256(currentValue) + error.amount);
64 setUint(key, newValue);
```

Because Solidity 0.7.6 uses unchecked arithmetic, large input values can cause the result of `+` to overflow, meaning the result of summing two positive values may be less than the input. Similarly, the `int256()` conversion may return a negative result for large `currentValue` input. This could theoretically cause confusing scenarios where a positive `error.amount` leads to an effective subtraction.

## Recommendations

The testing team recommends replacing the unsafe `int256` and `uint256` casts, as well as the unchecked `+` operator. While this could be done via the OpenZeppelin SafeMath library, it can be more simply replaced by making use of the existing `addUint` and `subUint` functions exposed by the `RocketStorage` contract. This also has the added gas-saving benefit of halving the number of external contract calls per iteration.

Such a fix could look like the following (note that `error.amount` is a signed `int256`):

```solidity
if (error.amount < 0) {
    subUint(key, uint256(-error.amount));
} else {
    addUint(key, uint256(error.amount));
}
```

> The Minipool nodeFee is denominated as a portion of 1 ether, so it should always be less than 10^18. As the `node.average.fee.numerator` stores the sum of all an operator’s Minipool fees, a valid value with potential to cause overflow problems would require the operator to have in the realm of at least 10^58 Minipools!

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Rocketpool |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/rocket-pool/rocket-pool-4-feedistributor-fix/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/rocket-pool/rocket-pool-4-feedistributor-fix/review.pdf

### Keywords for Search

`vulnerability`

