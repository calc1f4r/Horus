---
# Core Classification
protocol: 1inch Fixed Rate Swap Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10665
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/1inch-fixed-rate-swap-audit/
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
  - dexes
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L08] Unsafe explicit casting of integers

### Overview

See description below for full details.

### Original Finding Content

The [`Swap`](https://github.com/1inch/fixed-rate-swap/blob/b1600f61b77b6051388e6fb2cb0be776c5bcf2d1/contracts/FixedRateSwap.sol#L22) event takes an `address` and two `int256` parameters and it is emitted in the [`swap0To1`](https://github.com/1inch/fixed-rate-swap/blob/b1600f61b77b6051388e6fb2cb0be776c5bcf2d1/contracts/FixedRateSwap.sol#L228), [`swap1To0`](https://github.com/1inch/fixed-rate-swap/blob/b1600f61b77b6051388e6fb2cb0be776c5bcf2d1/contracts/FixedRateSwap.sol#L238), [`swap0To1For`](https://github.com/1inch/fixed-rate-swap/blob/b1600f61b77b6051388e6fb2cb0be776c5bcf2d1/contracts/FixedRateSwap.sol#L249), and [`swap1To0For`](https://github.com/1inch/fixed-rate-swap/blob/b1600f61b77b6051388e6fb2cb0be776c5bcf2d1/contracts/FixedRateSwap.sol#L263) functions.


During emission, however, the integer values being passed to the event are explicitly cast from `uint256` to `int256` values.


Although unlikely to be problematic in practice today, ecosystems developments such as unbounded flash loans of stablecoin assets could cause this design to exhibit undesirable behaviors in the future. On a given large enough `uint256` value, explicitly casting into an `int256` type would truncate its value. As a result, off-chain systems, dependent on the accuracy of the event emission, could be misled.


Consider redefining the `Swap` event to deal directly with `uint256` values so that the functions that emit the event can forego the explicit casts.


***Update:** Fixed in [commit `8436c6c`](https://github.com/1inch/fixed-rate-swap/commit/8436c6c4f3a54c9a79d8311f6fcaf72de9f8d4c9). 1inch team [imported the OpenZeppelin’s `SafeCast` library](https://github.com/1inch/fixed-rate-swap/blob/8436c6c4f3a54c9a79d8311f6fcaf72de9f8d4c9/contracts/FixedRateSwap.sol#L6) to safely cast the mentioned cases.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | 1inch Fixed Rate Swap Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/1inch-fixed-rate-swap-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

