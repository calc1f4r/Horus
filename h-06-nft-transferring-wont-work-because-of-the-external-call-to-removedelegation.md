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
solodit_id: 8732
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-golom-contest
source_link: https://code4rena.com/reports/2022-07-golom
github_link: https://github.com/code-423n4/2022-07-golom-findings/issues/377

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

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
finders_count: 10
finders:
  - TrungOre
  - Bahurum
  - 0xsanson
  - CertoraInc
  - GalloDaSballo
---

## Vulnerability Title

[H-06] NFT transferring won't work because of the external call to `removeDelegation`.

### Overview


This bug report is about an issue with the `VoteEscrowDelegation._transferFrom` function in the `VoteEscrowDelegation.sol` file. The issue is caused by the `removeDelegation` function, which is external. When the call is done by `this.removeDelegation(_tokenId)`, the msg.sender changes to the contract address. This causes the check in the `` function to fail and the function reverts. The impact of this bug is that the `VoteEscrowDelegation._transferFrom` function won't work.

The bug was found manually using VS Code and the author's mind. The recommended mitigation step is to make the `removeDelegation` function public and call it without changing the context (i.e. without changing msg.sender to the contract's address).

### Original Finding Content


<https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/vote-escrow/VoteEscrowDelegation.sol#L242><br>

<https://github.com/code-423n4/2022-07-golom/blob/e5efa8f9d6dda92a90b8b2c4902320acf0c26816/contracts/vote-escrow/VoteEscrowDelegation.sol#L211><br>

The `VoteEscrowDelegation._transferFrom` function won't work because it calls `this.removeDelegation(_tokenId)`. The `removeDelegation` function is external, so when the call is done by `this.removeDelegation(_tokenId)` msg.sender changes to the contract address.

This causes the check in the \`\` function to (most likely) fail because the contract is not the owner of the NFT, and that will make the function revert.<br>
`require(ownerOf(tokenId) == msg.sender, 'VEDelegation: Not allowed');`

### Recommended Mitigation Steps

Make the `removeDelegation` function public and call it without changing the context (i.e. without changing msg.sender to the contract's address).

**[zeroexdead (Golom) confirmed](https://github.com/code-423n4/2022-07-golom-findings/issues/377)**

**[zeroexdead (Golom) commented](https://github.com/code-423n4/2022-07-golom-findings/issues/377#issuecomment-1236183959):**
 > Fixed.
> 
> Ref: https://github.com/golom-protocol/contracts/commit/10ec920765a5ee2afc2fe269d32ea9138d1156b6

**[0xsaruman (Golom) resolved](https://github.com/code-423n4/2022-07-golom-findings/issues/377)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Golom |
| Report Date | N/A |
| Finders | TrungOre, Bahurum, 0xsanson, CertoraInc, GalloDaSballo, cryptphi, carlitox477, 0xA5DF, MEP, kenzo |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-golom
- **GitHub**: https://github.com/code-423n4/2022-07-golom-findings/issues/377
- **Contest**: https://code4rena.com/contests/2022-07-golom-contest

### Keywords for Search

`vulnerability`

