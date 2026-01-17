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
solodit_id: 31035
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

Rewards are withdrawn even if protocol is not su�ciently collateralized

### Overview

See description below for full details.

### Original Finding Content

## Diﬃculty: Low

## Type: Undefined Behavior

### Target: contracts/f(x)/v2/TreasuryV2.sol

## Description
The treasury allows any excess base token amount beyond what is considered collateral to be distributed by calling the `harvest` function. Some of this token amount is sent to the rebalance pool as rewards. Since the rebalance pool’s purpose is to encourage the re-collateralization of treasury, it follows that temporarily withholding the rewards until the protocol is re-collateralized, or using them to cover shortfalls, may more eﬀectively stabilize the system.

```solidity
/// @notice Harvest pending rewards to stability pool.
function harvest() external {
    FxStableMath.SwapState memory _state = _loadSwapState(Action.None);
    _updateEMALeverageRatio(_state);
    uint256 _totalRewards = harvestable();
    uint256 _harvestBounty = (getHarvesterRatio() * _totalRewards) / FEE_PRECISION;
    uint256 _rebalancePoolRewards = (getRebalancePoolRatio() * _totalRewards) / FEE_PRECISION;
    emit Harvest(msg.sender, _totalRewards, _rebalancePoolRewards, _harvestBounty);
    
    if (_harvestBounty > 0) {
        IERC20Upgradeable(baseToken).safeTransfer(_msgSender(), _harvestBounty);
        unchecked {
            _totalRewards = _totalRewards - _harvestBounty;
        }
    }
    
    if (_rebalancePoolRewards > 0) {
        _distributeRebalancePoolRewards(baseToken, _rebalancePoolRewards);
        unchecked {
            _totalRewards = _totalRewards - _rebalancePoolRewards;
        }
    }
    
    if (_totalRewards > 0) {
        IERC20Upgradeable(baseToken).safeTransfer(platform, _totalRewards);
    }
}
```

Figure 9.1: Reducing the base asset in Treasury (aladdin-v3-contracts/contracts/f(x)/v2/TreasuryV2.sol#384–413)

## Recommendations
- **Short term**: Consider pausing reward harvesting when the collateral ratio is below the stability ratio and even using the rewards to compensate for shortfalls.
- **Long term**: Perform additional review of the incentive compatibility and economic sustainability of the system.

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

