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
solodit_id: 40202
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

More granular limits for CCTP transfers

### Overview

See description below for full details.

### Original Finding Content

## Context
- **MainnetController.sol#L308**
- **ForeignController.sol#L182**

## Description
The controllers have the capability to transfer USDC from the proxy to various chains using the CCTP protocol, with the destination domains specified as parameters when the transfer function is called.

In our view, it would be more effective to implement granular rate limiting per domain rather than applying a global rate limit across all domains. This approach acknowledges that different domains may carry varying risk levels, and a lower limit for riskier domains would provide better security.

Currently, this functionality is not available, leaving open the potential for a relayer to deplete the global limit on just one domain, which could pose unnecessary risks.

## Recommendation
Consider making the rate limiting more granulated to improve the security per domain.

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

