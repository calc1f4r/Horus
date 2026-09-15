---
# Core Classification
protocol: Canto
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27552
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-canto
source_link: https://code4rena.com/reports/2023-10-canto
github_link: https://github.com/code-423n4/2023-10-canto-findings/issues/295

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - maanas
---

## Vulnerability Title

[M-01] The Liquidity mining callpath sidecar owner can pull native tokens from the `Dex`

### Overview


This bug report is about a vulnerability in the Liquidity Mining Path contract of Canto, a decentralized governance protocol. The vulnerability is in the `setConcRewards` and `setAmbRewards` functions, which do not check if the quoted amount of rewards are sent by the caller. This allows the owner to specify any total amount of native coin which are available in the `CrocSwapDex` from which the funds will be used when distributing the rewards. This can be demonstrated by using Hardhat to update TestLiquidityMining.js.

The type of vulnerability is a Rug-Pull, which is when a malicious actor exploits the trust of users to pull out funds from a smart contract.

The recommended mitigation step is to add a `msg.value` check in the rewards function to see that the total value is passed when call the functions. This is demonstrated by the code snippet provided in the report.

Canto has acknowledged and commented that rewards will be set and sent in the same Canto governance proposal.

### Original Finding Content


The owner of the liquidity mining sidecar can pull the native coins that are stored in the `CrocSwapDex` to reward the users.

### Proof of Concept

The `setConcRewards` and `setAmbRewards` functions don't check if the quoted amount of rewards are actually sent by the caller. This allows the owner to specify any total amount of native coin which are available in the `CrocSwapDex` from which the funds will be used when distributing the rewards.

```solidity
    function setConcRewards(bytes32 poolIdx, uint32 weekFrom, uint32 weekTo, uint64 weeklyReward) public payable {
        // require(msg.sender == governance_, "Only callable by governance");
        require(weekFrom % WEEK == 0 && weekTo % WEEK == 0, "Invalid weeks");
        while (weekFrom <= weekTo) {
            concRewardPerWeek_[poolIdx][weekFrom] = weeklyReward;
            weekFrom += uint32(WEEK);
        }
    }
```
<https://github.com/code-423n4/2023-10-canto/blob/40edbe0c9558b478c84336aaad9b9626e5d99f34/canto_ambient/contracts/callpaths/LiquidityMiningPath.sol#L65C7-L72>

```solidity
    function setAmbRewards(bytes32 poolIdx, uint32 weekFrom, uint32 weekTo, uint64 weeklyReward) public payable {
        // require(msg.sender == governance_, "Only callable by governance");
        require(weekFrom % WEEK == 0 && weekTo % WEEK == 0, "Invalid weeks");
        while (weekFrom <= weekTo) {
            ambRewardPerWeek_[poolIdx][weekFrom] = weeklyReward;
            weekFrom += uint32(WEEK);
        }
    }
```
<https://github.com/code-423n4/2023-10-canto/blob/40edbe0c9558b478c84336aaad9b9626e5d99f34/canto_ambient/contracts/callpaths/LiquidityMiningPath.sol#L74-L81>

According to [Ambient Docs](https://docs.ambient.finance/developers/token-transfers#native-ethereum) they allow for deposits in native tokens.

### Demo

Update TestLiquidityMining.js:

The funds added using `hardhat.setBalance()` is being used by the owner to distribute rewards

```diff
diff --git a/canto_ambient/test_canto/TestLiquidityMining.js b/canto_ambient/test_canto/TestLiquidityMining.js
index bd21a32..b917308 100644
--- a/canto_ambient/test_canto/TestLiquidityMining.js
+++ b/canto_ambient/test_canto/TestLiquidityMining.js
@@ -7,6 +7,7 @@ const { time } = require("@nomicfoundation/hardhat-network-helpers");
 var keccak256 = require("@ethersproject/keccak256").keccak256;
 
 const chai = require("chai");
+const { network, ethers } = require("hardhat");
 const abi = new AbiCoder();
 
 const BOOT_PROXY_IDX = 0;
@@ -218,7 +219,6 @@ describe("Liquidity Mining Tests", function () {
 		);
 		tx = await dex.userCmd(2, mintConcentratedLiqCmd, {
 			gasLimit: 6000000,
-			value: ethers.utils.parseUnits("10", "ether"),
 		});
 		await tx.wait();
 
@@ -243,6 +243,17 @@ describe("Liquidity Mining Tests", function () {
 			BigNumber.from("999898351768")
 		);
 
+		let dexBal = await ethers.provider.getBalance(dex.address);
+		expect(dexBal.eq(0)).to.be.eq(true);
+
+		// dex gains native token from other methods
+		await network.provider.send("hardhat_setBalance", [
+			dex.address,
+			ethers.utils.parseEther("2").toHexString(),
+		  ]);
+		dexBal = await ethers.provider.getBalance(dex.address);
+		expect(dexBal.eq(ethers.utils.parseEther("2"))).to.be.eq(true);
+
 		//////////////////////////////////////////////////
 		// SET LIQUIDITY MINING REWARDS FOR CONCENTRATED LIQUIDITY
 		//////////////////////////////////////////////////
```

### Tools Used

Hardhat

### Recommended Mitigation Steps

Add a `msg.value` check in the rewards function to see that the total value is passed when call the functions.

```diff
diff --git a/canto_ambient/contracts/callpaths/LiquidityMiningPath.sol b/canto_ambient/contracts/callpaths/LiquidityMiningPath.sol
index e6c63f7..44dd338 100644
--- a/canto_ambient/contracts/callpaths/LiquidityMiningPath.sol
+++ b/canto_ambient/contracts/callpaths/LiquidityMiningPath.sol
@@ -65,6 +65,7 @@ contract LiquidityMiningPath is LiquidityMining {
     function setConcRewards(bytes32 poolIdx, uint32 weekFrom, uint32 weekTo, uint64 weeklyReward) public payable {
         // require(msg.sender == governance_, "Only callable by governance");
         require(weekFrom % WEEK == 0 && weekTo % WEEK == 0, "Invalid weeks");
+        require((1 +(weekTo - weekFrom) / WEEK) * weeklyReward == msg.value);
         while (weekFrom <= weekTo) {
             concRewardPerWeek_[poolIdx][weekFrom] = weeklyReward;
             weekFrom += uint32(WEEK);
```

### Assessed type

Rug-Pull

**[OpenCoreCH (Canto) acknowledged and commented](https://github.com/code-423n4/2023-10-canto-findings/issues/295#issuecomment-1792892349):**
> Rewards will be set and sent in the same Canto governance proposal.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Canto |
| Report Date | N/A |
| Finders | maanas |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-canto
- **GitHub**: https://github.com/code-423n4/2023-10-canto-findings/issues/295
- **Contest**: https://code4rena.com/reports/2023-10-canto

### Keywords for Search

`vulnerability`

