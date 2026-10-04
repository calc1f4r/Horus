---
# Core Classification
protocol: Escher
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6356
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-escher-contest
source_link: https://code4rena.com/reports/2022-12-escher
github_link: https://github.com/code-423n4/2022-12-escher-findings/issues/392

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - rwa

# Audit Details
report_date: unknown
finders_count: 50
finders:
  - HollaDieWaldfee
  - yixxas
  - pauliax
  - ladboy233
  - zapaz
---

## Vulnerability Title

[H-02] `LPDA` price can underflow the price due to bad settings and potentially brick the contract

### Overview


This bug report concerns the Dutch auction implemented in the `LPDA` contract. It is implemented by configuring a start price and price drop per second. A bad set of settings can cause an issue where the elapsed duration of the sale multiplied by the drop per second gets bigger than the start price and underflows the current price calculation. This means that if `temp.dropPerSecond * timeElapsed > temp.startPrice` then the unsigned integer result will become negative and underflow, leading to potentially bricking the contract and an eventual loss of funds. 

Due to Solidity 0.8 default checked math, the subtraction of the start price and the drop will cause a negative value that will generate an underflow in the unsigned integer type and lead to a transaction revert. Calls to `getPrice` will revert, and since this function is used in the `buy` to calculate the current NFT price it will also cause the buy process to fail. The price drop will continue to increase as time passes, making it impossible to recover from this situation and effectively bricking the contract. This will eventually lead to a loss of funds because currently the only way to end a sale and transfer funds to the sale and fee receiver is to buy the complete set of NFTs in the sale (i.e. buy everything up to the `sale.finalId`) which will be impossible if the `buy` function is bricked. 

The PoC demonstrates a test where the start price is 1500 and the duration is 1 hour (3600 seconds) with a drop of 1 per second. At about ~40% of the elapsed time the price drop will start underflowing the price, reverting the calls to both `getPrice` and `buy`. 

The recommendation is to add a validation in the `LPDAFactory.createLPDASale` function to ensure that the given duration and drop per second settings can't underflow the price. This will prevent the contract from being bricked and the eventual loss of funds.

### Original Finding Content


The dutch auction in the `LPDA` contract is implemented by configuring a start price and price drop per second.

A bad set of settings can cause an issue where the elapsed duration of the sale multiplied by the drop per second gets bigger than the start price and underflows the current price calculation.

<https://github.com/code-423n4/2022-12-escher/blob/main/src/minters/LPDA.sol#L117>

```solidity
function getPrice() public view returns (uint256) {
    Sale memory temp = sale;
    (uint256 start, uint256 end) = (temp.startTime, temp.endTime);
    if (block.timestamp < start) return type(uint256).max;
    if (temp.currentId == temp.finalId) return temp.finalPrice;

    uint256 timeElapsed = end > block.timestamp ? block.timestamp - start : end - start;
    return temp.startPrice - (temp.dropPerSecond * timeElapsed);
}
```

This means that if `temp.dropPerSecond * timeElapsed > temp.startPrice` then the unsigned integer result will become negative and underflow, leading to potentially bricking the contract and an eventual loss of funds.

### Impact

Due to Solidity 0.8 default checked math, the subtraction of the start price and the drop will cause a negative value that will generate an underflow in the unsigned integer type and lead to a transaction revert.

Calls to `getPrice` will revert, and since this function is used in the `buy` to calculate the current NFT price it will also cause the buy process to fail. The price drop will continue to increase as time passes, making it impossible to recover from this situation and effectively bricking the contract.

This will eventually lead to a loss of funds because currently the only way to end a sale and transfer funds to the sale and fee receiver is to buy the complete set of NFTs in the sale (i.e. buy everything up to the `sale.finalId`) which will be impossible if the `buy` function is bricked.

### Proof of Concept

In the following test, the start price is 1500 and the duration is 1 hour (3600 seconds) with a drop of 1 per second. At about \~40% of the elapsed time the price drop will start underflowing the price, reverting the calls to both `getPrice` and `buy`.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "forge-std/Test.sol";
import {FixedPriceFactory} from "src/minters/FixedPriceFactory.sol";
import {FixedPrice} from "src/minters/FixedPrice.sol";
import {OpenEditionFactory} from "src/minters/OpenEditionFactory.sol";
import {OpenEdition} from "src/minters/OpenEdition.sol";
import {LPDAFactory} from "src/minters/LPDAFactory.sol";
import {LPDA} from "src/minters/LPDA.sol";
import {Escher721} from "src/Escher721.sol";

