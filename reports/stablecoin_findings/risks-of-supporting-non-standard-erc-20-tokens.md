---
# Core Classification
protocol: Ethena UStb token and minting
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59103
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethena-u-stb-token-and-minting/6cec4ac4-03e0-4949-ac0a-51d9c925d45a/index.html
source_link: https://certificate.quantstamp.com/full/ethena-u-stb-token-and-minting/6cec4ac4-03e0-4949-ac0a-51d9c925d45a/index.html
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
finders_count: 3
finders:
  - Roman Rohleder
  - Valerian Callens
  - Rabib Islam
---

## Vulnerability Title

Risks of Supporting Non-Standard ERC-20 Tokens

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> planned supported tokens don’t have these features - won’t fix

**File(s) affected:**`UStbMinting.sol`

**Description:** Supporting tokens with specific features such as fees, rebasing, pausable, upgradeable, blacklist-able, or hooks on transfers could negatively impact the main flows of the system (deposits via `mint()`, transfer to custody, redeems via `redeem()`) if no specific mitigation measure is enforced to limit the consequences. For instance, in the function `_transferCollateral()` if `asset` represents an asset where the amount transferred is different than the amount requested to be transferred (ex: if fees are enforced), the actual amount transferred to custodians may differ from the expected transferred amount.

**Recommendation:** Consider analyzing thoroughly from a security perspective any token you would like to be supported.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethena UStb token and minting |
| Report Date | N/A |
| Finders | Roman Rohleder, Valerian Callens, Rabib Islam |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethena-u-stb-token-and-minting/6cec4ac4-03e0-4949-ac0a-51d9c925d45a/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethena-u-stb-token-and-minting/6cec4ac4-03e0-4949-ac0a-51d9c925d45a/index.html

### Keywords for Search

`vulnerability`

