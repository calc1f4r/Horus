---
# Core Classification
protocol: generic
chain: everychain
category: economic
vulnerability_type: slippage_protection

# Attack Vector Details
attack_type: mev_extraction
affected_component: swap_execution

# DEX-Specific Fields
dex_type: concentrated_liquidity
attack_vectors:
  - sandwich_attack
  - frontrunning
  - deadline_bypass
  - slippage_bypass

# Technical Primitives
primitives:
  - amountOutMinimum
  - deadline
  - sqrtPriceLimitX96
  - slippage_tolerance
  - spot_price
  - twap_oracle

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.85
financial_impact: high

# Context Tags
tags:
  - uniswap_v3
  - uniswap_v4
  - concentrated_liquidity
  - mev
  - sandwich
  - frontrunning
  - slippage
  - deadline
  - dex

# Version Info
language: solidity
version: ">=0.8.0"
---

## References
- [H-01] reports/constant_liquidity_amm/h-01-lack-of-slippage-and-access-control-in-positionmanagersol-can-result-in-sto.md
- [H-04] reports/constant_liquidity_amm/h-04-multiple-swap-lack-slippage-protection.md
- [H-14] reports/constant_liquidity_amm/h-14-deadline-check-is-not-effective-allowing-outdated-slippage-and-allow-pendin.md
- [H-3] reports/constant_liquidity_amm/h-3-ineffective-slippage-mechanism-when-redeeming-proportionally.md
- [H-08] reports/constant_liquidity_amm/h-08-staking-unstaking-and-rebalancetoweight-can-be-sandwiched-mainly-reth-depos.md
- [M-01] reports/constant_liquidity_amm/m-01-missing-deadline-checks-allow-pending-transactions-to-be-maliciously-execut.md
- [OZ-JIT] reports/constant_liquidity_amm/sandwich-attack-possible-via-jit-attack-in-antisandwichhook.md
- [Gauntlet] reports/constant_liquidity_amm/deposit-and-withdraw-functions-are-susceptible-to-sandwich-attacks.md
- [OZ-Cast] reports/constant_liquidity_amm/slippage-check-can-be-bypassed-with-unsafe-cast.md
- [OZ-Init] reports/constant_liquidity_amm/front-running-pools-initialization-or-initial-deposit-can-lead-to-draining-initi.md
- [M-18] reports/constant_liquidity_amm/m-18-a-lack-of-slippage-protection-can-lead-to-a-significant-loss-of-user-funds.md

## Vulnerability Title

**Missing or Ineffective Slippage Protection in Concentrated Liquidity AMM Operations**

### Overview

Protocols integrating with Uniswap V3/V4 or similar concentrated liquidity AMMs frequently fail to implement adequate slippage protection mechanisms when performing swaps, adding/removing liquidity, or settling vault positions. This allows MEV bots to sandwich attack transactions or exploit stale slippage parameters from pending transactions, resulting in significant fund extraction from users.

### Vulnerability Description

#### Root Cause

This vulnerability exists because **swap operations set amountOutMinimum to 0 or use ineffective slippage calculations** when calling Uniswap V3/V4 functions, allowing 100% slippage tolerance. Additionally, **deadline parameters are often set to type(uint256).max or block.timestamp**, rendering them useless against pending transaction exploitation. The fundamental issues include:

1. **Hardcoded zero slippage**: Setting amountOutMinimum: 0 in swap parameters
2. **No deadline enforcement**: Using type(uint256).max or omitting deadline checks
3. **Spot price-based calculations**: Using manipulable spot prices instead of TWAPs for slippage bounds
4. **Unsafe type casting**: Negative deltas bypassing slippage checks via uint128 casting
5. **JIT liquidity attacks**: Attackers injecting concentrated liquidity to capture fees

#### Attack Scenario

**Scenario 1: Classic Sandwich Attack (Most Common - 43/43 reports)**

1. Alice submits a swap transaction with inadequate slippage protection (amountOutMinimum: 0)
2. MEV bot detects pending transaction in mempool
3. Bot front-runs Alice's transaction, buying the target token and moving price
4. Alice's transaction executes at manipulated (worse) price
5. Bot back-runs by selling tokens at inflated price
6. Bot profits from price difference; Alice loses value

**Scenario 2: Stale Transaction Exploitation (8/43 reports)**

1. Alice submits swap with outdated slippage tolerance when gas fees are high
2. Transaction stays pending for hours/days while price moves significantly
3. Original slippage parameters now allow massive price deviation
4. MEV bot executes transaction when profitable, sandwiching for maximum extraction

