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
solodit_id: 40490
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/0ab48a3e-6978-44e4-a6a7-67de330c70c0
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_may2024.pdf
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

The debt ceiling can be increased immediately after initialization

### Overview

See description below for full details.

### Original Finding Content

## LockstakeInit Script Overview

## Context
`LockstakeInit.sol#L170-L177`

## Description
Within the `LockstakeInit` script, the debt ceiling has to be set to the gap:

```solidity
dss.vat.file(cfg.ilk, "line", cfg.gap);
```

Then the `AutoLine` is configured for the ilk:

```solidity
AutoLineLike(dss.chainlog.getAddress("MCD_IAM_AUTO_LINE")).setIlk(cfg.ilk, cfg.maxLine, cfg.gap, cfg.ttl);
```

The `AutoLine` uses a public `exec` function which checks if the `ttl` was passed and that the `maxLine` was not reached. If these conditions are met, then the `Line` and `line` will be increased with the gap. 

Anyone can call the `exec` immediately and increase the debt ceiling (`line`) one more time because the `AutoLine` considers that when a new ilk is set, the debt ceiling should be increased afterward using the `exec` function so the `ttl` can enter into effect.

## Recommendation
Consider setting the `AutoLine` first, then call the `exec` to set the initial debt ceiling for the ilk in the vat.

**Maker's Decision**: We decided to accept this trade-off and keep consistency with the other init scripts.

**Cantina Managed**: Acknowledged.

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

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/0ab48a3e-6978-44e4-a6a7-67de330c70c0

### Keywords for Search

`vulnerability`

