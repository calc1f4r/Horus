---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40862
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad
source_link: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
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
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Christoph Michel
  - J4X98
---

## Vulnerability Title

Cannot use uint256.max to repay the balance of aavev3migrationbundler 

### Overview


This bug report discusses an issue with the AaveV3MigrationBundler contract. It states that passing the maximum value for the "amount" parameter in the aaveV3Repay function does not work as intended. The report explains that this causes the bundler to try and repay the entire borrow balance instead of just the bundler's balance. The report recommends capping the amount to the bundler's balance to avoid this issue.

### Original Finding Content

## AaveV3 Migration Bundler Issue Documentation

## Context
AaveV3MigrationBundler.sol#L37

## Description
The `aaveV3Repay`'s natspec states the following for the amount parameter:  
*The amount of asset to repay. Pass `type(uint256).max` to repay the bundler's asset balance.*  

However, passing `type(uint256).max` to repay the bundler's asset balance does not work. Note that if `amount == type(uint256).max`, this value is not adjusted and just forwarded to the `AAVE_V3_POOL.repay` call.

AaveV3 will execute this code:

```solidity
uint256 paybackAmount = params.interestRateMode == DataTypes.InterestRateMode.STABLE
? stableDebt
: variableDebt;
// note that useATokens is false for repay and this is not executed
if (params.useATokens && params.amount == type(uint256).max) {
    params.amount = IAToken(reserveCache.aTokenAddress).balanceOf(msg.sender);
}
// not executed either as params.amount = type(uint256).max
// meaning paybackAmount will stay at entire `variableDebt`
if (params.amount < paybackAmount) {
    paybackAmount = params.amount;
}
```

Note that `useATokens` is false for repays. This caps the amount to be repaid to the entire borrow balance, not to the bundler's balance. The call will revert as it tries to repay the entire borrow balance with the bundler's balance.

### Example
A user tries to migrate part of their position by trying to repay half of their borrow balance of 1000 assets. The first action in the bundle redeems shares from another protocol to receive the desired repay amount of roughly 500 assets, and the second action is to repay by setting `assets = type(uint256).max` to "repay the bundler's asset balance," as defined by the natspec. The batch will revert as Aave V3 will try to repay the entire borrow balance of 1000, but the bundler only has 500 assets.

## Recommendation
Consider always capping the amount to the bundler's balance. Trying to repay more will never work, and the protocol itself will already cap it to the entire borrow balance:

```solidity
- if (amount != type(uint256).max) amount = Math.min(amount, ERC20(asset).balanceOf(address(this)));
+ amount = Math.min(amount, ERC20(asset).balanceOf(address(this)));
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Christoph Michel, J4X98 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad

### Keywords for Search

`vulnerability`

