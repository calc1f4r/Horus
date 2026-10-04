---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25228
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto
source_link: https://code4rena.com/reports/2022-06-canto
github_link: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/244

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
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] Unable to check `state()` if `proposalId == 0`

### Overview


This bug report is about the `state()` function in the GovernorBravoDelegate.sol smart contract, which is part of the lending-market repository on GitHub. The bug is that the `state()` function cannot be called to view the proposal state if `proposalId == 0`. The bug was reported by hake, and it was found that there is no check to prevent queueing a `proposalId` with a value of 0 via the `queue()` function. This means that the `proposalId` could be set to 0, which is not allowed according to the `state()` function.

Nivasan1 (Canto) disputed the bug, saying that the ProposalId cannot be 0 as the proposal IDs are fixed and will be set via the cosmos-sdk. Alex the Entreprenerd (judge) commented that while the sponsor says the proposalId will never be 0, there is no way to avoid that at the Smart Contract level, meaning that any caller can set the proposal to 0.

The recommended mitigation steps for this bug is to implement a check to prevent queueing a `proposalId == 0`. This will help prevent setting the `proposalId` to 0, which is not allowed according to the `state()` function.

### Original Finding Content

_Submitted by hake_

<https://github.com/Plex-Engineer/lending-market/blob/755424c1f9ab3f9f0408443e6606f94e4f08a990/contracts/Governance/GovernorBravoDelegate.sol#L115>

`state()` function cannot be called to view proposal state if `proposalId == 0`.

### Proof of Concept

There is no check to prevent queueing a `proposalId` with a value of 0 via the [`queue()`](https://github.com/Plex-Engineer/lending-market/blob/755424c1f9ab3f9f0408443e6606f94e4f08a990/contracts/Governance/GovernorBravoDelegate.sol#L37-L47) function.<br>
However, in the `state()` function there is a check preventing using a `proposalId == 0`.<br>
For clarity: `initialProposalId` must be zero according to `_initiate()`, therefore, `proposalId` cannot be 0 according to check below.

```solidity
function state(uint proposalId) public view returns (ProposalState) {
    require(proposalCount >= proposalId && proposalId > initialProposalId, "GovernorBravo::state: invalid proposal id");
```

### Recommended Mitigation Steps

Implement check to preventing queueing a `proposalId == 0`.

**[nivasan1 (Canto) disputed and commented](https://github.com/code-423n4/2022-06-canto-findings/issues/244#issuecomment-1191992076):**
 > The ProposalId cannot be 0 as the proposal IDs are fixed and will be set via the cosmos-sdk.

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-findings/issues/244#issuecomment-1205692351):**
 > The warden has shown how, through a misconfiguration, a proposal could never be executable due to a revert in `state()`.
> 
> While I believe the warden has already shown a remediation that would cover this scenario, I believe the Warden has shown a unique possible situation that can cause the system to stop working as intended.
> 
> While the sponsor says the proposalId will never be 0, there is no way to avoid that at the Smart Contract level, meaning that any caller can set the proposal to 0.
> 
> For these reasons, I think Medium Severity to be appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto
- **GitHub**: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/244
- **Contest**: https://code4rena.com/reports/2022-06-canto

### Keywords for Search

`vulnerability`

