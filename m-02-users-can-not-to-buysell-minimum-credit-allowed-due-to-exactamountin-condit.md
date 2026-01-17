---
# Core Classification
protocol: Size
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38041
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-06-size
source_link: https://code4rena.com/reports/2024-06-size
github_link: https://github.com/code-423n4/2024-06-size-findings/issues/224

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
finders_count: 27
finders:
  - 0xStalin
  - BoltzmannBrain
  - inzinko
  - iam\_emptyset
  - carlos\_\_alegre
---

## Vulnerability Title

[M-02] Users can not to buy/sell minimum credit allowed due to exactAmountIn condition

### Overview


The bug report discusses an issue with the `BuyCreditMarket` and `SellCreditMarket` libraries in the SizeCredit project on GitHub. These libraries set a minimum amount of credit that can be bought or sold, but due to a coding error, users are unable to buy or sell smaller amounts above this minimum. This is because the code does not properly consider the `params.exactAmountIn` value, which can cause transactions to fail. The report provides a proof of concept for this issue and suggests a solution to fix it. The bug has been confirmed and fixed by the project team. 

### Original Finding Content


<https://github.com/code-423n4/2024-06-size/blob/8850e25fb088898e9cf86f9be1c401ad155bea86/src/libraries/actions/BuyCreditMarket.sol#L91><br><https://github.com/code-423n4/2024-06-size/blob/8850e25fb088898e9cf86f9be1c401ad155bea86/src/libraries/actions/SellCreditMarket.sol#L93>

### Impact

The minimum credit user can buy or sell can be gotten from `state.riskConfig.minimumCreditBorrowAToken` which was set as `5e6`. However, in `buyCreditMarket` and `sellCreditMarket` user can not buy or sell minimun credit allowed or small amount above it due to the `exactAmountIn` condition he chose.

**In `buyCreditMarket`:** when user set `params.exactAmountIn = true`, The `params.amount` value will be cash he want to use to buy credit. Since the `params.amount` value is cash it can be set less than `state.riskConfig.minimumCreditBorrowAToken` (5e6) as long as when the value get converted to credit it will reach the `state.riskConfig.minimumCreditBorrowAToken` value. But, unfortunately, in `validateBuyCreditMarket()` whenever `params.amount` is less than `state.riskConfig.minimumCreditBorrowAToken` the transaction will revert due to below code present in the function.

```javascript
if (params.amount < state.riskConfig.minimumCreditBorrowAToken) {
    revert Errors.CREDIT_LOWER_THAN_MINIMUM_CREDIT(params.amount, state.riskConfig.minimumCreditBorrowAToken);
}
```

For example, the cash user can use to buy minimum credit allowed (`5e6`) can be calculated as in the code below, And the value should be less than the minimum credit allowed (`5e6`).

```javascript
uint256 minimumCash = Math.mulDivUp(5e6, PERCENT, PERCENT + ratePerTenor);
```

**In `sellCreditMarket`:** when user set `params.exactAmountIn = false`, The `params.amount` will be the exact cash he want to receive. But he will also not be able to set the `params.amount` value to be less than `state.riskConfig.minimumCreditBorrowAToken` value due to the below code present in `validateSellCreditMarket()`.

    if (params.amount < state.riskConfig.minimumCreditBorrowAToken) {
        revert Errors.CREDIT_LOWER_THAN_MINIMUM_CREDIT(params.amount, state.riskConfig.minimumCreditBorrowAToken);
    }

### Proof of Concept

**For `BuyCreditMarket`:** Copy and paste below code in `/test/local/actions/BuyCreditMarket.t.sol`:

```javascript
function testFail_UserCanNotBuyMinimumCredit() public {
    // alice deposit weth
    _deposit(alice, weth, 100e18);

    // bob deposit usdc
    _deposit(bob, usdc, 200e6);

    // alice create a borrow offer
    _sellCreditLimit(alice, 0.03e18, 365 days);

    // calculate cash from minimum  credit borrowAToken allowed = 5e6
    uint256 minimumCash = Math.mulDivUp(5e6, PERCENT, PERCENT + 0.03e18);

    // Expect revert with an error CREDIT_LOWER_THAN_MINIMUM_CREDIT
    uint256 debtPositionId = _buyCreditMarket(bob, alice, minimumCash, 365 days, true);
}
```

Then run the test with below command, the test should pass because it will revert with an error `Errors.CREDIT_LOWER_THAN_MINIMUM_CREDIT`.

```
forge test --mt testFail_UserCanNotBuyMinimumCredit
```

**For `SellCreditMarket`:** Copy and paste below code in `/test/local/actions/SellCreditMarket.t.sol`:

