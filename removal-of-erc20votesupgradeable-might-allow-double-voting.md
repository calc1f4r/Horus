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
solodit_id: 19322
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

Removal of ERC20VotesUpgradeable Might Allow Double Voting

### Overview


This bug report is about the removal of OpenZeppelin’s ERC20VotesUpgradeable contract from the DIMO token. This contract is responsible for keeping track of historical balances so that voting power is retrieved from past snapshots instead of current balance, which is an important protection against double voting. After communication with the development team, it was determined that the governance functionality of the DIMO token is out of scope of this audit. However, the testing team cannot attest to the security of this system as the feature is in active development. The testing team also acknowledges that the development team is still moving forward based on the recommendations provided in this issue. The bug report also mentions a conflict caused by the mint() function across bridges. It is recommended to be aware of this issue and ensure that double vote counting is not possible with the protocol’s new governance implementation.

### Original Finding Content

Description
Because it was not possible to run a governance propose/vote test, this vulnerability could not be further investigated,
however it is a concern that OpenZeppelin’s ERC20VotesUpgradeable contract was removed between this version of
the token and its predecessor.
To quote OpenZeppelin’s Documentation:
"This extension will keep track of historical balances so that voting power is retrieved from past snapshots rather
than current balance, which is an important protection that prevents double voting."
Recommendations
Be aware of this issue and ensure that double vote counting is not possible with the protocol’s new governance imple-
mentation.
Resolution
After communication with the development team, it has been determined that the governance functionality of the
DIMO token is out of scope of this audit. This feature is in active development and therefore related issues have been
closed. As the governance functionality is out of scope, the testing team cannot attest to the security of this system.
The testing team acknowledges that the development team is still moving forward based on recommendations provided
in this issue.
Page | 6
Dimo Smart Contracts Detailed Findings
DMO-02 Token mint() Produces Conflicts Across Bridges

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

