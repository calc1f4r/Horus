---
# Core Classification
protocol: The Standard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41593
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clql6lvyu0001mnje1xpqcuvl
source_link: none
github_link: https://github.com/Cyfrin/2023-12-the-standard

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
finders_count: 1
finders:
  - t0x1c
---

## Vulnerability Title

User can get liquidated due to incorrect calculateMinimumAmountOut()

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2023-12-the-standard/blob/main/contracts/SmartVaultV3.sol#L206-L212">https://github.com/Cyfrin/2023-12-the-standard/blob/main/contracts/SmartVaultV3.sol#L206-L212</a>


## Summary
[calculateMinimumAmountOut()](https://github.com/Cyfrin/2023-12-the-standard/blob/main/contracts/SmartVaultV3.sol#L206-L212) calculations are prone to rounding-down error (almost every time). This means a user calling [swap](https://github.com/Cyfrin/2023-12-the-standard/blob/main/contracts/SmartVaultV3.sol#L225) will be undercollateralized if he receives this function's returned value (later being set as the `amountOutMinimum` inside `ISwapRouter.ExactInputSingleParams`), as the swap's `amountOut`. He can be immediately liquidated and the user unfairly loses his assets. <br>
The code should have checked at the end of the function whether the returned value will cause the vault to be undercollateralized.

[SmartVaultV3.sol::calculateMinimumAmountOut()](https://github.com/Cyfrin/2023-12-the-standard/blob/main/contracts/SmartVaultV3.sol#L206-L212)
```js
    function calculateMinimumAmountOut(bytes32 _inTokenSymbol, bytes32 _outTokenSymbol, uint256 _amount) private view returns (uint256) {
        ISmartVaultManagerV3 _manager = ISmartVaultManagerV3(manager);
        uint256 requiredCollateralValue = minted * _manager.collateralRate() / _manager.HUNDRED_PC();                         <---------------- @audit : rounding error here.
        uint256 collateralValueMinusSwapValue = euroCollateral() - calculator.tokenToEur(getToken(_inTokenSymbol), _amount);
        return collateralValueMinusSwapValue >= requiredCollateralValue ?
            0 : calculator.eurToToken(getToken(_outTokenSymbol), requiredCollateralValue - collateralValueMinusSwapValue);    <---------------- @audit : missing a check here.
    }
```

[SmartVaultV3.sol::swap()](https://github.com/Cyfrin/2023-12-the-standard/blob/main/contracts/SmartVaultV3.sol#L225)
```js
    function swap(bytes32 _inToken, bytes32 _outToken, uint256 _amount) external onlyOwner {
        uint256 swapFee = _amount * ISmartVaultManagerV3(manager).swapFeeRate() / ISmartVaultManagerV3(manager).HUNDRED_PC();
        address inToken = getSwapAddressFor(_inToken);
@---->  uint256 minimumAmountOut = calculateMinimumAmountOut(_inToken, _outToken, _amount);
        ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams({
                tokenIn: inToken,
                tokenOut: getSwapAddressFor(_outToken),
                fee: 3000,
                recipient: address(this),
                deadline: block.timestamp,
                amountIn: _amount - swapFee,
@-------->      amountOutMinimum: minimumAmountOut,
                sqrtPriceLimitX96: 0
            });
        inToken == ISmartVaultManagerV3(manager).weth() ?
            executeNativeSwapAndFee(params, swapFee) :
            executeERC20SwapAndFee(params, swapFee);
    }
```

## PoC
We will pick up the example from the [pre-existing unit test](https://github.com/Cyfrin/2023-12-the-standard/blob/main/test/smartVault.js#L345) `invokes swaprouter with value for eth swap, paying fees to protocol`, so that it's simpler to demonstrate. Apply the following patch to add steps to the test. Minor changes have also been made to `SmartVault3.sol` to enable logging inside the test:

```diff
diff --git a/contracts/SmartVaultV3.sol b/contracts/SmartVaultV3.sol
index fdc492d..7296c73 100644
--- a/contracts/SmartVaultV3.sol
+++ b/contracts/SmartVaultV3.sol
@@ -24,7 +24,7 @@ contract SmartVaultV3 is ISmartVault {
     IPriceCalculator public immutable calculator;
 
     address public owner;
-    uint256 private minted;
+    uint256 public minted;
     bool private liquidated;
 
     event CollateralRemoved(bytes32 symbol, uint256 amount, address to);
@@ -72,7 +72,7 @@ contract SmartVaultV3 is ISmartVault {
         }
     }
 
-    function maxMintable() private view returns (uint256) {
+    function maxMintable() public view returns (uint256) {
         return euroCollateral() * ISmartVaultManagerV3(manager).HUNDRED_PC() / ISmartVaultManagerV3(manager).collateralRate();
     }
 
diff --git a/test/smartVault.js b/test/smartVault.js
index 464b603..f9e39e2 100644
--- a/test/smartVault.js
+++ b/test/smartVault.js
@@ -348,17 +348,20 @@ describe('SmartVault', async () => {
       // user borrows 1200 EUROs
       const borrowValue = ethers.utils.parseEther('1200');
       await Vault.connect(user).mint(user.address, borrowValue);
+      console.log("Before Swap: is undercollateralized: %s, minted: %s, maxMintable: %s", await Vault.undercollateralised(), await Vault.minted(), await Vault.maxMintable());
+      expect(await Vault.undercollateralised()).to.eq(false);
+
       const inToken = ethers.utils.formatBytes32String('ETH');
       const outToken = ethers.utils.formatBytes32String('sUSD');
       // user is swapping .5 ETH
       const swapValue = ethers.utils.parseEther('0.5');
       const swapFee = swapValue.mul(PROTOCOL_FEE_RATE).div(HUNDRED_PC);
       // minimum collateral after swap must be €1200 (borrowed) + €6 (fee) * 1.2 (rate) = €1447.2
-      // remaining collateral not swapped: .5 ETH * $1600 = $800 = $800 / 1.06 = €754.72
-      // swap must receive at least €1320 - €754.72 = €692.48 = $734.032;
+      // remaining collateral not swapped: (1 - .5) ETH * $1600 = $800 = $800 / 1.06 = €754.72
+      // swap must receive at least €1447.2 - €754.72 = €692.48 = $734.032;
       const ethCollateralValue = swapValue.mul(DEFAULT_ETH_USD_PRICE).div(DEFAULT_EUR_USD_PRICE);
       const borrowFee = borrowValue.mul(PROTOCOL_FEE_RATE).div(HUNDRED_PC);
-      const minCollateralInUsd = borrowValue.add(borrowFee).mul(DEFAULT_COLLATERAL_RATE).div(HUNDRED_PC) // 110% of borrowed (with fee)
+      const minCollateralInUsd = borrowValue.add(borrowFee).mul(DEFAULT_COLLATERAL_RATE).div(HUNDRED_PC) // 120% of borrowed (with fee)
                                   .sub(ethCollateralValue) // some collateral will not be swapped
                                   .mul(DEFAULT_EUR_USD_PRICE).div(100000000) // convert to USD
                                   .div(BigNumber.from(10).pow(12)) // scale down because stablecoin is 6 dec
@@ -381,6 +384,20 @@ describe('SmartVault', async () => {
       expect(sqrtPriceLimitX96).to.equal(0);
       expect(txValue).to.equal(swapValue.sub(swapFee));
       expect(await protocol.getBalance()).to.equal(protocolBalance.add(swapFee));
+      
+      // @audit-info : credit the vault with `amountOutMinimum` worth of tokenOut to simulate completion of swap
+      await Stablecoin.mint(Vault.address, amountOutMinimum);
+      console.log("After Swap: is undercollateralized: %s, minted: %s, maxMintable: %s", await Vault.undercollateralised(), await Vault.minted(), await Vault.maxMintable());
+      expect(await Vault.undercollateralised()).to.eq(true);
+      
+      // @audit : vault can now be liquidated
+      await expect(VaultManager.connect(protocol).liquidateVault(1)).not.to.be.reverted;
+      const { minted, maxMintable, totalCollateralValue, collateral, liquidated } = await Vault.status();
+      expect(minted).to.equal(0);
+      expect(maxMintable).to.equal(0);
+      expect(totalCollateralValue).to.equal(0);
+      collateral.forEach(asset => expect(asset.amount).to.equal(0));
+      expect(liquidated).to.equal(true);
     });
 
     it('amount out minimum is 0 if over collateral still', async () => {
```

In the above test, once the swap is done, to simulate credit of the `tokenOut` we have credited the Vault with a value exactly equal to `amountOutMinimum`. We then checked if vault's liquidation was possible. Run the above via `npx hardhat test --grep 'invokes swaprouter with value for eth swap, paying fees to protocol'` to see the output:
```text
  SmartVault
    swaps
Before Swap: is undercollateralized: false, minted: 1206000000000000000000, maxMintable: 1257861635220125786163
After Swap:  is undercollateralized: true,  minted: 1206000000000000000000, maxMintable: 1205999999999999999999     <-------------- rounding-down leading to undercollateralization.
```

We were able to liquidate the vault successfully.

## Impact
- User loses his collateral and gets liquidated due to unfavourable swap implemented by the protocol

## Tools Used
Hardhat

## Recommendations
- We check for rounding-up of `requiredCollateralValue`.
- We perform an _"inverse-check"_ whether the returned value will cause the vault to be undercollateralized. If yes, increment the minimumOut variable. 

```diff
    function calculateMinimumAmountOut(bytes32 _inTokenSymbol, bytes32 _outTokenSymbol, uint256 _amount) private view returns (uint256) {
        ISmartVaultManagerV3 _manager = ISmartVaultManagerV3(manager);
        uint256 requiredCollateralValue = minted * _manager.collateralRate() / _manager.HUNDRED_PC();
+       if (requiredCollateralValue * _manager.HUNDRED_PC() < minted * _manager.collateralRate()) requiredCollateralValue++;
        uint256 collateralValueMinusSwapValue = euroCollateral() - calculator.tokenToEur(getToken(_inTokenSymbol), _amount);
-       return collateralValueMinusSwapValue >= requiredCollateralValue ?
+       uint256 minOut = collateralValueMinusSwapValue >= requiredCollateralValue ?
            0 : calculator.eurToToken(getToken(_outTokenSymbol), requiredCollateralValue - collateralValueMinusSwapValue);
+
+       // inverse-check
+       if (collateralValueMinusSwapValue < requiredCollateralValue) {
+           bool willGoUnder = minted > maxMintable() - calculator.tokenToEur(getToken(_inTokenSymbol), _amount) + calculator.tokenToEur(getToken(_outTokenSymbol), minOut);
+           if(willGoUnder) minOut++; 
+       }
+
+       return minOut;
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | The Standard |
| Report Date | N/A |
| Finders | t0x1c |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2023-12-the-standard
- **Contest**: https://codehawks.cyfrin.io/c/clql6lvyu0001mnje1xpqcuvl

### Keywords for Search

`vulnerability`

