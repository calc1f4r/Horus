---
# Core Classification
protocol: Moonwell
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26844
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-07-moonwell
source_link: https://code4rena.com/reports/2023-07-moonwell
github_link: https://github.com/code-423n4/2023-07-moonwell-findings/issues/276

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
finders_count: 5
finders:
  - sces60107
  - ABAIKUNANBAEV
  - Aymen0909
  - Jigsaw
  - hals
---

## Vulnerability Title

[M-08] `fastTrackProposalExecution` should only be callable when `TemporalGovernor` is paused

### Overview


A bug has been discovered in the `fastTrackProposalExecution` function of the `TemporalGovernor` contract. This function is meant to be used by the `TemporalGovernor` owner during periods of emergency, when the contract is paused, to fast track a certain proposal (queue and execute a proposal directly without delay or voting) with the goal of ensuring protocol safety. However, the function is missing the `whenPaused` modifier, meaning it can be called at any time to fast track any proposal and not just when the `TemporalGovernor` is paused. This issue goes against the intent of the governance process in which the members of the DAO are supposed to propose, vote and execute the proposals in a permissionless and decentralized manner and where the owner should not be able to execute actions on the protocol without the agreement of the members.

The recommended mitigation step is to add the `whenPaused` modifier to the `fastTrackProposalExecution` function, in order to ensure that the governance process will always work as a real DAO and the owner only intervene in the emergency cases. This has been confirmed by ElliotFriedman (Moonwell) in a duplicate issue.

### Original Finding Content


The function `fastTrackProposalExecution` is supposed to be used by the `TemporalGovernor` owner during periods of emergency, when the contract is paused to fast track a certain proposal (queue and execute a proposal directly without delay or voting), with gaol of ensuring the protocol safety.

But the function `fastTrackProposalExecution` is missing the `whenPaused` modifier which means it can be called at any time to fast track any proposal and not just when the `TemporalGovernor` is paused.

I submit this issue as only Medium risk because only the `TemporalGovernor` owner can call the `fastTrackProposalExecution` function (and i suppose that the owner is trusted and will not execute malicious actions), but this issue still goes against the intent of the governance process in which the members of the DAO are supposed to propose, vote and execute the proposals in a permissionless and decentralized manner and where the owner should not be able to execute actions on the protocol without the agreement of the members (except for those emergency situation of course).

### Proof of Concept

The issue is present in the `fastTrackProposalExecution` function below :

```solidity
/// @notice Allow the guardian to process a VAA when the
/// Temporal Governor is paused this is only for use during
/// periods of emergency when the governance on moonbeam is
/// compromised and we need to stop additional proposals from going through.
/// @param VAA The signed Verified Action Approval to process
function fastTrackProposalExecution(bytes memory VAA) external onlyOwner {
    // @audit can be called when contract is not paused 
    _executeProposal(VAA, true); /// override timestamp checks and execute
}
```

As it can be seen the function does not contain the `whenPaused` modifier and thus it can be called at any moment by the owner to fast track a proposal.

We can also notice that the function comments do mention the fact that it should only be called when the Temporal Governor is paused.

### Recommended Mitigation Steps

I recommend to add the `whenPaused` modifier to the `fastTrackProposalExecution` function, in order to ensure that the governance process will always work as a real DAO and the owner only intervene in the emergency cases.

**[ElliotFriedman (Moonwell) confirmed in a duplicate issue (245)](https://github.com/code-423n4/2023-07-moonwell-findings/issues/245)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Moonwell |
| Report Date | N/A |
| Finders | sces60107, ABAIKUNANBAEV, Aymen0909, Jigsaw, hals |

### Source Links

- **Source**: https://code4rena.com/reports/2023-07-moonwell
- **GitHub**: https://github.com/code-423n4/2023-07-moonwell-findings/issues/276
- **Contest**: https://code4rena.com/reports/2023-07-moonwell

### Keywords for Search

`vulnerability`

