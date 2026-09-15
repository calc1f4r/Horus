---
# Core Classification
protocol: Golom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 8747
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/59

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_marketplace
  - options_vault

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - IllIllI
  - 0x52
  - rotcivegaf
  - berndartmueller
  - kenzo
---

## Vulnerability Title

[M-10] Delegated NFTs that are withdrawn while still delegated will remain delegated even after burn

### Overview


This bug report focuses on an issue with the VoteEscrowDelegation.sol code in the 2022-07-golom GitHub repository. The bug affects the _burn function inherited from VoteEscrowCore.sol. The issue is that when an NFT is burned, the votes for that NFT are removed but the reference of the NFT is still stored in the delegation list. This causes a few issues, such as adding bloat to the getVotes and getPriorVotes functions, reducing the number of real users that can delegate, and adding gas cost when calling removeDelegation.

The recommended mitigation step is to override _burn in VoteEscrowDelegation and add this.removeDelegation(_tokenId), similar to how it was done in _transferFrom. This will ensure that when an NFT is burned, the reference to it is removed from the delegation list. This will help reduce bloat, increase the number of users that can delegate, and reduce the gas cost when calling removeDelegation.

### Original Finding Content


[VoteEscrowCore.sol#L1226-L1236](https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/vote-escrow/VoteEscrowCore.sol#L1226-L1236)<br>

Burn NFTs remained delegated causing bloat and wasting gas.

### Proof of Concept

VoteEscrowDelegation.sol doesn't change the withdraw or \_burn functions inherited from VoteEscrowCore.sol. These functions are ignorant of the delegation system and don't properly remove the delegation when burning an NFT. The votes for the burned NFT will be removed but the reference will still be stored in the delegation list where it was last delegated. This creates a few issues. 1) It adds bloat to both getVotes and getPriorVotes because it adds a useless element that must be looped through. 2) The max number of users that can delegate to another NFT is 500 and the burned NFT takes up one of those spots reducing the number of real users that can delegate. 3) Adds gas cost when calling removeDelegation which adds gas cost to \_transferFrom because removeElement has to cycle through a larger number of elements.

### Recommended Mitigation Steps

Override \_burn in VoteEscrowDelegation and add this.removeDelegation(\_tokenId), similar to how it was done in \_transferFrom.

**[zeroexdead (Golom) confirmed](https://github.com/code-423n4/2022-07-golom-findings/issues/59)**

**[zeroexdead (Golom) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/59#issuecomment-1236184219):**
 > Fixed.<br>
> Ref: https://github.com/golom-protocol/contracts/commit/a30a50abe1aa677374bdbf68e1e81d80e1545563

**[0xsaruman (Golom) resolved](https://github.com/code-423n4/2022-07-golom-findings/issues/59)**

**[LSDan (judge) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/59#issuecomment-1279177352):**
 > I agree with the wardens and sponsor who rate this as medium. It does negatively impact the functioning of the protocol, but none of the reporting wardens have shown how it can be used as a direct attack vector IMO.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Golom |
| Report Date | N/A |
| Finders | IllIllI, 0x52, rotcivegaf, berndartmueller, kenzo |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/59
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`vulnerability`

