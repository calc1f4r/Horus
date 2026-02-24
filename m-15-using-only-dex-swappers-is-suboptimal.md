---
# Core Classification
protocol: Tapiocadao
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31453
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-15] Using only DEX swappers is suboptimal

### Overview


This bug report discusses a problem with the Tapioca codebases that can have a medium impact and medium likelihood of occurring. The issue is that when swapping tokens, the current setup only uses three different DEXs (UniV2, UniV3, and Curve DeFi pools), which may not be ideal for maximizing the amount received in the exchange. The recommendation is to add at least one aggregator, such as 1inch or 0x, to the list of swappers to improve rates for swaps.

### Original Finding Content

**Severity**

Impact: Medium, swaps without aggregator might have a high price impact for large amounts.

Likelihood: Medium. Depending on how much amount it is being swapped this can be a frequent problem.

**Description**

Currently, most of the actions that need tokens to be swapped across Tapioca's codebases use the swappers, which currently, they are 3.

Each swapper uses a different DEX, UniV2, Univ3 and Curve DeFi pools. This is not the ideal scenario for most cases as when you are swapping you are trying to maximize the amountOut that you get in exchange for the tokens you swapped. To accomplish this and get better rates for your swaps, at least one aggregator should be added to the list of swappers.

**Recommendations**

Add at least one aggregator to the list of swappers. 1inch is my preferred one, but you could also go with 0x.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tapiocadao |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov Audit Group/2024-01-22-TapiocaDAO.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

