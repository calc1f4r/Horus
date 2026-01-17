---
# Core Classification
protocol: Lybra Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21317
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/08/lybra-finance/
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
finders_count: 0
finders:
---

## Vulnerability Title

Duplication of Bad Collateral Ratio  Acknowledged

### Overview

See description below for full details.

### Original Finding Content

#### Resolution



The Lybra Finance team has acknowledged this as a choice by design and provided the following note:



> 
> The liquidation ratio for each eUSD vault is fixed, and this has been stated in our docs. Therefore, we will keep it unchanged.
> 
> 
> 




#### Description


It is possible to set a bad collateral ratio in the `LybraConfigurator` contract for any vault:


**contracts/lybra/configuration/LybraConfigurator.sol:L137-L141**



```
function setBadCollateralRatio(address pool, uint256 newRatio) external onlyRole(DAO) {
 require(newRatio >= 130 \* 1e18 && newRatio <= 150 \* 1e18 && newRatio <= vaultSafeCollateralRatio[pool] + 1e19, "LNA");
 vaultBadCollateralRatio[pool] = newRatio;
 emit SafeCollateralRatioChanged(pool, newRatio);
}

```
But in the `LybraEUSDVaultBase` contract, this value is fixed and cannot be changed:


**contracts/lybra/pools/base/LybraEUSDVaultBase.sol:L19**



```
uint256 public immutable badCollateralRatio = 150 \* 1e18;

```
This duplication of values can be misleading at some point. It’s better to make sure you cannot change the bad collateral ratio in the `LybraConfigurator` contract for some types of vaults.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Lybra Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/08/lybra-finance/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

