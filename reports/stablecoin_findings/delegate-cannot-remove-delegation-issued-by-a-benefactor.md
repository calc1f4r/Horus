---
# Core Classification
protocol: Boundary
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64210
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
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
  - BengalCatBalu
  - Immeas
---

## Vulnerability Title

Delegate cannot remove delegation issued by a benefactor

### Overview

See description below for full details.

### Original Finding Content

**Description:** A delegate cannot remove delegation issued by a benefactor. Once delegation has been accepted by calling the `acceptDelegatedSigner` function, it can only be revoked by the benefactor by calling the `removeDelegatedSigner` function.

This contradicts the documentation, which states in the `05-Mint-and-Redeem` file that both roles can revoke delegation. Thus, this is a lack of functionality for the delegate.

```
Delegated Signing - Both EOA and contract benefactors can delegate signing to an approved EOA. Delegation requires two steps: benefactor calls initiateDelegatedSigner, delegate calls acceptDelegatedSigner. Either party can remove the delegation.
```
**Recommended Mitigation:** Add functionality to remove delegation for delegate

**Boundary:**
Resolved. Documentation corrected in [PR#165](https://github.com/boundary-labs/boundary-protocol-ethereum/pull/165) - contract behavior is correct, benefactors manage their delegates.

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Boundary |
| Report Date | N/A |
| Finders | BengalCatBalu, Immeas |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

