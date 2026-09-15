---
# Core Classification
protocol: Telcoin Platform Audit
chain: everychain
category: uncategorized
vulnerability_type: erc721

# Attack Vector Details
attack_type: erc721
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30181
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/156
source_link: none
github_link: https://github.com/sherlock-audit/2024-01-telcoin-judging/issues/199

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
  - erc721

# Audit Details
report_date: unknown
finders_count: 43
finders:
  - Aamirusmani1552
  - DenTonylifer
  - fibonacci
  - sobieski
  - 0xAsen
---

## Vulnerability Title

H-3: CouncilMember:burn renders the contract inoperable after the first execution

### Overview


This bug report discusses a critical vulnerability found in the CouncilMember contract, which is used for managing ERC721 tokens. The issue is caused by the `burn` function incorrectly managing the `balances` array, which results in several critical impacts, including making the contract inoperable and preventing token holders from interacting with their assets. The vulnerability was found by a group of researchers and confirmed through a proof of concept. The severity of the vulnerability is high and it is recommended to avoid popping out balances or consider migrating to ERC1155. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-01-telcoin-judging/issues/199 

## Found by 
0xAsen, 0xLogos, 0xadrii, 0xlamide, 0xmystery, 0xpep7, Aamirusmani1552, Arz, BAICE, Bauer, DenTonylifer, HonorLt, Ignite, IvanFitro, Jaraxxus, Kow, Krace, VAD37, alexbabits, almurhasan, araj, bitsurfer, dipp, fibonacci, ggg\_ttt\_hhh, gqrp, grearlake, jah, m4ttm, mstpr-brainbot, popeye, psb01, r0ck3tz, ravikiran.web3, sakshamguruji, sobieski, sonny2k, tives, ubl4nk, vvv, ydlee, zhuying, zzykxx
## Summary
The CouncilMember contract suffers from a critical vulnerability that misaligns the balances array after a successful burn, rendering the contract inoperable.

## Vulnerability Detail

The root cause of the vulnerability is that the `burn` function incorrectly manages the `balances` array, shortening it by one each time an ERC721 token is burned while the latest minted NFT still withholds its unique `tokenId` which maps to the previous value of `balances.length`.
```solidity
// File: telcoin-audit/contracts/sablier/core/CouncilMember.sol
210:    function burn(
        ...
220:        balances.pop(); // <= FOUND: balances.length decreases, while latest minted nft withold its unique tokenId
221:        _burn(tokenId);
222:    }
```

This misalignment between existing `tokenIds` and the `balances` array results in several critical impacts:

1. Holders with tokenId greater than the length of balances cannot claim.
2. Subsequent burns of tokenId greater than balances length will revert.
3. Subsequent mint operations will revert due to tokenId collision. As `totalSupply` now collides with the existing `tokenId`.
```solidity
// File: telcoin-audit/contracts/sablier/core/CouncilMember.sol
173:    function mint(
        ...
179:
180:        balances.push(0);
181:        _mint(newMember, totalSupply());// <= FOUND
182:    }
```

This mismanagement creates a cascading effect, collectively rendering the contract inoperable. Following POC will demonstrate the issue more clearly in codes.

### POC

