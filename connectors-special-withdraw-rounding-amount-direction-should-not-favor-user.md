---
# Core Classification
protocol: Balmy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46438
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/d365c977-e13a-41e2-84e3-67083ecbc362
source_link: https://cdn.cantina.xyz/reports/antina_balmy_november2024.pdf
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
  - Blockdev
  - ladboy233
---

## Vulnerability Title

Connectors special withdraw rounding amount direction should not favor user 

### Overview


This bug report discusses an issue with the rounding direction in the CompoundV2Connector and ERC4626Connector contracts. The rounding direction should always favor the protocol, but it currently favors the user. The recommended solution is to use Math.Rounding.Floor for Compound V2 and to use vault.convertToShares instead of previewWithdraw for ERC4626. The bug has been fixed in PR 114.

### Original Finding Content

## Context 
*File:* CompoundV2Connector.sol#L295-L334

## Description 
When a user withdraws, the rounding direction should always favor the protocol and not the user to make sure that the user cannot take advantage of such rounding error. Yet both Compound V2 special withdraw and ERC4626 special withdraw favor the user when computing cTokens and shares.

In Compound V2 Connector:
```solidity
uint256 shares = _convertAssetsToShares(assets, Math.Rounding.Ceil);
```
The rounding direction is `Ceil` instead of `Floor`. In ERC4626 connector special withdraw when the type is `WITHDRAW_ASSET_FARM_TOKEN_BY_ASSET_AMOUNT`. The `previewWithdraw` (see ERC4626Connector.sol#L217) from a standard vault (see ERC4626.sol#L161) rounds up as well.

```solidity
/** @dev See {IERC4626-previewWithdraw}. */
function previewWithdraw(uint256 assets) public view virtual returns (uint256) {
    return _convertToShares(assets, Math.Rounding.Ceil);
}
```

## Recommendation
1. For Compound V2, use `Math.Rounding.Floor` as rounding direction.
2. For ERC4626 connector, use `vault.convertToShares(assets)` instead of `previewWithdraw`.

## Balmy
The fix for the Compound connector was actually in the fix for `CompoundV2Connector#_convertSharesToAssets` which does not consider pending cToken interest (PR 101). 

You are also right that we should not use `previewWithdraw` for the ERC4626. But not only for rounding, we should not be using it because the vault could have fees enabled. 

I tested out a quick example based on this implementation (ERC4626Fees.sol):

### ERC4626 vault
- Total shares in vault = 2000
- Total assets in vault = 4000
- Withdraw fee = 5%

### Strategy
- Total shares owned by strategy = 500
- Reported balance = `previewRedeem(500) = 500 * 4000 / 2000 * 0.95 = 950`

### Vault
- Total shares for strategy = 1000
- Position shares = 500
- Position balance = `950 * 500 / 1000 = 475`

Assuming we are using `previewWithdraw`:
```
previewWithdraw(200) = (200 * 1.05) * 2000 / 4000 = 105
redeem(105) = (105 * 4000 / 2000) * 0.95 = 199.5
```

Assuming we are using `convertToShares`:
```
convertToShares(200) = 200 * 2000 / 4000 = 100
redeem(100) = (100 * 4000 / 2000) * 0.95 = 190
```

So indeed, `convertToShares` is the way to go. The fix is in PR 114.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Balmy |
| Report Date | N/A |
| Finders | Blockdev, ladboy233 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/antina_balmy_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/d365c977-e13a-41e2-84e3-67083ecbc362

### Keywords for Search

`vulnerability`

