---
# Core Classification
protocol: Tokemak
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53537
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-07-22-Tokemak.md
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
  - Hexens
---

## Vulnerability Title

[TOKE-25] Gas optimisation in fetching total assets

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** AutopoolETH.sol:deposit, mint, withdraw, redeem

**Description:**

In the function `deposit` of the AutopoolETH contract, the given amount in assets is checked against `maxDeposit`.  This function `maxDeposit` calls `_maxDeposit` internally with the result of calling `_totalAssetsTimeChecked`.

But afterwards, in `deposit` it also calls to `_totalAssetsTimeChecked` and the resulting total assets are used in `convertToShares` to calculate the user’s shares to mint.

The function `_totalAssetsTimeChecked` is not cheap, especially if any destination vault debt reports are stale and so calling it twice would be waste of gas for users, especially with the availability of `_maxDeposit`.

Furthermore, `_maxDeposit` will call `maxMint`, which internally calls `Autopool4626.maxMint`. This function also calls AutopoolDebt.totalAssetsTimeChecked, so in the end the expensive operation could be performed 3 times on deposit.

The same issues also exists in `mint`, `withdraw` and `redeem`.

```
    function deposit(
        uint256 assets,
        address receiver
    )
        public
        virtual
        override
        nonReentrant
        noNavPerShareDecrease(TotalAssetPurpose.Deposit)
        ensureNoNavOps
        returns (uint256 shares)
    {
        Errors.verifyNotZero(assets, "assets");

        // Handles the vault being paused, returns 0
        if (assets > maxDeposit(receiver)) {
            revert ERC4626DepositExceedsMax(assets, maxDeposit(receiver));
        }

        uint256 ta = _totalAssetsTimeChecked(TotalAssetPurpose.Deposit);
        shares = convertToShares(assets, ta, totalSupply(), Math.Rounding.Down);

        Errors.verifyNotZero(shares, "shares");

        _baseAsset.safeTransferFrom(msg.sender, address(this), assets);
        _assetBreakdown.totalIdle += assets;
        _tokenData.mint(receiver, shares);
    }
```

**Remediation:**  We would recommend to refactor `deposit`, `mint`, `withdraw` and `redeem` such that the `_totalAssetsTimeChecked` is only called once and the resulting amount is passed along.

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Tokemak |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-07-22-Tokemak.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

