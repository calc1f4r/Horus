---
# Core Classification
protocol: Super DCA Liquidity Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63422
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1171
source_link: none
github_link: https://github.com/sherlock-audit/2025-09-super-dca-judging/issues/1065

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
finders_count: 153
finders:
  - 0xpetern
  - 0xAadi
  - Aamirusmani1552
  - Artur
  - Chonkov
---

## Vulnerability Title

H-4: Bucket rewards will be wiped by stake/unstake before accrueRewards, lastRewardIndex resets without settling rewards, accrueRewards delta becomes 0

### Overview


This bug report discusses a vulnerability found in the SuperDCAStaking contract, which can result in a loss of accrued rewards for stakers. The root cause of the issue is that the contract resets the lastRewardIndex in stake/unstake without settling pending rewards, which can be exploited by calling stake/unstake right before accrueReward. This will cause the delta to be set to zero, resulting in a loss of rewards for users. The impact of this bug is considered high, as it can lead to a complete loss of rewards for stakers. The report also includes a PoC (proof of concept) test to demonstrate the issue and suggests a mitigation to fix the bug. The protocol team has already fixed this issue in the SuperDCAStaking contract.

### Original Finding Content


Source: https://github.com/sherlock-audit/2025-09-super-dca-judging/issues/1065 

## Found by 
0x00T1, 0xAadi, 0xAdwa, 0xB4nkz, 0xCrypt0nite, 0xCuru, 0xDemon, 0xDjango, 0xHexed, 0xImmortan, 0xaxaxa, 0xleo, 0xlookman, 0xpetern, 0xsolisec, 0xv1bh4, 0xzen, 33audits, 4Nescient, 8olidity, Aamirusmani1552, Al-Qa-qa, Almanax, Arav, Artur, BADROBINX, BengalCatBalu, Bobai23, Boy2000, BoyD, Chonkov, CodexBugmeNot, DemiGods, DuoSec, FonDevs, HeckerTrieuTien, Hunter, Hurricane, Icon\_0x, Ironsidesec, IzuMan, JeRRy0422, JohnTPark24, JohnWeb3, Josh4324, JuggerNaut, KiroBrejka, LonWof-Demon, MysteryAuditor, NHristov, Orhukl, OxSath404, Phaethon, R, Ragnarok, Razkky, SMB62, SOPROBRO, S\_722, Sa1ntRobi, ScarletFir, Siiiisivan, SuperDevFavour, Whiterabbit, WillyCode20, Y4nhu1, Yaneca\_b, ZeroEx, Ziusz, alexbabits, algiz, aman, ami, axelot, bam0x7, bbl4de, cholakovvv, dani3l526, deadmanwalking, denys\_sosnovskyi, derastephh, djshaneden, drdee, farman1094, fullstop, futureHack, gneiss, grigorovv17, harry, heavyw8t, hjo, illoy\_sci, itsRavin, ivanalexandur, jah, jayjoshix, jo13, kangaroo, kazan, ke1caM, kimnoic, kimonic, maigadoh, makeWeb3safe, marcosecure0x, merlin, mingzoox, ni8mare, nonso72, oct0pwn, omeiza, oot2k, patitonar, peazzycole, pindarev, pollersan, prosper, proxima\_centuri, pv, r1ver, rashmor, resosiloris, rsam\_eth, sedare, shiazinho, shieldrey, silver\_eth, slavina, softdev0323, soloking, sourav\_DEV, surenyan-oks, taticuvostru, techOptimizor, theholymarvycodes, thekmj, theweb3mechanic, tinnohofficial, tobi0x18, typicalHuman, ubl4nk, udo, v10g1, v\_2110, vinica\_boy, vivekd, volleyking, whitehair0330, wickie, x0t0wt1w, xxiv, yeahChibyke, zcai

### Summary

The contract resets a token bucket’s lastRewardIndex in stake / unstake without first settling pending rewards, this will cause a complete loss of accrued rewards for stakers as any user can call stake/unstake right before accrueReward and this will zero the bucket’s delta.

### Root Cause

