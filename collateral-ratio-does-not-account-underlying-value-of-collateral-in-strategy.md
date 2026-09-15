---
# Core Classification
protocol: AladdinDAO f(x) Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31034
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
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
finders_count: 2
finders:
  - Troy Sargent
  - Robert Schneider
---

## Vulnerability Title

Collateral ratio does not account underlying value of collateral in strategy

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: Medium

## Type: Undefined Behavior

**Target:** contracts/f(x)/v2/TreasuryV2.sol

## Description

When collateral is moved into the strategy, the `totalBaseToken` amount remains unchanged. This does not account for shortfalls and surpluses in the value of the collateral moved into the strategy, and as a result, the collateral ratio may be over-reported or under-reported, respectively.

The integration of strategies in the treasury has not been fully designed and has flaws as evidenced by TOB-ADFX-5. This feature should be reconsidered and thoroughly specified prior to active use. For example, it is unclear whether the strategy’s impact on the collateral ratio is robust below 130%. It may benefit the stability of the system to prevent too much of the collateral from entering strategies during periods of high volatility or when the system is not over-collateralized by implementing a buffer, or a maximum threshold of the amount of collateral devoted to strategies.

```solidity
function transferToStrategy(uint256 _amount) external override onlyStrategy {
    IERC20Upgradeable(baseToken).safeTransfer(strategy, _amount);
    strategyUnderlying += _amount;
}
```

*Figure 8.1 Collateral is moved into strategy without updating `totalBaseToken` (aladdin-v3-contracts/contracts/f(x)/v2/TreasuryV2.sol#375–378)*

Since `totalBaseToken` is not updated for strategies, it may not be reflected correctly in the amount of base token available to be harvested as reported by the `harvestable` function.

```solidity
function harvestable() public view returns (uint256) {
    uint256 balance = IERC20Upgradeable(baseToken).balanceOf(address(this));
    uint256 managed = getWrapppedValue(totalBaseToken);
    if (balance < managed) return 0;
    else return balance - managed;
}
```

*Figure 8.2: The rewards available to harvest do not consider the value of strategy (aladdin-v3-contracts/contracts/f(x)/v2/TreasuryV2.sol#274–279)*

## Recommendations

**Short term:** Disable the use of strategies for active deployments and consider removing the functionality altogether until it is fully specified and implemented.

**Long term:** Limit the number of features in core contracts and do not prematurely merge incomplete features.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | AladdinDAO f(x) Protocol |
| Report Date | N/A |
| Finders | Troy Sargent, Robert Schneider |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/2024-03-aladdinfxprotocol-securityreview.pdf

### Keywords for Search

`vulnerability`

