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
solodit_id: 63738
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Level-security-review_2025-04-09.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] `reward` does not account for an under-peg scenario

### Overview


This bug report discusses a problem with the `reward` function in a program. This function calculates the accrued yield, which is the profit earned from the program. However, the current calculation does not account for situations where the value of the assets in the program is lower than expected. This could lead to incorrect calculations and potentially cause problems for the program's stability. The report recommends considering the price of each asset when calculating the total value.

### Original Finding Content


## Severity

**Impact:** High

**Likelihood:** Low

## Description

When `reward` is called, it calculates the accrued yield as the total asset balances in the vault and across strategies, minus the minted shares in the vault.

```solidity
    function getAccruedYield(address[] calldata assets) public view returns (uint256 accrued) {
        uint256 total;

        for (uint256 i = 0; i < assets.length; i++) {
            address asset = assets[i];

            StrategyConfig[] memory strategies = allStrategies[asset];

            uint256 totalForAsset = vault._getTotalAssets(strategies, asset);
 >>>        total += totalForAsset.convertDecimalsDown(ERC20(asset).decimals(), vault.decimals());
        }
        uint256 vaultShares = vault.balanceOf(address(vault));
        accrued = total - vaultShares;

        return accrued;
    }
```

However, this doesn't account for scenarios where the underlying asset is currently under-peg ( price < $1). When the asset is under-peg, its actual value is lower than the calculated asset amount. This can result in an incorrect calculation of the accrued yield allocated to the treasury, potentially leading to lvlUSD being insufficiently collateralized in the event of a sharp price drop.

## Recommendations

Consider each asset price when calculating the total value.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

