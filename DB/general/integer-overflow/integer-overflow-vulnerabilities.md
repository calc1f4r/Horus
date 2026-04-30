---
# Core Classification
protocol: generic
chain: everychain
category: arithmetic
vulnerability_type: integer_overflow_underflow

# Attack Vector Details
attack_type: arithmetic_error
affected_component: numeric_operations

# Technical Primitives
primitives:
  - overflow
  - underflow
  - unchecked
  - SafeMath
  - uint256
  - int256
  - type_casting
  - unsafe_cast

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.6
financial_impact: high

# Context Tags
tags:
  - defi
  - arithmetic
  - solidity
  - real_exploit
  - DeFiHackLabs

# Version Info
language: solidity
version: "<0.8.0 or unchecked blocks"

# Source
source: DeFiHackLabs

# Pattern Identity (Required)
root_cause_family: arithmetic_error
pattern_key: arithmetic_error | numeric_operations | integer_overflow_underflow

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - SafeMath
  - _transfer
  - batchTransfer
  - burn
  - claimRewards
  - int256
  - msg.sender
  - overflow
  - processReward
  - processWithdraw
  - safeMul
  - transfer
  - transferProxy
  - type_casting
  - uint256
  - unchecked
  - underflow
  - unsafe_cast
---

# Integer Overflow/Underflow Vulnerabilities

## Overview

Integer overflow and underflow vulnerabilities occur when arithmetic operations exceed the maximum or minimum value representable by a data type, causing the value to wrap around. While Solidity 0.8.0+ includes built-in overflow checks, vulnerabilities persist in contracts using `unchecked` blocks, pre-0.8.0 code without SafeMath, or through unsafe type casting.

**Total Historical Losses from Analyzed Exploits: >$150M USD (historically significant, declining with Solidity 0.8+)**

---



#### Agent Quick View

- Root cause statement: Arithmetic wraps or truncates in a path that gates balance, debt, reward, supply, or collateral accounting, letting an attacker satisfy checks with a wrapped value while applying the original attacker-chosen amount.
- Pattern key: `arithmetic_error | numeric_operations | integer_overflow_underflow`
- Interaction scope: `single_contract`
- Primary affected component(s): `numeric_operations`
- High-signal code keywords: `unchecked`, `uint128`, `uint96`, `uint64`, `int256`, `SafeMath`, `batchTransfer`, `transferProxy`, `amount *`, `value + fee`, `balance - amount`, `claimRewards`, `processWithdraw`, `processReward`
- Typical sink / impact: `fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): user-controlled transfer, batch transfer, delegated transfer, reward claim, withdrawal, liquidation, fee, cast, or supply update
- Contract hop(s): usually single-contract arithmetic; may become multi-contract when wrapped token amounts feed AMM/lending accounting
- Trust boundary crossed: attacker-controlled numeric input enters invariant-critical arithmetic
- Shared state or sync assumption: totals, balances, rewards, and debt remain conserved across arithmetic and casts

#### Valid Bug Signals

- Solidity `<0.8.0` arithmetic lacks SafeMath or uses custom `safeAdd`/`safeMul` after the vulnerable expression already evaluated.
- Solidity `>=0.8.0` puts balance, reward, debt, or supply math in `unchecked` without a preceding bound that proves the operation cannot wrap.
- Downcast from `uint256`/`int256` to a smaller signed or unsigned type controls payout, debt delta, shares, or curve supply without `SafeCast`/range checks.
- A require/assert checks a wrapped intermediate such as `count * amount`, `value + fee`, or `balance - amount`, then later transfers/mints/burns the original amount.

#### False Positive Guards

- Not this bug when Solidity `>=0.8.0` checked arithmetic covers the operation and no unsafe downcast/unchecked block is on the critical path.
- Safe if `unchecked` is only used after a local invariant proves the exact operation cannot wrap for all attacker-controlled inputs.
- Safe if every downcast uses explicit bounds such as `require(x <= type(uint128).max)` or OpenZeppelin `SafeCast`.
- Requires attacker control of at least one operand or reachable protocol state that can push an intermediate outside the destination type bounds.

## Vulnerability Categories

### 1. Classic Overflow/Underflow (Pre-0.8.0)
Operations without SafeMath in older Solidity versions.

### 2. Unchecked Block Errors
Incorrect use of `unchecked` blocks in 0.8.0+ code.

### 3. Type Casting Overflow
Downcasting larger types to smaller types loses significant bits.

### 4. Signed Integer Issues
Overflow/underflow with signed integers (int256, int128, etc.).

### 5. Multiplication Overflow
Large multiplications that exceed max values.

---

## Vulnerable Pattern Examples

### Example 1: Classic Pre-0.8.0 Underflow [CRITICAL]

**Real Exploit: Beauty Chain (2018-04) - $900M Lost**

```solidity
// @PoC: DeFiHackLabs/src/test/2018-04/BEC_exp.sol
// Solidity version: <0.8.0
// ❌ VULNERABLE: No SafeMath, underflow possible

