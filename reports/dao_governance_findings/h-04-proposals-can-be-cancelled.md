---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3907
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-04-vader
github_link: https://github.com/code-423n4/2021-04-vader-findings/issues/227

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
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-04] Proposals can be cancelled

### Overview


This bug report is about a vulnerability in the DAO governance system that allows anyone to cancel any proposals by calling `DAO.cancelProposal(id, id)` with `oldProposalID == newProposalID`. This vulnerability could be used to launch a denial of service attack on the DAO governance, preventing any proposals from being executed. The recommended mitigation step is to check `oldProposalID == newProposalID`.

### Original Finding Content

Anyone can cancel any proposals by calling `DAO.cancelProposal(id, id)` with `oldProposalID == newProposalID`.
This always passes the minority check as the proposal was approved.

An attacker can launch a denial of service attack on the DAO governance and prevent any proposals from being executed.

Recommend checking that `oldProposalID` == `newProposalID`

**[strictly-scarce (vader) confirmed](https://github.com/code-423n4/2021-04-vader-findings/issues/227#issuecomment-828455719):**
 > This is valid, can fix with a `require()`


**[strictly-scarce (vader) commented](https://github.com/code-423n4/2021-04-vader-findings/issues/227#issuecomment-830634810):**




### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-vader
- **GitHub**: https://github.com/code-423n4/2021-04-vader-findings/issues/227
- **Contest**: https://code4rena.com/contests/2021-04-vader-protocol-contest

### Keywords for Search

`vulnerability`

