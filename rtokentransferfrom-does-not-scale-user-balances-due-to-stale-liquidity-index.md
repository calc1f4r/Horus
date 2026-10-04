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
solodit_id: 57175
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
finders_count: 34
finders:
  - kalogerone
  - t0x1c
  - nadirkhansec
  - bshyuunn
  - amarfares
---

## Vulnerability Title

RToken.transferFrom() Does Not Scale User Balances Due to Stale Liquidity Index

### Overview


This bug report discusses a problem with the `transferFrom()` function in the RToken contract. This function is supposed to adjust transfer amounts based on the current liquidity index to account for accrued interest. However, due to a coding error, the liquidity index is not updated and remains at its initial value of 1e27. As a result, transfer amounts are not correctly adjusted for interest accrual and user balances are not accurately reflected. This can lead to incorrect balance transfers and accounting inaccuracies. The report recommends implementing a dynamic liquidity index or regularly updating the index to ensure accurate scaling of transfers.

### Original Finding Content

## Summary

The `transferFrom()` function in the RToken contract is intended to scale transfer amounts based on the current liquidity index to reflect accrued interest. However, because the liquidity index (`_liquidityIndex`) is never updated in RToken.sol and remains fixed at its initial value (1e27), the scaling operation effectively does nothing. As a result, user balances are not correctly adjusted for interest accrual.

## Vulnerability Details

* **Stale Liquidity Index:** The `_liquidityIndex` is set during contract initialization and is meant to be updated by `updateLiquidityIndex()`. However, this function is never invoked by the LendingPool or any other contract, leaving `_liquidityIndex` permanently at 1e27.

- **Ineffective Scaling in transferFrom():** The function attempts to scale the transfer amount by dividing it by `_liquidityIndex` using `rayDiv()`, but since `_liquidityIndex` remains at 1e27, the scaling does not reflect any accrued interest.

  **Root Cause Code Snippet (RToken.sol):**

```Solidity
    //@audit - liquidity pool NEVER calls the function below. i.e. this fn is unusable.
    function updateLiquidityIndex(uint256 newLiquidityIndex) external override onlyReservePool {
        if (newLiquidityIndex < _liquidityIndex) revert InvalidAmount();
        _liquidityIndex = newLiquidityIndex;
        emit LiquidityIndexUpdated(newLiquidityIndex);
    }
```

**Affected Code Snippet (RToken.sol):**

```Solidity
function transferFrom(address sender, address recipient, uint256 amount) public override(ERC20, IERC20) returns (bool) {
        uint256 scaledAmount = amount.rayDiv(_liquidityIndex);//@audit this liquidity index is always 1e27.. i.e. NO SCALING or INTEREST.
        return super.transferFrom(sender, recipient, scaledAmount);
    }
```

## Poc:

Run the test below in LendingPool.test.js with command:

```Solidity
npx hardhat test test/unit/core/pools/LendingPool/LendingPool.test.js --show-stack-traces
```

