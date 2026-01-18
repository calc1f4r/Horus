# Pyth Oracle - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `pyth-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| Staleness Check | ✓ | Use Old Price (Flash Crash) |
| Confidence Band | ✓ | Bad Execution (Arb) |
| Fee Refund | ✓ | Protocol drains User ETH |
| Exponent Scaling| ✓ | 100x Price Error |
| Payable Update | ✓ | DOS (Cannot update) |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Staleness

**One-liner**: `getPriceUnsafe` + No checks = REKT.

**Quick Checks:**
- [ ] `getPriceUnsafe(id)` called?
- [ ] `publishTime >= block.timestamp - N` missing?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: No checks
PythStructs.Price memory p = pyth.getPriceUnsafe(id);
return p.price; 
```

---

### ⚠️ Category 2: Exponents

**One-liner**: Pyth returns `price` (int64) and `expo` (int32). `price` is NOT the real value.

**Quick Checks:**
- [ ] `price.price` used directly?
- [ ] `expo` ignored?
- [ ] Hardcoded `* 1e18` or `* 1e10`?

---

### ⚠️ Category 3: Confidence Interval

**One-liner**: If `conf` is high, the price is garbage.

**Quick Checks:**
- [ ] `price.conf` ignored?
- [ ] No `require(conf < limit)`?

---

## Secure Implementation Pattern

```solidity
// ✅ SECURE: Staleness & Exponent
function getPrice() public view returns (uint256) {
    // 1. Safe Getter (Reverts if old)
    PythStructs.Price memory p = pyth.getPriceNoOlderThan(id, 60);
    
    // 2. Confidence Check
    require(p.conf < MAX_CONFIDENCE);
    
    // 3. Exponent Normalization
    return convertToUint(p.price, p.expo, 18);
}
```

## Keywords for Code Search

```bash
# Unsafe Calls
grep "getPriceUnsafe" . -r

# Updates
grep "updatePriceFeeds" . -r

# Exponents
grep "expo" . -r
```

---

## References

- Use the [Pyth Agent](../pyth-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/oracle/pyth/`