Inside SuperDCAStaking::[accrueReward](https://github.com/sherlock-audit/2025-09-super-dca/blob/main/super-dca-gauge/src/SuperDCAStaking.sol#L284) we subtract the info.lastRewardIndex from rewardIndex, however inside stake/unstake we set lastRewardIndex == rewardIndex:

```solidity
    function unstake(address token, uint256 amount) external override {
        // Validate amount is non-zero and available
        if (amount == 0) revert SuperDCAStaking__ZeroAmount();

        // Check both token bucket and user balances are sufficient
        TokenRewardInfo storage info = tokenRewardInfoOf[token];
        if (info.stakedAmount < amount) revert SuperDCAStaking__InsufficientBalance();
        if (userStakes[msg.sender][token] < amount) revert SuperDCAStaking__InsufficientBalance();

        // Update global reward index to current time
        _updateRewardIndex();

        // Update token bucket accounting and user stakes
        info.stakedAmount -= amount;
    @>    info.lastRewardIndex = rewardIndex;

        totalStakedAmount -= amount;
        userStakes[msg.sender][token] -= amount;

        // Remove token from user's set if balance reaches zero
        if (userStakes[msg.sender][token] == 0) {
            userTokenSet[msg.sender].remove(token);
        }

        // Transfer SuperDCA tokens back to user
        IERC20(DCA_TOKEN).transfer(msg.sender, amount);
        emit Unstaked(token, msg.sender, amount);
    }


```

If stake/unstake were to be called just before accrueRewards the system "forgets" about past rewards and can make the accrueRewards return zero leading to 100% lost rewards for users.

### Internal Pre-conditions

Somebody called stake unstake before the hook _beforeAddLiquidity calls _handleDistributionAndSettlement

### External Pre-conditions

-

### Attack Path

1. Lets say lastIndex is 50, Index now will be 100, user or attacker calls stake/unstake just before _beforeAddLiquidity is triggered.
2. lastIndex becomes 100
3. _beforeAddLiquidity calls into accrueReward, because delta is `uint256 delta = rewardIndex - info.lastRewardIndex;` and stake/unstake was called before than, delta results is a small number or even 0 so basically no rewards




### Impact

High, the system forgets about past rewards, users will lose up to 100% of their rewards.

### PoC

Inside SuperDCAStaking.t.sol::TokenRewardInfos, copy paste this test:

```solidity
    function test_PoC_UnstakeBeforeAccrue_WipesBucketDelta() public {
        // Set up a single bucket stake
        vm.prank(user);
        staking.stake(tokenA, 100e18);

        // Let rewards accrue
        uint256 start = staking.lastMinted();
        uint256 secs = 100;
        vm.warp(start + secs);

        //what should be paid 
        uint256 expectedMint = secs * rate;
        assertGt(expectedMint, 0, "sanity");

        // Unstake before accrue resets bucket lastRewardIndex and wipes  delta
        vm.prank(user);
        staking.unstake(tokenA, 1);

        // Accrue now => pays 0 due to wiped delta
        vm.prank(gauge);
        uint256 paid = staking.accrueReward(tokenA);
        assertEq(paid, 0, "pending bucket rewards wiped by unstake reset");
    }
```

Run with `forge test --match-test test_PoC_UnstakeBeforeAccrue_WipesBucketDelta -vvvv`

Console.logs:
```solidity
   └─ ← [Return] 0
    ├─ [0] VM::assertEq(0, 0, "pending bucket rewards wiped by unstake reset") [staticcall]
    │   └─ ← [Return]
    └─ ← [Stop]
```

### Mitigation

Make the contract remember the passed rewards even after stake unstake has been called 

## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/Super-DCA-Tech/super-dca-gauge/pull/41






### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Super DCA Liquidity Network |
| Report Date | N/A |
| Finders | 0xpetern, 0xAadi, Aamirusmani1552, Artur, Chonkov, 0xDemon, udo, ami, 0xlookman, 0xaxaxa, Orhukl, Boy2000, LonWof-Demon, soloking, taticuvostru, Bobai23, omeiza, x0t0wt1w, prosper, WillyCode20, kazan, maigadoh, kangaroo, pollersan, bam0x7, v10g1, Ragnarok, pindarev, JohnTPark24, SOPROBRO, Al-Qa-qa, harry, ZeroEx, 4Nescient, r1ver, CodexBugmeNot, Hurricane, JeRRy0422, softdev0323, djshaneden, Ziusz, hjo, algiz, illoy\_sci, jayjoshix, 0xAdwa, 0xHexed, silver\_eth, theholymarvycodes, shieldrey, deadmanwalking, wickie, itsRavin, gneiss, sourav\_DEV, patitonar, futureHack, 0xImmortan, typicalHuman, bbl4de, alexbabits, mingzoox, fullstop, 0xCuru, BoyD, Icon\_0x, volleyking, tinnohofficial, Razkky, drdee, techOptimizor, yeahChibyke, proxima\_centuri, zcai, R, Whiterabbit, S\_722, Siiiisivan, Almanax, 0xsolisec, ni8mare, cholakovvv, marcosecure0x, nonso72, derastephh, SMB62, OxSath404, axelot, 0xzen, 0xCrypt0nite, grigorovv17, DuoSec, kimonic, 0xv1bh4, xxiv, Arav, DemiGods, 0xleo, 0x00T1, dani3l526, sedare, Y4nhu1, peazzycole, JohnWeb3, ScarletFir, SuperDevFavour, ke1caM, jo13, 0xDjango, makeWeb3safe, denys\_sosnovskyi, FonDevs, rashmor, farman1094, 33audits, 8olidity, 0xB4nkz, MysteryAuditor, shiazinho, Phaethon, pv, heavyw8t, thekmj, merlin, ubl4nk, Sa1ntRobi, HeckerTrieuTien, tobi0x18, whitehair0330, oct0pwn, surenyan-oks, v\_2110, aman, ivanalexur, JuggerNaut, jah, IzuMan, BengalCatBalu, theweb3mechanic, slavina, vinica\_boy, resosiloris, Ironsidesec, KiroBrejka, vivekd, BADROBINX, rsam\_eth, Yaneca\_b, NHristov, Hunter, kimnoic, oot2k, Josh4324 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2025-09-super-dca-judging/issues/1065
- **Contest**: https://app.sherlock.xyz/audits/contests/1171

### Keywords for Search

`vulnerability`

