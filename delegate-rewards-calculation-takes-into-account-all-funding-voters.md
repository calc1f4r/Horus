---
# Core Classification
protocol: Ajna Finance (Governance)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60605
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ajna-finance-governance/9ef9afc2-a7ab-42d3-bfbb-a2f6695c4cac/index.html
source_link: https://certificate.quantstamp.com/full/ajna-finance-governance/9ef9afc2-a7ab-42d3-bfbb-a2f6695c4cac/index.html
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
finders_count: 4
finders:
  - Guillermo Escobero
  - Nikita Belenkov
  - Rabib Islam
  - Jonathan Mevs
---

## Vulnerability Title

Delegate Rewards Calculation Takes Into Account All Funding Voters

### Overview


This bug report discusses an issue with the `StandardFunction.sol` file in a project. The function `_getDelegateReward()` is used to calculate rewards for users who have voted in both screening and funding rounds. However, if a user has not voted in the screening round, the function will not work and the rewards will be distributed incorrectly. This could lead to some users receiving rewards that they are not entitled to. The report recommends that the protocol should be updated to account for users who have not voted in the screening round.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `28de025759692d479252df537c2a861fa495ec0e`.

**File(s) affected:**`StandardFunction.sol`

**Description:** Delegate rewards are given when a user with delegated votes has voted in both screening and funding rounds.`_getDelegateReward()` function calculates the number of rewards the user should receive. It uses the following function:

rewards=TotalFundsAvailable∗UserUsedVotingPowerTotalCastedFundingVotes∗0.1 \begin{array}{ll} rewards = \dfrac{{TotalFundsAvailable * UserUsedVotingPower}}{TotalCastedFundingVotes} * 0.1 \end{array}

This logic works correctly if it is assumed that everyone has also voted in the screening round, which is not necessarily the case. If the user has not voted in the screening round, the function would revert. Hence the rewards are distributed amongst all users that have participated and have not participated in the screening round in the current logic, and some reward amounts will not be accessible to anyone.

**Exploit Scenario:**

1.   Ten users have voted in the funding round, but only two of them have voted in both funding and screening periods.
2.   The rewards will be calculated based on the sum of funding votes of all of the ten users, not just the eligible two users.

**Recommendation:** The protocol should account for users that have not voted in the screening round and hence should not be entitled to the rewards.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ajna Finance (Governance) |
| Report Date | N/A |
| Finders | Guillermo Escobero, Nikita Belenkov, Rabib Islam, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ajna-finance-governance/9ef9afc2-a7ab-42d3-bfbb-a2f6695c4cac/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ajna-finance-governance/9ef9afc2-a7ab-42d3-bfbb-a2f6695c4cac/index.html

### Keywords for Search

`vulnerability`

