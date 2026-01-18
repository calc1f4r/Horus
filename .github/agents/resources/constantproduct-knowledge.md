# Constant Product AMM - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `constantproduct-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures extracted from the full database.

---

## Core Invariants to Verify

| Invariant | Formula | Attack If Violated |
|-----------|---------|-------------------|
| Constant Product | `x * y = k` (post-swap) | Drain via fee/rounding errors |
| LP Fair Mint | `LP = min(Δx/x, Δy/y) * totalSupply` | First depositor inflation |
| Reserve Sync | `reserves == balanceOf(pool)` | Donation/skim attacks |
| Fee Collection | `k_new >= k_old` | Value extraction |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: First Depositor / Inflation Attacks

**One-liner**: Attacker manipulates LP token price by inflating reserves relative to supply.

**Quick Checks:**
- [ ] Is `MINIMUM_LIQUIDITY` burned on first deposit?
- [ ] Can LP tokens be burned to reduce supply near zero?
- [ ] Is there a migrator that bypasses MINIMUM_LIQUIDITY?
- [ ] Can pool be front-run created?

**Exploit Signature:**
```
totalSupply ≈ 0 + reserves >> 0 = share price explosion
```

**Reasoning Prompt:**
> "If I control the first deposit, can I make subsequent deposits round to zero LP tokens?"

---

### ⚠️ Category 2: Slippage Protection Vulnerabilities

**One-liner**: User receives fewer tokens than expected, MEV bots extract the difference.

**Quick Checks:**
- [ ] Is `amountOutMin` parameter enforced?
- [ ] Are there ANY swap paths with hardcoded `0` slippage?
- [ ] Do internal functions bypass slippage checks?
- [ ] Is there oracle-based slippage validation?

**Exploit Signature:**
```solidity
router.swap(..., 0, ...);  // amountOutMin = 0
```

**Reasoning Prompt:**
> "If I sandwich this transaction, how much can I extract?"

---

### ⚠️ Category 3: Sandwich & MEV Attacks

**One-liner**: Front-run + back-run user transactions to profit from price movement.

**Quick Checks:**
- [ ] Are large swaps protected?
- [ ] Do withdrawal operations swap atomically?
- [ ] Is there private mempool integration?
- [ ] Can protocol-level operations be sandwiched?

**Exploit Signature:**
```
Tx1 (attacker): Buy → Price up
Tx2 (victim): Buy at worse price  
Tx3 (attacker): Sell → Profit
```

**Reasoning Prompt:**
> "Which operations move price significantly and can be observed in mempool?"

---

### ⚠️ Category 4: Spot Price Manipulation (slot0)

**One-liner**: Flash loan moves spot price, protocol makes bad decision based on manipulated price.

**Quick Checks:**
- [ ] Is `slot0()` or `getReserves()` used for pricing?
- [ ] Is TWAP used instead?
- [ ] If TWAP, is period >= 30 minutes?
- [ ] Is there deviation check vs external oracle?

**Exploit Signature:**
```solidity
(uint160 sqrtPriceX96,,,,,,) = pool.slot0();  // ❌ Manipulatable
```

**Reasoning Prompt:**
> "Can I flash loan enough to move this price before the protocol reads it?"

---

### ⚠️ Category 5: Deadline Vulnerabilities

**One-liner**: Stale transactions executed at unfavorable prices.

**Quick Checks:**
- [ ] Is `deadline` a user parameter?
- [ ] Is `block.timestamp` used as default (always passes)?
- [ ] Are pending transactions exploitable if delayed?

**Exploit Signature:**
```solidity
router.swap(..., block.timestamp);  // ❌ No real deadline
```

**Reasoning Prompt:**
> "If this transaction sits in mempool for days, can it still execute profitably?"

---

### ⚠️ Category 6: Reserve Manipulation Attacks

**One-liner**: Attacker donates/skims tokens to manipulate reserve-based calculations.

**Quick Checks:**
- [ ] Do calculations use `balanceOf()` or synced reserves?
- [ ] Can anyone call `sync()`?
- [ ] Is IL protection based on current reserves?
- [ ] Can `skim()` be called by anyone?

**Exploit Signature:**
```solidity
uint256 reserves = token.balanceOf(pool);  // ❌ Includes donations
```

**Reasoning Prompt:**
> "If I donate tokens directly to the pool, what calculations get affected?"

---

### ⚠️ Category 7: LP Token Calculation Issues

**One-liner**: Decimal mismatches or formula errors cause incorrect LP valuation.

**Quick Checks:**
- [ ] Are token decimals normalized before calculations?
- [ ] Is `decimals()` vs `10**decimals()` used correctly?
- [ ] Is rounding direction correct (down for mint, up for burn)?
- [ ] Does LP calculation handle imbalanced additions?

**Exploit Signature:**
```solidity
value = reserve / IERC20(token).decimals();  // ❌ Should be 10**decimals()
```

**Reasoning Prompt:**
> "What happens with 6-decimal USDC paired with 18-decimal ETH?"

---

### ⚠️ Category 8: Callback & Reentrancy Attacks

**One-liner**: Unrestricted callbacks allow draining approved tokens or reentering mid-operation.

