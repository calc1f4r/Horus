# Missing Validation - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `missing-validation-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| Zero Address | ✓ | Bricked Contract / Burnt Funds |
| Oracle Freshness | ✓ | Stale Price Arbitrage |
| Array Lengths | ✓ | Logic Errors / Index Out of Bounds |
| Numeric Bounds | ✓ | 200% Fees / Zero Duration |
| Contract Existence | ✓ | Silent Failure (Call to Empty) |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Address Validation

**One-liner**: If you set a critical address (Admin, Vault, Token) to `address(0)`, game over.

**Quick Checks:**
- [ ] `constructor(address a)` -> `require(a != address(0))`?
- [ ] `setAdmin(address a)` -> `require(a != address(0))`?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: No check
function setOps(address _ops) external {
    ops = _ops; // If _ops is 0, operations stop.
}
```

---

### ⚠️ Category 2: Oracle Validation

**One-liner**: Just getting the price isn't enough; you must verify the price is *current* and *valid*.

**Quick Checks:**
- [ ] `updatedAt` checked against `block.timestamp`?
- [ ] `answeredInRound >= roundId`?
- [ ] `price > 0`?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Stale Price
(, int price, , , ) = oracle.latestRoundData();
return price; // Could be from 3 years ago
```

---

### ⚠️ Category 3: Array Mismatch

**One-liner**: Processing two arrays assumes they match up perfectly. If not, you pay the wrong person.

**Quick Checks:**
- [ ] `function batch(a[], b[])`
- [ ] `require(a.length == b.length)`?
- [ ] `require(a.length > 0)`?

---

### ⚠️ Category 4: Numeric Bounds

**One-liner**: Parameters must make sense physically/economically (Time > 0, Fee <= 100%).

**Quick Checks:**
- [ ] `setFee(uint x)` -> `require(x <= MAX_FEE)`?
- [ ] `setDuration(uint x)` -> `require(x >= MIN_DURATION)`?

---

## Secure Implementation Pattern

```solidity
// ✅ SECURE: Robust Validation
function initialize(address _token, uint256 _fee) external {
    require(_token != address(0), "Invalid token");
    require(Address.isContract(_token), "Not contract");
    require(_fee <= 10000, "Fee too high"); // 100%
    
    token = _token;
    fee = _fee;
}
```

## Keywords for Code Search

```bash
# Zero Checks
grep -A 2 "set" . -r

# Oracle Usage
grep -n "latestRoundData" . -r

# Array Functions
grep -n "\[\]" . -r

# Numeric Sets
grep -n "uint256" . -r | grep "set"
```

---

## References

- Use the [Missing Validation Agent](../missing-validation-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/general/missing-validations/`
