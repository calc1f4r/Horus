---
# Core Classification
protocol: Holder Incentive Program
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52240
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/dynex/holder-incentive-program
source_link: https://www.halborn.com/audits/dynex/holder-incentive-program
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Unsafe Downcasting of Rewards in restake Function

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `DynexHolderIncentiveProgram`contract performs unsafe downcasting from `uint128` to `uint64` in the `restake()` and `exit()` functions when handling user rewards. This causes silent truncation of reward values that exceed the maximum value of uint64 (e.g.: **2^64 - 1**):

```
    function restake() public whenNotPaused updateReward(msg.sender) {
        uint64 reward = uint64(usersInfo[msg.sender].reward);
        // ... // 
```

  

```
function exit() external 
{
         withdraw(uint64(usersInfo[msg.sender].balance));
         getReward();     
} 
```

  

The contract stores user rewards as `uint128` in the `UserInfo` struct:

```
    struct UserInfo {
        uint256 rewardPerTokenPaid;
        uint128 reward;//E total rewards earned by the user.
        uint128 balance;
```

  

When accumulated rewards exceed **2^64 - 1** (18.446 quintillion), the following security issues occur:

1. The `restake()` function silently truncates rewards above uint64 max, resulting in permanent loss of user rewards
2. The `exit()` function fails to withdraw the full balance due to the same truncation issue
3. Users with large accumulated rewards become unable to use these core contract functions

##### Proof of Concept

This test can be added to `stake.test.ts` :

```
describe("unsafe casting vulnerabilities", () => {
    let defaultAdmin: HardhatEthersSigner,
        rewardsDistribution: HardhatEthersSigner,
        user: HardhatEthersSigner,
        DHIPcontract: DynexHolderIncentiveProgram,
        dnxToken: ERC20Mock,
        userAddress: Address;
  
    const UINT64_MAX = BigInt(2 ** 64) - 1n;
    const stakeAmount = ethers.parseUnits("100000", DNX_DECIMALS);
    
    it("Should deploy and initialize contract", async () => {
      const deployStakingFixture = () => deployStaking(DNX_DECIMALS, ONE_MONTH);
      const deployment = await loadFixture(deployStakingFixture);
      defaultAdmin = deployment.defaultAdmin;
      rewardsDistribution = deployment.rewardsDistribution;
      user = deployment.user;
      DHIPcontract = deployment.DHIPcontract;
      dnxToken = deployment.dnxToken;
      userAddress = await user.getAddress();
    });
  
    it("Should demonstrate unsafe casting with large rewards", async () => {
      // First stake a normal amount
      await dnxToken.connect(user).approve(await DHIPcontract.getAddress(), stakeAmount);
      await DHIPcontract.connect(user).stake(stakeAmount);
  
      // Set up a reward scenario that will lead to large accumulation
      const massiveReward = UINT64_MAX; // Just under the uint64 max
      await dnxToken.connect(defaultAdmin).transfer(await DHIPcontract.getAddress(), massiveReward);
      
      // Set a very short duration to force high reward rate
      await DHIPcontract.connect(defaultAdmin).setRewardsDuration(1); // 1 second duration
      await DHIPcontract.connect(rewardsDistribution).notifyRewardAmount(massiveReward);
  
      // Wait to accumulate rewards
      await skipTime(2);
  
      await dnxToken.connect(defaultAdmin).transfer(await DHIPcontract.getAddress(), massiveReward);
      await DHIPcontract.connect(rewardsDistribution).notifyRewardAmount(massiveReward);

      await skipTime(2);

      const UINT64_MAX2 = BigInt(2 ** 65) - 2n;
      console.log("Rewards for user should be = %s",UINT64_MAX2);
  
      // Try to restake - should fail due to unsafe casting
      DHIPcontract.connect(user).restake();
  
      // Try to exit - should also fail
      DHIPcontract.connect(user).exit();
    });
  });  
```

  

And the result is :

![result-1.png](https://halbornmainframe.com/proxy/audits/images/6744593dbf5356ad47d8403f)

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:L/R:N/S:C (3.1)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:L/R:N/S:C)

##### Recommendation

It is recommended to replace the unsafe casting with safe operations or to not cast at all:

```
function restake() public whenNotPaused updateReward(msg.sender) {
    uint128 reward = usersInfo[msg.sender].reward;
    if (reward > type(uint64).max) revert RewardTooLarge();

    if (reward > 0) {
        usersInfo[msg.sender].reward = 0;
        totalSupply += uint64(reward);
        usersInfo[msg.sender].balance += uint64(reward);
        emit Restake(msg.sender, uint64(reward));
    }
    else {
        revert ZeroAmount();
    }
}
```

  

Similarly for the `exit()` function:

```
function exit() external {
    uint128 balance = usersInfo[msg.sender].balance;
    if (balance > type(uint64).max) revert BalanceTooLarge();

    withdraw(uint64(balance));
    getReward();
}
```

  

Add appropriate error definitions:

```
error RewardTooLarge();
error BalanceTooLarge();
```

##### Remediation

**NOT APPLICABLE:** This contract will be used exactly for `0xDNX` token which has 9 decimals and `HARD_CAP=110000000000000000`. Therefore, the maximum value of tokens can be stored in `uint64`, and the reward less than `HARD_CAP`, so this is not an issue.

##### References

[dynexcoin/DHIPSmartContracts/contracts/DynexHolderIncentiveProgram.sol#L258](https://github.com/dynexcoin/DHIPSmartContracts/blob/audit/contracts/DynexHolderIncentiveProgram.sol#L258)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Holder Incentive Program |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/dynex/holder-incentive-program
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/dynex/holder-incentive-program

### Keywords for Search

`vulnerability`

