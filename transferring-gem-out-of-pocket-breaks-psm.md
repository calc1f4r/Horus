---
# Core Classification
protocol: MakerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40970
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/53e12fbd-182a-45f9-a115-55fdea33c5c4
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_dss-lite-psm_oct2023.pdf
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
finders_count: 3
finders:
  - m4rio
  - shung
  - Christoph Michel
---

## Vulnerability Title

Transferring gem out of pocket breaks PSM

### Overview

See description below for full details.

### Original Finding Content

## DssPocket Contract Overview

## Context
DssPocket.sol#L97

## Description
All gem ERC20 for the PSM is held in a separate DssPocket contract. Its wards can approve the gem for any spender. If a spender besides the DssLitePsm transfers out gem, the fees accounting in `DssLitePsm.cut()` will not work correctly anymore and fees will be lost. Furthermore, the DssLitePsm debt cannot be cleared naturally anymore as part of the DAI-swapped-to-Gem disappeared.

## Recommendation
Only the DssLitePsm should be hoped to avoid breaking the accounting in DssLitePsm.

## Acknowledgements
- **Maker DAO:** Acknowledged.
- **Cantina Managed:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | m4rio, shung, Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_dss-lite-psm_oct2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/53e12fbd-182a-45f9-a115-55fdea33c5c4

### Keywords for Search

`vulnerability`

