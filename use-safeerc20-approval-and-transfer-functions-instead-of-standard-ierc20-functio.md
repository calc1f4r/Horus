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
solodit_id: 64619
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

Use `SafeERC20` approval and transfer functions instead of standard IERC20 functions for `liquidityToken`

### Overview

See description below for full details.

### Original Finding Content

**Description:** The on-ramping and off-ramping processes are linked to external liquidity tokens such as stablecoins whose code is not controlled by the protocol; hence use [`SafeERC20::forceApprove, transfer, safeTransfer`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol) when dealing with a range of potential tokens:
```solidity
on-ramp/provider/AllowanceAssetProvider.sol
98:        asset.transferFrom(assetProviderWallet, _buyer, _amount);

on-ramp/BaseOnRamp.sol
122:        liquidityToken.transferFrom(from, address(this), amount);
125:            liquidityToken.transfer(feeManager.feeCollector(), fee);
131:            liquidityToken.approve(address(USDCBridge), amountExcludingFee);
134:            liquidityToken.transfer(custodianWallet, amountExcludingFee);

off-ramp/provider/AllowanceLiquidityProvider.sol
141:        liquidityToken.transferFrom(liquidityProviderWallet, _redeemer, _liquidityAmount);

off-ramp/provider/CollateralLiquidityProvider.sol
186:        collateralToken.transferFrom(collateralProvider, address(this), collateralAmount);
189:        collateralToken.approve(address(externalCollateralRedemption), collateralAmount);
198:        liquidityToken.transfer(_redeemer, amountToSupply);

off-ramp/RedemptionManager.sol
43:            _params.asset.transferFrom(_params.redeemer, _params.liquidityProvider.recipient(), _params.assetAmount);
74:        _params.asset.transferFrom(_params.redeemer, _contractAddress, _params.assetAmount);
80:            _params.asset.transfer(_params.liquidityProvider.recipient(), _params.assetAmount);
96:        _params.liquidityProvider.liquidityToken().transfer(_params.redeemer, userSuppliedAmount);
100:            _params.liquidityProvider.liquidityToken().transfer(IFeeManager(_params.feeManager).feeCollector(), fee);
```

**Securitize:** Fixed in commit [a694dc3](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/a694dc32386e038f8541ef79155b7a06a905fc52).

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

