---
# Core Classification
protocol: Dyad
chain: everychain
category: economic
vulnerability_type: sandwich_attack

# Attack Vector Details
attack_type: sandwich_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18764
audit_firm: ZachObront
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-02-12-Dyad.md
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
  - sandwich_attack
  - nft
  - missing_check

protocol_categories:
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Zach Obront
---

## Vulnerability Title

[H-04] If insider deposits and unlocks in quick succession, attacker can steal their NFT and their deposit funds

### Overview


The bug report discusses a potential security flaw in the dNFT contract. The flaw is that an insider can unlock their NFTs without first making a deposit, which would allow any user to liquidate them and steal the NFT. This is especially dangerous because if a user calls both the unlock() and deposit() functions in quick succession, the malicious attacker can create a flashbots bundle to sandwich their liquidation transaction between the two, allowing them to successfully liquidate and steal the insider's NFT.

The recommendation is to add a check to the unlock() function to ensure this situation is avoided. This requires adding a MustDepositFirst() error to IDNft.sol.

The review notes that the new liquidation mechanism only liquidates if withdrawals exceed collateralization ratio, so this attack is no longer possible.

### Original Finding Content

The dNFT contract allows the owner to mint a predefined quantity of "insider" NFTs without any deposit attached to them. These NFTs begin in a locked state, which stops them from being immediately liquidated due to their lack of deposits.

The protocol enforces that, in order for insider's to mint any DYAD, they must unlock their NFTs (so that they will be subject to liquidation, like all other users).

However, there is no safety check for the opposite case, where an insider unlocks their NFT before making a deposit. In this situation, any user could liquidate them and steal their NFT.

This is especially dangerous because if a user calls both of these functions in quick succession, they may both be in the mempool at the same time. If this is the case, a malicious attacker can create a flashbots bundle to sandwich their liquidation transaction between the unlock() and deposit() transactions, with the result that:

- The attacker will successfully liquidate and steal the insider's NFT
- The deposit transaction will deposit the insider's ETH to the stolen NFT, securing it for the attacker

**Recommendation**

I would recommend adding a check to the unlock() function to ensure this situation is avoided:

```solidity
function unlock(uint id)
external
isNftOwner(id)
{
if (!id2Locked[id]) revert NotLocked();
if (id2Shared[id] == 0) revert MustDepositFirst();
id2Locked[id] = false;
emit Unlocked(id);
}
```

Note: This requires adding a MustDepositFirst() error to IDNft.sol.

**Review**

The new liquidation mechanism (see fix for H-02) only liquidates if withdrawals exceed collateralization ratio, so this attack is no longer possible.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ZachObront |
| Protocol | Dyad |
| Report Date | N/A |
| Finders | Zach Obront |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-02-12-Dyad.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Sandwich Attack, NFT, Missing Check`

