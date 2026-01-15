---
# Core Classification
protocol: Timeswap
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20277
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-15-Timeswap.md
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

protocol_categories:
  - liquid_staking
  - yield
  - services
  - synthetics
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-3 Wrong ERC1155 metadata URI

### Overview


This bug report is about the incorrect setting of URIs in two tokens, TimeswapV2LiquidityToken and TimeswapV2Token, that implement the ERC1155 metadata extension. As per the ERC1155 specification, the URIs must point to a JSON file that conforms to the "ERC-1155 Metadata URI JSON Schema". This incorrect setting of URIs will affect off-chain integrations with the tokens that will try to read tokens' metadata and fail. The recommended mitigation was to consider correctly setting the URIs in the two tokens or alternatively, to not implement the metadata extension. The team response was that the issue was fixed as suggested in a commit. The mitigation review was that TimeswapV2LiquidityToken and TimeswapV2Token were updated as per the recommendation, setting a metadata URI in their constructors.

### Original Finding Content

**Description:**
TimeswapV2LiquidityToken and TimeswapV2Token implement the ERC1155 metadata
extension, however they incorrectly set the URIs. As per the ERC1155 specification:
The URI MUST point to a JSON file that conformsto the "ERC-1155 Metadata URI JSON
Schema”.
Incorrectly-set URIs will affect off-chain integrations with the tokens that will try to read
tokens’ metadata and fail.

**Recommended Mitigation:**
Consider correctly setting the URIs in TimeswapV2LiquidityToken and TimeswapV2Token.
Alternatively, consider not implementing the metadata extension since it’s optional (this
would require copying the ERC1155 implementation from OpenZeppelin and removing the
metadata extension implementation; also, the IERC1155MetadataURI interface selector
should be removed from supported interfaces).

**Team Response:**
The issue was fixed as is suggested in this commit: commit.(https://github.com/Timeswap-Labs/Timeswap-V2-Monorepo/pull/483/commits/946eb502e3373b6339009121c1ca5f8d57be73ff)

**Mitigation review:**
TimeswapV2LiquidityToken and TimeswapV2Token were updated as per the
recommendation: the contracts set a metadata URI in their constructors.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Timeswap |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-15-Timeswap.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

