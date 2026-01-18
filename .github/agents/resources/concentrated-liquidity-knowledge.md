# Concentrated Liquidity - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `concentrated-liquidity-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| Init Protection | ✓ | Initial Fund Theft |
| Tick Boundary | ✓ | Stuck Liquidity / Underflow |
| Fee Segregation | ✓ | Fee Theft (Flash Loan) |
| Liquidity Cache | ✓ | Manipulation via Reentrancy |
| Math Direction | ✓ | Protocol Inefficiency / Loss |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Initialization

**One-liner**: If I can init the pool at `1:1` when market is `1:1000`, I steal the first deposit.

**Quick Checks:**
- [ ] `function initialize(...) public/external`?
- [ ] No `onlyOwner` or `onlyFactory`?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Permissionless Init
function initialize(uint160 price) external {
    require(slot0.price == 0); // Anyone can call this first
    slot0.price = price;
}
```

---

### ⚠️ Category 2: Fee Accounting

**One-liner**: If fee-growth isn't part of the "Total Value" check during deposit, I can extract it for free.

**Quick Checks:**
- [ ] `deposit` function mints shares?
- [ ] Does it calculate `totalAssets`?
- [ ] Does `totalAssets` include `pendingFees`?

---

### ⚠️ Category 3: Tick Inequalities

**One-liner**: Off-by-one errors at tick boundaries cause loops to skip updates.

**Quick Checks:**
- [ ] `<` used instead of `<=` at upper boundary?
- [ ] `tick % spacing == 0` check handled?

---

### ⚠️ Category 4: Liquidity Caching

**One-liner**: Reading liquidity, then doing an external call (transfer), then using the *old* liquidity value is a death sentence.

**Quick Checks:**
- [ ] `liq = pos.liquidity` -> Line 1
- [ ] `token.transfer(...)` -> Line 5
- [ ] Logic relies on `liq` -> Line 10

---

## Secure Implementation Pattern

```solidity
// ✅ SECURE: Initialization & Math
function initialize(uint160 price) external onlyOwner {
    // ...
}

function mint(...) {
    // ...
    if (tickLower <= current && current < tickUpper) {
        // active range
    }
}
```

## Keywords for Code Search

```bash
# Init
grep "initialize" . -r

# Tick Math
grep "TickMath" . -r
grep "computeSwapStep" . -r

# Liquidity
grep "liquidity" . -r
grep "positions" . -r
```

---

## References

- Use the [Concentrated Liquidity Agent](../concentrated-liquidity-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/amm/concentrated-liquidity/`
