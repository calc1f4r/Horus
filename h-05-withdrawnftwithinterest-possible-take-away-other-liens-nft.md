---
# Core Classification
protocol: Particle Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20703
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-particle
source_link: https://code4rena.com/reports/2023-05-particle
github_link: https://github.com/code-423n4/2023-05-particle-findings/issues/13

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
finders_count: 4
finders:
  - d3e4
  - minhquanym
  - bin2chen
  - rbserver
---

## Vulnerability Title

[H-05] withdrawNftWithInterest() possible take away other Lien's NFT

### Overview


This bug report describes an issue with the `withdrawNftWithInterest()` function which is used to retrieve NFTs. Currently, the protocol does not restrict the existence of only one Lien in the same NFT, meaning that if two different users supply Liens for the same NFT, the first user can withdraw the NFT with interest even though the other user's Lien is still valid. This could result in the second user losing their NFT and the funds associated with the Lien.

The recommended mitigation step for this issue is to determine whether there is an active loan before allowing the NFT to be withdrawn. This can be done by adding a `require` statement to the `withdrawNftWithInterest()` function that checks whether the `loanStartTime` is equal to 0.

The bug report was acknowledged by both Adriro and Wukong-Particle and was confirmed to be fixed.

### Original Finding Content


### Proof of Concept

`withdrawNftWithInterest()` is used to retrieve NFT. The only current restriction is if you can transfer out of NFT, it means an inactive loan.

```solidity
    function withdrawNftWithInterest(Lien calldata lien, uint256 lienId) external override validateLien(lien, lienId) {
        if (msg.sender != lien.lender) {
            revert Errors.Unauthorized();
        }

        // delete lien
        delete liens[lienId];

        // transfer NFT back to lender
        /// @dev can withdraw means NFT is currently in contract without active loan,
        /// @dev the interest (if any) is already accured to lender at NFT acquiring time
        IERC721(lien.collection).safeTransferFrom(address(this), msg.sender, lien.tokenId);
...
```
However, the current protocol does not restrict the existence of only one Lien in the same NFT.

For example, the following scenario.

1.  Alice transfers NFT_A and supply Lien\[1].
2.  Bob executes `sellNftToMarket()`.
3.  Jack buys NFT_A from the market.
4.  Jack transfers NFT_A and supply Lien\[2].
5.  Alice executing `withdrawNftWithInterest(1)` is able to get NFT_A successfully (because step 4 NFT_A is already in the contract). This results in the deletion of lien\[1], and Lien\[2]'s NFT_A is transferred away.

The result is: Jack's NFT is lost and Bob's funds are also lost.

### Recommended Mitigation Steps

Need to determine whether there is a Loan

```solidity
    function withdrawNftWithInterest(Lien calldata lien, uint256 lienId) external override validateLien(lien, lienId) {
        if (msg.sender != lien.lender) {
            revert Errors.Unauthorized();
        }

+       require(lien.loanStartTime == 0,"Active Loan");
```

### Assessed type

Context

**[adriro (warden) commented](https://github.com/code-423n4/2023-05-particle-findings/issues/13#issuecomment-1575278736):**
 > Nice finding

**[wukong-particle (Particle) confirmed and commented](https://github.com/code-423n4/2023-05-particle-findings/issues/13#issuecomment-1581317165):**
 > Fixed.
***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Particle Protocol |
| Report Date | N/A |
| Finders | d3e4, minhquanym, bin2chen, rbserver |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-particle
- **GitHub**: https://github.com/code-423n4/2023-05-particle-findings/issues/13
- **Contest**: https://code4rena.com/reports/2023-05-particle

### Keywords for Search

`vulnerability`