contract BeautyChain {
    mapping(address => uint256) public balances;
    
    function batchTransfer(address[] memory receivers, uint256 value) public {
        // @audit Integer overflow in multiplication!
        uint256 amount = receivers.length * value;
        // If receivers.length * value > type(uint256).max, it wraps to a small number
        
        require(balances[msg.sender] >= amount);
        balances[msg.sender] -= amount;
        
        for (uint256 i = 0; i < receivers.length; i++) {
            balances[receivers[i]] += value;
        }
    }
}

// Attack:
// Set value = type(uint256).max / 2 + 1
// Set receivers.length = 2
// amount = 2 * (type(uint256).max / 2 + 1) = 2 (overflow!)
// Only 2 tokens deducted from sender
// But each receiver gets type(uint256).max / 2 + 1 tokens
```

---

### Example 2: SmartMesh Overflow [CRITICAL]

**Real Exploit: SmartMesh (2018-04) - $140M Lost**

```solidity
// @PoC: DeFiHackLabs/src/test/2018-04/SmartMesh_exp.sol
// ❌ VULNERABLE: Overflow in transfer fee calculation

contract SmartMesh {
    mapping(address => uint256) public balances;
    
    function transferProxy(
        address from,
        address to,
        uint256 value,
        uint256 fee
    ) public {
        // @audit Overflow: value + fee can exceed uint256 max
        require(balances[from] >= value + fee);
        // If value = type(uint256).max, fee = 1
        // value + fee = 0 (overflow!)
        // Check passes with balance of 0!
        
        balances[from] -= value + fee;  // Underflows to huge number
        balances[to] += value;
    }
}
```

---

### Example 3: Unchecked Block Misuse [HIGH]

**Real Exploit: SCROLL Token (2024-05) - 76 ETH Lost**

```solidity
// @PoC: DeFiHackLabs/src/test/2024-05/SCROLL_exp.sol
// ❌ VULNERABLE: Unchecked block allows underflow
contract ScrollToken {
    mapping(address => uint256) public balances;
    
    function transfer(address to, uint256 amount) external {
        // @audit Developer used unchecked to save gas but introduced bug
        unchecked {
            // This can underflow if amount > balances[msg.sender]
            balances[msg.sender] -= amount;
            balances[to] += amount;
        }
    }
}

