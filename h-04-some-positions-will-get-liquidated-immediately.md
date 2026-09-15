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
solodit_id: 48943
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-04-rubicon
source_link: https://code4rena.com/reports/2023-04-rubicon
github_link: https://github.com/code-423n4/2023-04-rubicon-findings/issues/1180

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
finders_count: 6
finders:
  - immeas
  - cccz
  - kaden
  - ladboy233
  - 0xBeirao
---

## Vulnerability Title

[H-04] Some positions will get liquidated immediately

### Overview


This bug report is about a vulnerability found in the Rubicon compound fork. When a user opens a position, they make a deposit and take a loan against it using max liquidity. This loan can be dangerous because the interest rate for the loan needs to be higher than the interest for the deposit of the collateral. This means that in the block after the loan is taken, the position will become under water and can be liquidated. This only affects certain leverages and can be considered a medium severity issue. A proof of concept test has been provided to showcase how the account is subject to liquidation in the next block after leveraging. The recommended mitigation step is to introduce a safety factor for scaling the loans.

### Original Finding Content


When opening a position, the user makes a deposit and takes a loan against this on the Rubicon compound fork. This loan is taken using max liquidity:
<br><https://github.com/code-423n4/2023-04-rubicon/blob/main/contracts/utilities/poolsUtility/Position.sol#L306-L319>

```solidity
File: utilities/poolsUtility/Position.sol

306:    function _maxBorrow(
307:        address _bathToken
308:    ) internal view returns (uint256 _max) {
309:        (uint256 _err, uint256 _liq, uint256 _shortfall) = comptroller
310:            .getAccountLiquidity(address(this));
311:
312:        require(_err == 0, "_maxBorrow: ERROR");
313:        require(_liq > 0, "_maxBorrow: LIQUIDITY == 0");
314:        require(_shortfall == 0, "_maxBorrow: SHORTFALL != 0");
315:
316:        uint256 _price = oracle.getUnderlyingPrice(CToken(_bathToken));
317:        _max = (_liq.mul(10 ** 18)).div(_price);
318:        require(_max > 0, "_maxBorrow: can't borrow 0");
319:    }
```

The danger here, is the interest rate for a loan needs to be higher than the interest for the deposit of the collateral. Hence, the block after the loan is taken it will be under water.

Positions opened will, in the block after they are created, become under water and be possible to liquidate.

This only impacts a certain set of leverages (shorts 1x, longs 1.7x and so on) where you loan up to your collateral max; hence, medium severity.

A user will have to know about this behavior in `Position` and in the same tx (to be safe) increase their margin to not be vulnerable to liquidation.

### Proof of Concept

