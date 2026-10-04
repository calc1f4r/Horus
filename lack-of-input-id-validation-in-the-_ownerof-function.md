---
# Core Classification
protocol: Land and Tunnel Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33024
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/land-and-tunnel-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Lack of input id validation in the _ownerOf function

### Overview


The `_ownerOf` function in both Ethereum and Polygon implementations does not check if the input token ID corresponds to a 1x1 quad. This allows for tokens with larger quad sizes to be used, causing issues with external functions such as `burn`, `approve`, and `approveFor`. To fix this, additional checks need to be added to ensure only valid token IDs are processed. This issue has been resolved in a recent pull request.

### Original Finding Content

The `_ownerOf` function in both [Ethereum](https://github.com/thesandboxgame/sandbox-smart-contracts/blob/8430ea5fdb0f4905b9678689ce0cbc2f74a704b6/src/solc_0.5/Land/erc721/LandBaseTokenV3.sol#L656) and [Polygon](https://github.com/thesandboxgame/sandbox-smart-contracts/blob/8430ea5fdb0f4905b9678689ce0cbc2f74a704b6/src/solc_0.8/polygon/child/land/PolygonLandBaseTokenV2.sol#L729) implementations does not validate that the input `id` corresponds to a quad of size 1x1. This allows token ids that correspond to quads of size greater than 1 to be passed. External functions such as `burn`, `approve` and `approveFor` do not expect IDs for quads of such size, leading to unexpected consequences. For example, if a quad with a size greater than 1 were to be burnt, it would lead to the incorrect amount being decremented from `_numNFTPerAddress`.


Consider validating that the input ID corresponds to a single token. This can be done by adding additional checks to the function to ensure that only valid token IDs are processed.


***Update:** Resolved in [pull request #921](https://github.com/thesandboxgame/sandbox-smart-contracts/pull/921) at commit [97da7fb](https://github.com/thesandboxgame/sandbox-smart-contracts/pull/921/commits/97da7fb98e11c900f77ebac8c3b5459979441372).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Land and Tunnel Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/land-and-tunnel-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

