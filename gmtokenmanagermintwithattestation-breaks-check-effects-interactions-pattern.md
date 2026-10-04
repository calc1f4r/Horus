---
# Core Classification
protocol: Ondo Global Markets
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62339
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
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
  - Immeas
  - Al-Qa'qa'
---

## Vulnerability Title

`GMTokenManager::mintWithAttestation` breaks Check-Effects-Interactions pattern

### Overview

See description below for full details.

### Original Finding Content

**Description:** In [`GMTokenManager::mintWithAttestation`](https://github.com/ondoprotocol/rwa-internal/blob/a74d03f4a71bd9cac09e8223377b47f7d64ca8d4/contracts/globalMarkets/tokenManager/GMTokenManager.sol#L196-L231), the function transfers tokens from the user before performing internal accounting operations such as rate limiting, burning, and minting. This violates the check-effects-interactions pattern, where external calls (like token transfers) should typically come after all internal state updates to reduce risk.

While the token being transferred is assumed to be a trusted stablecoin, this ordering increases the surface area for unexpected behavior if any integrated token misbehaves (e.g., via callback hooks, pausable logic, or fee-on-transfer behavior).

Consider reordering operations in `mintWithAttestation` to follow the check-effects-interactions pattern—performing rate limiting, burns, and mints **before** calling `token.transferFrom()`.

**Ondo:** Fixed in commit [`29bdeb9`](https://github.com/ondoprotocol/rwa-internal/pull/470/commits/29bdeb92b8de97be3de6a60d78bf91449be90827)

**Cyfrin:** Verified. rate limiting now done before external calls.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Ondo Global Markets |
| Report Date | N/A |
| Finders | Immeas, Al-Qa'qa' |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-14-cyfrin-ondo-global-markets-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

