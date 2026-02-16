---
protocol: amm
chain: ethereum, bsc
category: amm_calculation
vulnerability_type: k_invariant_miscalculation

attack_type: constant_product_bypass
affected_component: swap_fee_calculation, k_check

primitives:
  - k_invariant_mismatch
  - fee_constant_mismatch
  - swap_output_overflow
  - constant_product_bypass

severity: critical
impact: fund_loss
exploitability: 0.9
financial_impact: critical

tags:
  - amm
  - constant_product
  - k_invariant
  - fee_calculation
  - swap_bug
  - Uranium
  - Nimbus
  - NowSwap
  - real_exploit
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 3
total_losses: "$50M+"
---

## DeFiHackLabs AMM Calculation Errors Compendium

### Overview

AMM calculation errors in constant-product (x*y=k) implementations are among the most devastating DeFi bugs because they undermine the fundamental swap invariant. This entry catalogs **3 real-world exploits** from 2021 totaling **$50M+ in losses**. The core pattern: a mismatch between the constant used in the K-invariant check and the constant used in the fee calculation creates a 100x gap that allows draining pool reserves.

### Root Cause: The 1000 vs 10000 Bug

UniswapV2's swap function uses a K-invariant check with adjustment for 0.3% swap fees:

```solidity
// UniswapV2 reference (CORRECT):
// Fee: 0.3% → multiply by 997/1000
// K-check: (balance0 * 1000 - amountIn0 * 3) * (balance1 * 1000 - amountIn1 * 3) >= k * 1000 * 1000
uint balance0Adjusted = balance0.mul(1000).sub(amount0In.mul(3));
uint balance1Adjusted = balance1.mul(1000).sub(amount1In.mul(3));
require(balance0Adjusted.mul(balance1Adjusted) >= _reserve0.mul(_reserve1).mul(1000**2));
```

The forks in this entry changed the fee from `3/1000` to `16/10000` (0.16%) but only updated the fee numerator to 16 — they forgot to change `1000` to `10000` in the K-check. This creates a **100x** gap in the invariant check.

---

### Vulnerable Pattern Examples

#### The Core Bug: K-Constant Mismatch [CRITICAL]

**Example 1: Uranium Finance — 100x K-Check Gap ($50M, 2021-04)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Fee uses 10000 base but K-check still uses 1000 base
// UniswapV2 fork with modified fee: 16/10000 = 0.16%

contract UraniumPair {
    function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external {
        // ... transfer tokens out ...

        uint balance0 = IERC20(token0).balanceOf(address(this));
        uint balance1 = IERC20(token1).balanceOf(address(this));

        uint amount0In = balance0 > _reserve0 - amount0Out
            ? balance0 - (_reserve0 - amount0Out) : 0;
        uint amount1In = balance1 > _reserve1 - amount1Out
            ? balance1 - (_reserve1 - amount1Out) : 0;

        // Fee calculation: 16/10000 = 0.16%
        uint balance0Adjusted = balance0.mul(10000).sub(amount0In.mul(16));
        uint balance1Adjusted = balance1.mul(10000).sub(amount1In.mul(16));

        // @audit CRITICAL BUG: K-check still uses 1000**2 instead of 10000**2
        require(
            balance0Adjusted.mul(balance1Adjusted) >=
            uint(_reserve0).mul(_reserve1).mul(1000**2),
            // @audit 1000**2 = 1,000,000
            // @audit Should be 10000**2 = 100,000,000
            // @audit The left side is 100x larger than it needs to be!
            // @audit This means the K-check is 100x more permissive
            'UraniumSwap: K'
        );
    }
}

// Attack: The 100x gap means attacker can extract ~99% of reserves
// Left side:  balance * 10000 (scaled up 10000x)
// Right side: reserve * 1000**2 (scaled up 1000000x BUT left is 10000*10000 = 100M)
// Net: attacker only needs to maintain K / 100, not K

// Exploit steps:
// 1. Send 1 WBNB into the pair (minimal input)
// 2. Request ~99.8% of BUSD reserves as output
// 3. K-check passes because 10000-scale adjustment >> 1000-scale requirement
// 4. Drain WBNB-BUSD pair completely

