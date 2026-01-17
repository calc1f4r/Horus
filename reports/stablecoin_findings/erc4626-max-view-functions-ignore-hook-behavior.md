---
# Core Classification
protocol: Euler Earn
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41986
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-October-2024.pdf
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
  - M4rio.eth
  - Christoph Michel
---

## Vulnerability Title

ERC4626 max* view functions ignore hook behavior

### Overview

See description below for full details.

### Original Finding Content

## Security Analysis Report

## Severity
**Low Risk**

## Context
`EulerEarnVault.sol#L80-L383`

## Description
The `deposit`, `mint`, `withdraw`, and `redeem` functions all call a hook (if defined) at the beginning which can revert to implement pause states, or user/global limits. However, the corresponding `max*` functions do not take the hook behavior into account. This violates EIP-4626 behavior for these functions:

- **MUST** factor in both global and user-specific limits.
- If deposits are entirely disabled (even temporarily), it **MUST** return `0` for `maxDeposit`.

## Recommendation
As the hook behavior can depend on the exact amount deposited/withdrawn, but the `max*` functions try to figure out the amount in the first place, it's hard to perfectly simulate the hook behavior for every amount state. 

One could consider:
- Calculating the max amount as it is currently done and performing a subsequent hook call simulation with this amount.
  
Alternatively, accept the non-compliance and document that the `max*` functions ignore hook behavior, which can lead to actual deposit/withdrawal reverting because of the hook. Integrators need to be able to handle this case.

## Fix
**Euler:** Fixed in PR 118 by adding comments for the non-compliance.  
**Spearbit:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Euler Earn |
| Report Date | N/A |
| Finders | M4rio.eth, Christoph Michel |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