Run `git apply` on the following patch then run `npx hardhat test` to run the POC.
```patch
diff --git a/telcoin-audit/test/sablier/CouncilMember.test.ts b/telcoin-audit/test/sablier/CouncilMember.test.ts
index 675b89d..ab96b08 100644
--- a/telcoin-audit/test/sablier/CouncilMember.test.ts
+++ b/telcoin-audit/test/sablier/CouncilMember.test.ts
@@ -1,13 +1,14 @@
 import { expect } from "chai";
 import { ethers } from "hardhat";
 import { SignerWithAddress } from "@nomicfoundation/hardhat-ethers/signers";
-import { CouncilMember, TestTelcoin, TestStream } from "../../typechain-types";
+import { CouncilMember, TestTelcoin, TestStream, ERC721Upgradeable__factory } from "../../typechain-types";
 
 describe("CouncilMember", () => {
     let admin: SignerWithAddress;
     let support: SignerWithAddress;
     let member: SignerWithAddress;
     let holder: SignerWithAddress;
+    let lastCouncilMember: SignerWithAddress;
     let councilMember: CouncilMember;
     let telcoin: TestTelcoin;
     let stream: TestStream;
@@ -18,7 +19,7 @@ describe("CouncilMember", () => {
     let supportRole: string = ethers.keccak256(ethers.toUtf8Bytes("SUPPORT_ROLE"));
 
     beforeEach(async () => {
-        [admin, support, member, holder, target] = await ethers.getSigners();
+        [admin, support, member, holder, target, lastCouncilMember] = await ethers.getSigners();
 
         const TestTelcoinFactory = await ethers.getContractFactory("TestTelcoin", admin);
         telcoin = await TestTelcoinFactory.deploy(admin.address);
@@ -182,6 +183,22 @@ describe("CouncilMember", () => {
                 it("the correct removal is made", async () => {
                     await expect(councilMember.burn(1, support.address)).emit(councilMember, "Transfer");
                 });
+                it.only("inoperable contract after burn", async () => {
+                    await expect(councilMember.mint(lastCouncilMember.address)).to.not.reverted;
+
+                    // This 1st burn will cause contract inoperable due to tokenId & balances misalignment
+                    await expect(councilMember.burn(1, support.address)).emit(councilMember, "Transfer");
+
+                    // Impact 1. holder with tokenId > balances length cannot claim
+                    await expect(councilMember.connect(lastCouncilMember).claim(3, 1)).to.revertedWithPanic("0x32"); // @audit-info 0x32: Array accessed at an out-of-bounds or negative index
+
+                    // Impact 2. subsequent burns of tokenId > balances length will revert
+                    await expect(councilMember.burn(3, lastCouncilMember.address)).to.revertedWithPanic("0x32"); 
+
+                    // Impact 3. subsequent mint will revert due to tokenId collision
+                    await expect(councilMember.mint(lastCouncilMember.address)).to.revertedWithCustomError(councilMember, "ERC721InvalidSender");
+
+                });
             });
         });
 

```

### Result 
>   CouncilMember
>     mutative
>       burn
>         Success
>           ✔ inoperable contract after burn (90ms)
>   1 passing (888ms)

The Passing execution of the POC confirmed that operations such as `claim`, `burn` & `mint` were all reverted which make the contract inoperable.

## Impact
The severity of the vulnerability is high due to the high likelihood of occurence and the critical impacts on the contract's operability and token holders' ability to interact with their assets. 

## Code Snippet
https://github.com/sherlock-audit/2024-01-telcoin/blob/main/telcoin-audit/contracts/sablier/core/CouncilMember.sol#L220

## Tool used
VsCode

## Recommendation
It is recommended to avoid popping out balances to keep alignment with uniquely minted tokenId. Alternatively, consider migrating to ERC1155, which inherently manages a built-in balance for each NFT.



## Discussion

**sherlock-admin2**

1 comment(s) were left on this issue during the judging contest.

**takarez** commented:
>  valid because { this is a valid findings because the watson explain how again the burn function will break a functionality just like the previous issue thus making it a dupp of 109}



**nevillehuang**

See comments [here](https://github.com/sherlock-audit/2024-01-telcoin-judging/issues/32) for duplication reasons.

**amshirif**

https://github.com/telcoin/telcoin-audit/pull/31

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Telcoin Platform Audit |
| Report Date | N/A |
| Finders | Aamirusmani1552, DenTonylifer, fibonacci, sobieski, 0xAsen, tives, grearlake, sonny2k, zzykxx, gqrp, psb01, 0xpep7, popeye, ydlee, jah, 0xadrii, alexbabits, m4ttm, VAD37, IvanFitro, Bauer, r0ck3tz, ggg\_ttt\_hhh, mstpr-brainbot, sakshamguruji, Arz, Ignite, araj, vvv, Jaraxxus, bitsurfer, ravikiran.web3, 0xLogos, Krace, 0xmystery, BAICE, 0xlamide, Kow, almurhasan, dipp, zhuying, HonorLt, ubl4nk |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-01-telcoin-judging/issues/199
- **Contest**: https://app.sherlock.xyz/audits/contests/156

### Keywords for Search

`ERC721`

