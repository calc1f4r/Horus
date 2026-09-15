---
# Core Classification
protocol: LoopVaults_2025-04-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58543
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/LoopVaults-security-review_2025-04-30.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Incorrect vesting interest calculation enables MEV attacks

### Overview


The bug report discusses a medium severity issue with a high likelihood of occurring. The problem is with the implementation of a function called `_vestingInterest()`, which is meant to prevent malicious attacks. However, the function is not working correctly as it returns 0 when a certain condition is met and then increases linearly until a certain time has passed. This means that if someone were to call another function called `totalAssets()` after this condition has been met, it would include all the interest earned, making it vulnerable to attacks. The recommendation to fix this issue is to change the calculation in the `_vestingInterest()` function to prevent this from happening.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** High

## Description

Given that the value of the positions is updated only when `updateInterval` time has passed, the interest is vested to prevent MEV attacks.

However, the implementation of `_vestingInterest()` is incorrect, as it returns 0 when `block.timestamp == lastUpdate` and increases linearly until `vestingDuration` is reached. This means that calling `totalAssets()` just after an update will include all the interest accrued, which makes the update subject to MEV attacks.

```solidity
    function totalAssets() public view override returns (uint256) {
        return lastTotalAssets - _vestingInterest();
    }

    function _vestingInterest() internal view returns (uint256) {
        if (block.timestamp - lastUpdate >= vestingDuration) return 0;

        uint256 __vestingInterest = (block.timestamp - lastUpdate) * vestingInterest / vestingDuration;
        return __vestingInterest;
    }
```

## Recommendations

```diff
-       uint256 __vestingInterest = (block.timestamp - lastUpdate) * vestingInterest / vestingDuration;
+	uint256 __vestingInterest = (vestingDuration - (block.timestamp - lastUpdate)) * vestingInterest / vestingDuration;
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | LoopVaults_2025-04-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/LoopVaults-security-review_2025-04-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

