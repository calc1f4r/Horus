---
# Core Classification
protocol: Inverse Finance
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5741
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-10-inverse-finance-contest
source_link: https://code4rena.com/reports/2022-10-inverse
github_link: https://github.com/code-423n4/2022-10-inverse-findings/issues/419

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Ch_301
---

## Vulnerability Title

[M-12]  Users could get some DOLA even if they are on liquidation position

### Overview


This bug report is about a vulnerability in the code of the Market.sol smart contract. The issue is that users are able to invoke the `forceReplenish()` function when they are in a liquidation position. This is possible because the `getCollateralValueInternal(user)` function only returns the value of the collateral, and not the value of the debt. As a result, the user could be in a liquidation position, but still be able to invoke `forceReplenish()` and get more DOLA. The recommended mitigation step is to use `getCreditLimitInternal()` rather than `getCollateralValueInternal()`.

### Original Finding Content

## Lines of code

https://github.com/code-423n4/2022-10-inverse/blob/main/src/Market.sol#L566


## Vulnerability details

## Impact
Users abels to invoke `forceReplenish()` when they are on liquidation position

## Proof of Concept
On `Market.sol` ==>  `forceReplenish()`
On this line 
```
uint collateralValue = getCollateralValueInternal(user);
```

`getCollateralValueInternal(user)` only return the value of the collateral 
```
    function getCollateralValueInternal(address user) internal returns (uint) {
        IEscrow escrow = predictEscrow(user);
        uint collateralBalance = escrow.balance();
        return collateralBalance * oracle.getPrice(address(collateral), collateralFactorBps) / 1 ether; 
```
So if the user have 1.5 wETH at the price of  1 ETH = 1600 USD
It will return `1.5 * 1600` and this value is the real value we can’t just check it directly with the debt like this 
```
 require(collateralValue >= debts[user], "Exceeded collateral value");
```
This is no longer `over collateralized` protocol 
The value needs to be multiplied by `collateralFactorBps / 10000`
-  So depending on the value of `collateralFactorBps` and `liquidationFactorBps` the user could be in the liquidation position but he is able to invoke `forceReplenish()` to cover all their `dueTokensAccrued[user]` on `DBR.sol` and get more `DOLA`
-  or it will lead a healthy debt to be in the liquidation position after invoking `forceReplenish()`
- 

## Recommended Mitigation Steps
Use `getCreditLimitInternal()` rather than `getCollateralValueInternal()`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Inverse Finance |
| Report Date | N/A |
| Finders | Ch_301 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-10-inverse
- **GitHub**: https://github.com/code-423n4/2022-10-inverse-findings/issues/419
- **Contest**: https://code4rena.com/contests/2022-10-inverse-finance-contest

### Keywords for Search

`Business Logic`

