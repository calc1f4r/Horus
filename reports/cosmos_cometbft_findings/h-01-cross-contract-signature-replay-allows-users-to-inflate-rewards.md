---
# Core Classification
protocol: HYBUX_2025-11-11
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63684
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/HYBUX-security-review_2025-11-11.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Cross-contract signature replay allows users to inflate rewards

### Overview


This bug report states that there is a problem with the signature verification in the `NFTStaking._stakeNFTs()` function. This means that an attacker can use the same signature on different contracts and exploit the system by staking low-rarity NFTs and receiving rewards as if they were high-rarity. To fix this issue, the contract address needs to be included in the signature hash to prevent this type of attack.

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The signature verification in `NFTStaking._stakeNFTs()` does not include the contract address in the hash, allowing signatures to be replayed across the three different NFTStaking contracts (WORLDS_STAKING, GRAYBOYS_STAKING, AVATARS_STAKING).

```solidity
bytes32 hash = keccak256(abi.encode(_sender, _tokenIds, _rarityWeightIndexes));
```

An attacker who owns the same token ID across different NFT collections can obtain a signature for a high-rarity NFT in one collection, then replay that signature when staking a low-rarity NFT with the same token ID in another collection. This results in the low-rarity NFT receiving rewards as if it were high-rarity.

Attack Example:
1. User owns token #100 in both Worlds (e.g. legendary, weight 100) and Grayboys (e.g. common, weight 1) collections
2. User obtains valid signature and stakes in Worlds contract (legitimate)
3. User replays the same signature on Grayboys contract with the common NFT
4. Common NFT now earns rewards with legendary multiplier

## Recommendations

Include the contract address in the signature hash to prevent cross-contract replay:

```solidity
bytes32 hash = keccak256(abi.encode(_sender, _tokenIds, _rarityWeightIndexes, address(this)));
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | HYBUX_2025-11-11 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/HYBUX-security-review_2025-11-11.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

