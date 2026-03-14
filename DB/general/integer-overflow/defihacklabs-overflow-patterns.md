---
protocol: generic
chain: ethereum
category: integer_overflow
vulnerability_type: arithmetic_overflow

# Pattern Identity (Required)
root_cause_family: arithmetic_invariant_break
pattern_key: arithmetic_overflow | token_transfer | integer_overflow_underflow | fund_loss, token_minting

# Interaction Scope
interaction_scope: single_contract

attack_type: integer_overflow_underflow
affected_component: token_transfer, batch_transfer

primitives:
  - uint256_overflow
  - batchTransfer_overflow
  - transferProxy_overflow
  - unchecked_arithmetic
  - pre_solidity_0_8

severity: critical
impact: fund_loss, token_minting
exploitability: 0.95
financial_impact: critical

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - "_value"
  - "require"
  - "safeAdd"
  - "safeMul"
  - "batchTransfer"
  - "transferProxy"
path_keys:
  - "bec_token"
  - "smartmesh"

tags:
  - integer_overflow
  - underflow
  - batchTransfer
  - transferProxy
  - SafeMath
  - pre_0_8
  - ERC20
  - real_exploit
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 2
total_losses: "$140M+ confirmed"
---

## DeFiHackLabs Integer Overflow Exploit Patterns


## References & Source Reports

