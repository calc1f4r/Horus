---
# Core Classification
protocol: Basis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16748
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/basis.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/basis.pdf
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
finders_count: 6
finders:
  - Gustavo Grieco
  - Robert Tonic
  - Josselin Feist
  - Benjamin Perez
  - Dominik Czarnota
---

## Vulnerability Title

Previously executed proposals can be re-executed

### Overview


This bug report is about a data validation issue in the ElectionCommission.sol (v0) code. It has been identified as having a low difficulty level. The code has three states for a proposal: PROPOSED, PASSED, and EXECUTED. The tallyProposalResult function is used to pass a proposal, and if it has enough votes, its state is set to PASSED. Once a proposal is passed, it can be executed through the execute function, which checks that the proposal has the PASSED state. The issue is that tallyProposalResult does not check that the proposal state is PROPOSED, so an attacker can trigger a vote tally again to change its state from EXECUTED to PASSED, and re-execute the proposal multiple times. This could lead to Basis holders losing trust in the system.

In the short term, the recommendation is to verify the proposal is in the PASSED state within tallyProposalResult before continuing with the tally. In the long term, it is suggested to add test coverage for all election scenarios.

### Original Finding Content

## Data Validation

**Type:** Data Validation  
**Target:** ElectionCommission.sol (v0)  

**Difficulty:** Low  

## Description

Once a proposal is passed, it can be executed. However, it is possible to repeat the vote counting on a previously-executed proposal in order to re-execute the proposal multiple times.

A proposal has three states: **PROPOSED**, **PASSED**, **EXECUTED** (ElectionCommission.sol#L227):
```solidity
enum ProposalState { PROPOSED, PASSED, EXECUTED }
```

### Figure 1: Proposal states

The `tallyProposalResult` functions are used to pass a proposal. If the proposal has enough votes, its state is set to **PASSED**.

Once a proposal is passed, it can be executed through `execute`:
```solidity
function execute(Proposal proposal) external notDuringVoteTally {
    require(proposalState[proposal] == ProposalState.PASSED);
    require(now < proposal.expiration());
    proposalState[proposal] = ProposalState.EXECUTED;
    require(_currentProposal == Proposal(0));
    _currentProposal = proposal;
    _currentProposal.execute();
    delete _currentProposal;
}
```

### Figure 2: ElectionCommission.execute function

The `execute` function checks that the proposal has the **PASSED** state. Upon a proposal’s execution, its state is changed to **EXECUTED**.

`tallyProposalResult(Proposal proposal, address[] delegates)` (ElectionCommission.sol#L283) does not check that the proposal state is **PROPOSED**. Therefore, once a proposal is executed, an attacker can trigger a vote tally again in order to change its state from **EXECUTED** to **PASSED**.

As a result, an attacker can re-execute a proposal.

## Exploit Scenario

A proposal is passed and executed. The proposal pauses the system for one hour. Bob forces a voting tally and then re-executes the proposal, causing the system to be paused a second time. As a result, Basis holders lose trust in the system.

## Recommendation

In the short term, verify the proposal is in the **PASSED** state within `tallyProposalResult` before continuing with the tally.  

ElectionCommission lacks unit tests despite its complexity. In the long term, consider adding test coverage for all election scenarios.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Basis |
| Report Date | N/A |
| Finders | Gustavo Grieco, Robert Tonic, Josselin Feist, Benjamin Perez, Dominik Czarnota, https://docs.google.com/document/d/1kKWrVfLjwWBtEMDSsidDeerC6Q4bnR-qC5p0z0_SYnE/edit# 1/68 |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/basis.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/basis.pdf

### Keywords for Search

`vulnerability`

