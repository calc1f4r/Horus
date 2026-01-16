---
# Core Classification
protocol: Pontem (Liquidswap)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48640
audit_firm: OtterSec
contest_link: https://pontem.network/
source_link: https://pontem.network/
github_link: github.com/pontem-network/pontem-network- liquidswap

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
finders_count: 3
finders:
  - OtterSec
  - Robert Chen
  - Fineas Silaghi
---

## Vulnerability Title

Unstrict Swap Invariant

### Overview


The program has a bug where it reports an incorrect swap when dealing with an uncorrelated curve. This happens when the lp_value after the swap is smaller than the lp_value before the swap. The swap should only be valid if the value after is greater than the value before. This bug could potentially exploit rounding errors and cause imprecision. The fix for this bug involves changing the assert condition to strictly greater. This bug has been resolved in a recent commit.

### Original Finding Content

## Handling Errors in Uncorrelated Curves

When dealing with an uncorrelated curve, the program introduced an error by reporting an incorrect swap if the `lp_value` after the swap is strictly smaller than the `lp_value` before the swap. The swap should be valid only when the value after is greater than the value before. Otherwise, swapping would be able to exploit potential rounding errors, depending on the precision of the relevant curves.

Some napkin math implies that the imprecision is non-trivial. For a token with 8 decimals, the stable swap math would give up to 1,000,000 atomic units of imprecision. This would represent up to 1% of the original token’s value.

```plaintext
sources/swap/liquidity_pool.move
assert!(
    lp_value_after_swap_and_fee >= lp_value_before_swap,
    ERR_INCORRECT_SWAP,
);
```

## Remediation

The incorrect assert can be fixed by making the condition strictly greater.

```plaintext
sources/libs/stable_curve.move
+ let cmp = u256::compare(&lp_value_after_swap_and_fee, &lp_value_before_swap_u256);
+ assert!(cmp == GREATER_THAN, ERR_INCORRECT_SWAP);
```

## Patch

Resolved in commit 637ad72.

© 2022 OtterSec LLC. All Rights Reserved. 8 / 17

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Pontem (Liquidswap) |
| Report Date | N/A |
| Finders | OtterSec, Robert Chen, Fineas Silaghi |

### Source Links

- **Source**: https://pontem.network/
- **GitHub**: github.com/pontem-network/pontem-network- liquidswap
- **Contest**: https://pontem.network/

### Keywords for Search

`vulnerability`