function exploit() external {
    // Flash swap: request nearly ALL reserves
    (uint112 reserve0, uint112 reserve1,) = pair.getReserves();
    uint256 drainAmount = uint256(reserve1) * 998 / 1000;  // 99.8% of reserves

    // Send minimal input
    WBNB.transfer(address(pair), 1 ether);

    // Request maximum output — K-check passes due to 100x gap
    pair.swap(0, drainAmount, address(this), "");
    // @audit Successfully drains $50M from pool
}
```
- **PoC**: `DeFiHackLabs/src/test/2021-04/Uranium_exp.sol`
- **Root Cause**: K-invariant check uses `1000**2` on the right side but fee adjustment uses `10000` on the left side. The left side is effectively 100x larger than needed, allowing near-complete reserve drainage.

**Example 2: Nimbus LP — Identical 1000 vs 10000 Bug (2021-10)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Exact same bug as Uranium — copied incorrect code

contract NimbusLP {
    function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external {
        // ... standard UniV2 swap logic ...

        uint balance0Adjusted = balance0.mul(10000).sub(amount0In.mul(25));
        uint balance1Adjusted = balance1.mul(10000).sub(amount1In.mul(25));
        // @audit Fee: 25/10000 = 0.25%

        require(
            balance0Adjusted.mul(balance1Adjusted) >=
            uint(_reserve0).mul(_reserve1).mul(1000**2),
            // @audit SAME BUG: 1000**2 instead of 10000**2
            'Nimbus: K'
        );
    }
}

// @audit Impact: Same 100x gap → can drain ~99% of each pool
```
- **PoC**: `DeFiHackLabs/src/test/2021-10/NimbusLP_exp.sol`
- **Root Cause**: Direct code copy from Uranium or same flawed fork template. 25/10000 fee with 1000**2 K-check.

**Example 3: NowSwap — Same Pattern, Different Fee (2021-08)** [HIGH]
```solidity
// ❌ VULNERABLE: Yet another fork with the same 1000 vs 10000 mismatch

contract NowSwapPair {
    function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external {
        // ... transfer out ...

        uint balance0Adjusted = balance0.mul(10000).sub(amount0In.mul(20));
        uint balance1Adjusted = balance1.mul(10000).sub(amount1In.mul(20));
        // @audit Fee: 20/10000 = 0.2%

        require(
            balance0Adjusted.mul(balance1Adjusted) >=
            uint(_reserve0).mul(_reserve1).mul(1000**2),
            // @audit SAME BUG AGAIN: 1000**2 not 10000**2
            'NowSwap: K'
        );
    }
}
```
- **PoC**: `DeFiHackLabs/src/test/2021-08/NowSwap_exp.sol`

---

### Mathematical Proof of Exploitability

```
Given:
  - Fee = F/10000 (e.g., 16/10000 for Uranium)
  - balance_adjusted = balance * 10000 - amountIn * F
  - K_check: balance0_adj * balance1_adj >= reserve0 * reserve1 * 1000^2

For a swap with amountIn tokens of token0, requesting amountOut of token1:

  Left side (simplified, one-sided swap):
    (reserve0 + amountIn) * 10000 * (reserve1 - amountOut) * 10000
    = 10000^2 * (reserve0 + amountIn)(reserve1 - amountOut)

  Right side:
    reserve0 * reserve1 * 1000^2

  Ratio: 10000^2 / 1000^2 = 100

  The check effectively requires:
    (reserve0 + amountIn)(reserve1 - amountOut) >= reserve0 * reserve1 / 100

  Instead of:
    (reserve0 + amountIn)(reserve1 - amountOut) >= reserve0 * reserve1

  Attacker can extract up to ~99% of one reserve with minimal input.
```

---

### Impact Analysis

#### Technical Impact
- **Complete pool drainage**: 99%+ of reserves extractable in single transaction
- **All pairs vulnerable**: Every trading pair on the DEX is affected
- **Trivial exploitation**: Requires only 1 token input to drain millions

#### Business Impact
| Protocol | Loss | Fee Config | Bug |
|----------|------|-----------|-----|
| Uranium Finance | $50M+ | 16/10000 | K uses 1000^2 instead of 10000^2 |
| Nimbus LP | Undisclosed | 25/10000 | Identical K mismatch |
| NowSwap | Undisclosed | 20/10000 | Identical K mismatch |

---

### Secure Implementation