**Quick Checks:**
- [ ] Is `uniswapV2Call` / `uniswapV3MintCallback` access-controlled?
- [ ] Are callbacks restricted to pool-only callers?
- [ ] Is there reentrancy protection on swap paths?
- [ ] Can malicious tokens reenter during transfer?

**Exploit Signature:**
```solidity
function uniswapV3MintCallback(...) external {  // ❌ No msg.sender check
    token.transferFrom(source, pool, amount);    // Anyone can call!
}
```

**Reasoning Prompt:**
> "If I call this callback directly with arbitrary data, what happens?"

---

### ⚠️ Category 9: Factory & Pool Creation Attacks

**One-liner**: Front-run pool creation or spoof pool existence.

**Quick Checks:**
- [ ] Is pool address deterministic and predictable?
- [ ] Is pool existence checked via factory.getPair() or balanceOf()?
- [ ] Is init_code_hash correct for the factory version?
- [ ] Can pool creation be permanently DOS'd?

**Exploit Signature:**
```solidity
// Pool existence via balance (wrong)
return token.balanceOf(computedPairAddr) > 0;  // ❌ Can be spoofed
```

**Reasoning Prompt:**
> "Can I deploy a fake pool at the computed address before the protocol?"

---

### ⚠️ Category 10: Decimal & Math Calculation Issues

**One-liner**: Formula mistakes or decimal errors cause catastrophic mispricing.

**Quick Checks:**
- [ ] Is swap output formula correct (Uniswap formula)?
- [ ] Are there division-before-multiplication precision losses?
- [ ] Are negative exponents handled (10**-x)?
- [ ] Is mulDiv used correctly for large numbers?

**Exploit Signature:**
```solidity
// Wrong swap formula
amountOut = (reserveOut * amountIn) / reserveIn;  // ❌ Missing fee adjustment

// Correct formula
amountOut = (amountIn * 997 * reserveOut) / (reserveIn * 1000 + amountIn * 997);
```

**Reasoning Prompt:**
> "Does this formula match the Uniswap V2 whitepaper exactly?"

---

### ⚠️ Category 11: Liquidity Migration Attacks

**One-liner**: Manipulate migration by inflating balances or assuming wrong ownership.

**Quick Checks:**
- [ ] Does migration use tracked balances or raw balanceOf()?
- [ ] Does protocol assume it owns 100% of pool liquidity?
- [ ] Can attacker donate to DOS migration?
- [ ] Is there a time lock on migration?

**Exploit Signature:**
```solidity
uint256 amount = token.balanceOf(address(this));  // ❌ Includes donations
```

**Reasoning Prompt:**
> "If I donate tokens right before migration, does it break?"

---

### ⚠️ Category 12: Flash Loan Graduation Attacks

**One-liner**: Use flash loan to artificially trigger threshold-based events.

**Quick Checks:**
- [ ] Are bonding curve graduations atomic with flash loan closure?
- [ ] Is there a time lock after graduation?
- [ ] Can market cap thresholds be flash-loan gamed?
- [ ] Is there a cooldown on major state changes?

**Exploit Signature:**
```
Block N: Flash loan → Buy tokens → Trigger graduation → Sell on Uniswap → Repay
```

**Reasoning Prompt:**
> "Can I make this protocol think it graduated when it really didn't?"

---

## Summary Attack Surface Matrix

| Target | Flash Loan | Front-Run | Donation | Callback |
|--------|:----------:|:---------:|:--------:|:--------:|
| First Deposit | ⚠️ | ⚠️ | ⚠️ | - |
| Swap | ⚠️ | ⚠️ | - | ⚠️ |
| Add Liquidity | - | ⚠️ | - | - |
| Remove Liquidity | ⚠️ | ⚠️ | ⚠️ | - |
| Oracle Read | ⚠️ | - | ⚠️ | - |
| Migration | - | ⚠️ | ⚠️ | - |
| Graduation | ⚠️ | ⚠️ | - | - |

---

## Keywords for Code Search

When reasoning suggests an area to investigate, search for:

```bash
# First depositor patterns
rg -n "MINIMUM_LIQUIDITY|totalSupply\s*==\s*0|sqrt\("

# Slippage patterns  
rg -n "amountOutMin|minAmountOut|slippage|0,\s*path|,\s*0\s*,"

# Price manipulation
rg -n "slot0|getReserves|sqrtPriceX96|observe\(|TWAP"

# Deadline patterns
rg -n "deadline|block\.timestamp"

# Callback patterns
rg -n "Callback|uniswapV2Call|uniswapV3.*Callback"

# Reserve patterns
rg -n "balanceOf\(address\(this\)\)|sync\(|skim\("

# Decimal patterns
rg -n "decimals\(\)|10\s*\*\*|1e18|1e6"
```

---

## References

- Full Database: [CONSTANT_PRODUCT_AMM_VULNERABILITIES.md](../../DB/amm/constantproduct/CONSTANT_PRODUCT_AMM_VULNERABILITIES.md)
- Main Agent: [constantproduct-reasoning-agent.md](../constantproduct-reasoning-agent.md)
- Context Builder: [audit-context-building.md](../audit-context-building.md)