// ✅ SECURE: Check before unchecked arithmetic
function transfer(address to, uint256 amount) external {
    require(balances[msg.sender] >= amount, "Insufficient balance");
    
    unchecked {
        // Safe because we checked above
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```

---

### Example 4: Unsafe Type Casting [HIGH]

**Real Exploit: Alkimiya_IO (2025-03) - $95.5K Lost**

```solidity
// @PoC: DeFiHackLabs/src/test/2025-03/Alkimiya_io_exp.sol
// ❌ VULNERABLE: Unsafe downcast loses significant bits
contract AlkimiyaVault {
    function processReward(uint256 amount) external {
        // @audit Downcasting uint256 to uint128 loses upper bits
        uint128 rewardAmount = uint128(amount);
        // If amount = 2^128 + 100, rewardAmount = 100
        
        _distributeReward(rewardAmount);
    }
    
    function processWithdraw(uint256 amount) external {
        // @audit Casting to int256 can overflow for large uint256
        int256 delta = int256(amount);
        // If amount > type(int256).max, this overflows to negative
        
        updateBalance(delta);
    }
}

// ✅ SECURE: Use SafeCast library
import "@openzeppelin/contracts/utils/math/SafeCast.sol";

contract SecureVault {
    using SafeCast for uint256;
    
    function processReward(uint256 amount) external {
        // Reverts if amount > type(uint128).max
        uint128 rewardAmount = amount.toUint128();
        _distributeReward(rewardAmount);
    }
    
    function processWithdraw(uint256 amount) external {
        // Reverts if amount > type(int256).max
        int256 delta = amount.toInt256();
        updateBalance(delta);
    }
}
```

---

### Example 5: Pandora ERC404 Underflow [HIGH]

**Real Exploit: Pandora (2024-02) - $17K Lost**

```solidity
// @PoC: DeFiHackLabs/src/test/2024-02/PANDORA_exp.sol
// ❌ VULNERABLE: Integer underflow in ERC404 implementation

contract PandoraToken {
    mapping(address => uint256) private _balances;
    mapping(address => uint256) private _ownedTokens;
    
    function _transfer(address from, address to, uint256 amount) internal {
        uint256 unit = _getUnit();
        
        uint256 balanceBeforeSender = _balances[from];
        uint256 balanceBeforeReceiver = _balances[to];
        
        _balances[from] -= amount;
        _balances[to] += amount;
        
        // @audit Underflow possible in NFT accounting
        unchecked {
            // If user had 0 NFTs but token balance, this underflows
            uint256 tokensToTransfer = 
                (balanceBeforeSender / unit) - (_balances[from] / unit);
            // ...
        }
    }
}
```

---

### Example 6: LW Token Underflow [HIGH]

**Real Exploit: LW Token (2024-07) - $7K Lost**

```solidity
// @PoC: DeFiHackLabs/src/test/2024-07/LW_exp.sol
// ❌ VULNERABLE: Underflow in reward calculation

contract LWStaking {
    mapping(address => uint256) public userDebt;
    mapping(address => uint256) public userRewards;
    
    function claimRewards() external {
        uint256 pending = calculatePending(msg.sender);
        
        // @audit Can underflow if debt > pending due to timing
        unchecked {
            uint256 reward = pending - userDebt[msg.sender];
            userRewards[msg.sender] = reward;
        }
    }
}
```

---

### Example 7: Qixi Underflow [MEDIUM]

**Real Exploit: Qixi (2022-08) - 6.08 BNB Lost**

```solidity
// @PoC: DeFiHackLabs/src/test/2022-08/Qixi_exp.sol
// ❌ VULNERABLE: Transfer with unchecked math

contract QixiToken {
    mapping(address => uint256) private _balances;
    uint256 public totalBurned;
    
    function _transfer(address from, address to, uint256 amount) internal {
        uint256 burnAmount = amount / 100; // 1% burn
        uint256 transferAmount = amount - burnAmount;
        
        // @audit Pre-0.8.0 style without SafeMath
        _balances[from] = _balances[from] - amount;  // Can underflow
        _balances[to] = _balances[to] + transferAmount;
        totalBurned = totalBurned + burnAmount;
    }
}
```

---

## Real-World Exploits Summary

| Protocol | Date | Loss | Vulnerability Type |
|----------|------|------|-------------------|
| Beauty Chain | 2018-04 | $900M | Multiplication overflow |
| SmartMesh | 2018-04 | $140M | Addition overflow |
| Poolz | 2023-03 | $390K | Integer overflow |
| SCROLL | 2024-05 | 76 ETH | Unchecked underflow |
| Pandora | 2024-02 | $17K | ERC404 underflow |
| LW | 2024-07 | $7K | Reward calculation underflow |
| Alkimiya | 2025-03 | $95.5K | Unsafe cast |
| Qixi | 2022-08 | 6 BNB | Transfer underflow |

---

## Secure Implementation Guidelines

### 1. Use Solidity 0.8.0+ Default Checks
```solidity
// In Solidity 0.8.0+, this automatically reverts on overflow
uint256 result = a + b;  // Safe by default
uint256 product = a * b; // Safe by default
```

### 2. Be Careful with Unchecked Blocks
```solidity
// ❌ DANGEROUS: No overflow protection
unchecked {
    result = a - b;  // Can underflow!
}

// ✅ SAFE: Verify before unchecked
require(a >= b, "Underflow");
unchecked {
    result = a - b;  // Safe because we checked
}
```

### 3. Use SafeCast for Type Conversions
```solidity
import "@openzeppelin/contracts/utils/math/SafeCast.sol";

using SafeCast for uint256;
using SafeCast for int256;

uint128 smallValue = largeValue.toUint128();  // Reverts if too large
int256 signedValue = unsignedValue.toInt256(); // Reverts if > int256.max
```

### 4. Use SafeMath for Pre-0.8.0 Code
```solidity
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

using SafeMath for uint256;

uint256 result = a.add(b);  // Reverts on overflow
uint256 diff = a.sub(b);    // Reverts on underflow
```

### 5. Validate Multiplication Results
```solidity
function safeMul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) return 0;
    uint256 c = a * b;
    require(c / a == b, "Multiplication overflow");
    return c;
}
```

---

## Detection Patterns

### Semgrep Rules
```yaml
rules:
  - id: unchecked-arithmetic
    patterns:
      - pattern: |
          unchecked {
              ... $VAR = $A - $B ...
          }
      - pattern-not-inside: |
          require($A >= $B, ...);
          unchecked { ... }
    message: "Unchecked subtraction without prior validation"
    severity: WARNING
    
  - id: unsafe-downcast
    patterns:
      - pattern: uint128($VAR)
      - pattern: uint64($VAR)
      - pattern: uint32($VAR)
      - pattern: int128($VAR)
    message: "Unsafe type downcast - use SafeCast"
    severity: WARNING
