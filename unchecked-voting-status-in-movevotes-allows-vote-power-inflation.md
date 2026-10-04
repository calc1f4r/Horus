---
# Core Classification
protocol: EYWA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44341
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/EYWA/DAO/README.md#7-unchecked-voting-status-in-movevotes-allows-vote-power-inflation
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

protocol_categories:
  - dexes

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Unchecked voting status in `moveVotes()` allows vote power inflation

### Overview


The `moveVotes()` method in the `EscrowManager` contract does not properly check if a token has already voted before allowing it to move its votes. This means that an attacker or any user could cast a vote, move their votes, and repeat the process to artificially inflate their voting power and manipulate the outcome of a vote. To fix this, a validation check should be added to `moveVotes()` similar to the one in `_update()`. This will prevent tokens from voting multiple times and ensure fair voting outcomes.

### Original Finding Content

##### Description

- https://gitlab.ubertech.dev/blockchainlaboratory/eywa-dao/blob/39fba4bee623a3e60a529416f93d76e73658440d/contracts/EscrowManager.sol#L396

The `moveVotes()` method in `EscrowManager` does not validate whether the token has already voted by checking the `s_hasVotedByTokenId` mapping.

Because there is no check of `s_hasVotedByTokenId[tokenId_]` within `moveVotes()`, an attacker (or any user) can:
1. Cast a vote.
2. Call `moveVotes()` to move their votes (via `DELEGATION_MANAGER`).
3. Repeat the above sequence.

By doing so, the user could artificially inflate their voting power, effectively manipulating voting outcomes.

##### Recommendation

Add a validation check for `s_hasVotedByTokenId[tokenId_]` in the `moveVotes()` method, similar to the one in `_update()`. For instance (https://gitlab.ubertech.dev/blockchainlaboratory/eywa-dao/blob/39fba4bee623a3e60a529416f93d76e73658440d/contracts/EscrowManager.sol#L517):
```solidity
if (s_hasVotedByTokenId[tokenId_]) {
    revert LockCurrentlyVoting();
}
```

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | EYWA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/EYWA/DAO/README.md#7-unchecked-voting-status-in-movevotes-allows-vote-power-inflation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