```Solidity
describe.only("RToken.transferFrom() Scaling Bug", function () {
    it("should transfer tokens using the stale liquidity index instead of the updated normalized income", async function () {
      // STEP 1: user1 deposits 1000 crvUSD into the lending pool to receive RToken.
      const user2initialBal = await rToken.balanceOf(user2.address); // initial balance of user2
      const depositAmount = ethers.parseEther("1000");
      await crvusd.connect(user1).approve(lendingPool.target, depositAmount);
      await lendingPool.connect(user1).deposit(depositAmount);
      const initialBalanceUser1 = await rToken.balanceOf(user1.address);
      expect(initialBalanceUser1).to.equal(depositAmount);

      // STEP 2: Mint an NFT for user1, deposit it as collateral, and then borrow some funds.
      const nftTokenId = 2; // assume token id 2 is available
      const nftPrice = ethers.parseEther("100");
      await raacHousePrices.setHousePrice(nftTokenId, nftPrice);
      await token.mint(user1.address, nftPrice);
      await token.connect(user1).approve(raacNFT.target, nftPrice);
      await raacNFT.connect(user1).mint(nftTokenId, nftPrice);
      await raacNFT.connect(user1).approve(lendingPool.target, nftTokenId);
      await lendingPool.connect(user1).depositNFT(nftTokenId);
      const borrowAmount = ethers.parseEther("50");
      await lendingPool.connect(user1).borrow(borrowAmount);

      // STEP 3: Advance time and update state so that interest accrues.
      await ethers.provider.send("evm_increaseTime", [30 * 24 * 60 * 60]);
      await ethers.provider.send("evm_mine", []);
      await lendingPool.connect(user1).updateState();

      // Retrieve the updated normalized income.
      const updatedNormalizedIncome = await lendingPool.getNormalizedIncome();
      console.log(
        "Updated normalized income:",
        updatedNormalizedIncome.toString()
      );

      // Retrieve the current (stale) liquidity index.
      const currentLiquidityIndex = await rToken.getLiquidityIndex();
      console.log(
        "Current liquidity index (stale):",
        currentLiquidityIndex.toString()
      );

      // STEP 4: Let user1 approve user2 to transfer 100 underlying crvUSD worth of RToken.
      const transferUnderlying = ethers.parseEther("100");
      await rToken.connect(user1).approve(user2.address, transferUnderlying);

      // Convert amounts to BigInt for calculations.
      const transferUnderlyingBigInt = BigInt(transferUnderlying.toString());
      const currentLiquidityIndexBigInt = BigInt(
        currentLiquidityIndex.toString()
      );
      const updatedNormalizedIncomeBigInt = BigInt(
        updatedNormalizedIncome.toString()
      );

      // Compute what the transfer amount would be if the updated normalized income were used.
      // expectedScaledTransfer = transferUnderlying * (stale liquidity index) / (updated normalized income).
      const expectedScaledTransfer =
        (transferUnderlyingBigInt * currentLiquidityIndexBigInt) /
        updatedNormalizedIncomeBigInt;
      // However, transferFrom() uses the stale liquidity index, so the actual scaled transfer is:
      // actualScaledTransfer = transferUnderlying * (stale liquidity index) / (stale liquidity index) = transferUnderlying.
      const actualScaledTransfer =
        (transferUnderlyingBigInt * currentLiquidityIndexBigInt) /
        currentLiquidityIndexBigInt;

      // Because updatedNormalizedIncome is higher than the stale liquidity index,
      // expectedScaledTransfer should be less than actualScaledTransfer.
      expect(actualScaledTransfer).to.be.gt(expectedScaledTransfer);

      // STEP 5: Execute transferFrom() – this call uses the stale liquidity index.
      await rToken
        .connect(user2)
        .transferFrom(user1.address, user2.address, transferUnderlying);

      // STEP 6: Verify that user2's final balance equals their initial balance plus the transfer amount computed
      // using the stale liquidity index (actualScaledTransfer), not the lower amount expected if updated normalized income were used.
      const user2ActualBalance = await rToken.balanceOf(user2.address);

      const user2ExpectedBalance =
        user2ActualBalance - actualScaledTransfer + expectedScaledTransfer;

      console.log("user2 Expected Balance:", user2ExpectedBalance);
      console.log("user2 Actual Balance:  ", user2ActualBalance);

      expect(user2ExpectedBalance).to.not.equal(user2ActualBalance);

      expect(expectedScaledTransfer).to.not.equal(actualScaledTransfer);

      console.log("expectedScaledTransfer:  ", expectedScaledTransfer);
      console.log("actualScaledTransfer:  ", actualScaledTransfer);
    });
  });
```

## Impact

* **Incorrect Balance Transfers:** Users’ balances are transferred without proper scaling, which undermines the interest-bearing feature of the RToken.
* **Accounting Inaccuracies:** Downstream functions such as `balanceOf()` and other transfer-related logic that depend on scaled balances will not accurately represent users’ holdings, jeopardizing the integrity of the lending and borrowing mechanisms.

## Tools Used

Manual review, Hardhat

## Recommendations

* **Dynamic Liquidity Index:** Instead of relying on the stale `_liquidityIndex`, the function should fetch the current liquidity index from the reserve pool using `getNormalizedIncome()`. This ensures that transfers are scaled according to the actual accrued interest.

- **Update Index Mechanism:** Alternatively, ensure that `updateLiquidityIndex()` is regularly called (for example, via automated triggers or integrated into common user actions) so that `_liquidityIndex` reflects the current interest conditions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | kalogerone, t0x1c, nadirkhansec, bshyuunn, amarfares, kapten_crtz, casinocompiler, 0x23r0, 0xnforcer, fresh, theirrationalone, damilolaedwards, farismaulana, aksoy, notbozho, roccomania, bluedragon, charlescheerful, moray5554, i3arba, 0xlouistsai, kirobrejka, agent3bood, h2134, foufrix, tigerfrake, kupiasec, tinnohofficial, trtrth, 0xmystery, 0xaadi, 0xtimefliez |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