**Fix 1: Consistent Fee Base Constants**
```solidity
// ✅ SECURE: Use same base constant for BOTH fee adjustment and K-check
uint256 constant FEE_BASE = 10000;
uint256 constant FEE = 16;  // 0.16%

function swap(uint amount0Out, uint amount1Out, address to, bytes calldata data) external {
    // ... transfer and balance calculation ...

    uint balance0Adjusted = balance0.mul(FEE_BASE).sub(amount0In.mul(FEE));
    uint balance1Adjusted = balance1.mul(FEE_BASE).sub(amount1In.mul(FEE));

    // @audit K-check uses FEE_BASE**2, matching the adjustment
    require(
        balance0Adjusted.mul(balance1Adjusted) >=
        uint(_reserve0).mul(_reserve1).mul(FEE_BASE ** 2),
        // @audit 10000**2 = 100,000,000 — matches left side scale
        'K'
    );
}
```

**Fix 2: Named Constants with Invariant Comment**
```solidity
// ✅ SECURE: Self-documenting code prevents copy-paste errors

/// @dev INVARIANT: FEE_DENOMINATOR must match K_SCALE_FACTOR
///      If fee = N/FEE_DENOMINATOR, then K check uses FEE_DENOMINATOR^2
uint256 private constant FEE_DENOMINATOR = 10000;
uint256 private constant K_SCALE_FACTOR = FEE_DENOMINATOR;  // @audit MUST equal FEE_DENOMINATOR

function _kCheck(uint256 b0, uint256 b1, uint256 r0, uint256 r1) internal pure {
    require(b0.mul(b1) >= r0.mul(r1).mul(K_SCALE_FACTOR ** 2), "K violated");
}
```

**Fix 3: Use UniswapV2 Unmodified K-Check**
```solidity
// ✅ SECURE: If you don't need custom fees, use UniswapV2's original constants
// 0.3% fee: fee = 3, base = 1000
uint balance0Adjusted = balance0.mul(1000).sub(amount0In.mul(3));
uint balance1Adjusted = balance1.mul(1000).sub(amount1In.mul(3));
require(
    balance0Adjusted.mul(balance1Adjusted) >=
    uint(_reserve0).mul(_reserve1).mul(1000**2),  // @audit 1000 matches 1000 ✓
    'UniswapV2: K'
);
```

---

### Detection Patterns

```bash
# K-invariant check with mismatched constants
grep -rn "1000\*\*2\|1000000\b" --include="*.sol" | \
  xargs grep -B 10 "10000\|FEE_BASE"
# @audit If fee uses 10000 but K uses 1000**2, it's the Uranium bug

# UniswapV2 fork swap functions
grep -rn "balance.*Adjusted.*mul.*sub" --include="*.sol" | head -20

# Custom fee constants in AMM forks
grep -rn "\.mul(10000)\|\.mul(1000)" --include="*.sol" | \
  grep -i "balance\|adjusted\|swap"

# Different constants in same function
grep -rn "function swap" --include="*.sol" -A 30 | \
  grep -E "(10000|1000)" | sort | uniq -c
```

---

### Audit Checklist

1. **Is this a UniswapV2 fork with modified fees?** — Check if fee base was changed from 1000
2. **Does the K-invariant check use the SAME base as the fee adjustment?** — Must be identical
3. **Are fee constants defined as named constants?** — Prevents copy-paste mismatches
4. **Has the swap function been modified from the original UniV2?** — Diff against canonical code
5. **Run the math: does left-side scale factor^2 == right-side scale factor?**

---

### Fork Audit Quick Check

For ANY UniswapV2 fork, immediately check:
```
1. Find the fee adjustment line:  balance.mul(X).sub(amountIn.mul(Y))
2. Find the K-check line:         require(... >= reserve0.mul(reserve1).mul(Z))
3. Verify: X^2 == Z
   - If X = 1000 and Z = 1000000 (1000^2): ✅ Correct
   - If X = 10000 and Z = 1000000 (1000^2): ❌ URANIUM BUG — 100x gap
   - If X = 10000 and Z = 100000000 (10000^2): ✅ Correct
```

---

### Keywords

- k_invariant
- constant_product
- fee_mismatch
- 1000_10000_bug
- swap_calculation
- amm_fork
- uniswapv2_fork
- pool_drain
- reserve_drain
- fee_base_constant
- DeFiHackLabs

---

### Related Vulnerabilities

- [AMM Constant Product Vulnerabilities](../../amm/constantproduct/AMM_CONSTANT_PRODUCT_VULNERABILITIES.md)
- [Flash Loan Attack Patterns](../../general/flash-loan-attacks/FLASH_LOAN_VULNERABILITIES.md)
