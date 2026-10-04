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
solodit_id: 57267
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
finders_count: 35
finders:
  - viquetoh
  - cd_pandora
  - pabloperezacc6
  - holydevoti0n
  - t0x1c
---

## Vulnerability Title

RAACToken burns less tokens than expected when feeCollector is unset

### Overview


The RAACToken contract has a bug where it burns less tokens than expected when the feeCollector address is set to the zero address. This means that not all tokens are being burned as intended, which can cause unexpected calculations and potentially lead to inflation in the system. To fix this, the recommendation is to check if the feeCollector address is set to zero and set the taxAmount to 0 in that case.

### Original Finding Content

## Summary

When the `feeCollector` is set to the zero address, the `RAACToken` contract burn function will burn `amount - taxAmount` and leave the `taxAmount` at the caller's address.

## Vulnerability Details

Burn amount is calculated as `amount - taxAmount` regardless of the `feeCollector` address. In case the `feeCollector` is set to the zero address, the `taxAmount` will not be transferred nor burned.

`/contracts/core/tokens/RAACToken.sol`
```javascript
    function burn(uint256 amount) external {
        uint256 taxAmount = amount.percentMul(burnTaxRate);
## not all tokens are burned here
@>      _burn(msg.sender, amount - taxAmount);
## if feeCollector == address(0) taxAmount will remain at the caller address
@>      if (taxAmount > 0 && feeCollector != address(0)) {
            _transfer(msg.sender, feeCollector, taxAmount);
        }
    }
```

## PoC (foundry)

```javascript
// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {Test} from "forge-std/Test.sol";
import {RAACToken} from "src/core/tokens/RAACToken.sol";
import {veRAACToken} from "src/core/tokens/veRAACToken.sol";
import {FeeCollector} from "src/core/collectors/FeeCollector.sol";
import {IFeeCollector} from "src/interfaces/core/collectors/IFeeCollector.sol";
import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TestRAACTokenBurn is Test {
    RAACToken public raacToken;
    FeeCollector public feeCollector;

    function setUp() public {
        raacToken = new RAACToken(address(this), 0, 0);
        raacToken.setMinter(address(this));

        veRAACToken veToken = new veRAACToken(address(raacToken));
        feeCollector =
            new FeeCollector(address(raacToken), address(veToken), address(this), address(this), address(this));

        // for simplicity, assume 100% should be burned
        feeCollector.updateFeeType(0, IFeeCollector.FeeType(0, 10_000, 0, 0));

        raacToken.manageWhitelist(address(feeCollector), true);
        raacToken.manageWhitelist(address(veToken), true);
        raacToken.manageWhitelist(address(this), true);

        raacToken.mint(address(this), 10_000);
    }

    function test_raac_burn() public {
        // set fee collector to address(0) to avoid collecting fees
        raacToken.setFeeCollector(address(0));

        uint256 amount = 10_000;
        assertEq(raacToken.balanceOf(address(feeCollector)), 0, "Fee collector should have 0 RAAC tokens");

        raacToken.approve(address(feeCollector), amount);
        feeCollector.collectFee(amount, 0);

        assertEq(raacToken.balanceOf(address(feeCollector)), amount, "Fee collector should have 10_000 RAAC tokens");

        vm.expectEmit(address(raacToken));
        emit IERC20.Transfer({
            from: address(feeCollector),
            to: address(0),
            // 10_000 tokens should be burned, but only 9950 will
            value: amount
        });

        vm.expectEmit(address(feeCollector));
        emit IFeeCollector.FeeDistributed({
            veRAACAmount: 0,
            // event will be emitted indicating that 10_000 tokens were burned
            burnAmount: amount,
            repairAmount: 0,
            treasuryAmount: 0
        });

        feeCollector.distributeCollectedFees();

        // feeCollector should have 0 RAAC tokens after burning, but it will remain 50
        assertEq(raacToken.balanceOf(address(feeCollector)), 0, "Fee collector should have 0 RAAC tokens");
    }
}
```

## Impact

As `FeeCollector.FeeDistributed` event will be emitted indicating that `amount` tokens were burned, but only `amount - taxAmount` will be actually burned. This can lead to unexpected calculations.

Unburned tokens may introduce inflation to the system. 

## Recommendations

Check if the `feeCollector` address is set to the zero address and set the `taxAmount` to 0 if so.

```diff
    function burn(uint256 amount) external {
        uint256 taxAmount = amount.percentMul(burnTaxRate);
+       if (taxAmount > 0 && feeCollector != address(0)) {
+           _transfer(msg.sender, feeCollector, taxAmount);
+       } else {
+           taxAmount = 0;
+       }
        _burn(msg.sender, amount - taxAmount);
-       if (taxAmount > 0 && feeCollector != address(0)) {
-           _transfer(msg.sender, feeCollector, taxAmount);
-       }
    }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | viquetoh, cd_pandora, pabloperezacc6, holydevoti0n, t0x1c, udo, skidd0016, joro, yas000x, kwakudr, 0x23r0, igdbaxe, dharkartz, 0x9527, johny7173, aksoy, tadev, bakhankov, dobrevaleri, calc1f4r, kweks, 0xlouistsai, siisivan, h2134, tigerfrake, sunless_, tinnohofficial, 0xmystery, josh4324, udogodwin2k22, alexczm, 0xaadi, glightspeed2 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

