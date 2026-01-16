---
# Core Classification
protocol: Curve DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17782
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf
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
  - Gustavo Grieco
  - Josselin Feist
  - Michael Colburn
---

## Vulnerability Title

Aragon’s voting does not follow voting best practices

### Overview


This bug report is related to data validation for LiquidityGauge.vy. It is classified as a medium difficulty bug. The issue is that the voting contract has no mitigation for quick vote and withdraw, no incentive to vote earlier and no mitigation for spam attacks. This means that an attacker with vote creation rights can create hundreds of thousands of votes and only one vote needs to pass for them to succeed. The short-term recommendation is to either improve Aragon's voting to mitigate the issues or implement a new voting contract and perform a security assessment on it before deployment. The long-term recommendation is to properly document and test the voting process and follow the community's progress regarding on-chain voting.

### Original Finding Content

## Data Validation

## Target: LiquidityGauge.vy

### Difficulty: Medium

### Description
Curve Dao uses Aragon for voting. Its voting logic is simple, but does not prevent several abuses that can occur with on-chain voting. 

In particular, the voting contract has the following issues:
- No mitigation for quick vote and withdraw (similar to issue TOB-CURVE-DAO-004).
- No incentive to vote earlier (similar to issue TOB-CURVE-DAO-017).
- No mitigation for spam attacks. An attacker with vote creation rights can create hundreds of thousands of votes, and will need only one to pass to succeed.

### Exploit Scenario
Eve is a miner. She creates new votes to set a new minter on ERC20CRV on every block. The other users cannot vote on all the votes. As a result, one vote is accepted, and Eve takes control of ERC20CRV’s minting.

### Recommendation
Blockchain-based online voting is a known challenge. No perfect solution has been found so far. 

Short term, consider either:
- Improving Aragon’s voting to mitigate the listed issues, or
- Implementing a voting contract to replace Aragon's. Perform a security assessment on the contract before deployment.

Long term, properly document and test the voting process. Closely follow the community’s progress regarding on-chain voting.

### References
- Security Disclosure: Aragon 0.6 Voting ("Voting v1")
- Aragon vote shows the perils of on-chain governance

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Curve DAO |
| Report Date | N/A |
| Finders | Gustavo Grieco, Josselin Feist, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/CurveDAO.pdf

### Keywords for Search

`vulnerability`

