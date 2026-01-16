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
solodit_id: 25218
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-canto
source_link: https://code4rena.com/reports/2022-06-canto
github_link: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/26

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
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-07] Anyone can create Proposal Unigov `Proposal-Store.sol`

### Overview


This bug report is about a vulnerability found in the Proposal Store and GovernorBravoDelegate contracts. These contracts are used to store and execute proposals that have already passed. It was discovered that anyone can add proposals to the Proposal Store contract directly via the AddProposal() function, bypassing the voting process and access control. This vulnerability was confirmed by tkkwon1998 (Canto) and Alex the Entreprenerd (judge) commented that it should be considered as High Severity. The recommended mitigation step is to add authorization checks for AddProposal() so that only the governance module can update the proposals.

### Original Finding Content

_Submitted by Soosh, also found by 0x1f8b, cccz, csanuragjain, hake, p4st13r4, Ruhum, TerrierLover, WatchPug, and zzzitron_

<https://github.com/Plex-Engineer/manifest/blob/688e9b4e7835854c22ef44b045d6d226b784b4b8/contracts/Proposal-Store.sol#L46><br>
<https://github.com/Plex-Engineer/lending-market/blob/b93e2867a64b420ce6ce317f01c7834a7b6b17ca/contracts/Governance/GovernorBravoDelegate.sol#L37>

Proposal Store is used to store proposals that have already passed (<https://code4rena.com/contests/2022-06-new-blockchain-contest#unigov-module-615-sloc>) " Upon a proposal’s passing, the proposalHandler either deploys the ProposalStore contract (if it is not already deployed) or appends the proposal into the ProposalStore’s mapping ( uint ⇒ Proposal)"

But anyone can add proposals to the contract directly via AddProposal() function.

Unigov proposals can be queued and executed by anyone in GovernorBravoDelegate contract<br>
<https://github.com/Plex-Engineer/lending-market/blob/b93e2867a64b420ce6ce317f01c7834a7b6b17ca/contracts/Governance/GovernorBravoDelegate.sol#L37>

### Proof of Concept

<https://github.com/Plex-Engineer/manifest/blob/688e9b4e7835854c22ef44b045d6d226b784b4b8/contracts/Proposal-Store.sol#L46>

### Recommended Mitigation Steps

Authorization checks for AddProposal, only governance module should be able to update.

**[tkkwon1998 (Canto) confirmed](https://github.com/code-423n4/2022-06-canto-findings/issues/26)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2022-06-canto-findings/issues/26#issuecomment-1211337729):**
 > The warden has shown how, due to a lack of checks, anyone can create, queue, and execute a proposal without any particular checks.
> 
> Because governance normally is limited via:
> - Voting on a proposal
> - Access control to limit transactions
> 
> And the finding shows how this is completely ignored; 
> 
> I believe High Severity to be appropriate.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-canto
- **GitHub**: https://github.com/code-423n4/2022-06-newblockchain-findings/issues/26
- **Contest**: https://code4rena.com/reports/2022-06-canto

### Keywords for Search

`vulnerability`

