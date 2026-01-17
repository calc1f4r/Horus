---
# Core Classification
protocol: Remora Final
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64222
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-17-cyfrin-remora-final-v2.0.md
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
finders_count: 1
finders:
  - 0xStalin
---

## Vulnerability Title

Users can reset the status of their `firstPurchase` on the `referralData` when the `stablecoin` doesn't revert on transfers to `address(0)`

### Overview

See description below for full details.

### Original Finding Content

**Description:** Users can create a referral to get a discount by calling [`ReferralManager::createReferral`](https://github.com/remora-projects/remora-dynamic-tokens/blob/final-audit-prep/contracts/CoreContracts/ReferralManager/ReferralManager.sol#L129-L145). The user receives a discount, and the referrer gets a bonus when the user makes their first purchase.

The system intends to give users a discount only once, but there is an edge case when the stablecoin allows transfer to address(0). This allows calling `ReferralManager::createReferral` and setting the `referrer` as `address(0)`. This effectively bypasses the check to validate if the user has already set a referrer and proceeds to set their `referralData.isFirstPurchase` as true, granting the discount to the user on the next purchase. This allows users to:
1. Call `ReferralManager::createReferral` setting `referrer` as address(0)
2. Purchase a token
3. Call `ReferralManager::createReferral` again setting `referrer` as address(0)

**Impact:** Users can game the referral system to receive a discount on all their purchases by resetting the `firstPurchase` status to true.

**Recommended Mitigation:** When creating the referral, validate that the `referrer` address is not the address(0).
Alternatively, acknowledge this issue and make sure the signers never generate a signature for the `referrer` set as address(0).

**Remora:** Fixed in commit [20eddec](https://github.com/remora-projects/remora-dynamic-tokens/commit/20eddec6e760c7c9bd3669c250e50e562312dfff)

**Cyfrin:** Verified.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Remora Final |
| Report Date | N/A |
| Finders | 0xStalin |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-11-17-cyfrin-remora-final-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

