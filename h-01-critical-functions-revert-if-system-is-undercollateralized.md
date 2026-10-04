---
# Core Classification
protocol: RWf(x)_2025-08-20
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63647
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/RWf(x)-security-review_2025-08-20.md
github_link: none

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

protocol_categories:
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Critical functions revert if system is undercollateralized

### Overview


The bug report is about an error in the internal function `Treasury._loadSwapState()`, which is used to calculate the `xNav` value. This calculation can cause an underflow error, leading to the failure of all transactions involving this function. This can result in the system becoming undercollateralized and lacking a mechanism to recover the collateralization ratio. To fix this, the report recommends adding a condition to the `redeem()` function and changing the calculation of `xNav` to prevent the underflow error.

### Original Finding Content


_Resolved_

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

The internal function `Treasury._loadSwapState()` calculates the `xNav` as follows:

```solidity
_state.xNav = _state.baseSupply.mul(_state.baseNav).sub(_state.fSupply.mul(_state.fNav)).div(_state.xSupply);
```

This is equivalent to:

```js
(baseSupplyNav - fSupplyNav) / xSupply
```

In the case of the system being undercollateralized (`baseSupplyNav < fSupplyNav`), the calculation of `xNav` will revert due to subtraction underflow. All transactions involving the execution of `_loadSwapState()` will fail, including all operations that aim to raise the collateral ratio so that it can return to a healthy state.

As a result, the protocol will lack any mechanism to recover the collateralization ratio once it falls below 100%.

### Proof of concept

Add the following code to the `Market.spec.ts` test file.

```ts
  context.only("audit", async () => {
    beforeEach(async () => {
      await oracle.setPrice(100000000000); // $1000 with 8 decimals
      await treasury.initializePrice();
      await weth.deposit({ value: ethers.parseEther("10") });
      await weth.approve(market.getAddress(), MaxUint256);
      await market.mint(ethers.parseEther("1"), deployer.address, 0, 0);
    });

    it("reverts when collateral ratio is below 100%", async () => {
      // The system becomes undercollateralized
      await oracle.setPrice(65000000000); // $650 with 8 decimals

      // Manager tries to raise collateral ratio, but transactions revert
      await expect(market.mintXToken(ethers.parseEther("1"), signer.address, 0))
        .to.revertedWith("SafeMath: subtraction overflow");
      await expect(market.addBaseToken(ethers.parseEther("1"), signer.address, 0))
        .to.revertedWith("SafeMath: subtraction overflow");
    });
  });
```

## Recommendations

```diff
  function redeem(
(...)
-   _baseOut = _state.redeem(_fTokenIn, _xTokenIn);
+   if (_state.xNav == 0) {
+     require (_xTokenIn == 0, "Undercollateralalized");
+     // only redeem fToken proportionally when under collateral.
+     _baseOut = _fTokenIn.mul( _state.baseSupply).div(_state.fSupply);
+   } else {
+     _baseOut = _state.redeem(_fTokenIn, _xTokenIn);
+   }

(...)

    if (_state.xSupply == 0) {
        // no xToken, treat the nav of xToken as 1.0
        _state.xNav = PRECISION;
	} else {
-		_state.xNav = _state.baseSupply.mul(_state.baseNav).sub(_state.fSupply.mul(_state.fNav)).div(_state.xSupply);
+		uint256 baseSupplyNav = _state.baseSupply.mul(_state.baseNav);
+		uint256 fSupplyNav = _state.fSupply.mul(_state.fNav);
+		if (baseSupplyNav <= fSupplyNav) {
+			_state.xNav = 0;
+		} else {
+			_state.xNav = baseSupplyNav.sub(fSupplyNav).div(_state.xSupply);
+		}
	}
```





### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | RWf(x)_2025-08-20 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/RWf(x)-security-review_2025-08-20.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

