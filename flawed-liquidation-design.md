---
# Core Classification
protocol: Flooring Marketplace
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47415
audit_firm: OtterSec
contest_link: https://github.com/flooringlab
source_link: https://github.com/flooringlab
github_link: https://github.com/flooringlab/uniswap-v3-staker

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
finders_count: 2
finders:
  - Robert Chen
  - Nicholas R.Putra
---

## Vulnerability Title

Flawed Liquidation Design

### Overview


The current check in the _checkUnstakeParam function is not properly preventing contracts from accessing the liquidation feature. This can allow attackers to manipulate prices on the Uniswap V3 pool by deploying a contract and then accessing the liquidation logic within its constructor. The check in the function is not effective because it only checks the length of the code of the sender, and since the logic for accessing the liquidation feature is in the constructor, the length of the code for the second contract remains at zero and bypasses the check. Additionally, the _isPositionInRange function directly retrieves the current tick from the pool without verifying its integrity, making it vulnerable to manipulation. This can be exploited to manipulate the tick value in the pool and trigger the liquidation process, resulting in the loss of user assets. To fix this issue, the liquidation function should be explicitly called from an externally owned account, and a price oracle check should be integrated to enhance security. This issue has been fixed in version c0d4f4f.

### Original Finding Content

## Vulnerability Report

The current `checkUnstakeParam` inadequately prevents contracts from accessing the liquidation feature. An attacker may deploy a contract to manipulate prices on the Uniswap V3 pool. Subsequently, they may deploy another contract to access the liquidation logic within its constructor. 

`_checkUnstakeParam` examines whether the sender is a contract by verifying the length of its code. Since the logic for accessing the liquidation feature is in the constructor under execution, the length of the code of the second contract remains zero, thus bypassing the contract check.

> _Uniswap V3 Staker.sol solidity
```solidity
function _checkUnstakeParam(
    IncentiveKey memory key,
    Deposit memory deposit,
    Stake memory stake,
    IncentiveConfig memory incentiveConfig
) private view returns (bool) {
    [...]
    // Anyone (except Contract Caller) can liquidate the stakes that are out of range
    // prevent price manipulation using Flash Loan or something else
    if (isLiquidation && _msgSender().code.length > 0) revert CannotLiquidateByContract();
    return isLiquidation;
}
```

Furthermore, `_isPositionInRange` directly retrieves the current tick from the Uniswap V3 pool’s slot0 data without verifying its integrity. This vulnerability, combined with the incorrect contract check mentioned above, may be exploited to manipulate the tick value in the pool, causing it to deviate from the specified range. Consequently, a malicious user may trigger the liquidation process, liquidating the user’s assets.

> _Uniswap V3 Staker.sol solidity
```solidity
function _isPositionInRange(IUniswapV3Pool pool, int24 tickLower, int24 tickUpper) private view
    returns (bool) {
    (, int24 tick, , , , , ) = pool.slot0();
    return tickLower <= tick && tick <= tickUpper;
}
```

© 2024 Otter Audits LLC. All Rights Reserved. 6/14

## Remediation
Explicitly require that the liquidation function is explicitly called from an externally owned account instead of solely relying on `_msgSender().code.length`. Additionally, integrating a price or oracle check alongside the existing tick-based range check will enhance security.

## Patch
Fixed in commit `0cd4f4f`.

© 2024 Otter Audits LLC. All Rights Reserved. 7/14

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Flooring Marketplace |
| Report Date | N/A |
| Finders | Robert Chen, Nicholas R.Putra |

### Source Links

- **Source**: https://github.com/flooringlab
- **GitHub**: https://github.com/flooringlab/uniswap-v3-staker
- **Contest**: https://github.com/flooringlab

### Keywords for Search

`vulnerability`

