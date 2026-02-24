---
# Core Classification
protocol: FCHAIN Validator and Staking Contracts Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55344
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fchain-validator-and-staking-contracts-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Locked-In Licenses Can Be Transferred

### Overview


The report discusses a bug in the FCHAIN smart contract system. It states that to become a validator, one must possess an FNode license and lock it into the StakeManager contract. Both validators and delegators can lock their licenses using a function called `_lockLicenses`. However, this function does not transfer ownership of the license to the contract, which means the owner can still transfer the license to someone else and earn rewards while the new owner cannot restake the token. The report suggests two solutions: either transfer the license to the contract during the locking process or make the licenses non-transferable while they are part of an active validator's weight. The team has acknowledged the bug and will resolve it, but they have stated that NFTs will be non-transferable for a year, so they will not make any changes at the moment.

### Original Finding Content

Possession of an [`FNode`](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/FNodes.sol) license is a [requirement to become a validator](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L194-L196) on FCHAIN. Validators must [lock](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L209) their ERC-721-compliant `FNode` tokens into the `StakeManager` contract to be recognized as active validators and receive incentives, while delegators can also [lock](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L268) and delegate their `FNode` tokens to active validators to earn rewards.

Within the `StakeManager` contract, both validators and delegators lock their `FNode` licenses by invoking the `internal` [`_lockLicenses` function](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L858) during the initiation phases of validator registration, delegator registration, or when adding new stakes. This function confirms that the [caller (`_msgSender`) is the owner of the ERC-721 token](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L879-L881) and then “locks” the token by [updating](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L889) the `tokenLockedBy[tokenID]` mapping. Notably, only the `internal` mapping is modified the token itself is not transferred to the contract.

This allows the owner of the `FNode` token to be able to transfer ownership of their "locked" license by invoking the `transferFrom` or `safeTransferFrom` functions of the `IERC721` interface, which effectively cancels their eligibility as a network validator. Nevertheless, the original stake in `StakeManager` continues to earn rewards since the license remains counted in the validator’s overall weight. In addition, the new owner of the license [cannot restake](https://github.com/0xFFoundation/fchain-contracts/blob/11ffd45bc95747b8d2432a2e8bb120d4a1dc19a2/src/StakeManager.sol#L884-L886) the token because it is already recorded in the `tokenLockedBy` mapping.

Consider transferring the `FNode` token to the `StakeManager` contract during the locking process and returning it to the validator or delegator upon unlocking. Alternatively, consider making the `FNode` tokens non-transferrable as long as they are part of an active validator's weight.

***Update:** Acknowledged, will resolve. The team stated:*

> *NFTs are going to be non-transferable for a year, so we are not going to change this part at the moment.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | FCHAIN Validator and Staking Contracts Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/fchain-validator-and-staking-contracts-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