```

### Manual Checklist
- [ ] Is Solidity version 0.8.0+ or SafeMath used?
- [ ] Are `unchecked` blocks preceded by appropriate checks?
- [ ] Are type downcasts using SafeCast?
- [ ] Are large multiplications checked for overflow?
- [ ] Are signed integer operations properly bounded?
- [ ] Is user input validated before arithmetic?

---

## Keywords for Search

`integer overflow`, `integer underflow`, `unchecked`, `SafeMath`, `uint256`, `int256`, `type casting`, `downcast`, `SafeCast`, `arithmetic overflow`, `multiplication overflow`, `subtraction underflow`, `wrap around`, `toUint128`, `toInt256`

---

## DeFiHackLabs Real-World Exploits (11 incidents)

**Category**: Integer Overflow | **Total Losses**: $1052.1M | **Sub-variants**: 2

### Sub-variant Breakdown

#### Integer-Overflow/Generic (9 exploits, $1043.0M)

- **Beauty Chain** (2018-04, $900.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2018-04/BEC_exp.sol`
- **SmartMesh** (2018-04, $140.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2018-04/SmartMesh_exp.sol`
- **Creat Future** (2022-04, $1.9M, bsc) | PoC: `DeFiHackLabs/src/test/2022-04/cftoken_exp.sol`
- *... and 6 more exploits*

#### Integer-Overflow/Unsafe Cast (2 exploits, $9.1M)

- **yETH** (2025-12, $9.0M, ethereum) | PoC: `DeFiHackLabs/src/test/2025-12/yETH_exp.sol`
- **Alkimiya_IO** (2025-03, $96K, ethereum) | PoC: `DeFiHackLabs/src/test/2025-03/Alkimiya_io_exp.sol`

### Complete DeFiHackLabs Exploit Table

| Protocol | Date | Loss | Vulnerability Sub-type | Chain |
|----------|------|------|----------------------|-------|
| Beauty Chain | 2018-04-22 | $900.0M | Integer Overflow | ethereum |
| SmartMesh | 2018-04-24 | $140.0M | Overflow | ethereum |
| yETH | 2025-12-01 | $9.0M | Unsafe Math | ethereum |
| Creat Future | 2022-04-11 | $1.9M | Overflow | bsc |
| Umbrella Network | 2022-03-20 | $700K | Underflow | ethereum |
| Poolz | 2023-03-15 | $390K | integer overflow | bsc |
| Alkimiya_IO | 2025-03-28 | $96K | unsafecast | ethereum |
| Pandora | 2024-02-08 | $17K | Integer Underflow | ethereum |
| LW | 2024-07-08 | $7K | Integer Underflow | bsc |
| SCROLL | 2024-05-29 | $76 | Integer Underflow | ethereum |
| Qixi | 2022-08-03 | $6 | Underflow | bsc |

### Top PoC References

- **Beauty Chain** (2018-04, $900.0M): `DeFiHackLabs/src/test/2018-04/BEC_exp.sol`
- **SmartMesh** (2018-04, $140.0M): `DeFiHackLabs/src/test/2018-04/SmartMesh_exp.sol`
- **yETH** (2025-12, $9.0M): `DeFiHackLabs/src/test/2025-12/yETH_exp.sol`
- **Creat Future** (2022-04, $1.9M): `DeFiHackLabs/src/test/2022-04/cftoken_exp.sol`
- **Umbrella Network** (2022-03, $700K): `DeFiHackLabs/src/test/2022-03/Umbrella_exp.sol`
- **Poolz** (2023-03, $390K): `DeFiHackLabs/src/test/2023-03/poolz_exp.sol`
- **Alkimiya_IO** (2025-03, $96K): `DeFiHackLabs/src/test/2025-03/Alkimiya_io_exp.sol`
- **Pandora** (2024-02, $17K): `DeFiHackLabs/src/test/2024-02/PANDORA_exp.sol`
- **LW** (2024-07, $7K): `DeFiHackLabs/src/test/2024-07/LW_exp.sol`
- **SCROLL** (2024-05, $76): `DeFiHackLabs/src/test/2024-05/SCROLL_exp.sol`

### Detection Patterns

#### Code Patterns to Look For
```
- Pre-0.8 arithmetic in guards: `uint256 total = count * amount; require(balance >= total);`
- Addition before balance check: `require(balance >= value + fee); balances[to] += value; balances[feeTo] += fee;`
- Unchecked balance/debt/reward math: `unchecked { balances[from] -= amount; rewards += amount * rate; }`
- Unsafe downcasts on accounting values: `uint128(amount)`, `uint96(shares)`, `int256(uint256Amount)`, `int128(delta)`
- Multiplication before division with attacker-sized operands: `amount * price / 1e18`, `shares * totalAssets / totalSupply`
```

#### Audit Checklist
- [ ] Verify source version and whether arithmetic is checked by Solidity or SafeMath on the exact expression.
- [ ] Verify `unchecked` blocks have preceding bounds that prove each operation cannot wrap.
- [ ] Verify downcasts use `SafeCast` or explicit `<= type(T).max` / signed range checks.
- [ ] Verify guard expressions and state updates use the same bounded quantity.
- [ ] Verify multiplication-before-division cannot overflow for maximum attacker-controlled inputs.

### Keywords for Search

> These keywords enhance vector search retrieval:

`DeFiHackLabs`, `SafeMath`, `_transfer`, `arithmetic`, `batchTransfer`, `burn`, `claimRewards`, `defi`, `int256`, `integer_overflow_underflow`, `msg.sender`, `overflow`, `processReward`, `processWithdraw`, `real_exploit`, `safeMul`, `solidity`, `transfer`, `transferProxy`, `type_casting`, `uint256`, `unchecked`, `underflow`, `unsafe_cast`
