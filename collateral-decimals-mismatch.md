---
# Core Classification
protocol: Vest Exchange
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47533
audit_firm: OtterSec
contest_link: https://www.vest.exchange/
source_link: https://www.vest.exchange/
github_link: https://github.com/VestLabs/contracts-v3-hardhat

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
finders_count: 4
finders:
  - Nicholas R. Putra
  - Robert Chen
  - OtterSec
  - Sebastian Yii
---

## Vulnerability Title

Collateral Decimals Mismatch

### Overview


This bug report addresses an issue within the Exchange platform where a calculation error occurs during the execution of orders. This error is caused by a lack of validation in the contract, which can lead to the transaction failing in certain scenarios. The bug has been fixed in the latest patch and the suggested solution is to add validation to ensure that the necessary decimals are present.

### Original Finding Content

## Notional Size Calculation in Exchange Contract

Within Exchange, specifically in the computation of `notionalSize` during the `executeOrder` process, a calculation occurs for determining the exponent needed to adjust the `notionalSize` precision.

## Exchange.sol (SOLIDITY)

```solidity
function executeOrder(
    Order calldata _order,
    OrderData calldata _orderData,
    bool _isLiq
) external onlyRole(ROUTER_ROLE) returns (bytes32, int256, int256, uint256, execPrice) {
    [...]
    settleOrder.notionalSize =
        abs(settleOrder.sizeDelta) *
        _orderData.spotPrice *
        uint256(
            10 **
            (tokenDecimals[collateralToken] -
            marketSettings[_order.underlying].sizeDecimals -
            marketSettings[_order.underlying].priceDecimals)
        );
    [...]
}
```

The current contract lacks validation to ensure that `tokenDecimals` is greater than or equal to the sum of `sizeDecimals` and `priceDecimals`. Therefore, in edge cases where `tokenDecimals` is smaller, the above code will cause the transaction to revert.

## Remediation

Add validation to ensure that `tokenDecimals` must be larger than the sum of `sizeDecimals` and `priceDecimals`.

## Patch

Fixed in commit `a6eee96`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Vest Exchange |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Robert Chen, OtterSec, Sebastian Yii |

### Source Links

- **Source**: https://www.vest.exchange/
- **GitHub**: https://github.com/VestLabs/contracts-v3-hardhat
- **Contest**: https://www.vest.exchange/

### Keywords for Search

`vulnerability`

