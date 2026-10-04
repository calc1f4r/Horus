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
solodit_id: 21362
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

Gas calculation frequently uses unchecked free variables

### Overview


This bug report is about an issue with unconstrained free variables being used to calculate the word-size cost in certain instances of opCALLDATACOPY, opCODECOPY, opEXTCODCOPY, and saveMemGAS. This issue was present in tag 0.5.2.0 and could lead to memory expansion. The fix for this issue was implemented in Pull Requests #199 and #221 by Polygon-Hermez. Spearbit acknowledged the fix.

### Original Finding Content

## Severity: Critical Risk

## Context
- `zkevm-rom:calldata-returndata-code.zkasm#L73`
- `zkevm-rom:calldata-returndata-code.zkasm#L225`
- `zkevm-rom:calldata-returndata-code.zkasm#L329`
- `zkevm-rom:utils.zkasm#L395`
- etc.

## Description
An example in `opCALLDATACOPY` where unconstrained free variables are used to calculate the word-size cost:

- `GAS - 3 => GAS :JMPN(outOfGas)`
- `GAS - ${3*((C+31)/32)} => GAS :JMPN(outOfGas)` ; Arith

In some places, like `opRETURNDATACOPY`, these are mostly performed using the arithmetic state machine:
- `${3*((C+31)/32)}`
- `C+31 => A`
- `(C+31)/32`
- `A :MSTORE(arithA)`
- `32 :MSTORE(arithB)`
- `:CALL(divARITH)`
- `$ => A :MLOAD(arithRes1)`

Mul operation with Arith:
- `3*((C+31)/32)`
- `3 :MSTORE(arithA)`
- `A :MSTORE(arithB)`
- `:CALL(mulARITH)`
- `$ => A :MLOAD(arithRes1)`
- `GAS - A => GAS :JMPN(outOfGas)`

Under tag 0.5.2.0, a number of instances remain, including:
- `opCALLDATCOPY`
- `opCODECOPY`
- `opEXTCODCOPY`
- The `saveMemGAS` utility affecting memory expansion.

## Polygon-Hermez
All unsafe computations have been fixed in PR #199 and PR #221.

## Spearbit
Acknowledged.

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

