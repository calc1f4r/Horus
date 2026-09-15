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
solodit_id: 57308
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
finders_count: 4
finders:
  - anonymousjoe
  - almur100
  - frndz0ne
  - t0x1c
---

## Vulnerability Title

When bad debt is accumulated the loss is not distributed amongst all suppliers leading to a huge loss for the last supplier to withdraw

### Overview


Summary:

The bug report discusses a vulnerability in a protocol that fails to distribute bad debt fairly among all suppliers. This leads to severe losses for the last supplier to withdraw, while early withdrawers suffer no loss. The report includes a Proof of Concept (PoC) code and its output, as well as the impact and tools used in the research. The report recommends that the protocol should distribute bad debt proportionally among all depositors to ensure fairness and reduce risk. 

### Original Finding Content

## Summary

When bad debt accumulates, it should be socialized among all suppliers to distribute the loss fairly.

However, the protocol fails to do this, causing only the **last users to withdraw** to bear the **full impact** of the bad debt. Early withdrawers suffer **no loss**, while the **last to withdraw** face **severe losses**.

## Vulnerability Details

The withdrawn assets is calculated as `shares * liquidityIndex` which does **not** take into account bad debt.

This means that even if bad debt accrues, the first users to withdraw will be able to withdraw their shares to assets at a **good rate**, leaving the last users with all the loss.

### PoC

