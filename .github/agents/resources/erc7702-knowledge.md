# ERC7702 Integration - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `erc7702-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| Universal Sig | ✓ | User Lockout (DOS) |
| Reentrancy Guard| ✓ | EOA Reentrancy Drain |
| Callback Support| ✓ | NFT Transfer Failure |
| Gas Handling | ✓ | Out of Gas (OOG) |
| Cross-Chain | ✓ | Fund Loss (Wrong Address) |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Brittle Code Checks

**One-liner**: `isContract(user)` is basically `random_bool()` now. Don't rely on it to decide how to verify a signature.

**Quick Checks:**
- [ ] `if (addr.code.length > 0)` used to branch logic?
- [ ] `Address.isContract` used before signature verification?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Logic Branching
if (signer.isContract()) {
    // 7702 user enters here, but might fail this call
    isValidSignature(...); 
} else {
    ecrecover(...);
}
```

---

### ⚠️ Category 2: EOA Reentrancy

**One-liner**: Treat `msg.sender` like a malicious contract, even if you think it's a user.

**Quick Checks:**
- [ ] `.call{value: x}("")` to `msg.sender`?
- [ ] State updates happen *after* the call? (CEI Violation)

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Reentrancy
(bool s, ) = msg.sender.call{value: amt}(""); // 7702 EOA re-enters
balances[msg.sender] -= amt; // Too late
```

---

### ⚠️ Category 3: Cross-Chain Identity

**One-liner**: My address on Ethereum might be a Gnosis Safe; my address on Polygon might be an empty EOA. Don't assume they are the same.

**Quick Checks:**
- [ ] `bridge(msg.sender)` defaulting to same address?
- [ ] No parameter to specify `destinationAddress`?

---

## Secure Implementation Pattern

```solidity
// ✅ SECURE: Universal Verification
function verify(address signer, bytes32 hash, bytes memory sig) internal view returns (bool) {
    // 1. Try ECDSA (Works for EOA & 7702)
    address recovered = ECDSA.recover(hash, sig);
    if (recovered == signer) return true;

    // 2. Try EIP-1271 (Works for Contract & 7702)
    try IERC1271(signer).isValidSignature(hash, sig) returns (bytes4 magic) {
        return magic == IERC1271.isValidSignature.selector;
    } catch {
        return false;
    }
}
```

## Keywords for Code Search

```bash
# Code Check
grep -n "extcodesize" . -r

# Callbacks
grep -n "onERC721Received" . -r

# Low level calls
grep -n ".call" . -r
```

---

## References

- Use the [ERC7702 Agent](../erc7702-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/general/erc7702-integration/`
