---
# Core Classification
protocol: AFI Vault
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 64133
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/afi-vault/dc8a68ae-e72b-4b63-bef2-544c709f6fda/index.html
source_link: https://certificate.quantstamp.com/full/afi-vault/dc8a68ae-e72b-4b63-bef2-544c709f6fda/index.html
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
finders_count: 3
finders:
  - Paul Clemson
  - Rabib Islam
  - Cameron Biniamow
---

## Vulnerability Title

Flawed Decimal Conversion Logic Understates Share Amount for Non-18-Decimal Assets

### Overview


The client reported a bug in the `afiVault.sol` file where the calculation for the number of shares to be minted is incorrect for assets with less than 18 decimals. This is due to faulty implementation of the `_convertToShares()` and `_convertToAssets()` functions. As a result, users who deposit assets with less than 18 decimals may receive significantly less shares than expected, leading to a negative user experience. The recommendation is to fix these functions by adjusting the input assets for their own decimal precision.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `038b476f8382008ae4723319e983628944243fc7`. The client provided the following explanation:

> Fixed _convertToShares() and _convertToAssets() to properly handle decimal conversion between assets and shares. Assets are now scaled up by the decimal offset (10^_decimalsOffset()) before conversion to shares, and scaled down when converting shares back to assets. Also updated totalAssets() to return assets in the asset's native decimal format.

**File(s) affected:**`afiVault.sol`

**Description:** The `afiVault` incorrectly calculates the number of shares that should be minted for assets that do not have 18 decimals. This is due to the faulty implementation of `_convertToShares()` and `_convertToAssets()`.

`_convertToShares()` calculates shares as `assets.mulDiv(PRECISION, exchangeRate(), rounding)`. While the `exchangeRate()` is scaled to 18 decimals (`1e18`), the input assets is used directly without being adjusted for its own decimal precision. For instance, this means that if someone deposits 100 USDC (which is `100 * 10^6`), and the exchange rate is 1:1 (represented as `1e18`), the calculation will be `(100 * 10^6) * 1e18 / 1e18`, which results in `100e6` shares. However, since the vault's shares have 18 decimals, the user should have received `100e18` shares.

This will constitute a significant negative impact from a UX perspective, leading to users having to deal with small decimals in terms of their shares.

**Recommendation:** The `_convertToShares()` and `_convertToAssets()` functions should be rectified. Consider, for instance, the following:

```
function _convertToShares(uint256 assets, Math.Rounding rounding) internal view virtual override returns (uint256) {
    uint256 scaledAssets = assets * (10 ** _decimalsOffset());
    return scaledAssets.mulDiv(PRECISION, exchangeRate(), rounding);
}

function _convertToAssets(uint256 shares, Math.Rounding rounding) internal view virtual override returns (uint256) {
    uint256 scaledAssets = shares.mulDiv(exchangeRate(), PRECISION, rounding);
    return scaledAssets / (10  _decimalsOffset());
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | AFI Vault |
| Report Date | N/A |
| Finders | Paul Clemson, Rabib Islam, Cameron Biniamow |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/afi-vault/dc8a68ae-e72b-4b63-bef2-544c709f6fda/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/afi-vault/dc8a68ae-e72b-4b63-bef2-544c709f6fda/index.html

### Keywords for Search

`vulnerability`

