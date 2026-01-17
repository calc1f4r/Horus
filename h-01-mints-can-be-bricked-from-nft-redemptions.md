---
# Core Classification
protocol: Pupniks
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31604
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Pupniks-security-review.md
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

[H-01] Mints can be bricked from NFT redemptions

### Overview


This bug report highlights a problem with Pupnik NFTs where they can be redeemed at any time after being minted. This can cause issues with subsequent sales, as the redemption decreases the number of NFTs available for sale. This bug can be easily exploited by malicious parties, making it a high severity issue. The report suggests two possible solutions: either keeping a separate variable to track minted NFTs, or delaying redemptions until the sale is complete. 

### Original Finding Content

**Severity**

**Impact:** High, prevents subsequent Pupnik sales

**Likelihood:** Medium, can be easily performed by malicious parties

**Description**

Pupnik NFTs can be redeemed at any point in time after it has been minted. Redeeming a Pupnik whose ID is strictly less than `amountMinted` while the sale is ongoing will cause subsequent sales to revert, because the redemption decrements `amountMinted`, which the sale relies on.

The decrement will attempt to mint the existing ID of `amountMinted` before it is decremented.

```solidity
uint256 currentAmount = amountMinted;

for (uint256 i = 1; i <= quantity;) {
  _mint(msg.sender, currentAmount + i);
  ++i;
}
```

**POC**

```solidity
function test_dos_sale(uint256 amount) public {
  // setup: mint 2-5 NFTs (exclude 1 because we need to redeem NFT id < lastMinted)
  amount = bound(amount, 2, 5);
  _deploy();

  changePrank(owner);
  pupniks.setSignerAddress(signer);
  pupniks.toggleSaleStatus();
  changePrank(user);

  uint256 nonce = 0;

  (bytes32 hash, uint8 v, bytes32 r, bytes32 s) = getSignature(user, nonce, amount, signerPkey);

  pupniks.mintPupnik{value: 0.5 ether * amount}(hash, abi.encodePacked(r, s, v), nonce, amount);

  // redeem 1 NFT
  pupniks.redeemPupnik(1);

  // then try to mint more, but it reverts with TokenAlreadyExists()
  nonce = 1;
  (hash, v, r, s) = getSignature(user, nonce, amount, signerPkey);
  vm.expectRevert(ERC721.TokenAlreadyExists.selector);
  pupniks.mintPupnik{value: 0.5 ether * amount}(hash, abi.encodePacked(r, s, v), nonce, amount);
}
```

**Recommendations**

Either have a separate variable that only keeps track of minted Pupniks and never decrements, or delay Pupnik redemptions for a fixed period till the sale is deemed complete.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Pupniks |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Pupniks-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

