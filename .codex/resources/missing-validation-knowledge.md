# Missing Validation - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `missing-validation-reasoning` agent. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

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

The same two checks in Rust: `if token == Pubkey::default() { return Err(InvalidToken) }` and `if fee > MAX_FEE_BPS { return Err(FeeTooHigh) }` — reject the zero value of the identity type, bound the parameter, and fail with an error rather than a panic. In Go: reject a nil config pointer and `fee > maxFeeBPS` before first use.

---

## Per-Language Validation Checklists

The categories above are stated in EVM terms. Run the same sweep with the target language's primitives — a zero-address check and a nil-pointer check are the same bug class. Keep the EVM checklist active too; do not drop it on non-EVM targets.

**Rust**
- [ ] `unwrap()`/`expect()` on external or deserialized input (panic = DoS)
- [ ] Integer casts via `as` on user-supplied amounts (truncation: `u64 as u32`)
- [ ] `unsafe` blocks reachable from public handlers
- [ ] Slice indexing / `.get(i)` on user-controlled indices
- [ ] Arithmetic overflow in release profiles (wrapped, not checked)
- [ ] Handler does not verify signer / account authority

**Go**
- [ ] Write to a nil map (panic) on unpopulated config/registry
- [ ] Nil deref on optional config or parsed message fields
- [ ] Paired slices from a message payload with `len(a) != len(b)`
- [ ] Unbounded goroutines/channels spawned from network input
- [ ] Missing mutex around shared state written by message handlers
- [ ] Integer truncation in `int()`/`uint64()` conversions of amounts

**C++**
- [ ] Bounds checks before `[]`/`at()`/pointer arithmetic on wire data
- [ ] Iterator invalidation while mutating in loops
- [ ] Lifetime/dangling references across async or callback boundaries
- [ ] Signed/unsigned mixing and overflow (unchecked pre-C++20)
- [ ] RAII misuse: early returns skipping rollback of ledger mutations
- [ ] Authorization field parsed from a message but never compared

**Move (Sui/Aptos)**
- [ ] Missing capability/signer check on privileged entry points
- [ ] Struct `ability` misuse (`copy`/`drop` on types that must stay linear)
- [ ] Shared-object sequencing (counter/epoch read before external calls)
- [ ] Unvalidated `id`/address parameters resolving attacker-controlled objects

**Translation rule**: `require(a != address(0))` means "reject the zero value of the identity type" in every language — default/null account, nil interface, null pointer. When a hunt card's example is EVM-only, hunt the equivalent gap in the target language's checklist above instead of skipping the card.

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

- Use the [Missing Validation Agent](../agents/missing-validation-reasoning.toml) for deep analysis.
- Full DB Path: `DB/general/missing-validations/`