```javascript
function testFail_UserCanNotSellMinimumCredit() public {
    // alice deposit usdc
    _deposit(alice, usdc, 200e6);

    // bob deposit weth
    _deposit(bob, weth, 100e18);

    // alice create a loan offer
    _buyCreditLimit(alice, block.timestamp + 365 days, YieldCurveHelper.pointCurve(365 days, 0.03e18));

    // calculate cash from minimum  credit borrowAToken allowed = 5e6
    uint256 minimumCreditInCash = Math.mulDivUp(5e6, PERCENT, PERCENT + 0.03e18);

    // Expect revert with an error CREDIT_LOWER_THAN_MINIMUM_CREDIT
    uint256 debtPositionId = _sellCreditMarket(bob, alice, RESERVED_ID, minimumCreditInCash, 365 days, false);
}
```

Then run the test with below command, the test should pass because it will revert with an error `Errors.CREDIT_LOWER_THAN_MINIMUM_CREDIT`.

```
forge test --mt testFail_UserCanNotSellMinimumCredit
```

### Recommended Mitigation Steps

In `validateBuyCreditMarket()` and  `validateSellCreditMarket()` for `BuyCreditMarket` and `SellCreditMarket` libraries respectively, there is a need of considering the condition of `params.exactAmountIn` value. The check should be implemented as shown below.

**For `BuyCreditMarket` library:** inside `validateBuyCreditMarket()` replace below code:

```javascript
if (params.amount < state.riskConfig.minimumCreditBorrowAToken) { // @audit 5e6 USDC
    revert Errors.CREDIT_LOWER_THAN_MINIMUM_CREDIT(params.amount, state.riskConfig.minimumCreditBorrowAToken);
}
```

With the below code:

```javascript
uint256 ratePerTenor = borrowOffer.getRatePerTenor(VariablePoolBorrowRateParams({variablePoolBorrowRate: state.oracle.variablePoolBorrowRate, variablePoolBorrowRateUpdatedAt: state.oracle.variablePoolBorrowRateUpdatedAt, variablePoolBorrowRateStaleRateInterval: state.oracle.variablePoolBorrowRateStaleRateInterval}), tenor);

if (params.exactAmountIn && params.amount < Math.mulDivUp(state.riskConfig.minimumCreditBorrowAToken, PERCENT, PERCENT + ratePerTenor)) {
    revert Errors.CREDIT_LOWER_THAN_MINIMUM_CREDIT(params.amount, state.riskConfig.minimumCreditBorrowAToken);
} else if (!params.exactAmountIn && params.amount < state.riskConfig.minimumCreditBorrowAToken) {
    revert Errors.CREDIT_LOWER_THAN_MINIMUM_CREDIT(params.amount, state.riskConfig.minimumCreditBorrowAToken);
}
```

**For `SellCreditMarket` library:** inside `validateSellCreditMarket()` replace below code:

```javascript
if (params.amount < state.riskConfig.minimumCreditBorrowAToken) { // @audit 5e6 USDC
    revert Errors.CREDIT_LOWER_THAN_MINIMUM_CREDIT(params.amount, state.riskConfig.minimumCreditBorrowAToken);
}
```

With the below code:

```javascript
uint256 ratePerTenor = loanOffer.getRatePerTenor(VariablePoolBorrowRateParams({variablePoolBorrowRate: state.oracle.variablePoolBorrowRate, variablePoolBorrowRateUpdatedAt: state.oracle.variablePoolBorrowRateUpdatedAt, variablePoolBorrowRateStaleRateInterval: state.oracle.variablePoolBorrowRateStaleRateInterval}), tenor);

if (params.exactAmountIn && params.amount < state.riskConfig.minimumCreditBorrowAToken) {
    revert Errors.CREDIT_LOWER_THAN_MINIMUM_CREDIT(params.amount, state.riskConfig.minimumCreditBorrowAToken);
} else if (!params.exactAmountIn && params.amount < Math.mulDivUp(state.riskConfig.minimumCreditBorrowAToken, PERCENT, PERCENT + ratePerTenor)) {
    revert Errors.CREDIT_LOWER_THAN_MINIMUM_CREDIT(params.amount, state.riskConfig.minimumCreditBorrowAToken);
}
```

### Assessed type

Invalid Validation

**[aviggiano (Size) confirmed and commented](https://github.com/code-423n4/2024-06-size-findings/issues/224#issuecomment-2214816587):**
 > Fixed in https://github.com/SizeCredit/size-solidity/pull/125

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Size |
| Report Date | N/A |
| Finders | 0xStalin, BoltzmannBrain, inzinko, iam\_emptyset, carlos\_\_alegre, trachev, pkqs90, zarkk01, KupiaSec, ether\_sky, samuraii77, said, DanielArmstrong, 0xRobocop, elhaj, dhank, ilchovski, 0x04bytes, 0xJoyBoy03, 1, 2, Jorgect, hyh, 0xarno, 0xanmol |

### Source Links

- **Source**: https://code4rena.com/reports/2024-06-size
- **GitHub**: https://github.com/code-423n4/2024-06-size-findings/issues/224
- **Contest**: https://code4rena.com/reports/2024-06-size

### Keywords for Search

`vulnerability`