**Scenario 3: JIT Liquidity Attack (3/43 reports)**

1. Protocol charges penalty fees on swaps, distributing to LPs
2. Attacker detects incoming swap transaction
3. Attacker adds concentrated liquidity at the target tick, capturing ~99% of active liquidity
4. Victim's swap executes, penalty distributed to LPs
5. Attacker receives majority of penalty fee, withdraws liquidity for profit

#### Vulnerable Pattern Examples

**Example 1: Hardcoded Zero Slippage in Swap** [Approx Severity: HIGH]
```solidity
// VULNERABLE: amountOutMinimum set to 0 allows 100% slippage
// Source: BakerFi (Code4rena), Surge (Shieldify)
function _swap(ISwapHandler.SwapParams memory params) internal override returns (uint256 amountOut) {
    if (params.mode == ISwapHandler.SwapType.EXACT_INPUT) {
        amountOut = _uniRouter.exactInputSingle(
            IV3SwapRouter.ExactInputSingleParams({
                tokenIn: params.underlyingIn,
                tokenOut: params.underlyingOut,
                amountIn: params.amountIn,
                amountOutMinimum: 0,  // @audit CRITICAL: No slippage protection!
                fee: fee,
                recipient: address(this),
                sqrtPriceLimitX96: 0   // @audit Also no price limit
            })
        );
    }
}
```

**Example 2: Disabled Deadline Check** [Approx Severity: HIGH]
```solidity
// VULNERABLE: deadline set to max uint256 effectively disables protection
// Source: Blueberry (Sherlock), PaprController (Code4rena)
swapRouter.swapExactTokensForTokens(
    rewards,
    0,
    swapPath,
    address(this),
    type(uint256).max  // @audit Deadline disabled! Old pending txs exploitable
);
```

**Example 3: Spot Price-Based Slippage Calculation** [Approx Severity: HIGH]
```solidity
// VULNERABLE: Using manipulable spot price for minOut calculation
// Source: Asymmetry Finance (Code4rena)
function deposit(uint256 _amount) external {
    // Current spot price can be manipulated right before this call
    uint256 spotPrice = poolBalanceA / poolBalanceB;
    
    // Applying slippage to manipulated spot price is useless
    uint256 minOut = _amount * spotPrice * (100 - maxSlippage) / 100;
    
    // Attacker front-runs to move spot price, then minOut check passes
    _swap(_amount, minOut);
}
```

**Example 4: Zero Slippage in Liquidity Operations** [Approx Severity: HIGH]
```solidity
// VULNERABLE: Liquidity operations without slippage protection
// Source: Maia DAO (Code4rena), Talos Strategy
(liquidityDifference, amount0, amount1) = nonfungiblePositionManager.increaseLiquidity(
    INonfungiblePositionManager.IncreaseLiquidityParams({
        tokenId: _tokenId,
        amount0Desired: amount0Desired,
        amount1Desired: amount1Desired,
        amount0Min: 0,  // @audit Should be non-zero!
        amount1Min: 0,  // @audit Should be non-zero!
        deadline: block.timestamp  // @audit Useless deadline
    })
);
```

**Example 5: Slippage Bypass via Unsafe Cast** [Approx Severity: MEDIUM]
```solidity
// VULNERABLE: Negative delta bypasses uint128 slippage check
// Source: Uniswap v4 Periphery (OpenZeppelin)
function validateMinOut(int128 amount0Delta, int128 amount1Delta, uint128 amount0Min, uint128 amount1Min) {
    // If hook returns negative delta (user must pay to withdraw)
    // casting to uint128 wraps around to a huge number, bypassing check
    require(uint128(amount0Delta) >= amount0Min);  // @audit Bypassed if delta < 0!
    require(uint128(amount1Delta) >= amount1Min);
}
```

### Impact Analysis

#### Technical Impact
- **Fund Extraction**: MEV bots extract value from every unprotected swap (15/43 reports)
- **Stale Transaction Exploitation**: Old pending transactions executed at manipulated prices (8/43 reports)
- **LP Fee Theft**: JIT liquidity attacks steal fee distributions (3/43 reports)
- **Vault Draining**: Entire vault balance extractable via sandwich on deposits/withdrawals (5/43 reports)

#### Business Impact
- **Direct User Losses**: 100% of swap value extractable in worst cases
- **Protocol Reputation**: Users lose trust when experiencing consistent MEV extraction
- **TVL Reduction**: LPs withdraw when sandwich attacks reduce returns

