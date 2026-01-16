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
solodit_id: 57299
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 14
finders:
  - patitonar
  - sunless_
  - 0x23r0
  - vasquez
  - z3nithpu1se
---

## Vulnerability Title

Users can lose additional collateral by depositing NFTs after grace period expiration

### Overview


This bug report discusses a problem in the code of the LendingPool function, which is used in a decentralized finance (DeFi) platform. The problem is that the function does not check if a user is under liquidation and if their grace period has expired. This means that users can deposit additional non-fungible tokens (NFTs) in an attempt to save their position, but if they fail to do so before the grace period ends, they will lose not only their original collateral but also the newly deposited NFTs. This can result in users losing more value than their original debt. The report includes a proof of concept and recommendations for fixing the issue.

### Original Finding Content

## Summary

The `LendingPool::depositNFT` function does not check if a user is under liquidation and if their grace period has expired. This allows users to deposit additional NFTs in an attempt to increase their health factor, but if they fail to close the liquidation because of the grace period expiration, they will lose all collateral including the newly deposited NFTs.

## Vulnerability Details

The `LendingPool::depositNFT` function lacks checks for:

1. Whether the user is under liquidation (`isUnderLiquidation[msg.sender]`)
2. Whether their grace period has expired (`block.timestamp > liquidationStartTime[msg.sender] + liquidationGracePeriod`)

This allows users to deposit additional NFTs even when their position is already eligible for liquidation and after the grace period has expired, resulting in the loss of more collateral than necessary.

## Impact

Users under liquidation can lose additional collateral by attempting to save their position after the grace period has expired. Since `finalizeLiquidation()` transfers all NFTs to the Stability Pool, any newly deposited NFTs will also be liquidated, causing users to lose more value than their original debt.

For example:

1. User has 100k debt and 125k in NFT collateral
2. Position becomes liquidatable and grace period expires
3. User deposits additional 50k NFT trying to save position
4. Liquidation executes, user loses 175k collateral to cover 100k debt

## Tools Used

Manual review

## Proof of Concept

Add the following test case to the `test/unit/core/pools/LendingPool/LendingPool.test.js` file in the `Liquidation` section:

```javascript
it("should demonstrate loss of additional collateral after grace period", async function () {
    // Set Stability Pool address (using owner for this test)
    await lendingPool.connect(owner).setStabilityPool(owner.address);
    await token.mint(owner.address, ethers.parseEther("100"));

    // Decrease house price and initiate liquidation
    await raacHousePrices.setHousePrice(1, ethers.parseEther("90"));

    // Initiate liquidation
    await lendingPool.connect(user2).initiateLiquidation(user1.address);

    // Advance time beyond grace period (72 hours)
    await ethers.provider.send("evm_increaseTime", [72 * 60 * 60 + 1]);
    await ethers.provider.send("evm_mine");

    // Verify the health factor is below the liquidation threshold
    const healthFactor = await lendingPool.calculateHealthFactor(user1.address);
    const healthFactorLiquidationThreshold = await lendingPool.healthFactorLiquidationThreshold();
    expect(healthFactor).to.be.lt(healthFactorLiquidationThreshold);

    // Mint new NFT to User1
    const tokenId = 2;
    await raacHousePrices.setHousePrice(tokenId, ethers.parseEther("100"));
    const housePrice = await raacHousePrices.tokenToHousePrice(tokenId);
    await token.mint(user1.address, housePrice);
    await token.connect(user1).approve(raacNFT.target, housePrice);
    await raacNFT.connect(user1).mint(tokenId, housePrice);

    // Deposit new NFT to collateral
    await raacNFT.connect(user1).approve(lendingPool.target, tokenId);
    await lendingPool.connect(user1).depositNFT(tokenId);

    // Verify the new health factor is below the liquidation threshold
    const healthFactorAfterDeposit = await lendingPool.calculateHealthFactor(user1.address);
    expect(healthFactorAfterDeposit).to.be.gt(healthFactorLiquidationThreshold);

    // User1 is still under liquidation 
    expect(await lendingPool.isUnderLiquidation(user1.address)).to.be.true;

    // User1 is not able to close liquidation
    await expect(lendingPool.connect(user1).closeLiquidation())
    .to.be.revertedWithCustomError(lendingPool, "GracePeriodExpired");

    // Stability Pool closes liquidation
    await expect(lendingPool.connect(owner).finalizeLiquidation(user1.address))
    .to.emit(lendingPool, "LiquidationFinalized")
    
    // Verify that the user is no longer under liquidation
    expect(await lendingPool.isUnderLiquidation(user1.address)).to.be.false;

    // Verify that the NFT has been transferred to the Stability Pool
    expect(await raacNFT.ownerOf(1)).to.equal(owner.address);
    expect(await raacNFT.ownerOf(tokenId)).to.equal(owner.address);
});
```

## Recommendations

Add liquidation status checks to the `depositNFT` function:

```diff
function depositNFT(uint256 tokenId) external nonReentrant whenNotPaused {
+   if (isUnderLiquidation[msg.sender] && 
+       block.timestamp > liquidationStartTime[msg.sender] + liquidationGracePeriod) {
+       revert CannotDepositAfterGracePeriod();
+   }
    // Rest of the function...
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | patitonar, sunless_, 0x23r0, vasquez, z3nithpu1se, heliosophistxiv, 0xekkoo, octeezy, federodes, mill1995, modey, 0xgee001, tigerfrake, charlescheerful |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

