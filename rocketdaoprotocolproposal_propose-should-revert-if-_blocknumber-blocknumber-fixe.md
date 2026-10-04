---
# Core Classification
protocol: Rocket Pool (Houston)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32003
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/12/rocket-pool-houston/
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
  - Dominik Muhs
  -  Valentin Quelquejay

---

## Vulnerability Title

RocketDAOProtocolProposal._propose() Should Revert if _blockNumber > block.number ✓ Fixed

### Overview


The report highlights an issue with the `RocketDAOProtocolProposal._propose()` function in the `contracts/contract/dao/protocol/RocketDAOProtocolProposal.sol` file. This function does not handle situations where the `_blockNumber` parameter is greater than the current block number, which can lead to undefined voting power in future proposals. The recommended solution is to update the function to reject transactions where `_blockNumber` is higher than `block.number` to ensure the voting process remains valid. The client has fixed this issue in a recent commit.

### Original Finding Content

#### Resolution



The client fixed this issue in commit `c60c1d292a81eb83c4c766425303f31c1d74901e` 


#### Description


Currently, the `RocketDAOProtocolProposal._propose()` function does not account for scenarios where `_blockNumber` is greater than `block.number`. This is a critical oversight, as voting power cannot be determined for future block numbers.


**contracts/contract/dao/protocol/RocketDAOProtocolProposal.sol:L351**



```
function _propose(string memory _proposalMessage, uint256 _blockNumber, uint256 _totalVotingPower, bytes calldata _payload) internal returns (uint256) {

```
#### Recommendation


We recommend updating the function to revert on transactions where `_blockNumber` exceeds `block.number`. This will prevent the creation of proposals with undefined voting power and maintain the integrity of the voting process.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Rocket Pool (Houston) |
| Report Date | N/A |
| Finders | Dominik Muhs,  Valentin Quelquejay
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/12/rocket-pool-houston/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

