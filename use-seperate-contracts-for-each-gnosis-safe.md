---
# Core Classification
protocol: Parcel
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54853
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/78a11a56-9b3d-4584-9c0c-b67194c5238a
source_link: https://cdn.cantina.xyz/reports/cantina_parcel_feb2023.pdf
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
finders_count: 3
finders:
  - Christos Pap
  - Krum Pashov
  - Gerard Persoon
---

## Vulnerability Title

Use seperate contracts for each gnosis safe 

### Overview


The bug report discusses an issue with the Storage.sol file, specifically with the Organizer/PayrollManager contract. When multiple DAOs use the same contract, it becomes difficult to separate the token flows. This can lead to confusion for recipients who work for different DAOs and could potentially be flagged on chain explorers as a bad actor. To avoid this, the report recommends using a proxy pattern to deploy separate contracts for each Gnosis safe. This will simplify the code and make it easier to rescue stuck funds. The issue has been solved in a pull request and verified by Cantina Security. 

### Original Finding Content

## Context
**File:** Storage.sol#L34

## Description
When several DAOs use the same contract for Organizer/PayrollManager, it is difficult to separate the token flows. For a recipient who works for different DAOs, it is hard to see from which DAO the tokens originated.

If a bad actor is also using the contract, tokens may appear to originate from that bad actor, which could result in being flagged on chain explorers. The combining of token flows resembles a token mixer like Tornado Cash. If the USDC/USDT of Organizer/PayrollManager were to be blacklisted, then all safes would encounter issues.

If there are any vulnerabilities in the contract (see other issues), funds could be mixed from different safes. This should be avoided if feasible. Additionally, potential users of the Parcel Payments protocol will be more inclined to use the product if funds are guaranteed to be separated.

Furthermore, having separate contracts for each safe will simplify the code:
- Onboarding after offboarding can be implemented in a straightforward way.
- The mapping for safes is no longer necessary, saving gas by not having to access it.
- The `executePayroll()` function doesn't have to query the initial balances; it can just return any remaining balance.
- It is far easier to rescue stuck funds (see the issue "ETH and tokens can get stuck").
- This will also help with the issue of "Address restrictions in AllowanceModule".

## Recommendation
Use a proxy pattern to deploy separate contracts for each Gnosis safe.

## Note
Attention point: there will be multiple instances of the Organizer/PayrollManager contract, each with its own `executePayroll()` function and its own `nonReentrant` modifier. Thus, reentrancy between multiple instances would be possible. However, because everything else is separated, this doesn’t introduce further risks as far as we can see.

## Parcel
Solved in PR 39.

## Cantina Security
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Parcel |
| Report Date | N/A |
| Finders | Christos Pap, Krum Pashov, Gerard Persoon |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_parcel_feb2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/78a11a56-9b3d-4584-9c0c-b67194c5238a

### Keywords for Search

`vulnerability`

