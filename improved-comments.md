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
solodit_id: 40205
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6e9c7968-9565-4b05-a8f2-f41ddc64ec27
source_link: https://cdn.cantina.xyz/reports/cantina_makerdao_alm_sept2024.pdf
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
finders_count: 2
finders:
  - m4rio
  - Jonatas Martins
---

## Vulnerability Title

Improved comments

### Overview

See description below for full details.

### Original Finding Content

## Context
See below

## Description
Throughout the code we could notice various comments that could be improved:

- **MainnetController.sol#L260**: `Approve DAI to PSM from the proxy (assumes the proxy has enough DAI)` could be `Approve DAI to PSM from the proxy because the daiUsds.usdsToDai always returns the usdsAmount`.
  
- **IRateLimits.sol#L106**: `@dev Sets rate limit data for a specific key` could be `@dev Sets rate limit data for a specific key with lastAmount == maxAmount and lastUpdated == block.timestamp to specify what happens with the last amount and last updated params`.
  
- **IRateLimits.sol**: The `IRateLimits` uses only `@dev` NatSpecs while the `IALMProxy` uses `@dev` and `@notice`, consider standardizing the NatSpec format.
  
- **IRateLimits.sol#L152**: Should specify that this function does not revert if `maxAmount` is reached.
  
- **MainnetController.sol#L284**: `// Swap USDC to DAI through the PSM` should be `// Swap USDC to DAI through the PSM 1:1`.

## Recommendation
Consider fixing the above comments.

## MakerDAO
Fixed in commit `5ea7f6d2`.

## Cantina Managed
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MakerDAO |
| Report Date | N/A |
| Finders | m4rio, Jonatas Martins |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_makerdao_alm_sept2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6e9c7968-9565-4b05-a8f2-f41ddc64ec27

### Keywords for Search

`vulnerability`

