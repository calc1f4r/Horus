---
# Core Classification
protocol: The Standard Auto Redemption
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45065
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
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
  - Giovanni Di Siena
---

## Vulnerability Title

Additional validation should be performed on the Chainlink Functions response

### Overview

See description below for full details.

### Original Finding Content

**Description:** When consuming a Chainlink Functions response, the following additional validation should be performed within `AutoRedemption::fulfillRequest`:
* Ensure the `_token` address is either a Hypervisor with valid data on the `SmartVaultYieldManager` contract (valid only for non-legacy vaults) or an accepted collateral token.
* Ensure the `_tokenID` has actually been minted such that `SmartVaultManagerV6::vaultData` will return a non-default `SmartVaultData` struct.

**The Standard DAO**
Fixed by commit [8ee0921](https://github.com/the-standard/smart-vault/commit/8ee0921026b5a56c0d441f3e87d5530506b7e445).

**Cyfrin:** Verified. `AutoRedemption::validData` has been added to verify that the vault address is non-zero and the token is a valid collateral token.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | The Standard Auto Redemption |
| Report Date | N/A |
| Finders | Giovanni Di Siena |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

