---
# Core Classification
protocol: SeaDrop
chain: everychain
category: uncategorized
vulnerability_type: update_state_after_admin_action

# Attack Vector Details
attack_type: update_state_after_admin_action
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6844
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Seadrop-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Seadrop-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - update_state_after_admin_action

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Sawmon and Natalie
  - Dravee
  - Harikrishnan Mulackal
---

## Vulnerability Title

ERC721SeaDrop 'sadmin would need to set feeBps manually after/before creation of each drop by the owner

### Overview


This bug report is about a problem with the ERC721SeaDrop.sol contract. When an owner creates either a public or token gated drop, the PublicDrop.feeBps/TokenGatedDropStage.feeBps parameter is initially set to 0. This means that the admin would need to set the feeBps parameter before the drop can start. If this is not done, the protocol fees will not be received. 

To mitigate this, the admin can monitor the activities on-chain and call either updatePublicDropFee or updateTokenGatedDropFee to set the feeBps. Alternatively, the admin can enforce that both updatePublicDrop and updatePublicDropFee (or updateTokenGatedDrop and updateTokenGatedDropFee) be called before a drop can start. Finally, the admin can set a flag to waive the protocol fee.

### Original Finding Content

## Severity: Medium Risk

## Context
- `ERC721SeaDrop.sol#L180`
- `ERC721SeaDrop.sol#L256`

## Description
When an owner of an `ERC721SeaDrop` token creates either a public or a token gated drop by calling `updatePublicDrop` or `updateTokenGatedDrop`, the `PublicDrop.feeBps` / `TokenGatedDropStage.feeBps` is initially set to 0. So the admin would need to set the `feeBps` parameter at some point (before or after). Forgetting to set this parameter results in not receiving the protocol fees.

## Recommendation
There are multiple ways to mitigate this:

1. The admin monitors the activities on-chain and if it sees a newly created drop, calls either `updatePublicDropFee` or `updateTokenGatedDropFee` (depending on the type of the drop) to set the `feeBps`.
   
2. Enforcing that both `updatePublicDrop` and `updatePublicDropFee` (or `updateTokenGatedDrop` and `updateTokenGatedDropFee`) be called by the owner and the admin before a drop can start. The enforcement can be either on the `ERC721SeaDrop` side or on the `SeaDrop` side. Also, there could be a flag set by the admin to waive the protocol fee.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | SeaDrop |
| Report Date | N/A |
| Finders | Sawmon and Natalie, Dravee, Harikrishnan Mulackal |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Seadrop-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Seadrop-Spearbit-Security-Review.pdf

### Keywords for Search

`Update State After Admin Action`

