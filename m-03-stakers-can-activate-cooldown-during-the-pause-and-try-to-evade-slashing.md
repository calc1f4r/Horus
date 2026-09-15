---
# Core Classification
protocol: Increment
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31615
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Increment-security-review.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] Stakers can activate cooldown during the pause and try to evade slashing

### Overview


The bug report highlights a potential issue with the `StakedToken.cooldown()` function, which is used by stakers to activate a cooldown period before they can withdraw their tokens. The report states that this function is missing a crucial modifier, which means that stakers can activate the cooldown even when the protocol is paused. This can have a high impact as it allows stakers to evade a potential slash event and cause other stakers to pay more for the slashing. The likelihood of this happening is low, but it is still a concerning issue. The report recommends adding the `whenNotPaused` modifier to the function to prevent stakers from exploiting this loophole.

### Original Finding Content

**Severity**

**Impact:** High, as staker can possibly evade the slash event and cause remaining stakers to pay more for the slashing

**Likelihood:** Low, when the protocol is paused, followed by slash event

**Description**

`StakedToken.cooldown()` is missing the `whenNotPaused` modifier. That means stakers can activate cooldown when the protocol is paused.

Stakers could be aware of or anticipate an upcoming slash event due to the pause and attempt to stay within unstake window by activating cooldown when the protocol is paused. As a pause event is an emergency action to mitigate certain risks, there are reasons to believe that a protocol deficit could occur after that, requiring a slash of staked tokens.

By activating cooldown during protocol pause, stakers could try to frontrun the slash event with redemption if it occurs within the unstake window. Those who succeeded in evading the slash event will cause the remaining stakers to pay more for the slashing.

Note that the stakers will be penalized with a reset of the reward multiplier for activating the cooldown, but the benefit of evading slash event will likely outweigh the additional rewards at an emergency pause event.

```Solidity
    //@audit missing whenNotPaused could allow
    function cooldown() external override {
        if (balanceOf(msg.sender) == 0) {
            revert StakedToken_ZeroBalanceAtCooldown();
        }
        if (isInPostSlashingState) {
            revert StakedToken_CooldownDisabledInPostSlashingState();
        }
        //solium-disable-next-line
        _stakersCooldowns[msg.sender] = block.timestamp;

        // Accrue rewards before resetting user's multiplier to 1
        smRewardDistributor.updatePosition(address(this), msg.sender);

        emit Cooldown(msg.sender);
    }
```

**Recommendations**

Add the `whenNotPaused` modifier to `cooldown()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Increment |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Increment-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

