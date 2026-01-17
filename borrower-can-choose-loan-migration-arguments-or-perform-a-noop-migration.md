---
# Core Classification
protocol: Maple Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54788
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/8ff1bbc8-5f91-4d10-9eea-cc9f88b82e62
source_link: https://cdn.cantina.xyz/reports/cantina_maple_apr2023.pdf
github_link: none

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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Christoph Michel
  - Riley Holterhus
  - Jonatas Martins
---

## Vulnerability Title

Borrower can choose Loan migration arguments or perform a noop migration 

### Overview


The MapleLoan upgrade function has a bug where borrowers can choose migration arguments that benefit them, or even skip the migration code altogether. This can be fixed by removing the option for borrowers to choose arguments and instead hardcoding them in the migrator contract. Alternatively, access to the upgrade function can be restricted to only the security admin. This bug has been fixed in the Maple and Cantina platforms.

### Original Finding Content

## MapleLoan Upgrade Function

## Context
- **Fixed-term loan**: MapleLoan
- **Open-term loan**: MapleLoan

## Description
The `MapleLoan.upgrade(uint256 toVersion_, bytes calldata arguments_)` function can be called by the borrower (and the security admin). The borrower can choose migration arguments for future migrations that are in their favor, such as increasing principal or decreasing interest rates. 

The borrower can also skip running the migration code but still upgrade to the latest loan version by encoding arguments that would not call the fallback function on the migrator. For example, for the old `MapleLoanV4Migrator`, they could have chosen arguments that call `encodeArguments(0)`, skipping the migration code in the fallback (the proxy would still point to the new implementation code).

## Recommendation
There is an incentive for the borrower to choose migration arguments in their favor or "deny" a migration by encoding a different function than the fallback. For better control, consider removing arguments as a parameter for MapleLoans and always call `IMapleProxyFactory(_factory()).upgradeInstance(toVersion_, "")` without arguments. The arguments should be hardcoded in the migrator contract. Alternatively, consider restricting upgrade access to only the security admin.

## Fixes
- **Maple**: Fixed in PR-61 (open-term loan) and PR-291 (fixed-term loan) by restricting upgrades to only the security admin.
- **Cantina**: Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Maple Finance |
| Report Date | N/A |
| Finders | Christoph Michel, Riley Holterhus, Jonatas Martins |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_maple_apr2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/8ff1bbc8-5f91-4d10-9eea-cc9f88b82e62

### Keywords for Search

`vulnerability`

