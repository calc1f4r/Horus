---
# Core Classification
protocol: Hyperdrive June 2023
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35855
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
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
finders_count: 4
finders:
  - Saw-Mon and Natalie
  - Christoph Michel
  - Deivitto
  - M4rio.eth
---

## Vulnerability Title

No LP fees when closing matured longs/shorts

### Overview


This bug report describes an issue with the Hyperdrive and HyperdriveLong smart contracts. When closing matured long positions, the function responsible for closing them does not take a fee on the share proceeds. This means that when traders close their positions, their share proceeds are reduced by the total fee, but the fee is not added back to the share reserves. This also applies to closing short positions. The recommendation is to adjust the code to take the fee when processing the matured bonds and add it back to the reserves, so that LPs and governance can receive their fees without having to wait for traders to close their positions. 

### Original Finding Content

## Severity: High Risk

## Context
- Hyperdrive.sol#L112
- HyperdriveLong.sol#L496

## Description
When closing matured longs through `closeLong` or `checkpoint`, `_applyCheckpoint` is first run, which closes the matured longs/shorts for this checkpoint. This function, however, does not take a fee on the `shareProceeds`. The share (and bond) reserves are updated by `updateLiquidity(-shareProceeds)`, which reduces the share proceeds by the fee-exclusive `shareProceeds`.

When traders now close their positions by calling `closeLong`, their own `shareProceeds` are reduced by the `totalFlatFee`, but this fee is never added back to the share reserves, i.e., never reinvested for the LPs. Note that the same issue also applies to closing shorts.

## Recommendation
Consider taking the flat fee already when processing the matured bonds the first time in `_applyCheckpoint`, adding back the total LP fee (`totalFlatFee - totalGovernanceFee`) to the reserves and increasing the `_governanceFeesAccrued` by `totalGovernanceFee`. (The governance fee is not reinvested in the pool.) The code in `closeLong` needs to be adjusted to not double-count any fees for the matured / non-matured paths. This also means that LPs & governance don't have to wait for LPs to close their positions to receive their fees.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Hyperdrive June 2023 |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Christoph Michel, Deivitto, M4rio.eth |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf

### Keywords for Search

`vulnerability`

