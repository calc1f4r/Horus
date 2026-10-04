---
# Core Classification
protocol: Maple Finance v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17418
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-maplefinance-mapleprotocolv2-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-maplefinance-mapleprotocolv2-securityreview.pdf
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
finders_count: 2
finders:
  - Simone Monica
  - Robert Schneider
---

## Vulnerability Title

Inaccurate accounting of unrealizedLosses during default warning revert

### Overview


This bug report highlights a Denial of Service vulnerability in the removeDefaultWarning function of the LoanManager contract. The triggerDefaultWarning function updates unrealizedLosses with the defaulting loan’s principal_, netInterest_, and netLateInterest_ values. However, when the warning is removed by the _revertDefaultWarning function, only the values of the defaulting loan’s principal and interest are decremented from unrealizedLosses, leaving a discrepancy equal to the amount of netLateInterest_. 

Exploit Scenario: Alice has missed several interest payments on her loan and is about to default. Bob, the poolManager, calls triggerDefaultWarning on the loan to account for the unrealized loss in the system. Alice makes a payment to bring the loan back into good standing, the claim function is triggered, and _revertDefaultWarning is called to remove the unrealized loss from the system. The net value of Alice’s loan’s late interest value is still accounted for in the value of unrealizedLosses. From then on, when users call Pool.withdraw, they will have to exchange more shares than are due for the same amount of assets.

Recommendations: To fix this issue, the value of netLateInterest should be added to the amount decremented from unrealizedLosses when removing the default warning from the system. Additionally, robust unit tests and fuzz tests should be implemented to validate math and accounting flows throughout the system to account for any unexpected accounting discrepancies.

### Original Finding Content

## Diﬃculty: High

## Type: Denial of Service

## Description
During the process of executing the `removeDefaultWarning` function, an accounting discrepancy fails to decrement `netLateInterest` from `unrealizedLosses`, resulting in an over-inﬂated value. The `triggerDefaultWarning` function updates `unrealizedLosses` with the defaulting loan’s `principal_`, `netInterest_`, and `netLateInterest_` values.

```solidity
emit UnrealizedLossesUpdated(unrealizedLosses += _uint128(principal_ + netInterest_ + netLateInterest_));
```

**Figure 8.1:** The `triggerDefaultWarning` function  
(pool-v2/contracts/LoanManager.sol#L331)

When the warning is removed by the `_revertDefaultWarning` function, only the values of the defaulting loan’s principal and interest are decremented from `unrealizedLosses`. This leaves a discrepancy equal to the amount of `netLateInterest_`.

```solidity
function _revertDefaultWarning(LiquidationInfo memory liquidationInfo_) internal {
    accountedInterest -= _uint112(liquidationInfo_.interest);
    unrealizedLosses  -= _uint128(liquidationInfo_.principal + liquidationInfo_.interest);
}
```

**Figure 8.2:** The `_revertDefaultWarning` function  
(pool-v2/contracts/LoanManager.sol#L631-L634)

## Exploit Scenario
Alice has missed several interest payments on her loan and is about to default. Bob, the poolManager, calls `triggerDefaultWarning` on the loan to account for the unrealized loss in the system. Alice makes a payment to bring the loan back into good standing; the claim function is triggered, and `_revertDefaultWarning` is called to remove the unrealized loss from the system. The net value of Alice’s loan’s late interest value is still accounted for in the value of `unrealizedLosses`. From then on, when users call `Pool.withdraw`, they will have to exchange more shares than are due for the same amount of assets.

## Recommendations
**Short term:** Add the value of `netLateInterest` to the amount decremented from `unrealizedLosses` when removing the default warning from the system.

**Long term:** Implement robust unit tests and fuzz tests to validate math and accounting flows throughout the system to account for any unexpected accounting discrepancies.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Maple Finance v2 |
| Report Date | N/A |
| Finders | Simone Monica, Robert Schneider |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-maplefinance-mapleprotocolv2-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2022-09-maplefinance-mapleprotocolv2-securityreview.pdf

### Keywords for Search

`vulnerability`

