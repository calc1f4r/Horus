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
solodit_id: 21365
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

Test failures in VMTests/vmPerformance/loopExp (potential issue in EXP)

### Overview


This bug report outlines a critical risk issue with the zkevm-testvectors Ethereum tests from VMTests/vmPerformance/loopExp.json. The error is that the program terminates with registers A, D, E, SR, CTX, PC, MAXMEM, and zkPC not set to zero. The failing tests can be found in the internal repository and are modified versions of Ethereum tests with lowered transaction gas limit and number of loop iterations. It is difficult to diagnose the exact cause since the testing infrastructure does not save trace log files in the case of such an error. The recommendation is to ensure these tests can be executed and verify that EXP behaves correctly. The issue has been fixed in PR #211 and improved zk-counters check in PR #212.

### Original Finding Content

## Severity: Critical Risk

**Context:** zkevm-testvectors

**Description:** Some Ethereum tests from `VMTests/vmPerformance/loopExp.json` are failing with the following error:

**Input:** `/0xPolygonHermez/zkevm-testvectors/tools/ethereum-tests/eth-inputs/GeneralStateTests/VMTests/loopExp_1.json`

**Start executor JS...**

**Error:**
```
Error: Program terminated with registers A, D, E, SR, CTX, PC, MAXMEM, zkPC not set to zero
```

**The list of failing tests:**
- loopExp_1
- loopExp_2
- loopExp_3

Tests can be found in our internal repository. They are modified versions of Ethereum tests with lowered transaction gas limit and number of loop iterations decreased to fit into the 30M gas limit.

It is hard to diagnose the exact reason since testing infrastructure does not save the trace log file (see *Trace log is not saved in case of "register not set to zero" error*) in case of such error (unlike in the case of *newStateRoot does not match error*).

We think this may signal a bug in the implementation of EXP.

**Recommendation:** Ensure these tests can be executed and verify that EXP behaves correctly.

**Polygon-Hermez:** Fixed in PR #211 and improved zk-counters check in PR #212.

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

