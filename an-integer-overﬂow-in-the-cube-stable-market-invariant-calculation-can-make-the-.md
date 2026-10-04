---
# Core Classification
protocol: FIVA Yield Tokenization Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57090
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-FIVA-yieldtokenizationprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-FIVA-yieldtokenizationprotocol-securityreview.pdf
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

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Tarun Bansal
  - Quan Nguyen
  - Nicolas Donboly
  - Coriolan Pinhas
---

## Vulnerability Title

An integer overﬂow in the cube stable market invariant calculation can make the AMM unusable for swaps

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: Low

## Type: Data Validation

## Description

The cube stable market AMM’s invariant calculation can overﬂow when performing cube operations on large token supplies, exceeding TON's integer limits. The overﬂow will result in users losing their funds in an attempt to swap any tokens from the pool. This market AMM uses an invariant function that performs cube operations on token supplies, creating a signiﬁcant risk of integer overﬂow. The invariant function is shown in figure 10.1:

```c
(int) invariant() inline {
    int res = math::cube(storage::total_supply_sy * storage::sy_pt_price / DIVIDER)
        * storage::total_supply_pt +
        (storage::total_supply_sy * storage::sy_pt_price / DIVIDER) *
        math::cube(storage::total_supply_pt);
    return res;
}
```

**Figure 10.1:** Invariant calculation for cube stable market (contracts/AMM/markets/cube_stable/math.fc#11–15)

This formula involves raising token supplies to the power of 3 and multiplying large numbers together, which can easily exceed the 256-bit integer capacity used in TON. This overﬂow will result in transaction failures.

In TON, integers have a maximum value of 2^256 - 1. If both SY and PT tokens have similar supplies and assuming `sy_pt_price ≈ DIVIDER`, the invariant formula can be simpliﬁed to the following:

```
token_amount^3 * token_amount + token_amount * token_amount^3
2 * token_amount^4 < 2^256
token_amount < 10^19
```

**Figure 10.2:** Max token supply calculation

For tokens with nine decimals, `real_world_amount < 10^10`, meaning if 10 billion SY and PT tokens are provided to the pool, an overﬂow can occur on the invariant calculation. Since the SY and PT tokens will always have nine decimals, the impact is limited to the case where the supply reaches 10 billion tokens. Users can withdraw their liquidity to bring the token supply below the 10 billion limit to make the pool swaps usable again.

## Exploit Scenario

Eve, an attacker, adds a calculated amount of liquidity that pushes the pool’s total supply close to 10 billion. When Alice, a victim, attempts to swap PT to SY tokens, she sends her PT tokens to the pool. The invariant calculation in the pool contract overﬂows and traps Alice’s PT tokens in the pool contract. Alice has already sent PT tokens but has not received SY tokens; she has lost her PT tokens.

## Recommendations

- **Short term:** Document this limitation and deploy a system to monitor pool reserves reaching the 10^10 limit. Such a system will help prevent fund loss to users.

- **Long term:** Conduct a thorough analysis of all mathematical overﬂows possible in the codebase. Based on the analysis results, implement overﬂow protection for identified critical paths, implement transaction revert handling, and update documentation with any additional discovered limitations.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | FIVA Yield Tokenization Protocol |
| Report Date | N/A |
| Finders | Tarun Bansal, Quan Nguyen, Nicolas Donboly, Coriolan Pinhas |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-FIVA-yieldtokenizationprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2025-05-FIVA-yieldtokenizationprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

