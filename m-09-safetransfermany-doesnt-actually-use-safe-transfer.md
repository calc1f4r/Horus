---
# Core Classification
protocol: Tigris Trade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6339
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-tigris-trade-contest
source_link: https://code4rena.com/reports/2022-12-tigris
github_link: https://github.com/code-423n4/2022-12-tigris-findings/issues/356

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:

protocol_categories:
  - dexes
  - services
  - derivatives
  - cross_chain
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - HollaDieWaldfee
  - 8olidity
  - 0xmuxyz
  - 0xA5DF
  - 0x4non
---

## Vulnerability Title

[M-09] safeTransferMany() doesn’t actually use safe transfer

### Overview


This bug report outlines a vulnerability in the `BondNFT` and `GovNFT` ERC721 implementations. The vulnerability is in the `safeTransferMany()` function, which does not actually use safe transfer and could lead to users getting their funds stuck in a contract that does not support ERC721. To prove the vulnerability, tests were added to the `GovNFT` tests that showed the expected behavior of the `safeTransferFrom()` function succeeding, but the `safeTransferMany()` function not reverting.

The recommended mitigation step is to call `_safeTransfer()` instead of `_transfer()` when using the `safeTransferMany()` function.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-12-tigris/blob/496e1974ee3838be8759e7b4096dbee1b8795593/contracts/GovNFT.sol#L247
https://github.com/code-423n4/2022-12-tigris/blob/496e1974ee3838be8759e7b4096dbee1b8795593/contracts/BondNFT.sol#L285


## Vulnerability details

Both `BondNFT` and `GovNFT` are an ERC721 implementation, they both also have a function named `safeTransferMany()` which its name implies is supposed to safe transfer many tokens at once.
However the function doesn't actually safe transfer (doesn't )

## Impact
Users might use this function, expecting it to verify that the receiver is an `ERC721Receiver`, but will get their funds stuck in a contract that doesn't support ERC721.

## Proof of Concept
I've added the following tests to the `GovNFT` tests.
1st test will succeed (tx will revert) since `safeTransferFrom()` does actually use safe transfer.
2nd will fail (tx won't revert), since `safeTransferMany()` doesn't actually use a safe transfer.

```diff
diff --git a/test/05.GovNFT.js b/test/05.GovNFT.js
index 711a649..d927320 100644
--- a/test/05.GovNFT.js
+++ b/test/05.GovNFT.js
@@ -98,6 +98,14 @@ describe("govnft", function () {
       expect(await govnft.pending(owner.getAddress(), StableToken.address)).to.equal(1500);
       expect(await govnft.pending(user.getAddress(), StableToken.address)).to.equal(500);
     });
+
+    it("Safe transfer to non ERC721Receiver", async function () {
+      
+      expect(govnft.connect(owner)['safeTransferFrom(address,address,uint256)'](owner.address,StableToken.address, 2)).to.be.revertedWith("ERC721: transfer to non ERC721Receiver implementer");
+    });
+    it("Safe transfer many  to non ERC721Receiver", async function () {
+      await expect(govnft.connect(owner).safeTransferMany(StableToken.address, [2])).to.be.revertedWith("ERC721: transfer to non ERC721Receiver implementer");
+    });
     it("Transferring an NFT with pending delisted rewards should not affect pending rewards", async function () {
       await govnft.connect(owner).safeTransferMany(user.getAddress(), [2,3]);
       expect(await govnft.balanceOf(owner.getAddress())).to.equal(0);

```

Output (I've shortened the output. following test will also fail, since the successful transfer will affect them):

```
      ✔ Safe transfer to contract
      1) Safe transfer many to contract


  11 passing (3s)
  1 failing

  1) govnft
       Reward system related functions
         Safe transfer many to contract:

      AssertionError: Expected transaction to be reverted
      + expected - actual

      -Transaction NOT reverted.
      +Transaction reverted.
```


## Recommended Mitigation Steps
Call `_safeTransfer()` instead of `_transfer()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Tigris Trade |
| Report Date | N/A |
| Finders | HollaDieWaldfee, 8olidity, 0xmuxyz, 0xA5DF, 0x4non |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-tigris
- **GitHub**: https://github.com/code-423n4/2022-12-tigris-findings/issues/356
- **Contest**: https://code4rena.com/contests/2022-12-tigris-trade-contest

### Keywords for Search

`vulnerability`

