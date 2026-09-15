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
solodit_id: 32004
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/12/rocket-pool-houston/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Unused Parameter and Improper Parameter Sanitization in RocketNetworkVoting.calculateVotingPower() ✓ Fixed

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



The client fixed the issue in commit `aff5be87c2bc6fd4966be743cf8370fb43fac917` and provided the following statement:


* `matchedETH` was left over from previous design, removed.
* Added assertion for block number
* The upgrade script ensures there is at least 1 snapshot of the RPL price




#### Description


The `matchedETH` parameter in `RocketNetworkVoting.calculateVotingPower()` is unused.


**contracts/contract/network/RocketNetworkVoting.sol:L110-L111**



```
// Get contracts
RocketDAOProtocolSettingsNodeInterface rocketDAOProtocolSettingsNode = RocketDAOProtocolSettingsNodeInterface(getContractAddress("rocketDAOProtocolSettingsNode"));

```
Additionally, the `_block` parameter is not sanitized. Thus, if calling the function with a block number `_block` where `_block >= block.number`, the call will revert because of a division-by-zero error. Indeed, `rocketNetworkSnapshots.lookupRecent` will return a `rplPrice` of zero since the checkpoint does not exist. Consequently, the function `calculateVotingPower` will revert when computing the `maximumStake`.


**contracts/contract/network/RocketNetworkVoting.sol:L102-L105**



```
key = keccak256(abi.encodePacked("rpl.staked.node.amount", _nodeAddress));
uint256 rplStake = uint256(rocketNetworkSnapshots.lookupRecent(key, uint32(_block), 5));

return calculateVotingPower(rplStake, ethMatched, ethProvided, rplPrice);

```
**contracts/contract/network/RocketNetworkVoting.sol:L114-L114**



```
uint256 maximumStake = providedETH * maximumStakePercent / rplPrice;

```
#### Recommendation


We recommend removing the unused parameter to enhance code clarity. The presence of unused parameters can lead to potential confusion for future developers. Additionally, we recommend ensuring that the snapshotted `rplPrice` value exists before it is used to compute the `maximumStake` value.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

