---
# Core Classification
protocol: Emojicoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53231
audit_firm: OtterSec
contest_link: https://x.com/EconiaLabs
source_link: https://x.com/EconiaLabs
github_link: https://github.com/econia-labs/emojicoin-dot-fun

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Robert Chen
---

## Vulnerability Title

Frontrunning Matched Funds for Unfair Gains

### Overview


The report discusses a potential issue with the allocation of matched funds in the emojicoin arena module. This issue can arise due to the way matched amounts are distributed. An attacker can exploit this by creating multiple pools with small amounts, increasing their chances of being selected during the crank scheduling. They can then manipulate the price of their own token and buy into the pool to capture the matched funds. To prevent this, it is recommended to limit the number of pools a single address can create.

### Original Finding Content

## Potential for Frontrunning in Matching Funds

There is potential for frontrunning when matching funds are allocated. This issue arises due to the way matched amounts are distributed. The emojicoin arena module features a mechanism where users may lock in a portion of their contribution to receive matched funds from the vault. 

An attacker may create a large number of pools with small amounts, increasing the likelihood that one of their pools is chosen during the crank scheduling. Before the crank selects a melee, the attacker may buy a large amount of their own token, driving up its price, inflating its value relative to other tokens in the pool. Consequently, if their pool is selected, they may then buy into the pool and swap out their tokens to capture the matched funds.

## Remediation

- Limit the number of pools a single address may create to prevent spamming the crank with attacker’s pools.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Emojicoin |
| Report Date | N/A |
| Finders | Robert Chen |

### Source Links

- **Source**: https://x.com/EconiaLabs
- **GitHub**: https://github.com/econia-labs/emojicoin-dot-fun
- **Contest**: https://x.com/EconiaLabs

### Keywords for Search

`vulnerability`

