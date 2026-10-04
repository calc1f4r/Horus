---
# Core Classification
protocol: P2P.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35032
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Fee%20Distributor%20Diff%20Audit%20(v1)/README.md#2-the-slashed-validators-stake-gets-split-between-client-referrer-and-service
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
  - MixBytes
---

## Vulnerability Title

The slashed validator's stake gets split between `client`, `referrer`, and `service`

### Overview


The bug report describes an issue with a specific line of code in a project. The issue occurs when a user's stake is slashed in ETH2 staking and withdrawn to the project's contract. This causes a check to fail, resulting in the user receiving less ETH than they initially deposited and their stake being split in a way that is not intended. The severity of this issue is marked as critical because it affects the user's funds and stake. The report recommends replacing the check and introducing a registry to help with validator exiting and marking the contract's balance at the time of the exit. This will allow for proper withdrawal of funds by the user.

### Original Finding Content

##### Description
There is an issue at line https://github.com/p2p-org/eth-staking-fee-distributor-contracts/blob/30a7ff78e8285f2eae4ae552efb390aa4453a083/contracts/feeDistributor/ContractWcFeeDistributor.sol#L114.
If the user's stake deposited by `client` gets slashed in ETH2 staking and is withdrawn to the `ContractWcFeeDistributor` contract (and all previous rewards were withdrawn), the `balance >= COLLATERAL` check will not pass. In that case, execution after the `if` block continues, and the users' deposit gets split as if it were rewarded.
A CRITICAL severity level was assigned to that issue because the user receives less ETH than they initially deposited minus the slashing penalty. Their stake is also split into `referrer` and `service`, which shouldn't happen in a normal case.

##### Recommendation
We recommend replacing the `balance >= COLLATERAL` check at line https://github.com/p2p-org/eth-staking-fee-distributor-contracts/blob/30a7ff78e8285f2eae4ae552efb390aa4453a083/contracts/feeDistributor/ContractWcFeeDistributor.sol#L114 and introduce a special registry of initially deposited validators public keys. It will help protocol owners to approve validator exiting (initially triggered by the user). Also, it would be useful to mark the current contract balance at the time of the validator exit being started. At the time when the contract receives a stake, withdrawal can be marked as finished, and the user is able to withdraw up to `address(this).balance - markedBalance`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | P2P.org |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/Staking%20Fee%20Distributor%20Diff%20Audit%20(v1)/README.md#2-the-slashed-validators-stake-gets-split-between-client-referrer-and-service
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

