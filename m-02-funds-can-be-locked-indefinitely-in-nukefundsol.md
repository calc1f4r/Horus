---
# Core Classification
protocol: TraitForge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37922
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-07-traitforge
source_link: https://code4rena.com/reports/2024-07-traitforge
github_link: https://github.com/code-423n4/2024-07-traitforge-findings/issues/1078

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
finders_count: 4
finders:
  - Sabit
  - KupiaSec
  - dimulski
  - 0xDemon
---

## Vulnerability Title

[M-02] Funds can be locked indefinitely in NukeFund.sol

### Overview


This bug report is about a contract called NukeFund, which has a unique way of distributing funds. The main issue is that the only way to withdraw funds is through a function called `nuke()`, which relies on users taking action. This creates a risk of permanently locked funds if all NFTs are burned or if users do not call the `nuke()` function. The report recommends adding a function for the contract owner to withdraw funds in case of emergencies or when all NFTs are burned. The severity of this bug has been decreased to medium.

### Original Finding Content


<https://github.com/code-423n4/2024-07-traitforge/blob/279b2887e3d38bc219a05d332cbcb0655b2dc644/contracts/NukeFund/NukeFund.sol#L40-L61>

### Impact

- Permanent loss of funds.
- Dependency on user action.

### Proof of Concept

The NukeFund contract has a unique fund distribution model where the primary - and only - method to withdraw funds is through the `nuke()` function. This design creates a specific set of circumstances under which funds can be extracted from the contract.

Practical example: Let's say the contract has accumulated 100 ETH in its fund. A user holding a qualified NFT (let's call it TokenID 42) wants to claim a portion of this fund.

    function nuke(uint256 tokenId) public whenNotPaused nonReentrant {
        // ... (verification checks)
        uint256 claimAmount = /* calculated based on nuke factor */;
        fund -= claimAmount;
        nftContract.burn(tokenId);
        payable(msg.sender).call{value: claimAmount}("");
        // ... (event emissions)
    }

<https://github.com/code-423n4/2024-07-traitforge/blob/279b2887e3d38bc219a05d332cbcb0655b2dc644/contracts/NukeFund/NukeFund.sol#L153-L183>

In this scenario:

- The user calls nuke(42).
- The function calculates the claim amount based on the token's properties.
- The NFT (TokenID 42) is burned.
- The calculated amount is sent to the user.
- The fund is reduced by the claimed amount.

This process works as intended, but it relies entirely on NFT holders initiating the withdrawal process. There's no other mechanism for fund distribution or withdrawal, which leads to the second point.

- Risk of permanently locked funds.

If all NFTs are burned or if no one calls the `nuke()` function, there's a real risk that funds could remain permanently locked in the contract.

Practical example: Imagine a scenario where the contract has accumulated 500 ETH over time. There are only 10 NFTs left that are eligible for nuking.

**Scenario A: All NFTs are burned:**

- Users with the remaining 10 NFTs all call `nuke()`.
- After these transactions, all NFTs are burned.
- The contract still holds, say, 100 ETH (depending on the nuke factor calculations).
- There are no more NFTs left to trigger the `nuke()` function.
- The remaining 100 ETH is now locked in the contract with no way to withdraw it.

OR

- Users decide to directly call `burn()` to ball their NFTs.

```
 function burn(uint256 tokenId) external whenNotPaused nonReentrant {
    require(
      isApprovedOrOwner(msg.sender, tokenId),
      'ERC721: caller is not token owner or approved'
    );
    if (!airdropContract.airdropStarted()) {
      uint256 entropy = getTokenEntropy(tokenId);
      airdropContract.subUserAmount(initialOwners[tokenId], entropy);
    }
    _burn(tokenId);
  }
```

<https://github.com/code-423n4/2024-07-traitforge/blob/279b2887e3d38bc219a05d332cbcb0655b2dc644/contracts/TraitForgeNft/TraitForgeNft.sol#L141-L151>

**Scenario B: Inactivity:**

- Out of the 10 NFT holders, only 5 decide to call `nuke()`.
- The other 5 forget about their NFTs or lose access to their wallets.
- The contract is left with 200 ETH and 5 unclaimed NFTs.
- If these 5 NFTs are never used to call `nuke()`, the 200 ETH remains locked indefinitely.

### Recommended Mitigation Steps

Add a function that allows the contract owner to withdraw funds in case of emergencies or when all NFTs are burned.

### Assessed type

Context

**[Koolex (judge) decreased severity to Medium](https://github.com/code-423n4/2024-07-traitforge-findings/issues/1078#issuecomment-2332322248)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | TraitForge |
| Report Date | N/A |
| Finders | Sabit, KupiaSec, dimulski, 0xDemon |

### Source Links

- **Source**: https://code4rena.com/reports/2024-07-traitforge
- **GitHub**: https://github.com/code-423n4/2024-07-traitforge-findings/issues/1078
- **Contest**: https://code4rena.com/reports/2024-07-traitforge

### Keywords for Search

`vulnerability`

