---
# Core Classification
protocol: Reality Cards
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42232
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-06-realitycards
source_link: https://code4rena.com/reports/2021-06-realitycards
github_link: https://github.com/code-423n4/2021-06-realitycards-findings/issues/160

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
  - cdp
  - cross_chain
  - synthetics
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-12] `RCNftHubL2.safeTransferFrom` not according to spec

### Overview


The `RCNftHubL2.safeTransferFrom` function in the ERC721 token contract is not properly checking if the receiver is an `IERC721Receiver`, which is required by the ERC721 spec. This means that contracts that do not know how to handle ERC721 tokens can still accept them, which goes against the spec. The reporter recommends implementing the `IERC721Receiver` check in `safeTransferFrom`. The bug has been confirmed and resolved by the project team.

### Original Finding Content

_Submitted by [cmichel](https://twitter.com/cmichelio), also found by [0xRajeev](https://twitter.com/0xRajeev)_

The `RCNftHubL2.safeTransferFrom` function does not correctly implement the ERC721 spec:
> When using `safeTransferFrom`, the token contract checks to see that the receiver is an IERC721Receiver, which implies that it knows how to handle ERC721 tokens. [ERC721](https://docs.openzeppelin.com/contracts/2.x/api/token/erc721#IERC721-safeTransferFrom)

This check is not implemented, it just drops the `_data` argument.

Contracts that don't know how to handle ERC721 tokens (are not an `IERC721Receiver`) can accept them but they should not when using `safeTransferFrom` according to spec.

Recommend Implementing the `IERC721Receiver` check in `safeTransferFrom`.

**[Splidge (Reality Cards) confirmed and resolved](https://github.com/code-423n4/2021-06-realitycards-findings/issues/160#issuecomment-865141409):**
 > This has been fixed while working on issue #118
> commit [here](https://github.com/RealityCards/RealityCards-Contracts/commit/a628ac8e0132f7ca4159980f791ae820100c0888)



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Reality Cards |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-06-realitycards
- **GitHub**: https://github.com/code-423n4/2021-06-realitycards-findings/issues/160
- **Contest**: https://code4rena.com/reports/2021-06-realitycards

### Keywords for Search

`vulnerability`

