---
# Core Classification
protocol: Berachain Governance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52850
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Governance-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Governance-Spearbit-Security-Review-October-2024.pdf
github_link: none

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
finders_count: 2
finders:
  - Tnch
  - Xmxanuel
---

## Vulnerability Title

proposer cannot cancel a proposal with a GOV_VOTING_DELAY=0 after propose block.timstamp + 1

### Overview


The bug report is about an issue in the OZ governance contracts, specifically in the DeployGovernance.s.sol file. The contracts have a parameter called votingDelay which determines the timestamp for the ERC20 balance snapshot and the start of the voting process. However, in the Berachain deployment script, the GOV_VOTING_DELAY is set to 0 which causes problems when trying to cancel a proposal. This is because the internal clock in the governor contract is based on blocks and a GOV_VOTING_DELAY of 0 is converted to 1 block, making it nearly impossible to cancel a proposal after its creation. This can lead to accidental voting for incorrect proposals. The recommendation is to allow proposals to be canceled even when GOV_VOTING_DELAY is set to 0. This issue has been fixed in the Berachain deployment script. 

### Original Finding Content

Severity: Medium Risk
Context: DeployGovernance.s.sol#L19
Description: The OZ governance contracts include a parameter calledvotingDelay , which specifies a time delay
between the block.timestamp of the proposal's creation and the start of the voting process. The votingDelay
determines the timestamp for the ERC20 balance snapshot. Before voting begins, the state is referred to as
Pending in the OZ governance contracts.
In the default setup, proposals can only be canceled while in the Pending state.
• GovernanceUpgradable.cancel
// public cancel restrictions (on top of existing _cancel restrictions).
_validateStateBitmap(proposalId, _encodeStateBitmap(ProposalState.Pending));
However, in the Berachain deployment script, theGOV_VOTING_DELAY is set to 0. The internal clock in the governor
contract is based on blocks and the GOV_VOTING_DELAY=0 is converted to 1 block because the timeToBlocks
helper function (See: DeployGovernance.s.sol#L97 ) has a fallback for zero blocks:
// Fallback for safety:
if (blocks == 0) {
blocks = 1;
}
A proposal can only be canceled at the propose timestamp + 1. As a result, it is nearly impossible to cancel a
proposal after its creation for the user.
Recommendation: The need to cancel a proposal can arise quickly, for example through a configuration error. If
it is not possible to cancel the proposal, user might accidentally vote for an incorrect one.
Consider allowing proposals to be canceled even when GOV_VOTING_DELAY=0 . From a technical standpoint, a
proposal could be canceled in any state exceptProposalState.Canceled , ProposalState.Expired , and Propos-
alState.Executed .
Berachain: Fixed in commit 424f533d.
Spearbit: Resolved.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Berachain Governance |
| Report Date | N/A |
| Finders | Tnch, Xmxanuel |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Governance-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Governance-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

