---
# Core Classification
protocol: Nft Loots
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20620
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-NFT Loots.md
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
  - Pashov
---

## Vulnerability Title

[M-03] Lootbox input validation should be present

### Overview


This bug report outlines an issue with the `NFTLootbox` contract, which can leave NFTs stuck in the contract forever. The bug is caused by the owner of the `NFTLootbox` not properly validating the `_priceForPlay` and `_duration` values when creating the lootbox. The `_priceForPlay` should have an upper bound, as if it's too big then no one will want to participate and the NFTs will remain stuck in the contract. The `_duration` value should have a lower and an upper bound, as too low of a duration doesn't make sense and too big of a duration can leave NFTs stuck in the contract forever. If the owner fat-fingers the duration and adds one or two digits it can become a big problem. The impact of this bug is high, as it can leave NFTs stuck in the contract forever, however the likelihood of it occurring is low, as it requires a fat-finger or misconfiguration by the `NFTLootbox` owner. The recommendation is to add a lower & upper bound checks for `_duration` and a max value check for `_priceForPlay` in the `createLootbox` method.

### Original Finding Content

**Impact:**
High, as it can leave NFTs stuck in the contract forever

**Likelihood:**
Low, as it requires a fat-finger or misconfiguration by the `NFTLootbox` owner

**Description**

Both the `_priceForPlay` and `_duration` values should be properly validated in `NFTLootbox::createLootbox`. The `_priceToPlay` has to have an upper bound, because if it's too big then no one will want to participate and until the duration passes the NFTs will be stuck in the contract. For the `_duration` value there should be a lower and an upper bound, as too low of a duration doesn't make sense but too big of a duration can leave NFTs stuck in the contract forever. If the owner fat-fingers the duration and adds one or two digits it can become a big problem.

**Recommendations**

Add a lower & upper bound checks for `_duration` and a max value check for `_priceForPlay` in the `createLootbox` method.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nft Loots |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-NFT Loots.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

