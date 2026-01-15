---
# Core Classification
protocol: Tracer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19733
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/tracer/tracer/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/tracer/tracer/review.pdf
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
  - yield
  - services
  - derivatives

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Double Voting by Delegaters

### Overview


This bug report describes a problem with voting rights in a governance network. If a user has delegated their voting rights to another member, the recipient of these rights is able to propose/vote with the combined value of their stake plus any delegated stake. However, as there are no restrictions on withdrawing delegated stake once a vote has already been made, a user is able to double vote by transferring this stake to another account and voting on the same proposal. This process is outlined in a scenario in the report. The recommendation is to ensure that no vote is counted twice and potentially add a lockup period when entering and exiting the system, or alternatively, voting could be restricted to pre-existing users who have staked their funds before the respective proposal has been made.

### Original Finding Content

Description
If a user has delegated their voting rights to another member of the governance network, the recipient of these
rights is able to propose/vote with the combined value of their stake plus any delegated stake. However, as
there are no restrictions on withdrawing delegated stake once a vote has already been made, a user is able to
double vote by transferring this stake to another account and voting on the same proposal.
This process can be further outlined in the following scenario:
1. Alice and Bob both decide they want to stake their governance tokens.
2. Bob delegates his stake to Alice, relinquishing him of his voting rights until he decides to remove Alice as
his delegate.
3. Alice submits an arbitrary proposal, whereby her entire stake (including any delegated stake) is counted as
aYesvote.
4. Alice and Bob both wait some time for the warm up period to pass and then Bob proceeds to withdraw his
stake while the proposal is still actively being voted on.
5. Bob then transfers his governance token to an arbitrary account controlled by him and restakes his gover-
nance tokens.
6. With no cooldown on voting after staking, Bob is able to vote on the same proposal, effectively double
voting.
Refer to the test test_withdraw_double_vote() intest_gov.py for a proof of concept.
Recommendations
Ensure that no vote is counted twice and potentially add a lockup period when entering and exiting the system.
Alternatively, voting could be restricted to pre-existing users who have staked their funds before the respective
proposal has been made.
Page | 19
Tracer Protocol Detailed Findings
TCR-12 Possible Double Voting for Proposers

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Tracer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/tracer/tracer/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/tracer/tracer/review.pdf

### Keywords for Search

`vulnerability`

