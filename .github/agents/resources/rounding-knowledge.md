# Rounding & Precision - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `rounding-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| Mul Before Div | ✓ | Massive Precision Loss |
| Rounding Direction | ✓ | User Profit / Protocol Loss |
| Zero Check | ✓ | Locked Funds / Fee Bypass |
| High Precision | ✓ | Inaccurate Accounting |
| Scale Factor | ✓ | Rounding to Zero |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Division Before Multiplication

**One-liner**: Dividing first truncates the decimal part, which is then lost for the subsequent multiplication.

**Quick Checks:**
- [ ] Pattern: `(a / b) * c`
- [ ] Pattern: `a.div(b).mul(c)`
- [ ] Pattern: `x = a / b; y = x * c;`

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Precision loss
uint256 ratio = current / target; // Rounds down (often to 0 or 1)
uint256 final = amount * ratio; 
```

**Reasoning Prompt:**
> "If `current` is 99 and `target` is 100, `ratio` becomes 0. `final` becomes 0. Is this intended?"

---

### ⚠️ Category 2: Rounding to Zero (Fee Bypass)

**One-liner**: Small inputs result in calculated values < 1, which Solidity truncates to 0.

**Quick Checks:**
- [ ] Fee calc: `amount * fee / 10000`
- [ ] Reward calc: `stake * rate / time`
- [ ] Is there a check `require(fee > 0)`?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Fee bypass
uint256 fee = (amount * 5) / 1000; // 0.5% fee
// If amount < 200, fee is 0.
```

---

### ⚠️ Category 3: Incorrect Rounding Direction

**One-liner**: Rounding should always favor the protocol (secure) or the invariant holder.

**Quick Checks:**
- [ ] `convertToShares` (Deposit): Rounds DOWN? (Correct)
- [ ] `convertToAssets` (Withdraw): Rounds DOWN? (Correct, user gets less)
- [ ] `previewMint` (User owes assets): Rounds UP? (Correct, user pays more)
- [ ] `previewWithdraw` (User owes shares): Rounds UP? (Correct, user burns more)

---

### ⚠️ Category 4: Locked Funds (Reward Distribution)

**One-liner**: `rewardPerToken` rounds to 0 due to high supply or low reward rate, making all claims 0.

**Quick Checks:**
- [ ] Formula: `(reward * 1e18) / totalSupply`
- [ ] Is `1e18` (Precision Factor) large enough for the max `totalSupply`?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Insufficient precision
uint256 rpt = (reward * 1e12) / totalSupply;
// If reward=1e18 and supply=1e30 (SHIB style), rpt = 0.
```

---

## Secure Implementation Pattern

```solidity
// ✅ SECURE: Full Precision
using Math for uint256;

function calculateAccurate(uint256 a, uint256 b, uint256 c) public pure returns (uint256) {
    // 1. Multiply first
    // 2. Use 256 for no overflow (checked)
    // 3. Round appropriately (Up/Down)
    return a.mulDiv(b, c, Math.Rounding.Down);
}
```

## Keywords for Code Search

```bash
# Division operators
rg -n "/|div\("

# Rounding func
rg -n "mulDiv|FixedPoint"

# Constants
rg -n "1e18|10\*\*18|10000"

# Zero Checks
rg -n "require.*> 0"
```

---

## References

- Use the [Rounding Agent](../rounding-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/general/rounding-precision-loss/`
