---
# Core Classification
protocol: Securitize Public Stock Ramp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64616
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
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
finders_count: 4
finders:
  - 0ximmeas
  - Stalin
  - Dacian
  - Jorge
---

## Vulnerability Title

Missing `liquidityToken` validation in `CollateralLiquidityProvider::initialize`

### Overview

See description below for full details.

### Original Finding Content

**Description:** The `CollateralLiquidityProvider::setExternalCollateralRedemption` function includes a validation check to ensure the liquidity token of the new external collateral redemption contract matches the existing `liquidityToken`:

```solidity
function setExternalCollateralRedemption(address _externalCollateralRedemption) external onlyRole(DEFAULT_ADMIN_ROLE) {
        if (_externalCollateralRedemption == address(0)) {
            revert NonZeroAddressError();
        }

        if (
            address(
                ILiquidityProvider(address(ISecuritizeOffRamp(_externalCollateralRedemption).liquidityProvider()))
                    .liquidityToken()
            ) != address(liquidityToken)//@audit-ok (low) why this i not checked in intializatuion
        ) {
            revert LiquidityTokenMismatch();
        }
        address oldExternalCollateral = address(externalCollateralRedemption);
        externalCollateralRedemption = ISecuritizeOffRamp(_externalCollateralRedemption);
        emit ExternalCollateralRedemptionUpdated(oldExternalCollateral, address(externalCollateralRedemption));
    }
```

However, `CollateralLiquidityProvider::initialize` sets the same `externalCollateralRedemption` without performing this validation:

```solidity
function initialize(
    address _liquidityToken,
    address _recipient,
    address _securitizeOffRamp,
    address _externalCollateralRedemption,
    address _collateralProvider
) public onlyProxy initializer {
    // ... zero address checks only ...

    liquidityToken = IERC20Metadata(_liquidityToken);
    externalCollateralRedemption = ISecuritizeOffRamp(_externalCollateralRedemption);
    ...
    //@audit missing validation that _externalCollateralRedemption's liquidity token matches _liquidityToken
}
```

**Impact:** During contract deployment, an admin could mistakenly initialize the contract with an `_externalCollateralRedemption` that uses a different liquidity token than the configured `_liquidityToken`.

**Recommended Mitigation:** Add the liquidity token validation to the  `CollateralLiquidityProvider::initialize`.

**Securitize:** Fixed in commit [d8fd4fb](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/d8fd4fb9c38ed4d006df7ace366d30de239d6d4a).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Securitize Public Stock Ramp |
| Report Date | N/A |
| Finders | 0ximmeas, Stalin, Dacian, Jorge |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-securitize-public-stock-ramp-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

