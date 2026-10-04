---
# Core Classification
protocol: Rubicon
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48983
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-rubicon
source_link: https://code4rena.com/reports/2023-04-rubicon
github_link: https://github.com/code-423n4/2023-04-rubicon-findings/issues/293

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
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Bauer
  - nobody2018
---

## Vulnerability Title

[M-27] Both buyAllAmountWithLeverage and sellAllAmountWithLeverage always revert

### Overview


The `buyAllAmountWithLeverage` and `sellAllAmountWithLeverage` functions in the `Position` contract are not working properly, causing all users to be unable to open leveraged positions. This is due to a bug in the `openPosition` function which relies on the `_borrowLimit` function to calculate the amount of iterations needed to reach the desired amount with leverage. This function only works if the contract has already provided collateral, but since the `Position` contract is a new user to the comptroller, it does not have any tokens and therefore reverts. This can be exploited by front-running or transferring 1wei `_bathToken` to the newly created `Position` contract. To fix this, the `comptroller.getAccountLiquidity` function should be used instead of the balance of `_bathToken` as the condition for calling `_maxBorrow`.

### Original Finding Content


<https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/utilities/poolsUtility/Position.sol#L545> <br><https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/utilities/poolsUtility/Position.sol#L306-L319>

Both `buyAllAmountWithLeverage` and `sellAllAmountWithLeverage` always revert. **So all users cannot open a leveraged position**.

### Proof of Concept

`openPosition` is the entry point for users to open long/short positions, internally calling the `_borrowLimit` function to calculate an amount of iterations needed to reach desired amount with leverage. The logic of this function is: if the collateral has been provided, then the `_maxBorrow` function will be called to calculate the maximum amount available to borrow from `_bathToken` market, and then the returned result will be added to the `_loopBorrowed` variable.

```solidity
// check if collateral was already supplied
        uint256 _minted = IERC20(_bathToken).balanceOf(address(this));
    // how much is borrowed on a current loop
        uint256 _loopBorrowed;

        while (_assetAmount <= _desiredAmount) {
            if (_limit == 0) {
        // if collateral already provided
                if (_minted != 0) {
                    uint256 _max = _maxBorrow(_bathToken);

            // take into account previous collateral
                    _loopBorrowed = wmul(_assetAmount, _collateralFactor).add(
                        _max
                    );
```

Next, look at the code of `_maxBorrow`:

```solidity
function _maxBorrow(
        address _bathToken
    ) internal view returns (uint256 _max) {
        (uint256 _err, uint256 _liq, uint256 _shortfall) = comptroller
            .getAccountLiquidity(address(this));		//if address(this) is new user of comptroller, _liq always equal to 0

        require(_err == 0, "_maxBorrow: ERROR");
        require(_liq > 0, "_maxBorrow: LIQUIDITY == 0");	//if _liq equals to 0, tx will revert.
        require(_shortfall == 0, "_maxBorrow: SHORTFALL != 0");

        uint256 _price = oracle.getUnderlyingPrice(CToken(_bathToken));
        _max = (_liq.mul(10 ** 18)).div(_price);
        require(_max > 0, "_maxBorrow: can't borrow 0");
    }
```

To make the `_liq` returned by `comptroller.getAccountLiquidity(address(this))` be 0, then `address(this)` must not provide any collateral. In other words, **this contract is a new user to the comptroller**. Obviously, the `Position` contract created by the user meets this condition.

The condition for calling `_maxBorrow` is that `IERC20(_bathToken).balanceOf(address(this))` returns a non-zero value. **A newly created Position contract does not have any tokens. However, we can transfer 1wei `_bathToken` to it**. This allows the code to execute to `_maxBorrow` and revert.

**There are two ways to transfer `_bathToken` to the newly created `Position`**:

1.  Front-run `buyAllAmountWithLeverage` or `sellAllAmountWithLeverage`.
2.  Once the Position is created, transfer all `_bathTokens` supported by `BathHouseV2` to it. The amount transferred is 1wei.

In fact, `_maxBorrow` will also revert in normal scenario. `Position` borrows other tokens resulting in `_liq` being 0.

### Recommended Mitigation Steps

We should use `comptroller.getAccountLiquidity` instead of the balance of `_bathToken` as the condition for calling `_maxBorrow`.

```diff
--- a/contracts/utilities/poolsUtility/Position.sol
+++ b/contracts/utilities/poolsUtility/Position.sol
@@ -534,7 +534,7 @@ contract Position is Ownable, DSMath {
         uint256 _desiredAmount = wmul(_assetAmount, _leverage);

         // check if collateral was already supplied
-        uint256 _minted = IERC20(_bathToken).balanceOf(address(this));
+        (,uint256 _minted,) = comptroller.getAccountLiquidity(address(this));
        // how much is borrowed on a current loop
         uint256 _loopBorrowed;
```

**[daoio (Rubicon) confirmed](https://github.com/code-423n4/2023-04-rubicon-findings/issues/293#issuecomment-1547149797)**

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2023-04-rubicon-findings/issues/293#issuecomment-1549767282):**
 > Medium: loss of functionality due to griefing from external party.
 >
 > Marking as best because it mentions an additional attack path compared to counterpart.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Rubicon |
| Report Date | N/A |
| Finders | Bauer, nobody2018 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-rubicon
- **GitHub**: https://github.com/code-423n4/2023-04-rubicon-findings/issues/293
- **Contest**: https://code4rena.com/reports/2023-04-rubicon

### Keywords for Search

`vulnerability`