| Label | Source | Path / URL |
|-------|--------|------------|
| [BEC-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2018-04/BEC_exp.sol` |
| [SMT-POC] | DeFiHackLabs | `DeFiHackLabs/src/test/2018-04/SMT_exp.sol` |

---

### Overview

Integer overflow vulnerabilities in pre-Solidity 0.8. tokens enabled the creation of tokens from nothing. This entry catalogs **2 landmark exploits** from 2018 that together demonstrate how unchecked arithmetic in ERC20 implementations can bypass balance checks and create billions in phantom tokens. These are historical but critical for auditing legacy contracts and understanding why SafeMath / Solidity >= 0.8 checks are essential.


### Agent Quick View

| Field | Value |
|-------|-------|
| Root Cause | `arithmetic_invariant_break` |
| Pattern Key | `arithmetic_overflow | token_transfer | integer_overflow_underflow | fund_loss, token_minting` |
| Severity | CRITICAL |
| Impact | fund_loss, token_minting |
| Interaction Scope | `single_contract` |
| Chain(s) | ethereum |


### Root Cause

In Solidity < 0.8.0, arithmetic operations silently overflow/underflow:
- `uint256(2) - uint256(3) = 2^256 - 1` (underflow → max value)
- `uint256(2^255) * 2 = 0` (overflow → wraps to zero)

If a `require()` check uses an expression that overflows, the check passes when it shouldn't.

---

### Vulnerable Pattern Examples

#### Pattern 1: batchTransfer Overflow [CRITICAL]

> **pathShape**: `atomic`

**Example 1: BEC Token (Beauty Chain) — batchTransfer Creates Tokens ($900M market cap, 2018-04)** [CRITICAL]
```solidity
// ❌ VULNERABLE: batchTransfer has unchecked multiplication overflow
// Solidity 0.4.x — NO automatic overflow checks

contract BECToken {
    mapping(address => uint256) balances;

    function batchTransfer(address[] _receivers, uint256 _value) public returns (bool) {
        uint cnt = _receivers.length;

        // @audit CRITICAL: This multiplication can OVERFLOW
        uint256 amount = uint256(cnt) * _value;
        // If cnt = 2 and _value = 2^255:
        //   amount = 2 * 2^255 = 2^256 = 0 (OVERFLOW!)

        // @audit Balance check passes because amount = 0
        require(cnt > 0 && cnt <= 20);
        require(_value > 0 && balances[msg.sender] >= amount);
        // require(balances[msg.sender] >= 0) → ALWAYS TRUE!

        balances[msg.sender] = balances[msg.sender].sub(amount);
        // @audit Subtracts 0 from sender (no actual deduction)

        for (uint i = 0; i < cnt; i++) {
            balances[_receivers[i]] = balances[_receivers[i]].add(_value);
            Transfer(msg.sender, _receivers[i], _value);
            // @audit Each receiver gets _value = 2^255 tokens
            // @audit Created from nothing — sender loses 0, receivers gain 2^255 each
        }
        return true;
    }
}

// Attack:
// 1. Call batchTransfer with 2 addresses and _value = 2^255
// 2. amount = 2 * 2^255 = 0 (overflow)
// 3. require(balances[sender] >= 0) → passes (anyone has >= 0)
// 4. balances[sender] -= 0 (no deduction)
// 5. balances[receiver1] += 2^255 (half of uint256 max)
// 6. balances[receiver2] += 2^255 (half of uint256 max)
// 7. Total tokens created: 2^256 ≈ 1.15 × 10^77 BEC tokens from nothing

// Result: Attacker dumps tokens on exchanges → BEC price crashes to $0
// Market cap was ~$900M before exploit
```
- **PoC**: `DeFiHackLabs/src/test/2018-04/BEC_exp.sol`
- **Root Cause**: `uint256(cnt) * _value` overflows to 0 when `cnt * _value >= 2^256`. The balance check `require(balances[msg.sender] >= amount)` becomes `require(balances[msg.sender] >= 0)` which is always true. Each recipient receives `_value` tokens that were never deducted from anyone.

---

#### Pattern 2: transferProxy Overflow [CRITICAL]

> **pathShape**: `atomic`

**Example 2: SmartMesh (SMT) — transferProxy Free Token Creation ($140M, 2018-04)** [CRITICAL]
```solidity
// ❌ VULNERABLE: transferProxy has unchecked addition overflow in fee calculation

contract SMTToken {
    mapping(address => uint256) balances;

    function transferProxy(
        address _from,
        address _to,
        uint256 _value,
        uint256 _feeSmt,   // Fee paid to relayer
        uint8 _v, bytes32 _r, bytes32 _s
    ) public returns (bool) {
        // Verify EIP-712 style signature from _from
        // ... signature verification ...

        // @audit CRITICAL: _value + _feeSmt can OVERFLOW
        require(balances[_from] >= _feeSmt + _value);
        // If _value = 2^256 - 100 and _feeSmt = 100:
        //   _feeSmt + _value = 100 + (2^256 - 100) = 2^256 = 0 (OVERFLOW!)
        // require(balances[_from] >= 0) → ALWAYS TRUE!

        // @audit Transfers happen with original (huge) _value
        balances[_to] += _value;         // @audit Receiver gets 2^256 - 100 tokens
        balances[msg.sender] += _feeSmt;  // @audit Relayer gets 100 tokens

        // @audit Deduction: balances[_from] -= (_feeSmt + _value) = -= 0
        balances[_from] -= _feeSmt + _value;  // Subtracts 0!

        return true;
    }
}

// Attack:
// 1. Choose _value = MAX_UINT256 - _feeSmt (so sum overflows to 0)
// 2. Sign the transferProxy message
// 3. require(balances[_from] >= 0) passes for ANY balance (even 0)
// 4. _to receives MAX_UINT256 - _feeSmt tokens (effectively infinite)
// 5. msg.sender gets _feeSmt tokens
// 6. _from loses 0 tokens (overflow in subtraction)

// Attacker dumped fabricated SMT on Huobi exchange
// Token immediately delisted, ~$140M in supposed value evaporated
```
- **PoC**: `DeFiHackLabs/src/test/2018-04/SMT_exp.sol`
- **Root Cause**: `_feeSmt + _value` overflows to 0 when the attacker chooses `_value = type(uint256).max - _feeSmt + 1`. The balance check passes with zero balance, no tokens are deducted, but both the recipient and relayer receive massive token amounts.

---

### General Overflow Pattern

```solidity
// ❌ VULNERABLE: ANY of these patterns in Solidity < 0.8.0

// Pattern A: Multiplication overflow
uint256 total = quantity * price;
require(balances[sender] >= total);  // total could be 0

// Pattern B: Addition overflow
uint256 sum = amount + fee;
require(balances[sender] >= sum);  // sum could wrap to 0

// Pattern C: Subtraction underflow
uint256 remaining = balance - withdrawal;
// remaining could be MAX_UINT256 if withdrawal > balance

// Pattern D: Array length overflow
uint256 newLength = array.length + count;
// newLength could wrap, enabling out-of-bounds write
```

---

### Impact Analysis

#### Technical Impact
- **Infinite token creation**: Attackers create tokens from nothing, bypassing supply constraints
- **Exchange dump**: Created tokens sold on exchanges before detection
- **Irreversible**: No way to "uncreate" phantom tokens without contract migration

#### Historical Impact
| Token | Loss/Impact | Overflow Type | Date |
|-------|-------------|---------------|------|
| BEC (Beauty Chain) | ~$900M market cap destroyed | `cnt * _value` multiplication overflow | Apr 2018 |
| SMT (SmartMesh) | ~$140M, Huobi delisted | `_feeSmt + _value` addition overflow | Apr 2018 |

**Industry Response**: These exploits (both in April 2018) directly led to:
- Exchanges implementing batch transfer pause mechanisms
- OpenZeppelin SafeMath becoming standard
- Solidity 0.8.0 adding built-in overflow checks (released Jan 2021)

---

### Secure Implementation

**Fix 1: SafeMath (Solidity < 0.8.0)**
```solidity
// ✅ SECURE: Use OpenZeppelin SafeMath for all arithmetic
import "@openzeppelin/contracts/math/SafeMath.sol";

contract SecureToken {
    using SafeMath for uint256;

    function batchTransfer(address[] memory receivers, uint256 value) public {
        // @audit SafeMath.mul reverts on overflow instead of wrapping
        uint256 amount = receivers.length.mul(value);
        require(balances[msg.sender] >= amount, "insufficient balance");

        balances[msg.sender] = balances[msg.sender].sub(amount);
        for (uint i = 0; i < receivers.length; i++) {
            balances[receivers[i]] = balances[receivers[i]].add(value);
        }
    }
}
```

**Fix 2: Solidity >= 0.8.0 Built-in Checks**
```solidity
// ✅ SECURE: Solidity 0.8+ automatically reverts on overflow/underflow
pragma solidity ^0.8.0;

contract SecureToken {
    function batchTransfer(address[] calldata receivers, uint256 value) external {
        // @audit This automatically reverts if receivers.length * value overflows
        uint256 amount = receivers.length * value;
        require(balances[msg.sender] >= amount, "insufficient balance");

        balances[msg.sender] -= amount;
        for (uint i = 0; i < receivers.length; i++) {
            balances[receivers[i]] += value;
        }
    }
}
```

**Fix 3: Explicit Overflow Check Pattern**
```solidity
// ✅ SECURE: Manual overflow check for critical operations
function safeAdd(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    require(c >= a, "addition overflow");  // @audit c < a means overflow occurred
    return c;
}

function safeMul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) return 0;
    uint256 c = a * b;
    require(c / a == b, "multiplication overflow");  // @audit c/a != b means overflow
    return c;
}
```

---

### Detection Patterns

```bash
# Solidity version < 0.8.0 (overflow-vulnerable)grep -rn "pragma solidity" --include="*.sol" | \
  grep -E "0\.[4-7]\."

