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
solodit_id: 40203
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

Missing comment about counterintuitive quote amount in swap

### Overview

See description below for full details.

### Original Finding Content

## MainnetController.sol Function: swapUSDSToUSDC

## Context
MainnetController.sol#L243

## Description
The `MainnetController` includes a function called `swapUSDSToUSDC`, which allows swapping an amount of USDS to USDC. This function takes the USDC amount, which is denominated in 6 decimals, and then normalizes it to 18 decimals (the denomination of USDS). The normalized amount is then used to complete the swap and convert it to USDC.

The issue here is the counterintuitive nature of the parameter. Given the function name `swapUSDSToUSDC`, one would logically expect the parameter to be the USDS amount (denominated in 18 decimals). However, in this case, the parameter is actually the USDC amount. This behavior is also tied to the rate limiter, which uses the USDC amount as a rate-limiting key.

While we understand the design decision behind this approach—specifically to avoid precision loss when converting from 18 decimals to 6 decimals—it may not be immediately apparent to relayers. This could result in confusion and lead them to mistakenly input a USDS amount instead of the expected USDC amount.

## Recommendation
Consider improving the documentation of this behavior, even though the variable is named `usdc` to clearly indicate that a USDC amount is expected. It would be beneficial to highlight this aspect further to ensure that users fully understand the function's requirements, helping to prevent potential errors in the future.

## Additional Information
- **MakerDAO:** Fixed in commit 5ea7f6d2.
- **Cantina Managed:** Verified.

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

