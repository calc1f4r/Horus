---
# Core Classification
protocol: Benqi Ignite
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44256
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
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
finders_count: 2
finders:
  - Immeas
  - Giovanni Di Siena
---

## Vulnerability Title

Ignite fee is not returned for pre-validated `QI` stakes in the event of registration failure

### Overview


This bug report is about an issue with the `1 AVAX` Ignite fee that is applied to pre-validated `QI` stakes. If the registration process fails, the fee is not refunded to the user's stake amount, unlike other registration methods. This means that users who register with a hosted Zeeve validator will not get their Ignite fee back if the registration fails. The recommended solution is to refund the Ignite fee if the registration fails. The bug has been fixed by the BENQI team in their latest commit. The fee will now only be taken from successful registrations during the call to `Ignite::releaseLockedTokens`.

### Original Finding Content

**Description:** The `1 AVAX` [Ignite fee](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L387) applied to pre-validated `QI` stakes is [paid to the fee recipient](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L388) at the time of registration. If this registration fails (e.g. due to off-chain BLS proof validation), the registration will be [marked as withdrawable](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L620) once `Ignite::releaseLockedTokens` is called; however, since the fee has already been paid and [deducted from the user's stake amount](https://github.com/Benqi-fi/ignite-contracts/blob/bbca0ddb399225f378c1d774fb70a7486e655eea/src/Ignite.sol#L397), it will not be returned with the refunded `QI` stake. This behavior differs from the other registration methods, which all refund the usually non-refundable fee in the event of registration failure.

**Impact:** Users who register with a hosted Zeeve validator will not be refunded the Ignite fee if registration fails.

**Recommended Mitigation:** Refund the Ignite fee if registration fails for pre-validated `QI` stakes.

**BENQI:** Fixed in commit [f671224](https://github.com/Benqi-fi/ignite-contracts/commit/f67122426c5dff6023da1ec9602c1959703db28e).

**Cyfrin:** Verified. The fee is now taken from successful registrations during the call to `Ignite::releaseLockedTokens`.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Benqi Ignite |
| Report Date | N/A |
| Finders | Immeas, Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

