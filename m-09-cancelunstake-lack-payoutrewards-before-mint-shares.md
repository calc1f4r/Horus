---
# Core Classification
protocol: Reserve
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27341
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-06-reserve
source_link: https://code4rena.com/reports/2023-06-reserve
github_link: https://github.com/code-423n4/2023-06-reserve-findings/issues/10

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
  - cdp
  - yield
  - launchpad
  - privacy

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - 0xA5DF
  - ronnyx2017
  - rvierdiiev
---

## Vulnerability Title

[M-09] `cancelUnstake` lack `payoutRewards` before mint shares

### Overview


A bug was discovered in the `cancelUnstake` function of the StRSR protocol, which allowed users to withdraw from the unstake queue without calling `payoutRewards` and receive more rewards than they should have. This could have resulted in users receiving rewards that did not belong to them.

A proof of concept test was conducted to demonstrate the bug, and the results showed that users who called `payoutRewards` before `cancelUnstake` received fewer rewards than those who called `cancelUnstake` before `payoutRewards`.

To mitigate this issue, the protocol team proposed calling `payoutRewards` before minting shares. This was confirmed by the team and a pull request was made to implement the mitigation. The mitigation was confirmed and the full details can be found in reports from the team.

### Original Finding Content


`cancelUnstake` will cancel the withdrawal request in the queue can mint shares as the current `stakeRate`. But it doesn't `payoutRewards` before `mintStakes`. Therefor it will mint stRsr as a lower rate, which means it will get more rsr.

### Impact

Withdrawers in the unstake queue can `cancelUnstake` without calling `payoutRewards` to get more rsr rewards that should not belong to them.

### Proof of Concept

POC test/ZZStRSR.test.ts git patch

```patch
diff --git a/test/ZZStRSR.test.ts b/test/ZZStRSR.test.ts
index ecc31f68..b2809129 100644
--- a/test/ZZStRSR.test.ts
+++ b/test/ZZStRSR.test.ts
@@ -1333,6 +1333,46 @@ describe(`StRSRP${IMPLEMENTATION} contract`, () => {
       expect(await stRSR.exchangeRate()).to.be.gt(initialRate)
     })
 
+    it('cancelUnstake', async () => {
+      const amount: BigNumber = bn('10e18')
+
+      // Stake
+      await rsr.connect(addr1).approve(stRSR.address, amount)
+      await stRSR.connect(addr1).stake(amount)
+      await rsr.connect(addr2).approve(stRSR.address, amount)
+      await stRSR.connect(addr2).stake(amount)
+      await rsr.connect(addr3).approve(stRSR.address, amount)
+      await stRSR.connect(addr3).stake(amount)
+
+      const  initExchangeRate = await stRSR.exchangeRate();
+      console.log(initExchangeRate);
+
+      // Unstake addr2 & addr3 at same time (Although in different blocks, but timestamp only 1s)
+      await stRSR.connect(addr2).unstake(amount)
+      await stRSR.connect(addr3).unstake(amount)
+
+      // skip 1000 block PERIOD / 12000s
+      await setNextBlockTimestamp(Number(ONE_PERIOD.mul(1000).add(await getLatestBlockTimestamp())))
+
+      // Let's cancel the unstake in normal
+      await expect(stRSR.connect(addr2).cancelUnstake(1)).to.emit(stRSR, 'UnstakingCancelled')
+      let exchangeRate = await stRSR.exchangeRate();
+      expect(exchangeRate).to.equal(initExchangeRate)
+      
+      // addr3 cancelUnstake after payoutRewards
+      await stRSR.payoutRewards()
+      await expect(stRSR.connect(addr3).cancelUnstake(1)).to.emit(stRSR, 'UnstakingCancelled')
+
+      // Check balances addr2 & addr3
+      exchangeRate = await stRSR.exchangeRate();
+      expect(exchangeRate).to.be.gt(initExchangeRate)
+      const addr2NowAmount = exchangeRate.mul(await stRSR.balanceOf(addr2.address)).div(bn('1e18'));
+      console.log("addr2", addr2NowAmount.toString());
+      const addr3NowAmount = exchangeRate.mul(await stRSR.balanceOf(addr3.address)).div(bn('1e18'));
+      console.log("addr3",addr3NowAmount.toString());
+      expect(addr2NowAmount).to.gt(addr3NowAmount)
+    })
+
     it('Rewards should not be handed out when paused but staking should still work', async () => {
       await main.connect(owner).pauseTrading()
       await setNextBlockTimestamp(Number(ONE_PERIOD.add(await getLatestBlockTimestamp())))

```

The test simulates two users unstake and cancelUnstake operations at the same time.But the addr2 calls payoutRewards after his cancelUnstake. And addr3 calls cancelUnstake after payoutRewards. Addr2 gets more rsr than addr3 in the end.

run test:

    PROTO_IMPL=1 npx hardhat test --grep cancelUnstake test/ZZStRSR.test.ts

log:

      StRSRP1 contract
        Add RSR / Rewards
    BigNumber { value: "1000000000000000000" }
    addr2 10005345501258588240
    addr3 10000000000000000013

### Recommended Mitigation Steps

Call `_payoutRewards` before mint shares.

**[tbrent (Reserve) confirmed and commented](https://github.com/code-423n4/2023-06-reserve-findings/issues/10#issuecomment-1589913989):**
 > Agree with severity and proposed mitigation.

**[Reserve mitigated](https://github.com/code-423n4/2023-08-reserve-mitigation#individual-prs):**
> Payout rewards during cancelUnstake.<br>
> PR: https://github.com/reserve-protocol/protocol-private/pull/3

**Status:** Mitigation confirmed. Full details in reports from [rvierdiiev](https://github.com/code-423n4/2023-08-reserve-mitigation-findings/issues/16), [0xA5DF](https://github.com/code-423n4/2023-08-reserve-mitigation-findings/issues/33), and [ronnyx2017](https://github.com/code-423n4/2023-08-reserve-mitigation-findings/issues/26) - and also shared below in the [Mitigation Review](#mitigation-review) section.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Reserve |
| Report Date | N/A |
| Finders | 0xA5DF, ronnyx2017, rvierdiiev |

### Source Links

- **Source**: https://code4rena.com/reports/2023-06-reserve
- **GitHub**: https://github.com/code-423n4/2023-06-reserve-findings/issues/10
- **Contest**: https://code4rena.com/reports/2023-06-reserve

### Keywords for Search

`vulnerability`