#### Affected Scenarios
- **Vault Deposits/Withdrawals**: Most commonly affected (12/43 reports)
- **Token Swaps**: Core swap operations (15/43 reports)
- **Liquidity Rebalancing**: Strategy rebalance operations (6/43 reports)
- **Fee Collection**: Reward harvesting and fee distribution (4/43 reports)
- **Pool Initialization**: Initial liquidity provision (3/43 reports)

### Secure Implementation

**Fix 1: Proper Slippage Protection with User-Specified Minimums**
```solidity
// SECURE: Caller specifies minimum output amount
function swap(
    address tokenIn,
    address tokenOut,
    uint256 amountIn,
    uint256 minAmountOut,  // User-specified slippage protection
    uint256 deadline       // User-specified deadline
) external returns (uint256 amountOut) {
    require(block.timestamp <= deadline, "Transaction expired");
    
    amountOut = router.exactInputSingle(
        ISwapRouter.ExactInputSingleParams({
            tokenIn: tokenIn,
            tokenOut: tokenOut,
            amountIn: amountIn,
            amountOutMinimum: minAmountOut,  // Enforced slippage
            fee: poolFee,
            recipient: msg.sender,
            deadline: deadline,               // Real deadline
            sqrtPriceLimitX96: 0
        })
    );
    
    require(amountOut >= minAmountOut, "Slippage exceeded");
}
```

**Fix 2: TWAP-Based Slippage Calculation**
```solidity
// SECURE: Use TWAP oracle for slippage bounds (not spot price)
function getMinAmountOut(
    address tokenIn,
    address tokenOut, 
    uint256 amountIn,
    uint256 maxSlippageBps
) public view returns (uint256 minAmountOut) {
    // Use 30-minute TWAP, not spot price
    uint256 twapPrice = oracle.getTwapPrice(tokenIn, tokenOut, 30 minutes);
    
    uint256 expectedOutput = amountIn * twapPrice / 1e18;
    minAmountOut = expectedOutput * (10000 - maxSlippageBps) / 10000;
}
```

**Fix 3: Safe Delta Handling for v4 Hooks**
```solidity
// SECURE: Properly handle negative deltas
function validateMinOut(
    int128 amount0Delta, 
    int128 amount1Delta, 
    int128 amount0Min,  // Allow negative minimums
    int128 amount1Min
) internal pure {
    // Direct comparison without unsafe casting
    require(amount0Delta >= amount0Min, "Amount0 below minimum");
    require(amount1Delta >= amount1Min, "Amount1 below minimum");
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- amountOutMinimum: 0 or amount0Min: 0, amount1Min: 0
- deadline: type(uint256).max or block.timestamp
- No minAmountOut parameter in swap functions
- Using spot price for slippage calculation instead of TWAP
- Unsafe casting of int128 to uint128 for slippage checks
```

#### Audit Checklist
- [ ] All swap operations have non-zero amountOutMinimum or equivalent
- [ ] All deadline parameters use user-specified values, not block.timestamp
- [ ] Slippage bounds calculated using TWAP, not manipulable spot prices
- [ ] Liquidity operations (mint, burn, increase, decrease) have slippage protection
- [ ] No unsafe int-to-uint casts in slippage validation

### Real-World Examples

#### Known Exploits & Audit Findings
- **BakerFi** (Code4rena, 2024) - Multiple swaps lack slippage, HIGH severity
- **Blueberry** (Sherlock, 2023) - Deadline set to max, enabling stale tx exploitation, HIGH
- **Asymmetry Finance** (Code4rena, 2023) - rETH swaps sandwichable via spot price, HIGH, 74 finders
- **Maia DAO** (Code4rena, 2023) - Talos vaults lack slippage on all operations, MEDIUM
- **Surge** (Shieldify, 2024) - PositionManager amountOutMin: 0 enables theft, HIGH
- **Notional** (Sherlock, 2022) - Slippage bypass via 0% tolerance, MEDIUM
- **OpenZeppelin Uniswap Hooks** (2024) - JIT attack bypasses anti-sandwich hook, HIGH

### Keywords for Search

slippage, sandwich_attack, frontrunning, MEV, amountOutMinimum, deadline, sqrtPriceLimitX96, front_running, pending_transaction, spot_price_manipulation, TWAP, uniswap_v3, uniswap_v4, concentrated_liquidity, swap_protection, minAmountOut, amount0Min, amount1Min, JIT_liquidity, mempool_exploitation, stale_transaction, price_manipulation, exactInputSingle, increaseLiquidity

### Related Vulnerabilities

- **Price Oracle Manipulation** - Stale/manipulated oracles compound slippage issues
- **Vault Inflation Attack** - First depositor attacks on vault shares
