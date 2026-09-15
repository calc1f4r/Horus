---
# Core Classification
protocol: Aave Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11594
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/aave-protocol-audit/
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[C03] Deposits not marked as collateral can still be liquidated

### Overview


This bug report is about an issue in the `liquidationCall` function of the LendingPoolLiquidationManager.sol contract. The issue is due to a logic flaw in the function, where the conditional statement in lines 92 and 93 is erroneous. This means that the expected behavior of only allowing assets marked as collateral to be liquidated is not enforced, as the function succeeds even when the reserve is not enabled as collateral and the user did not mark it as collateral. 

The recommended solution is to modify the conditional statement in lines 92 and 93 to `core.isReserveUsageAsCollateralEnabled(_collateral) &amp;&amp; core.isUserUseReserveAsCollateralEnabled(_collateral, _user);`, and to implement thorough related unit tests. 

The issue has since been fixed in Merge Request #59, but specific unit tests covering this case are still missing.

### Original Finding Content

When a user [deposits](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L90) an asset into the lending pool, they can choose whether the asset functions as collateral by means of the [`_useAsCollateral` flag](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPool.sol#L93). While the expected behavior is that only assets marked as collateral can be liquidated, this restriction is not enforced.


The issue is due to a logic flaw in the [`liquidationCall` function](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPoolLiquidationManager.sol#L72). This function should require that the reserve is enabled as collateral and the user has marked that reserve as collateral. However, the conditional statement in [lines 92 and 93](https://gitlab.com/aave-tech/dlp/contracts/blob/1f8e5e65a99a887a5a13ad9af6486ebf93f57d02/contracts/lendingpool/LendingPoolLiquidationManager.sol#L92-93) is erroneous. Consequently, assuming the other liquidation requirements hold, `liquidationCall` succeeds when either:


* The reserve `_collateral` is enabled as collateral (regardless of the user preference)
* The reserve `_collateral` is not enabled as collateral and the user did not mark it as collateral


Consider modifying the conditional statement in lines 92 and 93 to `core.isReserveUsageAsCollateralEnabled(_collateral) &amp;&amp; core.isUserUseReserveAsCollateralEnabled(_collateral, _user);`. Afterwards, implementing thorough related unit tests is highly advisable.


**Update**: *Fixed in [MR#59](https://gitlab.com/aave-tech/dlp/contracts/merge_requests/59/diffs). Specific unit tests covering this case are still missing.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Aave Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/aave-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

