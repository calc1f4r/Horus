---
# Core Classification
protocol: Ethena Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45268
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-11-ethena-labs
source_link: https://code4rena.com/reports/2024-11-ethena-labs
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

protocol_categories:
  - staking_pool
  - decentralized_stablecoin

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[L-05] If the `collateral_asset` is native token, minting is unavailable even though redeeming is available.

### Overview

See description below for full details.

### Original Finding Content


In the `_transferCollateral` function, if the `collateral_asset` is native token, it reverts. This causes minting reverts.

```solidity
File: contracts\ustb\UStbMinting.sol
608:         if (!tokenConfig[asset].isActive || asset == NATIVE_TOKEN) revert UnsupportedAsset();
```

However, redeeming is available even though the `collateral_asset` is native token.

```solidity
    function _transferToBeneficiary(address beneficiary, address asset, uint128 amount) internal {
L:588:  if (asset == NATIVE_TOKEN) {
            if (address(this).balance < amount) revert InvalidAmount();
            (bool success, ) = (beneficiary).call{value: amount}("");
            if (!success) revert TransferFailed();
        } else {
            if (!tokenConfig[asset].isActive) revert UnsupportedAsset();
            IERC20(asset).safeTransfer(beneficiary, amount);
        }
    }
```

Improve the minting mechanism to allow native token.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ethena Labs |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2024-11-ethena-labs
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2024-11-ethena-labs

### Keywords for Search

`vulnerability`

