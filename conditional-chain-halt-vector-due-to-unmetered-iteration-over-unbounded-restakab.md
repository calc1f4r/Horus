---
# Core Classification
protocol: MilkyWay
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46098
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/5e314c79-7894-4e92-9513-79a9b09b08b0
source_link: https://cdn.cantina.xyz/reports/report_cantina_solo_milkyway_january2025.pdf
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
  - alpo
---

## Vulnerability Title

Conditional chain halt vector due to unmetered iteration over unbounded restakable asset under default params 

### Overview


A bug has been found in the allocation.go file, specifically in lines 231-240. This bug allows for a chain halt vector to be exploited by creating delegations with long lists of spam token denoms. However, the likelihood of this happening is low since the system has moved away from default parameters and set a list of restakable denoms. It is still important to address this bug as it could potentially cause a permissionless chain halt in the future. The recommended solution is to either cap the number of denoms per delegation or add an additional gas cost for delegations with a large number of denoms. This bug has been fixed in PR 27 and has been verified by Alpo. The risk associated with this bug is low.

### Original Finding Content

## Vulnerability Report

## Context
`allocation.go#L231-L240`

## Description
In the case where no denoms are allowed as restakable, allowed denom checks are skipped and all denoms are restakable. Due to linear iteration over reward denoms when calculating operator rewards, these circumstances expose a chain halt vector that can be exploited by creating delegations with long lists of spam token denoms.

## Likelihood
While this bug would be exploitable under default params, the current system has moved off of them and set a list of restakable denoms, so likelihood has been marked as **Low**. It is still important this is addressed, as the moment there is a reset back to default params (or the list of allowed restakable denoms is reset), a permissionless chain halt will be exposed.

## Recommendation
Similar to other related issues around linear iteration over delegation denoms, there are two options for fixing this:

1. Cap the number of denoms per delegation (recommended).
2. If a cap of >3 (or no cap at all) is an important product priority, add an additional gas cost to delegations that scales linearly with the number of denoms.

## MilkyWay
Fixed in PR 27.

## Alpo
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | MilkyWay |
| Report Date | N/A |
| Finders | alpo |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/report_cantina_solo_milkyway_january2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/5e314c79-7894-4e92-9513-79a9b09b08b0

### Keywords for Search

`vulnerability`

