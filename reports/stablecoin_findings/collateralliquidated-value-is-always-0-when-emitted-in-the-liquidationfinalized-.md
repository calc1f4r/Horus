---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57312
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - hieutrinh02
  - joicygiore
  - crunter
  - johny7173
  - meeve
---

## Vulnerability Title

`collateralLiquidated` value is always 0 when emitted in the `LiquidationFinalized` event

### Overview

See description below for full details.

### Original Finding Content

## Summary

An incorrect value for `collateralLiquidated` is emitted in the `LiquidationFinalized` event due to deletion from the array before the event is emitted

## Vulnerability Details

By examining the event definition, we can see that `collateralLiquidated` should represent the total value of collateral that was liquidated.

```solidity
     /**
     * @notice Emitted when a liquidation is finalized
     * @param liquidator The address of the liquidator
     * @param user The address of the user being liquidated
     * @param debtRepaid The amount of debt repaid
     * @param collateralLiquidated The amount of collateral liquidated
     */
    event LiquidationFinalized(address indexed liquidator, address indexed user, uint256 debtRepaid, uint256 collateralLiquidated);
```

In the `finalizeLiquidation()` function, the following flow occurs:

```solidity
     /**
     * @notice Allows the Stability Pool to finalize the liquidation after the grace period has expired
     * @param userAddress The address of the user being liquidated
     */
    function finalizeLiquidation(address userAddress) external nonReentrant onlyStabilityPool {
        
        -- SNIPET --
               
         // Transfer NFTs to Stability Pool
        for (uint256 i = 0; i < user.nftTokenIds.length; i++) {
            uint256 tokenId = user.nftTokenIds[i];
            user.depositedNFTs[tokenId] = false;
            raacNFT.transferFrom(address(this), stabilityPool, tokenId);
        }
        delete user.nftTokenIds;

         -- SNIPET --

        //@audit-issue Wrong amount in the event, collateral value will always be 0 since the values are deleted beforehand
        emit LiquidationFinalized(stabilityPool, userAddress, userDebt, getUserCollateralValue(userAddress));
    }
```

The function `getUserCollateralValue()` which is called in the `LiquidationFinalized` event loop through the user's `nftTokenIds` array and sum up their prices.

```solidity
 function getUserCollateralValue(address userAddress) public view returns (uint256) {
        UserData storage user = userData[userAddress];
        uint256 totalValue = 0;

        for (uint256 i = 0; i < user.nftTokenIds.length; i++) {
            uint256 tokenId = user.nftTokenIds[i];
            uint256 price = getNFTPrice(tokenId);
            totalValue += price;
        }

        return totalValue;
    }
```

Since the whole array has been deleted before the event has been emitted (line `delete user.nftTokenIds`), the result from `getUserCollateralValue()` value will always be 0.

## POC

Adjust the test `should allow Stability Pool to close liquidation after grace period` in the `LendingPool.test.js` to also check the args of the emitted event like this:

```solidity
it("should allow Stability Pool to close liquidation after grace period", async function () {
      // Decrease house price and initiate liquidation
      // FIXME: we are using price oracle and therefore the price should be changed from the oracle.
      await raacHousePrices.setHousePrice(1, ethers.parseEther("90"));
      await lendingPool.connect(user2).initiateLiquidation(user1.address);
  
      // Advance time beyond grace period (72 hours)
      await ethers.provider.send("evm_increaseTime", [72 * 60 * 60 + 1]);
      await ethers.provider.send("evm_mine");
  
      // Fund the stability pool with crvUSD
      await crvusd.connect(owner).mint(owner.address, ethers.parseEther("1000"));

      // Set Stability Pool address (using owner for this test)
      await lendingPool.connect(owner).setStabilityPool(owner.address);
  
     //@audit add `withArgs` 
      await expect(lendingPool.connect(owner).finalizeLiquidation(user1.address))
        .to.emit(lendingPool, "LiquidationFinalized").withArgs(owner.address, user1.address, "100024403756302198934", 0);
        
      // Verify that the user is no longer under liquidation
      expect(await lendingPool.isUnderLiquidation(user1.address)).to.be.false;
  
      // Verify that the NFT has been transferred to the Stability Pool
      expect(await raacNFT.ownerOf(1)).to.equal(owner.address);

      // Verify that the user's debt has been repaid
      const userClosedLiquidationDebt = await lendingPool.getUserDebt(user1.address);
      expect(userClosedLiquidationDebt).to.equal(0);

      // Verify that the user's health factor is now at its maximum (type(uint256).max)
      const healthFactor = await lendingPool.calculateHealthFactor(user1.address);
      expect(healthFactor).to.equal(ethers.MaxUint256);

    });
```

## Impact

The inaccurate emitted event causes confusion and misleads users. It also makes protocol monitoring more difficult, as the collateral value always appears as 0. Additionally, this issue could impact the reliability of the protocol

## Tools Used

Manual review

## Recommendations

Save the collateral value in the local variable to be able to emit it correctly in the event

```Solidity

function finalizeLiquidation(address userAddress) external nonReentrant onlyStabilityPool {
        
        -- SNIPET --
  
        uint256 collateralValue = 0;  // local variable 

        for (uint256 i = 0; i < user.nftTokenIds.length; i++) {
            uint256 tokenId = user.nftTokenIds[i];
            collateralValue += getNFTPrice(tokenId); // add the price of each NFT 
            user.depositedNFTs[tokenId] = false;
            raacNFT.transferFrom(address(this), stabilityPool, tokenId);
        }
        delete user.nftTokenIds;

         -- SNIPET --
        emit LiquidationFinalized(stabilityPool, userAddress, userDebt, collateralValue);
    }
```

Adjust the test and rerun it:

```solidity
it("should allow Stability Pool to close liquidation after grace period", async function () {
      // Decrease house price and initiate liquidation
      // FIXME: we are using price oracle and therefore the price should be changed from the oracle.
      await raacHousePrices.setHousePrice(1, ethers.parseEther("90"));
      await lendingPool.connect(user2).initiateLiquidation(user1.address);
  
      // Advance time beyond grace period (72 hours)
      await ethers.provider.send("evm_increaseTime", [72 * 60 * 60 + 1]);
      await ethers.provider.send("evm_mine");
  
      // Fund the stability pool with crvUSD
      await crvusd.connect(owner).mint(owner.address, ethers.parseEther("1000"));

      // Set Stability Pool address (using owner for this test)
      await lendingPool.connect(owner).setStabilityPool(owner.address);

      const cV = await lendingPool.getUserCollateralValue(user1.address);
  
      await expect(lendingPool.connect(owner).finalizeLiquidation(user1.address))
        .to.emit(lendingPool, "LiquidationFinalized").withArgs(owner.address, user1.address, "100024403756302198934", cV);
        
      // Verify that the user is no longer under liquidation
      expect(await lendingPool.isUnderLiquidation(user1.address)).to.be.false;
  
      // Verify that the NFT has been transferred to the Stability Pool
      expect(await raacNFT.ownerOf(1)).to.equal(owner.address);

      // Verify that the user's debt has been repaid
      const userClosedLiquidationDebt = await lendingPool.getUserDebt(user1.address);
      expect(userClosedLiquidationDebt).to.equal(0);

      // Verify that the user's health factor is now at its maximum (type(uint256).max)
      const healthFactor = await lendingPool.calculateHealthFactor(user1.address);
      expect(healthFactor).to.equal(ethers.MaxUint256);

    });
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | hieutrinh02, joicygiore, crunter, johny7173, meeve, dimah7, avoloder, modey, joro |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

