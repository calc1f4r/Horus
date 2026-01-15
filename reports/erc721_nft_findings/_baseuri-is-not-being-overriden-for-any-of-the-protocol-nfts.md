---
# Core Classification
protocol: Collar Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46574
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/5d300ba8-b59a-4b83-a436-56077b2fa4e9
source_link: https://cdn.cantina.xyz/reports/cantina_solo_collar_october2024.pdf
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
  - kankodu
---

## Vulnerability Title

_baseURI Is Not Being Overriden for Any of the Protocol NFTs 

### Overview


The bug report discusses an issue with the BaseNFT.sol code, specifically with the tokenURI(uint256) method. This method is used by NFT marketplaces to retrieve metadata associated with each NFT. However, since the protocol does not override this method or the _baseURI() method, NFT marketplaces are forced to display a default image instead of the correct metadata. To fix this, the report recommends overriding the _baseURI() method to return a URL pointing to the correct metadata for each NFT. Alternatively, the approach of other protocols like UniswapV3 and SablierV2 could be followed, where an SVG is returned directly from the Solidity code. This SVG does not need to be complex and could simply display a static text like "Collar Position". The bug has been fixed in the latest commit. 

### Original Finding Content

## NFT TokenURI Issue and Recommendations

## Context
BaseNFT.sol#L16

## Description
An added advantage of representing positions as NFTs is that users can sell their NFTs to exit their positions before expiry. All NFT marketplaces call the `tokenURI(uint256)` method to retrieve the metadata associated with each NFT. Since the protocol is not overriding 

- `function tokenURI(uint256 tokenId) returns (string memory)`
- `function _baseURI() returns (string memory)`

the NFT marketplace will be forced to display a default image, which isn't ideal.

## Recommendation
To improve this, consider overriding `function _baseURI() returns (string memory)` to return a URI pointing to your URL, such as [https://nftinfo.collarprotocol.xyz/](https://nftinfo.collarprotocol.xyz/), and ensure it returns the correct metadata for each NFT. Alternatively, you could follow the approach of UniswapV3 or SablierV2 and return an SVG directly from the Solidity code. The SVG doesn’t need to be as complex or dynamic as UniswapV3’s; even a simple, static text like "Collar Position" would be preferable to showing nothing.

## Fixes
- **Collar:** Fixed in commit 91a2c55f.
- **Kankodu:** Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Collar Protocol |
| Report Date | N/A |
| Finders | kankodu |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_solo_collar_october2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5d300ba8-b59a-4b83-a436-56077b2fa4e9

### Keywords for Search

`vulnerability`

