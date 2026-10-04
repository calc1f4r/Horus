---
# Core Classification
protocol: Quadrata Lending
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61657
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/quadrata-lending/a3d2d9c8-6ebd-4c3e-a146-501cecf3e98c/index.html
source_link: https://certificate.quantstamp.com/full/quadrata-lending/a3d2d9c8-6ebd-4c3e-a146-501cecf3e98c/index.html
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

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Roman Rohleder
  - Ibrahim Abouzied
  - Cristiano Silva
---

## Vulnerability Title

Burnt Passports And Increased AML Scores May Lead To Locked Funds

### Overview


This bug report discusses an issue with the `CToken.sol` file, which affects users who have had their passport burnt. This prevents them from taking any actions on their `CToken`s or accumulated debt. This is due to a call to `getHighestAMLScore()` which requires a passport, and the inability to access `reader.getAttributesFree()`. As a result, users are unable to redeem their `CToken`s or have their collateral liquidated. The report also mentions that borrowers who fall below their collateral requirements cannot be liquidated if their AML score increases after borrowing funds. The recommendation is for the team to make design decisions to address this issue, such as storing a mapping of addresses to a DID or creating a method for seizing funds of locked tokens.

### Original Finding Content

**Update**
From dev team:

> Users should not be able to interact with the lending contracts if they do not meet the minimum criteria (i.e. having a passport + AML above a specific risk score). Similar to how funds are frozen in TradFi for any regulatory red flags, this is a business decision to deal with bad actors in DeFi. Those risks will be explicitly mentioned to the user ahead of any actions (deposits, borrows, etc..).

**File(s) affected:**`CToken.sol`

**Description:** If a user has their passport burnt, no actions can be taken on their `CToken`s or any accumulated debt. This is because `getHighestAMLScore()` makes a call to `reader.getAttributesFree()`, which requires the user to have a passport. Not only will `CToken`'s be locked with the user being unable to call `redeem()`, but their collateral cannot be liquidated either, as `repayBorrowFresh()` requires a passport for both the `borrower` and the `payer`.

Additionally, a borrower below their collateral requirements cannot be liquidated if their AML score becomes greater than 8 after they've already borrowed funds.

**Recommendation:** Addressing this issue will require some design decisions by the team. Burning a passport does not delete the AML score mapping in `_attributesByDID[]`. A new design might allow for storing a mapping of addresses to a DID so that an AML score can be retrieved for users who've burnt their passports. Alternatively, a method can be made for seizing funds of locked tokens and adding them to the reserve.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Quadrata Lending |
| Report Date | N/A |
| Finders | Roman Rohleder, Ibrahim Abouzied, Cristiano Silva |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/quadrata-lending/a3d2d9c8-6ebd-4c3e-a146-501cecf3e98c/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/quadrata-lending/a3d2d9c8-6ebd-4c3e-a146-501cecf3e98c/index.html

### Keywords for Search

`vulnerability`

