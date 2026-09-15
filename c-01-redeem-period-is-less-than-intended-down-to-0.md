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
solodit_id: 31607
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Increment-security-review.md
github_link: none

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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[C-01] Redeem period is less than intended down to 0

### Overview


The report is about a bug in a system where users are unable to redeem their StakedTokens if the cooldown period is twice as long as the unstake window. This means that the underlying tokens are stuck and cannot be accessed by the user. The likelihood of this bug occurring is high due to a calculation mistake. The recommended solution is to refactor the check in the system.

### Original Finding Content

**Severity**

**Impact:** High, StakedTokens are not redeemable in case the cooldown period is 2 times greater than unstake window, therefore underlying tokens are stuck forever

**Likelihood:** High, calculation mistake on redeem

**Description**

To redeem StakedToken, the user needs to submit a request to `cooldown()` and wait time of `COOLDOWN_SECONDS`.
Then he should be able to redeem for a period of `UNSTAKE_WINDOW` after cooldown.

However, this check underestimates the open window by `2 * COOLDOWN_SECONDS`:

```solidity
    function _redeem(address from, address to, uint256 amount) internal {
        ...

        // Users can redeem without waiting for the cooldown period in a post-slashing state
        if (!isInPostSlashingState) {
            // Make sure the user's cooldown period is over and the unstake window didn't pass
            uint256 cooldownStartTimestamp = _stakersCooldowns[from];
            if (block.timestamp < cooldownStartTimestamp + COOLDOWN_SECONDS) {
                revert StakedToken_InsufficientCooldown(cooldownStartTimestamp + COOLDOWN_SECONDS);
            }
@>          if (block.timestamp - cooldownStartTimestamp + COOLDOWN_SECONDS > UNSTAKE_WINDOW) {
                revert StakedToken_UnstakeWindowFinished(cooldownStartTimestamp + COOLDOWN_SECONDS + UNSTAKE_WINDOW);
            }
        }

        // ... redeem logic
    }
```

[Here you can see PoC](https://gist.github.com/T1MOH593/e0a5424ca14facb3661b78c3d14530b1)

**Recommendations**

Refactor check to:

```diff
-          if (block.timestamp - cooldownStartTimestamp + COOLDOWN_SECONDS > UNSTAKE_WINDOW) {
+          if (block.timestamp - cooldownStartTimestamp - COOLDOWN_SECONDS > UNSTAKE_WINDOW) {
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

