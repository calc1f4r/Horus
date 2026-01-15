---
# Core Classification
protocol: Dexe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27314
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-10-cyfrin-dexe.md
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

protocol_categories:
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Dacian
  - 0kage
---

## Vulnerability Title

Changing `nftMultiplier` address by executing a proposal that calls `GovPool::setNftMultiplierAddress()` can deny existing users from claiming pending nft multiplier rewards

### Overview


This bug report is about the `GovPool::setNftMultiplierAddress()` function in the DeXe Protocol. This function is called by an internal proposal and updates the nft multiplier address to a new contract. When calculating rewards, `GovPoolRewards::_getMultipliedRewards()` calls `GovPool::getNftContracts()` to retrieve the nft multiplier address. This means that if the contract is updated to a different one, any unclaimed nft multiplier rewards will no longer exist.

The impact of this bug is that users will lose their unclaimed nft multiplier rewards when a proposal gets required votes to execute `GovPool::setNftMultiplierAddress()`.

The recommended mitigation for this bug is to save the address of the current nft multiplier contract for each proposal when the proposal is created, such that updating the global nft multiplier address would only take effect for new proposals. Additionally, user notifications should be implemented to alert all users with unclaimed NFT multiplier rewards to collect them before the proposal voting period concludes. Furthermore, explicit disclaimers should be included in the documentation to inform users that voting on a proposal aimed at updating multiplier rewards may result in the forfeiture of unclaimed rewards.

The DeXe team has acknowledged this bug and stated that if a DAO decides to add/remove the NFT multiplier, it should affect every DAO member regardless. This can work in two ways: if a DAO decides to add an NFT multiplier, every unclaimed reward will be boosted.

### Original Finding Content

**Description:** [`GovPool::setNftMultiplierAddress()`](https://github.com/dexe-network/DeXe-Protocol/tree/f2fe12eeac0c4c63ac39670912640dc91d94bda5/contracts/gov/GovPool.sol#L343-L345) which can be called by an internal proposal updates the nft multiplier address to a new contract.

`GovPoolRewards::_getMultipliedRewards()` [calls](https://github.com/dexe-network/DeXe-Protocol/tree/f2fe12eeac0c4c63ac39670912640dc91d94bda5/contracts/libs/gov/gov-pool/GovPoolRewards.sol#L203) `GovPool::getNftContracts()` to retrieve the nft multiplier address when calculating rewards. If the contract has been updated to a different one any unclaimed nft multiplier rewards will no longer exist.

**Impact:** Users will lose their unclaimed nft multiplier rewards when a proposal gets required votes to execute `GovPool::setNftMultiplierAddress()`.

**Proof of Concept:** N/A

**Recommended Mitigation:** The address of the current nft multiplier contract could be saved for each proposal when the proposal is created, such that updating the global nft multiplier address would only take effect for new proposals.

If this is indeed the intended design, consider implementing user notifications to alert all users with unclaimed NFT multiplier rewards to collect them before the proposal voting period concludes. Furthermore, consider incorporating explicit disclaimers in the documentation to inform users that voting on a proposal aimed at updating multiplier rewards may result in the forfeiture of unclaimed rewards. This transparency will help users make informed decisions and mitigate potential unexpected outcomes.

**Dexe:**
Acknowledged; this is expected behavior. If a DAO decides to add/remove the NFT multiplier, it should affect every DAO member regardless. This actually works in two ways: if a DAO decides to add an NFT multiplier, every unclaimed reward will be boosted.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Dexe |
| Report Date | N/A |
| Finders | Dacian, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-10-cyfrin-dexe.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

