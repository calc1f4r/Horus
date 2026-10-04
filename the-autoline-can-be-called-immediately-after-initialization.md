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
solodit_id: 54441
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ccf91a4a-d29b-40e7-b48e-2669edc06b7e
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_dssallocator_sep2023.pdf
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

The AutoLine can be called immediately after initialization 

### Overview

See description below for full details.

### Original Finding Content

## Audit Overview for AllocatorInit.sol

## Context
`deploy/AllocatorInit.sol`

## Description
Within the scoped commit for the audit, in the `AllocatorInit.sol` setup, the `Line` and `line` for a specific ilk was set to a debt ceiling which could be very high.

```solidity
// Relevant lines
require(cfg.debtCeiling < WAD, "AllocatorInit/incorrect-ilk-line-precision");
dss.vat.file(ilk, "line", cfg.debtCeiling * RAD);
dss.vat.file("Line", dss.vat.Line() + cfg.debtCeiling * RAD);
```

After discussing with the client, the decision was made that they will be using the AutoLine approach, which allows you to increase an ilk debt ceiling gradually according to a specified gap (amount) and ttl (cooldown time). A new commit was provided with the AutoLine configuration.

Within this commit, the initial debt ceiling was set to the gap, and then the AutoLine is configured for the specific ilk. The AutoLine uses a public `exec` function which checks if the ttl was passed and that the maxLine was not reached. If these conditions are met, then the `Line` and `line` will be increased by the gap.

Because the initialization increases the gap directly within the vat:

```solidity
dss.vat.file(ilk, "line", cfg.gap);
dss.vat.file("Line", dss.vat.Line() + cfg.gap);
```

Then, setting the AutoLine is done with:

```solidity
AutoLineLike(dss.chainlog.getAddress("MCD_IAM_AUTO_LINE")).setIlk(ilk, cfg.maxLine, cfg.gap, cfg.ttl);
```

Anyone can call the `exec` immediately and increase the debt ceiling (`line`) one more time. This is due to the fact that the AutoLine considers that when a new ilk is set, the debt ceiling should be increased afterward using the `exec` function for the ttl to take effect.

## Recommendation
Consider setting the AutoLine first, then call the exec to set up the initial debt ceiling for the ilk.

## Maker
So far, this has been the way to set the line initially for all the ilks that have been created since the AutoLine exists. But it is definitely a good point to think about.

## Cantina
Acknowledged.

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

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_dssallocator_sep2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ccf91a4a-d29b-40e7-b48e-2669edc06b7e

### Keywords for Search

`vulnerability`