PoC test, `PositionTest.t.sol`:

    pragma solidity ^0.8.0;

    import "../../contracts/compound-v2-fork/WhitePaperInterestRateModel.sol";
    import "../../contracts/compound-v2-fork/CErc20Delegate.sol";
    import "../../contracts/compound-v2-fork/CErc20.sol";
    import "../../contracts/compound-v2-fork/Comptroller.sol";
    import "../../contracts/compound-v2-fork/CToken.sol";
    import "../../contracts/periphery/TokenWithFaucet.sol";
    import "../../contracts/periphery/DummyPriceOracle.sol";
    import "../../contracts/RubiconMarket.sol";
    import "../../contracts/BathHouseV2.sol";
    import "../../contracts/utilities/poolsUtility/Position.sol";
    import "../../contracts/utilities/poolsUtility/PoolsUtility.sol";

    import "forge-std/Test.sol";

    contract PositionTest is Test {
      //========================CONSTANTS========================
      address public owner;
      address FEE_TO = 0x0000000000000000000000000000000000000FEE;
      // core contracts
      RubiconMarket market;
      Comptroller comptroller;
      BathHouseV2 bathHouse;

      DummyPriceOracle oracle;

      // test tokens
      TokenWithFaucet TEST;
      TokenWithFaucet TUSDC;

      CErc20 cTEST;
      CErc20 cTUSDC;

      address alice = 0x0000000000000000000000000000000000000123;
      address bob = 0x0000000000000000000000000000000000000124;

      function setUp() public {
        owner = msg.sender;
        // deploy Comptroller instance
        comptroller = new Comptroller();

        // deploy new Market instance and init
        market = new RubiconMarket();
        market.initialize(FEE_TO);
        market.setFeeBPS(10);

        // deploy test tokens
        TEST = new TokenWithFaucet(address(this), "Test", "TEST", 18);
        TUSDC = new TokenWithFaucet(address(this), "Test Stablecoin", "TUSDC", 6);
        vm.label(address(TEST),"TEST");
        vm.label(address(TUSDC),"TUSDC");

        // baseRate = 0.3, multiplierPerYear = 0.02
        WhitePaperInterestRateModel irModel = new WhitePaperInterestRateModel(3e17, 2e16);
        CErc20Delegate bathTokenImplementation = new CErc20Delegate();

        bathHouse = new BathHouseV2();
        bathHouse.initialize(address(comptroller),address(this));
        bathHouse.createBathToken(address(TEST), irModel, 1e18, address(bathTokenImplementation), "");
        bathHouse.createBathToken(address(TUSDC), irModel, 1e18, address(bathTokenImplementation), "");

        cTEST = CErc20(bathHouse.getBathTokenFromAsset(address(TEST)));
        cTUSDC = CErc20(bathHouse.getBathTokenFromAsset(address(TUSDC)));

        // 1:1 for simplicity
        oracle = new DummyPriceOracle();
        oracle.addCtoken(cTUSDC,1e30);
        oracle.addCtoken(cTEST,1e18);

        comptroller._supportMarket(cTEST);
        comptroller._supportMarket(cTUSDC);
        comptroller._setPriceOracle(oracle);
        comptroller._setCloseFactor(0.5e18); // 0.5 close factor, same as compound mainnet
        comptroller._setLiquidationIncentive(1.08e18); // 8% same as compound mainnet
        comptroller._setCollateralFactor(cTEST,0.7e18);
        comptroller._setCollateralFactor(cTUSDC,0.7e18);

        TEST.mint(address(bob),100e18);
        vm.startPrank(bob);
        TEST.approve(address(cTEST),50e18);
        cTEST.mint(50e18);
        vm.stopPrank();

        // add some $$$ to the Market
        TEST.faucet();
        TUSDC.faucet();
        TEST.approve(address(market), type(uint256).max);
        TUSDC.approve(address(market), type(uint256).max);

        market.offer(100e6, TUSDC, 100e18, TEST);
      }

      function test_LiquidatePositionAfterCreation() public {
        PoolsUtility pools = new PoolsUtility();
        pools.initialize(address(oracle),address(market),address(bathHouse));

        vm.prank(alice);
        pools.createPosition();

        address[] memory positions = pools.getPositions(alice);
        Position position = Position(positions[0]);

        uint256 amount = 10e6;
        TUSDC.mint(alice,amount);
        vm.startPrank(alice);
        TUSDC.approve(address(position),amount);
        position.sellAllAmountWithLeverage(
            address(TUSDC),
            address(TEST),
            amount,
            1e18
        );
        vm.stopPrank();

        (, uint256 liquidity, uint256 shortfall) = comptroller.getAccountLiquidity(address(position));
        assertEq(0,liquidity);
        // position under water
        assertEq(0,shortfall);

        // next block
        vm.roll(block.number + 1);

        // trigger interest calculation
        uint256 borrowBalance = cTEST.borrowBalanceCurrent(address(position));

        (, liquidity, shortfall) = comptroller.getAccountLiquidity(address(position));
        assertEq(0,liquidity);
        assertGt(shortfall,0);

        // becomes liquidated
        vm.startPrank(bob);
        TEST.approve(address(cTEST),borrowBalance/2);
        cTEST.liquidateBorrow(address(position),borrowBalance/2,cTUSDC);
        vm.stopPrank();
      }
    }

`closeFactor` and `liquidationIncentive` is the same as compound on mainnet.

Added a mint function in the `TokenWithFaucet`:

```solidity
    function mint(address account, uint256 amount) external {
        _mint(account, amount);
    }
```

### Tools Used

Manual audit, forge

### Recommended Mitigation Steps

Introduce a safety factor to scale the loans, which the user can provide when opening the `position`.

**[daoio (Rubicon) confirmed via duplicate issue #827](https://github.com/code-423n4/2023-04-rubicon-findings/issues/827#issuecomment-1547185833)**

**[HickupHH3 (judge) increased severity to High and commented](https://github.com/code-423n4/2023-04-rubicon-findings/issues/1180#issuecomment-1549781170):**
 > Selected as best because of the POC, which showcases how the account is subject to liquidation in the next block after leveraging.

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
| Finders | immeas, cccz, kaden, ladboy233, 0xBeirao, ast3ros |

### Source Links

- **Source**: https://code4rena.com/reports/2023-04-rubicon
- **GitHub**: https://github.com/code-423n4/2023-04-rubicon-findings/issues/1180
- **Contest**: https://code4rena.com/reports/2023-04-rubicon

### Keywords for Search

`vulnerability`

