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
solodit_id: 19324
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/dimo/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/dimo/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Voting Process Reverts

### Overview


A bug was found in the Dimo token in DimoV2.sol, where the removal of OpenZeppelin's ERC20VotesUpgradeable contract caused it to be impossible to propose a governance vote. Calling DimoGovernance.propose() caused the call to token.getPastVotes(account, blockNumber) to revert. The recommendation was to modify DimoV2 to reimplement OpenZeppelin's ERC20VotesUpgradeable. After communication with the development team, it was determined that the governance functionality of the DIMO token was out of scope of this audit, and the testing team could not attest to the security of this system. The development team is still moving forward based on the recommendations provided. Additionally, a function signature collision was found that created inaccessible codeblocks.

### Original Finding Content

## Description
Because of the removal of OpenZeppelin’s `ERC20VotesUpgradeable` contract from the Dimo token in `DimoV2.sol`, it is not possible to propose a governance vote. Calls to `DimoGovernance.propose()` revert because `propose()` calls `token.getPastVotes(account, blockNumber)`.

## Recommendations
Modify `DimoV2` to reimplement OpenZeppelin’s `ERC20VotesUpgradeable`.

## Resolution
After communication with the development team, it has been determined that the governance functionality of the DIMO token is out of scope of this audit. This feature is in active development and therefore related issues have been closed. As the governance functionality is out of scope, the testing team cannot attest to the security of this system. The testing team acknowledges that the development team is still moving forward based on recommendations provided in this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

