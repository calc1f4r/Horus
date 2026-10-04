---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28127
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#4-there-is-no-recovery-option-for-erc721
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

There is no recovery option for ERC721

### Overview


This bug report is about the `transferToVault()` function not supporting ERC721 tokens. This function is located in the Lido.sol file and can be found at the following link: https://github.com/lidofinance/lido-dao/blob/801d3e854efb33ff33a59fe51187e187047a6be2/contracts/0.4.24/Lido.sol#L356. The recommendation is to add another function to recover ERC721 tokens. This bug report is important to note because ERC721 tokens are a type of digital asset that is used in a variety of applications, such as gaming, digital art, and collectibles. It is important to make sure that the transferToVault() function supports ERC721 tokens in order to ensure that users can safely and securely transfer these digital assets.

### Original Finding Content

##### Description
The `transferToVault()` function doesn't support ERC721 tokens: 
https://github.com/lidofinance/lido-dao/blob/801d3e854efb33ff33a59fe51187e187047a6be2/contracts/0.4.24/Lido.sol#L356
##### Recommendation
It is necessary to add another function to recover ERC721.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Lido%20Protocol/README.md#4-there-is-no-recovery-option-for-erc721
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

