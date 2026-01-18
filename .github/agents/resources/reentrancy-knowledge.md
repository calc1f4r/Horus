# Reentrancy - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `reentrancy-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| CEI Pattern | ✓ | Classic Reentrancy |
| ReentrancyGuard | ✓ | Double Spend / Drain |
| Read-Only Protection | ✓ | Price Manipulation |
| Cross-Function Lock | ✓ | State Corruption |
| Hook Safety | ✓ | Callback Reentrancy |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Classic Reentrancy (CEI Violation)

**One-liner**: Updating state *after* an external call allows the attacker to repeat the call before the state update happens.

**Quick Checks:**
- [ ] Is `balance[msg.sender] -= amount` done BEFORE `call`?
- [ ] Is `isDeposited = false` done BEFORE `call`?
- [ ] Are logs/events irrelevant? (Yes, only state matters)

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Interaction before Effect
(bool success, ) = msg.sender.call{value: amount}("");
require(success);
balances[msg.sender] = 0; // Too late! Re-entered above.
```

**Reasoning Prompt:**
> "If I call `withdraw` recursively inside the receive hook, is `balances` already 0?"

---

### ⚠️ Category 2: Cross-Function Reentrancy

**One-liner**: Re-entering a *different* function that shares state with the first function.

**Quick Checks:**
- [ ] Does Function A call external?
- [ ] Does Function B use state modified by A?
- [ ] Does Function B rely on A finishing?
- [ ] Are they both protected by `nonReentrant`?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Shared state, separate functions
function withdraw() {
    uint bal = balances[msg.sender];
    msg.sender.call{value: bal}(""); // Re-enter transfer() here
    balances[msg.sender] = 0;
}

function transfer(address to, uint amount) {
    // Balances not updated yet!
    if (balances[msg.sender] >= amount) { ... }
}
```

---

### ⚠️ Category 3: Read-Only Reentrancy

**One-liner**: Reading data (view function) from a contract that is currently in a "dirty" reentrancy state.

**Quick Checks:**
- [ ] Does protocol read P/L or Price from a 3rd party (Curve/Balancer)?
- [ ] Is that read done purely via `view` function?
- [ ] Does the 3rd party expose a reentrancy lock via view?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Trusting view during callback
function getPrice() view returns (uint) {
    // Balancer vault: inside joinPool callback
    // Balances updated, Supply NOT updated
    return vault.getPoolTokens(...) / pool.totalSupply(); // Price manipulated!
}
```

**Reasoning Prompt:**
> "Is the pool I'm querying currently executing a swap/join/exit?"

---

### ⚠️ Category 4: ERC721/1155 Hook Reentrancy

**One-liner**: `safeTransferFrom` and `_mint` trigger `onERC721Received` on the receiver, handing over control flow.

**Quick Checks:**
- [ ] Does function use `safeTransfer` or `_safeMint`?
- [ ] Is there state processing *after* this call?
- [ ] Is `nonReentrant` used?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Hook callback
_safeMint(msg.sender, tokenId); // Calls onERC721Received
totalSupply++; // Limit check bypassed if re-entered
```

---

## Secure Implementation Pattern

```solidity
// ✅ SECURE: Checks-Effects-Interactions
function withdraw(uint256 amount) external nonReentrant {
    // 1. Checks
    require(balances[msg.sender] >= amount, "Insufficient funds");
    
    // 2. Effects
    balances[msg.sender] -= amount;
    
    // 3. Interactions
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}
```

## Keywords for Code Search

```bash
# External calls
rg -n "\.call\{|\.transfer\(|\.safeTransfer"

# Reentrancy guards
rg -n "nonReentrant|ReentrancyGuard"

# Hooks
rg -n "onERC721Received|onERC1155Received"

# Read-only checks
rg -n "ensureNotInVaultContext|_checkReentrancy"
```

---

## References

- Use the [Reentrancy Agent](../reentrancy-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/general/reentrancy/`
