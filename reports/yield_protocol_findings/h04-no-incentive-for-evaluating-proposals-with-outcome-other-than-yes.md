---
# Core Classification
protocol: Audius Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11315
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/audius-contracts-audit/
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
  - services
  - cross_chain
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[H04] No incentive for evaluating proposals with outcome other than Yes

### Overview


This bug report is about the `evaluateProposalOutcome` function of the `Governance` contract. This function is used to execute the target contract for proposals with a Yes quorum and to update the proposal state. However, when a proposal does not reach the quorum or is rejected, this function spends gas to update the state, which does not have any incentive for the caller. This could lead to many closed proposals with an outdated `InProgress` state, which could be confusing to voting interfaces. Therefore, it is suggested to add an incentive for the caller of the `evaluateProposalOutcome` function, so there are better guarantees that the state of the proposals will be up-to-date. 

This bug was fixed in pull requests [#575](https://github.com/AudiusProject/audius-protocol/pull/575) and [#609](https://github.com/AudiusProject/audius-protocol/pull/609). Now, before submitting a new proposal, the status of all the proposals that can be evaluated have to be up-to-date. This could make it too expensive for somebody to send new proposals if they have to evaluate many old proposals. In this case, again, only the administrators might be incentivized to evaluate all the proposals in order to unblock the system. Additionally, [setting the maximum number of in-progress proposals](https://github.com/AudiusProject/audius-protocol/blob/f38eed25e094144a98886c06546c3f885a009e31/eth-contracts/contracts/Governance.sol#L589) emits no event.

### Original Finding Content

After a voting period has ended, the [`evaluateProposalOutcome` function of the `Governance` contract](https://github.com/AudiusProject/audius-protocol/blob/6f3b31562b9d4c43cef91af0a011986a2580fba2/eth-contracts/contracts/Governance.sol#L316) can be called to try to execute the target contract for proposals with a Yes quorum and to update the proposal state.


There is an incentive for approved proposals to be executed by their proposers or supporters. However, when a proposal does not reach the quorum (or is rejected), this function spends gas to update the state. It is unclear why a user would pay for this gas to clean up the proposals state. Since anybody can submit a proposal at any time, this could lead to many closed proposals with an outdated `InProgress` state. This could be confusing to voting interfaces which will have to inspect the proposal to check if they are actually open.


Consider adding an incentive for the caller of the `evaluateProposalOutcome` function, so there are better guarantees that the state of the proposals will be up-to-date.


***Update:** Fixed in pull requests [#575](https://github.com/AudiusProject/audius-protocol/pull/575) and [#609](https://github.com/AudiusProject/audius-protocol/pull/609). Now, before submitting a new proposal, the status of all the proposals that can be evaluated have to be up-to-date. Note that this could make it too expensive for somebody to send new proposals if they have to evaluate many old proposals. In this case, again, only the administrators might be incentivized to evaluate all the proposals in order to unblock the system. Also note that [setting the maximum number of in-progress proposals](https://github.com/AudiusProject/audius-protocol/blob/f38eed25e094144a98886c06546c3f885a009e31/eth-contracts/contracts/Governance.sol#L589) emits no event.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Audius Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/audius-contracts-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

