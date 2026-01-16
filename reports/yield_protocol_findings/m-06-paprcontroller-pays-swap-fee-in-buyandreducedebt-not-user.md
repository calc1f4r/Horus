---
# Core Classification
protocol: Backed Protocol
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6211
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-12-papr-contest
source_link: https://code4rena.com/reports/2022-12-backed
github_link: https://github.com/code-423n4/2022-12-backed-findings/issues/196

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 15
finders:
  - Franfran
  - fs0c
  - HollaDieWaldfee
  - 0x52
  - Jeiwan
---

## Vulnerability Title

[M-06] PaprController pays swap fee in buyAndReduceDebt, not user

### Overview


This bug report is about the `buyAndReduceDebt` function in the `PaprController` contract, which allows users to buy Papr tokens for underlying tokens and burn them to reduce their debt. The function allows the caller to specify a swap fee, but in reality, the fee is collected from `PaprController` itself. Since `PaprController` is not designed to hold any underlying tokens, calling `buyAndReduceDebt` with a swap fee set will result in a revert. The function can also be used to transfer out any underlying tokens sent to the contract mistakenly.

The bug was identified using manual review and a proof of concept was provided. The recommended mitigation step is to consider a change to the `buyAndReduceDebt` function which would replace the `transfer` call with a `safeTransferFrom` call. This would ensure that the fee is taken from the caller, not from the `PaprController` contract.

### Original Finding Content

## Lines of code

https://github.com/with-backed/papr/blob/9528f2711ff0c1522076b9f93fba13f88d5bd5e6/src/PaprController.sol#L226


## Vulnerability details

## Impact
Since `PaprController` is not designed to hold any underlying tokens, calling `buyAndReduceDebt` with a swap fee set will result in a revert. The function can also be used to transfer out any underlying tokens sent to the contract mistakenly.
## Proof of Concept
`PaprController` implements the `buyAndReduceDebt` function, which allows users to buy Papr tokens for underlying tokens and burn them to reduce their debt ([PaprController.sol#L208](https://github.com/with-backed/papr/blob/9528f2711ff0c1522076b9f93fba13f88d5bd5e6/src/PaprController.sol#L208)). Optionally, the function allows the caller to specify a swap fee: a fee that's collected from the caller. However, in reality, the fee is collected from `PaprController` itself: `transfer` instead of `transferFrom` is called on the underlying token ([PaprController.sol#L225-L227](https://github.com/with-backed/papr/blob/9528f2711ff0c1522076b9f93fba13f88d5bd5e6/src/PaprController.sol#L225-L227)):
```solidity
if (hasFee) {
    underlying.transfer(params.swapFeeTo, amountIn * params.swapFeeBips / BIPS_ONE);
}
```

This scenario is covered by the `testBuyAndReduceDebtReducesDebt` test ([BuyAndReduceDebt.t.sol#L12](https://github.com/with-backed/papr/blob/9528f2711ff0c1522076b9f93fba13f88d5bd5e6/test/paprController/BuyAndReduceDebt.t.sol#L12)), however the fee is not actually set in the test:
```solidity
// Fee is initialized but not set.
uint256 fee;
underlying.approve(address(controller), underlyingOut + underlyingOut * fee / 1e4);
swapParams = IPaprController.SwapParams({
    amount: underlyingOut,
    minOut: 1,
    sqrtPriceLimitX96: _maxSqrtPriceLimit({sellingPAPR: false}),
    swapFeeTo: address(5),
    swapFeeBips: fee
});
```

If fee is set in the test, the test wil revert with an "Arithmetic over/underflow" error:
```diff
--- a/test/paprController/BuyAndReduceDebt.t.sol
+++ b/test/paprController/BuyAndReduceDebt.t.sol
@@ -26,7 +26,7 @@ contract BuyAndReduceDebt is BasePaprControllerTest {
         IPaprController.VaultInfo memory vaultInfo = controller.vaultInfo(borrower, collateral.addr);
         assertEq(vaultInfo.debt, debt);
         assertEq(underlyingOut, underlying.balanceOf(borrower));
-        uint256 fee;
+        uint256 fee = 1e3;
         underlying.approve(address(controller), underlyingOut + underlyingOut * fee / 1e4);
         swapParams = IPaprController.SwapParams({
             amount: underlyingOut,
```

## Tools Used
Manual review
## Recommended Mitigation Steps
Consider this change:
```diff
--- a/src/PaprController.sol
+++ b/src/PaprController.sol
@@ -223,7 +223,7 @@ contract PaprController is
         );

         if (hasFee) {
-            underlying.transfer(params.swapFeeTo, amountIn * params.swapFeeBips / BIPS_ONE);
+            underlying.safeTransferFrom(msg.sender, params.swapFeeTo, amountIn * params.swapFeeBips / BIPS_ONE);
         }

         _reduceDebt({account: account, asset: collateralAsset, burnFrom: msg.sender, amount: amountOut});
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Backed Protocol |
| Report Date | N/A |
| Finders | Franfran, fs0c, HollaDieWaldfee, 0x52, Jeiwan, bin2chen, Saintcode_, noot, KingNFT, stealthyz, evan, teawaterwire, unforgiven, rvierdiiev, poirots |

### Source Links

- **Source**: https://code4rena.com/reports/2022-12-backed
- **GitHub**: https://github.com/code-423n4/2022-12-backed-findings/issues/196
- **Contest**: https://code4rena.com/contests/2022-12-papr-contest

### Keywords for Search

`Business Logic`