```javascript
  import { expect, use } from 'chai';
  import hre from "hardhat";
  const { ethers } = hre;

  describe("RAAC PoC", function() {
    let owner, user1, user2, user3;
    let crvusd, raacNFT, raacHousePrices;
    let lendingPool, rToken, debtToken;
    let token;
  
    beforeEach(async function () {
      [owner, user1, user2, user3] = await ethers.getSigners();
  
      const CrvUSDToken = await ethers.getContractFactory("crvUSDToken");
      crvusd = await CrvUSDToken.deploy(owner.address);
    
      await crvusd.setMinter(owner.address);
    
      token = crvusd;
    
      const RAACHousePrices = await ethers.getContractFactory("RAACHousePrices");
      raacHousePrices = await RAACHousePrices.deploy(owner.address);
    
      const RAACNFT = await ethers.getContractFactory("RAACNFT");
      raacNFT = await RAACNFT.deploy(crvusd.target, raacHousePrices.target, owner.address);
    
    
      const RToken = await ethers.getContractFactory("RToken");
      rToken = await RToken.deploy("RToken", "RToken", owner.address, crvusd.target);
    
      const DebtToken = await ethers.getContractFactory("DebtToken");
      debtToken = await DebtToken.deploy("DebtToken", "DT", owner.address);
  
      const RAACToken = await ethers.getContractFactory("RAACToken");
      const raacToken = await RAACToken.deploy(owner.address, 100, 50);

      const DEToken = await ethers.getContractFactory("DEToken");
      const deToken = await DEToken.deploy("DEToken", "DEToken", owner.address, rToken.target);
    
      const initialPrimeRate = ethers.parseUnits("0.1", 27);
  
      const LendingPool = await ethers.getContractFactory("LendingPool");
      lendingPool = await LendingPool.deploy(
        crvusd.target,
        rToken.target,
        debtToken.target,
        raacNFT.target,
        raacHousePrices.target,
        initialPrimeRate
      );

      await lendingPool.setStabilityPool(owner.address);

      await rToken.setReservePool(lendingPool.target);
      await debtToken.setReservePool(lendingPool.target);
  
      await rToken.transferOwnership(lendingPool.target);
      await debtToken.transferOwnership(lendingPool.target);
  
      // mint tokens to users
      const mintAmount = ethers.parseEther("1000");
      await crvusd.mint(user1.address, mintAmount);
      await crvusd.mint(user2.address, mintAmount);
      await crvusd.mint(user3.address, mintAmount);
      await crvusd.mint(owner.address, ethers.parseEther("800"));
  
      await crvusd.connect(user1).approve(lendingPool.target, mintAmount);
      await crvusd.connect(user2).approve(lendingPool.target, mintAmount);
      await crvusd.connect(user3).approve(lendingPool.target, mintAmount);
  
      // set house prices
      await raacHousePrices.setOracle(owner.address);
      await raacHousePrices.setHousePrice(1, ethers.parseEther("500"));
      await raacHousePrices.setHousePrice(2, ethers.parseEther("500"));
  
      await ethers.provider.send("evm_mine", []);
  
      // mint NFTs to user1
      const tokenId = 1;
      const amountToPay1 = ethers.parseEther("500");
      const amountToPay2 = ethers.parseEther("500");
  
      await token.mint(user1.address, amountToPay1 + amountToPay2);
      await token.connect(user1).approve(raacNFT.target, amountToPay1 + amountToPay2);
      await raacNFT.connect(user1).mint(tokenId, amountToPay1);
      await raacNFT.connect(user1).mint(tokenId + 1, amountToPay2);
  
      // suppliers deposits assets into the lending pool
      const depositAmount = ethers.parseEther("1000");
      await crvusd.connect(user2).approve(lendingPool.target, depositAmount);
      await lendingPool.connect(user2).deposit(depositAmount);
      await crvusd.connect(user3).approve(lendingPool.target, depositAmount);
      await lendingPool.connect(user3).deposit(depositAmount);
  
      await ethers.provider.send("evm_mine", []);
  
      expect(await crvusd.balanceOf(rToken.target)).to.equal(ethers.parseEther("2000"));
    });
    it("does not distribute the loss among all suppliers during bad debt", async () => {
      // borrower provides collateral (1000e18)
      const tokenId1 = 1;
      const tokenId2 = 2;
      await raacNFT.connect(user1).approve(lendingPool.target, tokenId1);
      await lendingPool.connect(user1).depositNFT(tokenId1);
      await raacNFT.connect(user1).approve(lendingPool.target, tokenId2);
      await lendingPool.connect(user1).depositNFT(tokenId2);

      // borrows 800e18 (ltv = 80%)
      await lendingPool.connect(user1).borrow(ethers.parseEther("800"));
      
      // the borrower's collateral drops by 40% in value (ltv = 120%) => extremely unhealthy ltv | low health factor
      await raacHousePrices.setHousePrice(1, ethers.parseEther("300"));
      await raacHousePrices.setHousePrice(2, ethers.parseEther("300"));

      // liquidate borrower
      await lendingPool.initiateLiquidation(user1.address);
      
      // increase time by 3 days
      await ethers.provider.send("evm_increaseTime", [72 * 60 * 60 + 1]);
      await ethers.provider.send("evm_mine");

      // finalize liquidation | the stability pool does not have enough assets to cover the bad debt
      // using the owner as stability pool for simplicity
      await expect(lendingPool.connect(owner).finalizeLiquidation(user1.address))
        .to.be.revertedWithCustomError(crvusd, "ERC20InsufficientAllowance");
      
      // the protocol is now suffering from bad debt accrual => suppliers withdraw their assets
      await lendingPool.connect(user2).withdraw(ethers.parseEther("1000"));
      // the last supplier to withdraw faces the full impact of the bad debt
      await expect(lendingPool.connect(user3).withdraw(ethers.parseEther("1000")))
        .to.be.revertedWithCustomError(crvusd, "ERC20InsufficientBalance");

      console.log("User1 balance: ", await crvusd.balanceOf(user2));
      console.log("user2 balance: ", await crvusd.balanceOf(user3));
    });
  });
```

#### Output

```Solidity
  RAAC PoC
User1 balance:  1000000000000000000000n
user2 balance:  0n
    ✔ does not distribute the loss among all suppliers during bad debt (5553ms)


  1 passing (25s)
```

## Impact

* **Severe fund loss** for the last users to withdraw.

* **Early withdrawers profit at the expense of late withdrawers**.

* **Unfair distribution of risk**, reducing protocol **trust and stability**.

## Tools Used

Manual Reseach, VSCode

## Recommendations

Ensure bad debt is proportionally distributed among all depositors rather than **concentrated** on the last to withdraw.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | anonymousjoe, almur100, frndz0ne, t0x1c |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

