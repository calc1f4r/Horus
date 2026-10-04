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
solodit_id: 31616
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

[M-04] Disabling of cooldown during post-slash can be bypassed

### Overview


This bug report states that there is a medium severity bug in the `StakedToken` contract that allows a staker to bypass the disabling of the cooldown function during the post-slashing period. This means that the staker can still activate the cooldown even though it is supposed to be disabled. This can happen when the staker transfers the token to another account that has a valid cooldown timestamp. The code in question uses a weighted average to set the receiving account's cooldown timestamp, allowing the staker to activate the cooldown for the transferred token. The report recommends disabling the transfer of `StakedToken` during the post-slashing period to prevent this bypass.

### Original Finding Content

**Severity**

**Impact:** Medium, as staker can bypass disabling of cooldown

**Likelihood:** Medium, during the post slash period

**Description**

When `StakedToken` is in the post-slashing state, the cooldown function is disabled, preventing the staker from activating it by setting `_stakersCooldowns[msg.sender] = block.timestamp`.

However, the staker can possibly bypass the disabling of the cooldown function by transferring to another account that has a valid cooldown timestamp.

That is because when `fromCooldownTimestamp` is expired/not-set and `toCooldownTimestamp` is valid, the weighted average will be set for the receiving account's cooldown timestamp.

That will allow the staker to activate the cooldown for the staked token sent from the sending account.

```Solidity
    function getNextCooldownTimestamp(
        uint256 fromCooldownTimestamp,
        uint256 amountToReceive,
        address toAddress,
        uint256 toBalance
    ) public view returns (uint256) {
        uint256 toCooldownTimestamp = _stakersCooldowns[toAddress];
        if (toCooldownTimestamp == 0) return 0;

        uint256 minimalValidCooldownTimestamp = block.timestamp - COOLDOWN_SECONDS - UNSTAKE_WINDOW;

        //@audit when `toCooldownTimestamp` is still valid, this will continue to next line
        if (minimalValidCooldownTimestamp > toCooldownTimestamp) return 0;

        //@audit when `fromCooldownTimestamp` has expired/not set, it will be set to current time
        if (minimalValidCooldownTimestamp > fromCooldownTimestamp) {
            fromCooldownTimestamp = block.timestamp;
        }
        //@audit weighted-average will be set for recieving account, when `toCooldownTimestamp` is still valid
        //       and this will activate cooldown for the sent amount
        if (fromCooldownTimestamp >= toCooldownTimestamp) {
            toCooldownTimestamp = (amountToReceive * fromCooldownTimestamp + (toBalance * toCooldownTimestamp))
                / (amountToReceive + toBalance);
        }

        return toCooldownTimestamp;
    }
```

**Recommendations**

Disable transfer of `StakedToken` during post-slashing state to prevent bypassing of the disabling of cooldown.

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

