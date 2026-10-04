---
# Core Classification
protocol: Talentir Token & Marketplace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60733
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/talentir-token-marketplace/08aae35f-7537-45ef-ae98-0dc5c0e1abe1/index.html
source_link: https://certificate.quantstamp.com/full/talentir-token-marketplace/08aae35f-7537-45ef-ae98-0dc5c0e1abe1/index.html
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
finders_count: 4
finders:
  - Zeeshan Meghji
  - Julio Aguliar
  - Hytham Farah
  - Roman Rohleder
---

## Vulnerability Title

Approval Not Updated when Changing the Marketplace Address in `TalentirTokenV1`

### Overview


This report discusses a bug in a code that was recently updated. The update introduced a new feature that allows the owner to remove approval of an address for a list of user wallets. However, this also creates a risk of centralization as the owner can revoke approval for any address at any time. The bug affects the `TalentirTokenV1` file and occurs when the marketplace address is changed. Newly minted tokens will have the new marketplace address approved, but previously minted tokens will still have the old marketplace address approved. This means that the old marketplace can still interact with users' tokens, putting them at risk. The recommendation is to add a second blocklist address or remind users to revoke old permissions.

### Original Finding Content

**Update**
In PR-41, the team added functionality that allows the `owner` to remove approval of an address for a list of user wallets. This functionality adds some centralization risk, as the owner is free to revoke approval of any address for any user, but solves the issue.

**File(s) affected:**`TalentirTokenV1`

**Description:** When the marketplace address is changed in `TalentirTokenV1.setMarketplace()` only newly minted tokens will have it approved for all, while previously minted tokens will still have the old marketplace address approved for all. This would lead the tokens to be at risk of token owners of previously minted tokens until they manually revoke/update the approval via `setApprovalForall()`.

**Recommendation:** Consider adding a second blocklist address that would block all outdated marketplaces from interacting with users' ERC-1155 tokens, or at the very least, ensure that users are reminded to revoke old permissions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Talentir Token & Marketplace |
| Report Date | N/A |
| Finders | Zeeshan Meghji, Julio Aguliar, Hytham Farah, Roman Rohleder |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/talentir-token-marketplace/08aae35f-7537-45ef-ae98-0dc5c0e1abe1/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/talentir-token-marketplace/08aae35f-7537-45ef-ae98-0dc5c0e1abe1/index.html

### Keywords for Search

`vulnerability`

