---
# Core Classification
protocol: Interplanetary Consensus (Ipc)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37358
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary Consensus (IPC).md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

Reward Distribution Mechanism in `submitCheckpoint` Function can be gamed

### Overview


The current version of the SubnetActorManagerFacet contract has a problem with its `submitCheckpoint` function. This allows relayers to potentially manipulate the reward system by submitting checkpoints late and still receiving rewards. This can lead to a decrease in rewards for honest and timely relayers, as well as misalignment of incentives for relayers to copy others' submissions rather than submitting honestly. This vulnerability could also be exploited by malicious actors to consistently receive rewards without doing any real work. To fix this issue, it is recommended to redesign the reward mechanism using a commit-reveal scheme, where relayers first commit to a checkpoint without revealing their identity or submission details, and then reveal their submissions after a designated period. This can prevent front-running and copying of submissions. Other solutions may also be considered for this problem.

### Original Finding Content

**Severity**: High

**Status**: Acknowledged

**Location**: SubnetActorManagerFacet.sol

**Description**

The current implementation of the `submitCheckpoint` function in the contract allows for potential gaming of the reward system by validators. A significant loophole exists where a relayer can receive rewards even when submitting a checkpoint late. This opens up a scenario where a relayer can listen to other relayers' submissions and submit within the same epoch, potentially even front-running these transactions. This behavior leads to the dilution of fee distribution, as more relayers share the fees, thereby reducing the intended rewards for timely and legitimate submissions.
**Implications**:
Dilution of Rewards: Genuine relayers who submit checkpoints promptly might receive lower rewards due to the increased number of participants in the reward pool, including those who submit late.
Incentive Misalignment: This issue could lead to a scenario where relayers are incentivized to wait and copy other submissions rather than participating in a timely and honest manner.
Potential for Manipulation: Malicious actors could exploit this vulnerability to consistently gain rewards without contributing meaningful work.

**Recommendation** :

Implement Commit-Reveal Scheme: Redesign the reward mechanism using a commit-reveal scheme. In this approach, relayers would first commit to a checkpoint without revealing their identity or submission details. After a designated commit period, a separate reveal phase would allow relayers to disclose their submissions. This method can prevent front-running and copying of submissions. This is a suggestion, there may be other approaches more appropriate for this protocol.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Interplanetary Consensus (Ipc) |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary Consensus (IPC).md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