contract AuditTest is Test {
    address deployer;
    address creator;
    address buyer;

    FixedPriceFactory fixedPriceFactory;
    OpenEditionFactory openEditionFactory;
    LPDAFactory lpdaFactory;

    function setUp() public {
        deployer = makeAddr("deployer");
        creator = makeAddr("creator");
        buyer = makeAddr("buyer");

        vm.deal(buyer, 1e18);

        vm.startPrank(deployer);

        fixedPriceFactory = new FixedPriceFactory();
        openEditionFactory = new OpenEditionFactory();
        lpdaFactory = new LPDAFactory();

        vm.stopPrank();
    }
    
    function test_LPDA_getPrice_NegativePrice() public {
        // Setup NFT and create sale
        vm.startPrank(creator);

        Escher721 nft = new Escher721();
        nft.initialize(creator, address(0), "Test NFT", "TNFT");

        // Duration is 1 hour (3600 seconds), with a start price of 1500 and a drop of 1, getPrice will revert and brick the contract at about 40% of the elapsed duration
        uint48 startId = 0;
        uint48 finalId = 1;
        uint80 startPrice = 1500;
        uint80 dropPerSecond = 1;
        uint96 startTime = uint96(block.timestamp);
        uint96 endTime = uint96(block.timestamp + 1 hours);

        LPDA.Sale memory sale = LPDA.Sale(
            startId, // uint48 currentId;
            finalId, // uint48 finalId;
            address(nft), // address edition;
            startPrice, // uint80 startPrice;
            0, // uint80 finalPrice;
            dropPerSecond, // uint80 dropPerSecond;
            endTime, // uint96 endTime;
            payable(creator), // address payable saleReceiver;
            startTime // uint96 startTime;
        );
        LPDA lpdaSale = LPDA(lpdaFactory.createLPDASale(sale));

        nft.grantRole(nft.MINTER_ROLE(), address(lpdaSale));

        vm.stopPrank();

        // simulate we are in the middle of the sale duration
        vm.warp(startTime + 0.5 hours);

        vm.startPrank(buyer);

        // getPrice will revert due to the overflow caused by the price becoming negative
        vm.expectRevert();
        lpdaSale.getPrice();

        // This will also cause the contract to be bricked, since buy needs getPrice to check that the buyer is sending the correct amount
        uint256 amount = 1;
        uint256 price = 1234;
        vm.expectRevert();
        lpdaSale.buy{value: price * amount}(amount);

        vm.stopPrank();
    }
}
```

### Recommendation

Add a validation in the `LPDAFactory.createLPDASale` function to ensure that the given duration and drop per second settings can't underflow the price.

```solidity
require((sale.endTime - sale.startTime) * sale.dropPerSecond <= sale.startPrice, "MAX DROP IS GREATER THAN START PRICE");
```

**[stevennevins (Escher) confirmed](https://github.com/code-423n4/2022-12-escher-findings/issues/392)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Escher |
| Report Date | N/A |
| Finders | HollaDieWaldfee, yixxas, pauliax, ladboy233, zapaz, Ch_301, minhtrng, carrotsmuggler, jadezti, lukris02, kaliberpoziomka8552, minhquanym, Chom, gz627, slvDev, danyams, mahdikarimi, 0x446576, kree-dotcom, 0xA5DF, adriro, nameruse, Franfran, reassor, hihen, immeas, jayphbee, 0xDecorativePineapple, 0xbepresent, sorrynotsorry, Ruhum, Aymen0909, Tricko, 0xRobocop, Madalad, hansfriese, chaduke, imare, Parth, 8olidity, lumoswiz, neumo, bin2chen, 0xDave, kiki_dev, evan, rvierdiiev, obront, jonatascm, poirots |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-escher
- **GitHub**: https://github.com/code-423n4/2022-12-escher-findings/issues/392
- **Contest**: https://code4rena.com/contests/2022-12-escher-contest

### Keywords for Search

`vulnerability`

