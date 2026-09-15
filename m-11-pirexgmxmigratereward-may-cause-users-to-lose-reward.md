---
# Core Classification
protocol: Redacted Cartel
chain: everychain
category: uncategorized
vulnerability_type: migration_loss

# Attack Vector Details
attack_type: migration_loss
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6048
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-11-redacted-cartel-contest
source_link: https://code4rena.com/reports/2022-11-redactedcartel
github_link: https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/249

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - migration_loss

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - bin2chen
---

## Vulnerability Title

[M-11] PirexGmx#migrateReward() may cause users to lose Reward.

### Overview


This bug report is about a vulnerability in the PirexGmx.sol contract. It has been identified that the current migration process, which involves calling #completemigration() followed by #migrateward(), can cause users to lose rewards if AutoPxGmx#compound() is called by a bot. 

The issue is that the producer of PirexRewards.sol remains the old PirexGmx, which can still execute two lines of code (https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/PirexGmx.sol#L824-L828 and https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/PirexGmx.sol#L940-L949). This can lead to the old PirexGmx#claimRewards() being called, which will return zero rewards and the reward of AutopXGMX will be lost.

There are two recommended mitigation steps to solve this issue. The first is to set the producer of PirexRewards to the new PirexGmx in completeMigration(). The second is to set the old PirexGmx's "pirexRewards" to address(0) in #migrateReward(), so that it cannot be used to get rewards.

### Original Finding Content


`PirexGmx#migrateReward()` may cause users to lose Reward before PirexRewards.sol set new PirexGmx.

### Proof of Concept

The current migration process is: `call # completemigration ()-> # migrateward ()`

After this method, the producer of PirexRewards.sol contract is still the old PirexGmx.

At this time, if `AutoPxGmx#compound ()` is called by bot:

`AutoPxGmx#compound() -> PirexRewards#.claim() -> old_PirexGmx#claimRewards()`

`Old_PirexGmx#claimRewards ()` will return zero rewards and the reward of AutopXGMX will be lost.

Old PirexGmx still can execute
<https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/PirexGmx.sol#L824-L828>

<https://github.com/code-423n4/2022-11-redactedcartel/blob/03b71a8d395c02324cb9fdaf92401357da5b19d1/src/PirexGmx.sol#L940-L949>

### Recommended Mitigation Steps

There are two ways to solve the problem.

1.  Set the producer of PirexRewards to the new PirexGmx in `completeMigration ()`.
2.  In `#migrateReward ()`, set the old PirexGmx's "pirexRewards" to `address(0)`, so that you can't use the old PirexGmx to get rewards

Simply use the second, such as:

```solidity
    function migrateReward() external whenPaused {
        if (msg.sender != migratedTo) revert NotMigratedTo();
        if (gmxRewardRouterV2.pendingReceivers(address(this)) != address(0))
            revert PendingMigration();

        // Transfer out any remaining base reward (ie. WETH) to the new contract
        gmxBaseReward.safeTransfer(
            migratedTo,
            gmxBaseReward.balanceOf(address(this))
        );
+       pirexRewards ==address(0);   //*** set pirexRewards=0,Avoid claimRewards () being called by mistake.***//
    }
```

**[drahrealm (Redacted Cartel) confirmed](https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/249)** 

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Redacted Cartel |
| Report Date | N/A |
| Finders | bin2chen |

### Source Links

- **Source**: https://code4rena.com/reports/2022-11-redactedcartel
- **GitHub**: https://github.com/code-423n4/2022-11-redactedcartel-findings/issues/249
- **Contest**: https://code4rena.com/contests/2022-11-redacted-cartel-contest

### Keywords for Search

`Migration Loss`

