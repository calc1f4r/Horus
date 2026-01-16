---
# Core Classification
protocol: Gitcoin Passport
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31157
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-03-gitcoin
source_link: https://code4rena.com/reports/2024-03-gitcoin
github_link: https://github.com/code-423n4/2024-03-gitcoin-findings/issues/9

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
finders_count: 4
finders:
  - 0xDING99YA
  - Stormy
  - oakcobalt
---

## Vulnerability Title

[H-01] `userTotalStaked` invariant will be broken due to vulnerable implementations in `release()`

### Overview


This bug report highlights an issue with the `userTotalStaked` calculation in the `release()` function of the `IdentityStaking` contract. Due to this error, users may lose funds when trying to withdraw their staked amount. The report includes a proof of concept showcasing the incorrect calculation and provides a suggested mitigation step. The bug has been confirmed and marked as high severity. Gitcoin has since mitigated the issue by updating the calculation in the `release()` function. 

### Original Finding Content


`userTotalStaked` invariant will be broken due to vulnerable implementations in `release()`. Users might lose funds due to underflow errors in withdraw methods.

### Proof of Concept

According to the [readme](https://github.com/code-423n4/2024-03-gitcoin/tree/main), `userTotalStaked` invariant should always hold true:

`userTotalStaked[address] = selfStakes[address].amount + sum(communityStakes[address][x].amount for all x staked on by this address)`

However, this can be broken in `release()` flow due to `userTotalStaked` is not updated together with `selfStakes[address].amount` or `communityStakes[address][x].amount`.

```solidity
//id-staking-v2/contracts/IdentityStaking.sol
  function release(
    address staker,
    address stakee,
    uint88 amountToRelease,
    uint16 slashRound
  ) external onlyRole(RELEASER_ROLE) whenNotPaused {
...
    if (staker == stakee) {
...
      selfStakes[staker].slashedAmount -= amountToRelease;
      //@audit selfStakes[staker].amount is updated but `userTotalStaked` is not
|>    selfStakes[staker].amount += amountToRelease;
    } else {
...
      communityStakes[staker][stakee].slashedAmount -= amountToRelease;
      //@audit communityStakes[staker].amount is updated but `userTotalStaked` is not
|>    communityStakes[staker][stakee].amount += amountToRelease;
    }
...
```

https://github.com/code-423n4/2024-03-gitcoin/blob/6529b351cd72a858541f60c52f0e5ad0fb6f1b16/id-staking-v2/contracts/IdentityStaking.sol#L562-L563

For comparison, in other flows such as staking, withdrawing and slashing, `userTotalStaked` is always updated in sync with `selfStakes`/`communityStakes`.

POC:

1. Alice `selfStakes()` 100000 ether and `communityStakes()` 100000 at round 1.
2. Alice's `selfStake` and `communityStake` are slashed by 80% each.
3. Alice appealed and was released the full slashed amount. Alice's staked balance is restored to 100000 ether each. But `userTotalStaked` is not restored.
4. Alice's unlocked but cannot withdraw the 100000x2 ether balance due to underflow. She can only withdraw 20000x2 ether.

See test below:

In `id-staking-v2/test/IdentityStaking.ts`, first add `import { PANIC_CODES} from "@nomicfoundation/hardhat-chai-matchers/panic";`. 

Then copy this test inside `describe("slashing/releasing/burning tests", function () {`.

```ts
it.only("userTotalStaked is broken, user lose funds", async function(){
  //Step2: Round1 - slash Alice's self and community stake of 80000 each
  await this.identityStaking
  .connect(this.owner)
  .slash(
    this.selfStakers.slice(0, 1),
    this.communityStakers.slice(0, 1),
    this.communityStakees.slice(0, 1),
    80,
  );
  //Step2: Round1 - Alice's community/self stake is 20000 after slashing
  expect(
    (
      await this.identityStaking.communityStakes(
        this.communityStakers[0],
        this.communityStakees[0],
      )
    ).amount,
  ).to.equal(20000);
  //Step2: Round1 - total slashed amount 80000 x 2
  expect(await this.identityStaking.totalSlashed(1)).to.equal(160000);
  //Step3: Round1 - Alice appealed and full slash amount is released 80000 x 2
  await this.identityStaking
  .connect(this.owner)
  .release(this.selfStakers[0], this.selfStakers[0], 80000, 1);

  await this.identityStaking
  .connect(this.owner)
  .release(this.communityStakers[0], this.communityStakees[0], 80000, 1);


  //Step3: Round1 - After release, Alice has full staked balance 100000 x 2 
  expect((await this.identityStaking.selfStakes(this.selfStakers[0])).amount).to.equal(100000);
  expect((await this.identityStaking.communityStakes(this.communityStakers[0],this.communityStakees[0])).amount).to.equal(100000);
  expect(await this.identityStaking.totalSlashed(1)).to.equal(0);

  // Alice's lock expired
  await time.increase(twelveWeeksInSeconds + 1);
  //Step4: Alice trying to withdraw 100000 x 2 from selfStake and communityStake. Tx reverted with underflow error. 
  await  expect((this.identityStaking.connect(this.userAccounts[0]).withdrawSelfStake(100000))).to.be.revertedWithPanic(PANIC_CODES.ARITHMETIC_UNDER_OR_OVERFLOW);
  await  expect((this.identityStaking.connect(this.userAccounts[0]).withdrawCommunityStake(this.communityStakees[0],100000))).to.be.revertedWithPanic(PANIC_CODES.ARITHMETIC_UNDER_OR_OVERFLOW);
  //Step4: Alice could only withdraw 20000 x 2. Alice lost 80000 x 2.
  await this.identityStaking.connect(this.userAccounts[0]).withdrawSelfStake(20000);
  await this.identityStaking.connect(this.userAccounts[0]).withdrawCommunityStake(this.communityStakees[0],20000);


 })
```

### Tools Used

Hardhat

### Recommended Mitigation Steps

In `release()`, also update `userTotalStaked`.

**[nutrina (Gitcoin) confirmed](https://github.com/code-423n4/2024-03-gitcoin-findings/issues/9#issuecomment-1998055081)**

**[Alex the Entreprenerd (judge) commented](https://github.com/code-423n4/2024-03-gitcoin-findings/issues/9#issuecomment-1999415371):**
 > The warden has shown how, due to incorrect accounting, `userTotalStaked` may end up being less than intended, causing a loss of funds to users.
> 
> Due to the impact, I agree with High Severity.

**[Gitcoin mitigated](https://github.com/code-423n4/2024-03-gitcoin-mitigation?tab=readme-ov-file#mitigations-to-be-reviewed):**
> This [PR](https://github.com/gitcoinco/id-staking-v2/pull/8) fixes the `userTotalStaked` invariant (accounting error) [here](https://github.com/code-423n4/2024-03-gitcoin-findings/issues/9).

**Status:** Mitigation confirmed. Full details in reports from [oakcobalt](https://github.com/code-423n4/2024-03-gitcoin-mitigation-findings/issues/2), [Stormy](https://github.com/code-423n4/2024-03-gitcoin-mitigation-findings/issues/9) and [0xDING99YA](https://github.com/code-423n4/2024-03-gitcoin-mitigation-findings/issues/5).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gitcoin Passport |
| Report Date | N/A |
| Finders | 0xDING99YA, Stormy, oakcobalt |

### Source Links

- **Source**: https://code4rena.com/reports/2024-03-gitcoin
- **GitHub**: https://github.com/code-423n4/2024-03-gitcoin-findings/issues/9
- **Contest**: https://code4rena.com/reports/2024-03-gitcoin

### Keywords for Search

`vulnerability`

