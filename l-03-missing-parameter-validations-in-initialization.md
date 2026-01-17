---
# Core Classification
protocol: Harmonixfinance Tokensale Hyperliquid
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63982
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarmonixFinance-TokenSale-Hyperliquid-Security-Review.md
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
  - Shieldify Security
---

## Vulnerability Title

[L-03] Missing Parameter Validations in Initialization

### Overview

See description below for full details.

### Original Finding Content


## Severity

Low Risk

## Description

The initialization function does not validate that `pricePerToken > 0` and `maxRaise > 0`. These missing checks allow deployment with invalid configurations that either break view functions or make the entire sale useless.

If `pricePerToken = 0`, the `saleStatus()` view function always reverts due to division by zero, breaking all UIs and frontends.

If `maxRaise = 0`, the sale accepts deposits but allocates nothing. All users get 100% refunds after settlement, making the sale completely pointless.

## Location of Affected Code

File: [contracts/token_sales/HarTokenSale.sol#L96-L114](https://github.com/harmonixfi/core-contracts/blob/72db1cc14bd3601a94a97e5096400599f5a72cac/contracts/token_sales/HarTokenSale.sol#L96-L114)

```solidity
function initialize(address owner_, address purchaseToken_, SaleConfigStruct memory saleConfig_, SonarConfigStruct memory sonarConfig_) external initializer {
    require(purchaseToken_ != address(0), "Init: zero token");
    require(saleConfig_.whitelistReserve <= saleConfig_.maxRaise, "Init: reserve too high");
    require(saleConfig_.priorityMaxAmount > 0, "Init: zero priority cap");
    // Missing: require(saleConfig_.pricePerToken > 0, "Init: zero price");
    // Missing: require(saleConfig_.maxRaise > 0, "Init: zero max raise");

    saleConfig = saleConfig_;
}
```

File: [contracts/token_sales/HarTokenSale.sol#L302](https://github.com/harmonixfi/core-contracts/blob/72db1cc14bd3601a94a97e5096400599f5a72cac/contracts/token_sales/HarTokenSale.sol#L302)

```solidity
// pricePerToken = 0 breaks this:
function saleStatus(address investor) external view returns (...) {
    allocated = accepted / saleConfig.pricePerToken;  // ← Division by zero
}
```

File: [contracts/token_sales/HarTokenSale.sol#L187-L196](https://github.com/harmonixfi/core-contracts/blob/72db1cc14bd3601a94a97e5096400599f5a72cac/contracts/token_sales/HarTokenSale.sol#L187-L196)

```solidity
// maxRaise = 0 makes this useless:
function _finalizeSettlement() internal {
    uint256 remainingCapacity = saleConfig.maxRaise > whitelistAllocated
        ? saleConfig.maxRaise - whitelistAllocated
        : 0;  // Always 0 if maxRaise = 0
    // Result: totalAccepted = 0
}
```

## Impact

**With `pricePerToken = 0`:**

- All `saleStatus()` calls revert
- Frontends can't display user allocations
- Severely degraded UX (core functions still work but no visibility)

**With `maxRaise = 0`:**

- Sale accepts deposits but allocates zero tokens
- All users waste gas claiming 100% refunds
- Protocol wastes deployment costs and reputation damage

Both are easy deployment mistakes that should be caught at initialization.

## Recommendation

Add both validations during initialization:

```solidity
function initialize(...) external initializer {
    require(purchaseToken_ != address(0), "Init: zero token");
    require(saleConfig_.pricePerToken > 0, "Init: zero price");
    require(saleConfig_.maxRaise > 0, "Init: zero max raise");
    require(saleConfig_.whitelistReserve <= saleConfig_.maxRaise, "Init: reserve too high");
    require(saleConfig_.priorityMaxAmount > 0, "Init: zero priority cap");
    require(saleConfig_.saleOpen < saleConfig_.settleTime, "Init: sale opens after settlement");
    // code
}
```

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Harmonixfinance Tokensale Hyperliquid |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarmonixFinance-TokenSale-Hyperliquid-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

