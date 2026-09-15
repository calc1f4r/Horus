---
# Core Classification
protocol: Behodler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1377
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-01-behodler-contest
source_link: https://code4rena.com/reports/2022-01-behodler
github_link: https://github.com/code-423n4/2022-01-behodler-findings/issues/106

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

protocol_categories:
  - cross_chain
  - services
  - cdp
  - dexes
  - liquid_staking

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - camden
  - kirk-baird
---

## Vulnerability Title

[M-12] You can flip governance decisions without extending vote duration

### Overview


This bug report is about a vulnerability in a voting system that allows a user to flip the decision without triggering the logic to extend the vote duration. The user can send one vote in one transaction to go to 0, then in a subsequent transaction send enough to flip the vote. The recommended mitigation step is to make sure that going to 0 is equivalent to a flip, but going away from 0 isn't a flip. This will prevent the user from flipping the decision without triggering the logic to extend the vote duration.

### Original Finding Content

_Submitted by camden, also found by kirk-baird_

The impact here is that a user can, right at the end of the voting period, flip the decision without triggering the logic to extend the vote duration. The user doesn't even have to be very sophisticated: they can just send one vote in one transaction to go to 0, then in a subsequent transaction send enough to flip the vote.

#### Proof of Concept

<https://github.com/code-423n4/2022-01-behodler/blob/608cec2e297867e4d954a63fecd720e80c1d5ae8/contracts/DAO/LimboDAO.sol#L281>
You can send exactly enough fate to send the fate amount to 0, then send fate to change the vote. You'll never trigger this logic.

On the first call, to send the currentProposalState.fate to 0, `(fate + currentFate) * fate == 0`, so we won't extend the proposal state.

Then, on the second call, to actually change the vote, `fate * currentFate == 0` because `currentFate` is 0.

#### Recommended Mitigation Steps

Make sure that going to 0 is equivalent to a flip, but going away from 0 isn't a flip.

**[gititGoro (Behodler) confirmed and commented](https://github.com/code-423n4/2022-01-behodler-findings/issues/106#issuecomment-1027529133):**
 > Changing the logic to include this edge case can get a little convoluted. One thing I thought of is to change the condition to 
> currentFate*fate<0 && currrentFate*currentFate>fate*fate but then moving from 0 to positive won't flip the vote.
> What about requiring the square of your vote to not equal the currentFate and reverting if not? In other words, your vote needs to either have no flipping impact or clearly be intended to flip, not just to cancel out all other votes.

**[gititGoro (Behodler) commented](https://github.com/code-423n4/2022-01-behodler-findings/issues/106#issuecomment-1036954286):**
 > After some consideration, I'm going to implement the square of votes != currentVote rule as a tie makes no sense in the context of whether to execute. 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Behodler |
| Report Date | N/A |
| Finders | camden, kirk-baird |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-behodler
- **GitHub**: https://github.com/code-423n4/2022-01-behodler-findings/issues/106
- **Contest**: https://code4rena.com/contests/2022-01-behodler-contest

### Keywords for Search

`vulnerability`

