---
# Core Classification
protocol: Algebra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27867
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Algebra%20Finance/Periphery/README.md#2-the-operator-address-is-not-reset-after-the-position-token-transfer
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

The operator address is not reset after the position token transfer

### Overview


This bug report is about a problem in the LimitOrderManager.sol contract. It deals with the NFT position owner setting a token operator to use the permit functionality. The operator address is used at a specific line in the contract and the 'getApproved' function is used to get the address of the entity which is allowed to make transfers. The problem is that a new owner may not know about the given permit and the token operator is still able to make transfers and burn/collect a limit order position on behalf of the new token owner. 

The recommendation is to override the ERC721 '_transfer' functionality and reset the '_limitPositions[tokenId] value on transfer. This way, the new owner will know about the given permit and the token operator will not be able to make transfers or burn/collect a limit order position on behalf of the new token owner.

### Original Finding Content

##### Description
A NFT position owner can set token `operator` to use permit functionality - https://github.com/cryptoalgebra/Algebra/blob/bddd6487c86e0d6afef39638159dc403a91ba433/src/periphery/contracts/LimitOrderManager.sol#L275. The operator address is used at the line https://github.com/cryptoalgebra/Algebra/blob/bddd6487c86e0d6afef39638159dc403a91ba433/src/periphery/contracts/LimitOrderManager.sol#L270. The `getApproved` function is used in a ERC721 standard to get an address of the entity which is allowed to make transfers. The user may give a permit to desired `operator`, then sell/transfer the NFT token. A new owner may not know about the given permit - the token operator is still able to make transfers and burn/collect a limit order position on behalf of the new token owner.
##### Recommendation
We recommend overriding the ERC721 `_transfer` functionality and resetting the `_limitPositions[tokenId]` value on transfer.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Algebra Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Algebra%20Finance/Periphery/README.md#2-the-operator-address-is-not-reset-after-the-position-token-transfer
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

