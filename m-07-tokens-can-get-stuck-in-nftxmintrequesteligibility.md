---
# Core Classification
protocol: NFTX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42186
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-05-nftx
source_link: https://code4rena.com/reports/2021-05-nftx
github_link: https://github.com/code-423n4/2021-05-nftx-findings/issues/59

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
  - dexes
  - cross_chain
  - rwa
  - leveraged_farming
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-07] Tokens can get stuck in `NFTXMintRequestEligibility`

### Overview


The bug report discusses an issue with ERC721 tokens, specifically with the `amounts` array being ignored. This can cause problems when calling the `NFTXMintRequestEligibility.requestMint` function, as the `ERC721.transferFrom` function is still executed even if `amounts[i]` is set to 0. This means that the user cannot reclaim the requested mint later and the token becomes stuck. Additionally, subscribers to the `Request` event can be tricked by specifying `amounts[i] > 1` in the ERC721 case, even though only one token was transferred. The report recommends checking `amounts[i] == 1` for ERC721 tokens and `amounts[i] > 0` for 1155 tokens in the `requestMint` function to avoid these issues. 

### Original Finding Content


When dealing with ERC721 (instead of 1155) the amounts array is ignored, which leads to an issue.

User can call `NFTXMintRequestEligibility.requestMint` for an ERC721 with `amounts[i] = 0`.
The `ERC721.transferFrom` is still executed but user cannot `reclaimRequestedMint` later and the NFT is stuck as it checks (`amounts[i] > 0`).


Tokens can get stuck.
Also, subscribers to `Request` event could be tricked by specifying `amounts[i] > 1` in the ERC721 case, as only one token was transferred, but the amount multiple quantities get logged.

Recommend that `requestMint`: Check `amounts[i] == 1` in ERC721 case, `amounts[i] > 0` in 1155 case.

**- [0xKiwi (NFTX) confirmed](https://github.com/code-423n4/2021-05-nftx-findings/issues/59)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | NFTX |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-nftx
- **GitHub**: https://github.com/code-423n4/2021-05-nftx-findings/issues/59
- **Contest**: https://code4rena.com/reports/2021-05-nftx

### Keywords for Search

`vulnerability`

