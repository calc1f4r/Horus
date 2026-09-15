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
solodit_id: 3908
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-04-vader
github_link: https://github.com/code-423n4/2021-04-vader-findings/issues/187

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

[H-05] Flash loans can affect governance voting in DAO.sol

### Overview


This bug report is about a vulnerability in DAO governance which can be exploited by flash loans. Flash loans allow a single voter to increase their voting weight significantly and influence the voting outcome to their choice. This has already been seen in the MakerDAO governance. The proof of concept is a link to a GitHub code and the recommended mitigation steps are to account for flash loans in countMemberVotes() by using weight from previous blocks or consider capping the weight of individual voters.

Flash loans are a serious vulnerability that can be used to manipulate the voting outcome in DAO governance. Flash loans allow a single voter to borrow a large amount of tokens in order to increase their voting weight and influence the voting outcome. This has already been observed in the MakerDAO governance and is a serious concern.

In order to mitigate this vulnerability, the code should be changed to account for flash loans in countMemberVotes() by using weight from previous blocks or consider capping the weight of individual voters. This will help to ensure that the voting outcome is not manipulated by a single voter.

### Original Finding Content


Flash loans can significantly increase a single voter's weight and be used to impact the voting outcome. A voter can borrow a significant quantity of tokens to increase their voting weight in a transaction within which, they also deterministically  influence the voting outcome to their choice.

This has already happened in the case of MakerDAO governance where [a flash loan was used to affect voting outcome](https://forum.makerdao.com/t/urgent-flash-loans-and-securing-the-maker-protocol/4901) and noted by the Maker team as: “a practical example for the community that flash loans can and may impact system governance”

Given that flash loans are a noted concern, the impact of it to DAO governance which can control all critical protocol parameters should be mitigated as in other places.

Recommend accounting for flash loans in `countMemberVotes()` by using weight from previous blocks or consider capping the weight of individual voters. ([L158-L163](https://github.com/code-423n4/2021-04-vader/blob/3041f20c920821b89d01f652867d5207d18c8703/vader-protocol/contracts/DAO.sol#L158-L163))

**[strictly-scarce (vader) disputed](https://github.com/code-423n4/2021-04-vader-findings/issues/187#issuecomment-830608957):**
 > Not valid.
> All pools use slip-based fees so flash loan attack by buying up USDV or synths is not going to work.

**[dmvt (judge) commented](https://github.com/code-423n4/2021-04-vader-findings/issues/187#issuecomment-847890126):**
 > The funds to execute this attack do not need to come from a pool. It could be done as simply as malicious members pooling their funds in a flash loan contract, and each borrowing the funds in turn to vote.



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
- **GitHub**: https://github.com/code-423n4/2021-04-vader-findings/issues/187
- **Contest**: https://code4rena.com/contests/2021-04-vader-protocol-contest

### Keywords for Search

`vulnerability`

