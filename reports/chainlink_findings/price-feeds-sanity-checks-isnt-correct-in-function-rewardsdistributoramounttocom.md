---
# Core Classification
protocol: Alchemix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38194
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/alchemix-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31383%20-%20%5bSC%20-%20Low%5d%20price%20feeds%20sanity%20checks%20isnt%20correct%20in%20funct....md

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

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - jasonxiale
---

## Vulnerability Title

price feed's sanity checks isn't correct in function `RewardsDistributor.amountToCompound`

### Overview

See description below for full details.

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/RewardsDistributor.sol

Impacts:
- Protocol insolvency

## Description
## Brief/Intro
The timestamp of the price update (priceTimestamp) is checked to be less than 60 days in the past, however the oracle's heartbeat is 24 hours. Hence, any price older than the heartbeat might actually be stale

## Vulnerability Details
In [RewardsDistributor.amountToCompound](https://github.com/alchemix-finance/alchemix-v2-dao/blob/f1007439ad3a32e412468c4c42f62f676822dc1f/src/RewardsDistributor.sol#L116-L133), the function use `require(block.timestamp - priceTimestamp < staleThreshold, "Price is stale");` to check for stale price, which is not correct.

```solidity
116     function amountToCompound(uint256 _alcxAmount) public view returns (uint256, uint256[] memory) {
117         // Increased for testing since tests go into future
118         uint256 staleThreshold = 60 days;
119 
120         (uint80 roundId, int256 alcxEthPrice, , uint256 priceTimestamp, uint80 answeredInRound) = priceFeed
121             .latestRoundData();
122 
123         require(answeredInRound >= roundId, "Stale price");
124         require(block.timestamp - priceTimestamp < staleThreshold, "Price is stale"); <<<--- Here the function checks stale price using 60 days
125         require(alcxEthPrice > 0, "Chainlink answer reporting 0");
126 
127         uint256[] memory normalizedWeights = IManagedPool(address(balancerPool)).getNormalizedWeights();
128 
129         uint256 amount = (((_alcxAmount * uint256(alcxEthPrice)) / 1 ether) * normalizedWeights[0]) /
130             normalizedWeights[1];
131 
132         return (amount, normalizedWeights);
133     }
```

## Impact Details
The timestamp of the price update (priceTimestamp) is checked to be less than 60 days in the past, however the oracle's heartbeat is 24 hours. Hence, any price older than the heartbeat might actually be stale.

## References
Add any relevant links to documentation or code



## Proof of Concept
In the follow code, I will demo that [RewardsDistributor.amountToCompound](https://github.com/alchemix-finance/alchemix-v2-dao/blob/f1007439ad3a32e412468c4c42f62f676822dc1f/src/RewardsDistributor.sol#L116-L133) can use stale price. And because `RewardsDistributor.amountToCompound` is used by `RewardsDistributor.claim` in [RewardsDistributor.sol#L175](https://github.com/alchemix-finance/alchemix-v2-dao/blob/f1007439ad3a32e412468c4c42f62f676822dc1f/src/RewardsDistributor.sol#L175), so the stale price might impact the transaction.

Add the following code in `src/test/Minter.t.sol` and run
```bash
FOUNDRY_PROFILE=default forge test --fork-url https://eth-mainnet.alchemyapi.io/v2/0TbY2mhyGA4gLPShfh-PwBlQ3PDNUdL1 --fork-block-number 17133822 --mc MinterTest --mt testPriceFeedStalePrice -vv
[⠊] Compiling...
No files changed, compilation skipped

Ran 1 test for src/test/Minter.t.sol:MinterTest
[PASS] testPriceFeedStalePrice() (gas: 68962)
Logs:
  block.timestamp                   : 1682553635
  block.number                      : 17133822
  roundId                           : 18446744073709554224
  alcxEthPrice                      : 9554123643227504
  startedAt                         : 1682506295
  priceTimestamp                    : 1682506295
  answeredInRound                   : 18446744073709554224
  amountToCompound()                : 238853091080687600
  ----------forward 50 days---------
  block.timestamp                   : 1686873635
  block.number                      : 17133822
  roundId                           : 18446744073709554224
  alcxEthPrice                      : 9554123643227504
  startedAt                         : 1682506295
  priceTimestamp                    : 1682506295
  answeredInRound                   : 18446744073709554224
  amountToCompound()                : 238853091080687600

Suite result: ok. 1 passed; 0 failed; 0 skipped; finished in 5.71ms (426.97µs CPU time)

Ran 1 test suite in 1.84s (5.71ms CPU time): 1 tests passed, 0 failed, 0 skipped (1 total tests)
```

For the output above, we can see that even after 50 days, function  `RewardsDistributor.amountToCompound` doesn't revert, which isn't right.

```solidity
    function testPriceFeedStalePrice() public {

        AggregatorV3Interface priceFeed = distributor.priceFeed();
        
        uint80 roundId;
        int256 alcxEthPrice;
        uint256 startedAt;
        uint256 priceTimestamp;
        uint80 answeredInRound;
        uint256 amount; 

        (roundId, alcxEthPrice, startedAt, priceTimestamp, answeredInRound) = priceFeed.latestRoundData();
        (amount, ) = distributor.amountToCompound(100e18);
        console2.log("block.timestamp                   :", block.timestamp);
        console2.log("block.number                      :", block.number);
        console2.log("roundId                           :", roundId);
        console2.log("alcxEthPrice                      :", uint(alcxEthPrice));
        console2.log("startedAt                         :", startedAt);
        console2.log("priceTimestamp                    :", priceTimestamp);
        console2.log("answeredInRound                   :", answeredInRound);
        console2.log("amountToCompound()                :", amount);
    
        console2.log("----------forward 50 days---------");
        // Here we forward 50 days, and we can call `distributor.amountToCompound` without revert
        hevm.warp(block.timestamp + 50 days);
        (roundId, alcxEthPrice, startedAt, priceTimestamp, answeredInRound) = priceFeed.latestRoundData();
        (amount, ) = distributor.amountToCompound(100e18);
        console2.log("block.timestamp                   :", block.timestamp);
        console2.log("block.number                      :", block.number);
        console2.log("roundId                           :", roundId);
        console2.log("alcxEthPrice                      :", uint(alcxEthPrice));
        console2.log("startedAt                         :", startedAt);
        console2.log("priceTimestamp                    :", priceTimestamp);
        console2.log("answeredInRound                   :", answeredInRound);
        console2.log("amountToCompound()                :", amount);
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Alchemix |
| Report Date | N/A |
| Finders | jasonxiale |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31383%20-%20%5bSC%20-%20Low%5d%20price%20feeds%20sanity%20checks%20isnt%20correct%20in%20funct....md
- **Contest**: https://immunefi.com/bounty/alchemix-boost/

### Keywords for Search

`vulnerability`

