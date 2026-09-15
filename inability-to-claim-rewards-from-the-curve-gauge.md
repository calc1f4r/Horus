---
# Core Classification
protocol: Notional Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63525
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Notional%20Finance/Notional%20v4/README.md#1-inability-to-claim-rewards-from-the-curve-gauge
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

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - insurance

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Inability to Claim Rewards From the Curve Gauge

### Overview


The report highlights a bug in the CurveConvex2Token._unstakeLpTokens() function, where users are not able to claim rewards when withdrawing from the Curve gauge. This is because the function does not include the _claim_rewards flag, which is needed to claim rewards during the withdraw call. This results in users losing accrued rewards and reduces the effective yield. The recommendation is to create a reward manager for the Curve gauge to handle rewards claiming and distributing CRV through the standard reward distribution mechanism. The issue has been fixed in a recent pull request.

### Original Finding Content

##### Description
The `CurveConvex2Token._unstakeLpTokens()` function calls `ICurveGauge(CURVE_GAUGE).withdraw(poolClaim)`, which takes only the `poolClaim` parameter. However, the Curve gauge `withdraw()` function supports an optional `_claim_rewards` flag, which allows claiming rewards during the withdraw call:

```python
@external
@nonreentrant('lock')
def withdraw(_value: uint256, _claim_rewards: bool = False):
```

As implemented, the strategy does not claim rewards when withdrawing from the gauge, so users do not automatically receive accrued rewards when exiting positions.

```solidity
function _unstakeLpTokens(uint256 poolClaim) internal {
    if (CONVEX_REWARD_POOL != address(0)) {
        bool success = IConvexRewardPool(CONVEX_REWARD_POOL).
            withdrawAndUnwrap(poolClaim, false);
        require(success);
    } else {
        ICurveGauge(CURVE_GAUGE).withdraw(poolClaim);
    }
}
```

Although `withdrawAndUnwrap()` also does not claim rewards on unstakes for Convex, Convex strategies are wired to the `ConvexRewardManager` contract that later claims and distributes rewards to users. In contrast, pure Curve gauge strategies do not have such a manager configured, therefore, users cannot claim gauge rewards and lose a material portion of APR.

This issue is classified as **High** severity because users lose accrued rewards and effective yield is reduced.

##### Recommendation
We recommend creating a reward manager for the Curve gauge that handles rewards claiming and distributing CRV via the standard reward distribution mechanism.

> **Client's Commentary:**
> Fixed in this PR: https://github.com/notional-finance/notional-v4/pull/28

---


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Notional Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Notional%20Finance/Notional%20v4/README.md#1-inability-to-claim-rewards-from-the-curve-gauge
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

