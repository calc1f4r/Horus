---
# Core Classification
protocol: Level_2025-04-09
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63748
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Level-security-review_2025-04-09.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[L-06] `LevelReserveLens` returns incorrect reserves

### Overview

See description below for full details.

### Original Finding Content


The `_getReserves()` function in the `LevelReserveLens` contract currently only includes reserves from the v1 vaults, completely ignoring collateral held in the v2 vaults. As a result, it underestimates the total reserves backing lvlUSD, returning v1Reserves + 0—with the v2 collateral effectively hardcoded to zero:

```solidity
    function _getReserves(IERC20Metadata collateral, address waCollateralAddress, address symbioticVault)
        internal
        view
        override
        returns (uint256)
    {
        uint256 v1Reserves = super._getReserves(collateral, waCollateralAddress, symbioticVault);

        uint256 boringVaultValue = 0;

        return v1Reserves + boringVaultValue;
    }
```

This misrepresentation can lead to inaccurate reserve data for any consumers relying on this function, potentially affecting financial decisions.

Add a public function to the `VaultManager` contract that returns the total assets held for a given collateral token. Then, update `_getReserves()` in LevelReserveLens to use this new function instead of the hardcoded zero for v2.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Level_2025-04-09 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Level-security-review_2025-04-09.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

