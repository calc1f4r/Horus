---
# Core Classification
protocol: Reserve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57080
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-08-reserve-protocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-08-reserve-protocol-securityreview.pdf
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
  - liquid_staking
  - cdp
  - yield
  - launchpad
  - privacy

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Felipe Manzano
  - Anish Naik
---

## Vulnerability Title

Inconsistent use of the FixLib library

### Overview

See description below for full details.

### Original Finding Content

## Description

According to the protocol specification for arithmetic operations, all computations performed on `uint192` values, which represent `uint192x18` variables, should use the **FixLib** library. However, numerous computations in the codebase do not comply with the guidance in the specification.

The protocol specification has the following general guidelines on using the **FixLib** library for `uint192` values:

- Never allow a `uint192` to be implicitly upcast to a `uint256` without a comment explaining what is happening and why.
- Never explicitly cast between `uint192` and `uint256` values without doing the appropriate numeric conversion (e.g., `toUint()` or `toFix()`).
- Use standard arithmetic operations on `uint192` values only if you are gas-optimizing a hotspot in p1 and need to remove **FixLib** calls (and leave inline comments explaining what you are doing and why).

The codebase does not consistently follow these guidelines. Figure 15.1 shows an instance in which a `uint256` is downcast to a `uint192` without an explicit comment.

```solidity
// ==== Compute and accept collateral ====
// D18{BU} = D18{BU} * {qRTok} / {qRTok}
uint192 amtBaskets = uint192(
    totalSupply() > 0 ? mulDiv256(basketsNeeded, amtRToken, totalSupply()) :
    amtRToken
);
```

**Figure 15.1:** Part of the issue function in `RToken.sol#L127-131`

In the code in figure 15.2, standard arithmetic operations are performed on `uint192` values, but there are no inline comments indicating whether the operations are meant to optimize gas.

```solidity
// ==== Compute and accept collateral ====
// Paying out the ratio r, N times, equals paying out the ratio (1 - (1-r)^N) 1 time.
// Apply payout to RSR backing
uint192 payoutRatio = FIX_ONE - FixLib.powu(FIX_ONE - rewardRatio, numPeriods);
```

**Figure 15.2:** Part of the `_payoutRewards` function in `StRSR.sol#L334-336`

Failure to use the **FixLib** library for operations on `uint192` values and to comply with the protocol specification can lead to undefined system behavior.

## Recommendations

**Short term:** Update all parts of the codebase that are not compliant with the protocol specification and include additional comments explaining any deviations from the specification.

**Long term:** Use differential testing to determine whether the use of standard arithmetic operations on `uint192` values introduces any edge cases that would not be an issue if the **FixLib** library were used instead.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Reserve |
| Report Date | N/A |
| Finders | Felipe Manzano, Anish Naik |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-08-reserve-protocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-08-reserve-protocol-securityreview.pdf

### Keywords for Search

`vulnerability`