# batchTransfer / batch operations without SafeMath
grep -rn "function batch\|function multi" --include="*.sol" | \
  xargs grep -A 20 "\.length.*\*\|amount.*\+\|_value.*\+" | \
  grep -L "SafeMath\|using.*Math"

# Unchecked arithmetic near balance checks
grep -rn "require.*balance.*>=\|require.*>=.*balance" --include="*.sol" | \
  xargs grep -B 5 "\*\s\|+\s" | grep -L "safe\|SafeMath\|0\.8"

# transferProxy / meta-transaction patterns
grep -rn "function transferProxy\|function metaTransfer" --include="*.sol"
```

---

### Audit Checklist

1. **What Solidity version is used?** — < 0.8.0 means ALL arithmetic is overflow-vulnerable
2. **Is SafeMath used for EVERY arithmetic operation?** — Not just some
3. **Are there batch/multi transfer functions?** — `quantity * value` is the classic overflow
4. **Are there fee + value addition patterns?** — `fee + value` can overflow to 0
5. **Are there `unchecked {}` blocks in Solidity >= 0.8?** — These opt out of safety checks
6. **Do balance checks use computed sums?** — If the sum overflows, the check is meaningless

---

### Keywords

- integer_overflow
- underflow
- batchTransfer
- transferProxy
- SafeMath
- unchecked
- uint256_overflow
- pre_solidity_0_8
- multiplication_overflow
- addition_overflow
- phantom_tokens
- DeFiHackLabs

---

### Related Vulnerabilities

- [Integer Overflow Vulnerabilities](../../general/integer-overflow/integer-overflow-vulnerabilities.md)
- [Access Control](../../general/access-control/access-control-vulnerabilities.md)
