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
solodit_id: 48952
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-rubicon
source_link: https://code4rena.com/reports/2023-04-rubicon
github_link: https://github.com/code-423n4/2023-04-rubicon-findings/issues/545

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
  - yield
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cccz
---

## Vulnerability Title

[H-13] When opening a position, the collateral of the previous position is used for borrowing, which makes the user more easily liquidated

### Overview


This bug report discusses a potential issue with the Rubicon protocol where users may be at risk of being liquidated due to the use of collateral from previous positions when opening a new position. This can occur when the user has not reached the maximum borrowable amount in their previous positions and collateral is automatically used for borrowing, causing the user to reach the liquidation threshold. A proof of concept has been provided to demonstrate this issue. The recommended mitigation step is to consider not using collateral from previous positions for borrowing when opening a new position. The severity of this issue has been disputed by the Rubicon team, but the judge has determined it to be a high risk as it significantly increases the chances of being liquidated.

### Original Finding Content


When a user opens a position, if there is collateral in previous positions that have not reached the maximum borrowable amount, this collateral will be used for borrowing, which may cause the user to reach the liquidation threshold, resulting in the user being liquidated.

```solidity
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

I will use an example to illustrate it:

Consider the WBTC collateralization rate is 0.7.

Alice is long WBTC using 1e8 WBTC and 1.6x leverage, the contract will collateralize 1e8 WBTC and borrow 0.6e8 WBTC, at which point Alice is 0.7 - 0.6/1 = 10% away from the liquidation threshold.

If Alice continues to use 1e8 WBTC and 1.8x leverage to long WBTC, the previous position will be able to borrow 0.1e8 WBTC, plus the 0.7e8 WBTC that was borrowed by collateralizing 1e8 WBTC, which can be covered without further collateralizing and borrowing, resulting in Alice currently being 0.7 - (0.7 + 0.7)/(1+1) = 0 away from the liquidation threshold. I.e. if the price of WBTC drops slightly, Alice will be liquidated.

If under normal circumstances, Alice is long WBTC using 1e8 WBTC and 1.8x leverage, the contract will collateralize 1e8 WBTC and borrow 0.7e8 WBTC, then collateralize 0.7e8 WBTC and borrow 0.1 WBTC, at which point Alice is 0.7 - 0.8/1.7 = 23% from the liquidation threshold.

The following POC indicates that when a user opens a position with 1.6x and 1.8x leverage in succession, the user will reach the liquidation threshold:

```js
    describe("Long positions 📈", function () {
      it("LPOC1", async function () {
        const { owner, testCoin, testStableCoin, Position, rubiconMarket, comptroller } = await loadFixture(
          deployPoolsUtilityFixture
        );
        const TEST_AMOUNT_1 = parseUnits("1");
        const x1_6 = parseUnits("1.6");

        await Position.connect(owner).buyAllAmountWithLeverage(
          testCoin.address,
          testStableCoin.address,
          TEST_AMOUNT_1,
          x1_6
        );
        console.log("owner liquidity %s",await comptroller.getAccountLiquidity(Position.address));
        const x1_8 = parseUnits("1.8");

        await Position.connect(owner).buyAllAmountWithLeverage(
          testCoin.address,
          testStableCoin.address,
          TEST_AMOUNT_1,
          x1_8
        );
        console.log("owner liquidity %s",await comptroller.getAccountLiquidity(Position.address));
      });
      it("LPOC2", async function () {
        const { owner, testCoin, testStableCoin, Position, rubiconMarket, comptroller } = await loadFixture(
          deployPoolsUtilityFixture
        );
        const TEST_AMOUNT_1 = parseUnits("1");
        const x1_8 = parseUnits("1.8");

        await Position.connect(owner).buyAllAmountWithLeverage(
          testCoin.address,
          testStableCoin.address,
          TEST_AMOUNT_1,
          x1_8
        );
        console.log("owner liquidity %s",await comptroller.getAccountLiquidity(Position.address));
      });
```

```sh
  Leverage positions Test
    Pools Utility Test
      Long positions 📈
owner liquidity [
  BigNumber { value: "0" },
  BigNumber { value: "90000000000000000" },
  BigNumber { value: "0" }
]
owner liquidity [
  BigNumber { value: "0" },
  BigNumber { value: "0" },
  BigNumber { value: "0" }
]
        ✓ LPOC1
owner liquidity [
  BigNumber { value: "0" },
  BigNumber { value: "347451975478099020" },
  BigNumber { value: "0" }
]
```

### Proof of Concept

<https://github.com/code-423n4/2023-04-rubicon/blob/511636d889742296a54392875a35e4c0c4727bb7/contracts/utilities/poolsUtility/Position.sol#L537-L550>

### Tools Used

Hardhat

### Recommended Mitigation Steps

Consider not using collateral from previous positions for borrowing when opening a position.

**[daoio (Rubicon) disagreed with severity and commented](https://github.com/code-423n4/2023-04-rubicon-findings/issues/545#issuecomment-1534801924):**
 > Yeah, the issue is correct. It will increase a possibility of being liquidated, though it was an intended behavior.

**[HickupHH3 (judge) commented](https://github.com/code-423n4/2023-04-rubicon-findings/issues/545#issuecomment-1569793812):**
 > A bit of similarity with [#1180](https://github.com/code-423n4/2023-04-rubicon-findings/issues/1180), but conditions to achieve it are different.
> 
> Keeping it as High because probability of liquidation at this point is very high, as good as degen trading.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Rubicon |
| Report Date | N/A |
| Finders | cccz |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-rubicon
- **GitHub**: https://github.com/code-423n4/2023-04-rubicon-findings/issues/545
- **Contest**: https://code4rena.com/reports/2023-04-rubicon

### Keywords for Search

`vulnerability`

