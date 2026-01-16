---
# Core Classification
protocol: Aave Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13606
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2020/09/aave-protocol-v2/
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

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Sergii Kravchenko
  - Bernhard Mueller
---

## Vulnerability Title

Interest rates are updated incorrectly

### Overview


This bug report is about an issue with the function `updateInterestRates()` which updates the borrow rates of a reserve. The rates depend on the available liquidity and must be recalculated each time the liquidity changes. The function is called ahead of minting or burning ATokens. However, in the `LendingPoolCollateralManager` an interest rate update is performed *after* aTokens have been burned, resulting in an incorrect interest rate. To fix this issue, the recommendation is to update the interest rates before calling `collateralAtoken.burn()`. This issue was independently discovered by the Aave developers and has already been fixed by the end of the audit.

### Original Finding Content

#### Resolution



This issue was independently discovered by the Aave developers and had already been fixed by the end of the audit.


The function `updateInterestRates()` updates the borrow rates of a reserve. Since the rates depend on the available liquidity they must be recalculated each time liquidity changes. The function takes the amount of liquidity added or removed as the input and is called ahead of minting or burning ATokens. However, in `LendingPoolCollateralManager` an interest rate update is performed *after* aTokens have been burned, resulting in an incorrect interest rate.


**code/contracts/lendingpool/LendingPoolCollateralManager.sol:L377-L382**



```
vars.collateralAtoken.burn(
  user,
  receiver,
  vars.maxCollateralToLiquidate,
  collateralReserve.liquidityIndex
);

```
**code/contracts/lendingpool/LendingPoolCollateralManager.sol:L427-L433**



```
//updating collateral reserve
collateralReserve.updateInterestRates(
  collateral,
  address(vars.collateralAtoken),
  0,
  vars.maxCollateralToLiquidate
);

```
**Recommendation**


Update interest rates before calling `collateralAtoken.burn()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Aave Protocol V2 |
| Report Date | N/A |
| Finders | Sergii Kravchenko, Bernhard Mueller |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2020/09/aave-protocol-v2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

