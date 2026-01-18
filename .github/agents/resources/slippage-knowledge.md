# Slippage Protection - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `slippage-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| User Min Params | ✓ | Sandwich Attack |
| Enforced Deadline | ✓ | Delayed Execution (Bad Price) |
| Liquidity Ratios | ✓ | Unbalanced Add/Remove |
| No Zero Hardcodes | ✓ | Total Loss |
| Oracle bounds | ✓ | Price Manipulation |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Zero Slippage (Sandwich Attack)

**One-liner**: Allowing `amountOutMin` to be 0 (or 1) means the transaction will accept ANY output quantity, inviting MEV bots to front-run and steal value.

**Quick Checks:**
- [ ] Call to `router.swap...` uses `0` for min param?
- [ ] User parameter `minAmount` is ignored?
- [ ] `minAmount` derived from `balanceOf` (which is manipulable)?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Hardcoded zero
router.swapExactTokensForTokens(
    amountIn,
    0, // amountOutMin: Accepts 0 tokens!
    path,
    to,
    deadline
);
```

**Reasoning Prompt:**
> "If a whale buys massive amounts of this token just before my transaction, do I still execute and get dust?"

---

### ⚠️ Category 2: Defeated Deadlines

**One-liner**: Using `block.timestamp` as the deadline means "valid whenever mined", removing protection against transactions being held until market conditions worsen.

**Quick Checks:**
- [ ] `deadline` param is `block.timestamp`?
- [ ] `deadline` param is `type(uint256).max`?
- [ ] No `deadline` param at all?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Current time always passes check
require(block.timestamp <= block.timestamp, "EXPIRED");
```

---

### ⚠️ Category 3: Unprotected Liquidity Operations

**One-liner**: Adding liquidity involves two assets. If their ratio isn't pinned by minimums, an attacker can manipulate the pool ratio to steal the added funds.

**Quick Checks:**
- [ ] `addLiquidity`: Has `minA` AND `minB`?
- [ ] `removeLiquidity`: Has `minA` AND `minB`?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Only one side protected
router.addLiquidity(
    tokenA, tokenB,
    amtA, amtB,
    minA, 0, // minB is 0!
    to, time
);
```

---

### ⚠️ Category 4: Withdrawals & Leverage

**One-liner**: Burning shares (Withdrawal) or Deleveraging (selling collateral) implies a swap. If the user can't limit the maximum shares burnt or minimum assets received, they get sandwiched.

**Quick Checks:**
- [ ] Vault `withdraw`: Has `maxSharesBurned`? (If requesting assets)
- [ ] Leverage `close`: Has `minCollateralOut`?

---

## Secure Implementation Pattern

```solidity
// ✅ SECURE: Full User Control
function swap(uint256 amountIn, uint256 minAmountOut, uint256 deadline) external {
    // 1. Check Deadline
    require(block.timestamp <= deadline, "Expired");

    // 2. Execute Swap with User Min
    uint[] memory amounts = router.swapExactTokensForTokens(
        amountIn,
        minAmountOut, // Passed through!
        path,
        msg.sender,
        deadline
    );
    
    // 3. Redundant Check (Optional but good)
    require(amounts[amounts.length - 1] >= minAmountOut, "Slippage");
}
```

## Keywords for Code Search

```bash
# Slippage params
rg -n "amountOutMin|amountAMin|amountBMin|minOutput"

# Vulnerable defaults
rg -n "swap.*\(.*,\s*0\s*,"

# Deadlines
rg -n "deadline|block\.timestamp"

# Liquidity ops
rg -n "addLiquidity|removeLiquidity"
```

---

## References

- Use the [Slippage Agent](../slippage-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/general/slippage-protection/`
