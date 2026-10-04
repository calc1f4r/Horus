---
# Core Classification
protocol: Dimo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53749
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/dimo/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/dimo/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Removal of ERC20VotesUpgradeableMight Allow Double Voting

### Overview


This bug report discusses a potential vulnerability in the governance functionality of the DIMO token. Due to technical limitations, it was not possible to fully investigate the issue. However, it is concerning that a contract from the token's previous version was removed, potentially allowing for double voting. The report recommends being cautious of this issue and ensuring that the new governance implementation does not allow for double voting. The development team has acknowledged the issue but has stated that it is outside the scope of the audit. The testing team cannot confirm the security of the system and the development team is working on addressing the issue.

### Original Finding Content

## Description

Because it was not possible to run a governance propose/vote test, this vulnerability could not be further investigated. However, it is a concern that OpenZeppelin’s `ERC20VotesUpgradeable` contract was removed between this version of the token and its predecessor. 

To quote OpenZeppelin’s Documentation:

> "This extension will keep track of historical balances so that voting power is retrieved from past snapshots rather than current balance, which is an important protection that prevents double voting."

## Recommendations

Be aware of this issue and ensure that double vote counting is not possible with the protocol’s new governance implementation.

## Resolution

After communication with the development team, it has been determined that the governance functionality of the DIMO token is out of scope of this audit. This feature is in active development and therefore related issues have been closed. As the governance functionality is out of scope, the testing team cannot attest to the security of this system. The testing team acknowledges that the development team is still moving forward based on recommendations provided in this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Dimo |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/dimo/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/dimo/review.pdf

### Keywords for Search

`vulnerability`

