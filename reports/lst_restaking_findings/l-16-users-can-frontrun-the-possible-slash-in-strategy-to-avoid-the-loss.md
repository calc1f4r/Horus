---
# Core Classification
protocol: Elytra_2025-07-27
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63594
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-27.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-16] Users can frontrun the possible slash in strategy to avoid the loss

### Overview

See description below for full details.

### Original Finding Content


_Resolved_

When users withdraw assets or request to withdraw assets, we will calculate the current total asset tvl and get the share's price.

In our strategy, we will stake assets with validators. The strategy will get some rewards and maybe some potential slash according to validators' behavior. The code below is a simulation of behavior from H_02.t.sol.

Users can monitor the related validators' performance, and withdraw or request withdraw before there is a possible slashing. Users can avoid the potential loss.

```solidity
    function generateYield(address asset, uint256 yieldAmount) external {
        accumulatedYield[asset] += yieldAmount;
    }

    // Simulate slashing/loss
    function simulateSlashing(address asset, uint256 lossAmount) external {
        uint256 totalBalance = deposits[asset] + accumulatedYield[asset];
        if (lossAmount >= totalBalance) {
            deposits[asset] = 0;
            accumulatedYield[asset] = 0;
        } else {
            // Reduce from yield first, then from deposits
            // We will reduct the yield at first, then reduct the principle here.
            if (accumulatedYield[asset] >= lossAmount) {
                accumulatedYield[asset] -= lossAmount;
            } else {
                uint256 fromYield = accumulatedYield[asset];
                uint256 fromDeposits = lossAmount - fromYield;
                accumulatedYield[asset] = 0;
                deposits[asset] -= fromDeposits;
            }
        }
    }

```

**Recommendations**

When users request withdrawal, record the current share's price. When users finish withdrawal, we should check the latest share's price. If the latest share's price is less than the recorded share price, the users should incur some loss.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Elytra_2025-07-27 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Elytra-security-review_2025-07-27.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

