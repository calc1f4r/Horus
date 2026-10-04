---
# Core Classification
protocol: Polygon zkEVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21367
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-1-Spearbit-27-March.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-1-Spearbit-27-March.pdf
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

# Audit Details
report_date: unknown
finders_count: 8
finders:
  - Thibaut Schaeffer
  - Alex Beregszaszi
  - Lucas Vella
  - Miguel Palhas
  - Paweł Bylica
---

## Vulnerability Title

Insufﬁcient check about division remainder

### Overview


This bug report describes a critical issue with the divARITH subroutine in the zkevm-rom:utils.zkasm code. The subroutine uses the arithmetic state machine to perform division, and the equation used is A * B + C = D * 2**256 + E, where all the variables are 256-bit unsigned numbers. The subroutine performs two checks before invoking the state machine, division by zero (A == 0) and E < A. If either of these conditions are met, the subroutine directly returns (0, 0) or (0, E) respectively. However, the comment in line 501 states that a check for remainder < divisor is performed after invoking the state machine, but the code actually performs a different check. This means a malicious prover can forge invalid division and modulo operations. The issue was fixed in PR #205, and acknowledged by Spearbit.

### Original Finding Content

## Critical Risk Report

## Severity
**Critical Risk**

## Context
`zkevm-rom:utils.zkasm#L501`

## Description
The `divARITH` subroutine uses the arithmetic state machine to perform division. The equation used is:

```
A * B + C = D * 2**256 + E
```

All of those variables are 256-bit unsigned numbers, but the equation is an equation on integers. The subroutine computes `E / A` and `E % A` at the same time (both `E` and `A` are inputs to the subroutine and are assigned like that to the variables of the state machine).

The subroutine performs two checks before it invokes the state machine. Those are:
- Division by zero (`A == 0`), it directly returns `(0, 0)`
- `E < A`: In this case, it directly returns `(0, E)`

Then it invokes the state machine, setting:

- `D = 0`
- `B = ${E/A}` (free input)
- `C = ${E%A}` (free input)

Choosing these free inputs makes the state machine succeed. The problem is that the remainder `${E%A}` is only a proper remainder if it is less than `A`. If we, for example, invoke the state machine with `B = ${E/A - 1}` and `C = ${(E%A) + A}`, this will also satisfy the equation (as long as `E/A >= 1` and we don’t get an arithmetic overflow).

In line 501, a comment states that this check "remainder < divisor" is performed after invoking the state machine, but the code actually performs a different check: It invokes the LT state machine on `C` and `E` and thus compares `C < E` instead of `C < A`. This means a malicious prover can forge invalid division and modulo operations.

Note that due to the check against `E < A` before invoking the state machine, we only invoke the state machine in the case that `A <= E` and thus the invalid check `C < E` is never stricter than the correct check `C < A`, which resulted in this not being discovered in tests.

## Recommendation
Change the code after line 501 from:

- `C => A` ; remainder
- `E => B` ; divisor

to:

- `A => B` ; divisor
- `C => A` ; remainder

## Additional Information
**Polygon-Hermez**: Fixed in PR #205.  
**Spearbit**: Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Polygon zkEVM |
| Report Date | N/A |
| Finders | Thibaut Schaeffer, Alex Beregszaszi, Lucas Vella, Miguel Palhas, Paweł Bylica, Christian Reitwiessner, Andrei Maiboroda, Leo Alt |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-1-Spearbit-27-March.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/PolygonzkEVM-Protocol/zkEVM-engagement-1-Spearbit-27-March.pdf

### Keywords for Search

`vulnerability`

