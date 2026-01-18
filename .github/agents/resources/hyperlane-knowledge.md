# Hyperlane Bridge - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `hyperlane-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| MailboxOnly | ✓ | Spoofing Interface |
| Sender Check | ✓ | Spoofing Source |
| Origin Check | ✓ | Spoofing Chain |
| Replay Guard | ✓ | Double Minting |
| IGP Payment | ✓ | Stuck Messages |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Access Control

**One-liner**: If `handle` isn't restricted to `Mailbox`, anyone can call it.

**Quick Checks:**
- [ ] `function handle(...)` calls `onlyMailbox`?
- [ ] `require(msg.sender == address(mailbox))`?

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: No check
function handle(...) external {
    _mint(...); // I call this directly
}
```

---

### ⚠️ Category 2: Source Verification

**One-liner**: Just because it came from the Mailbox doesn't mean it's friendly. The Mailbox delivers messages from *anyone*.

**Quick Checks:**
- [ ] `require(_sender == trustedRemote)`?
- [ ] `require(_origin == trustedChain)`?

---

### ⚠️ Category 3: Gas Payment (IGP)

**One-liner**: You must pay the Interchain Gas Paymaster (IGP) to get your message delivered.

**Quick Checks:**
- [ ] `igp.payForGas{value: ...}()` called?
- [ ] Is `refund` handled?

---

## Secure Implementation Pattern

```solidity
// ✅ SECURE: Full Check
modifier onlyMailbox() {
    require(msg.sender == address(mailbox), "Only Mailbox");
    _;
}

function handle(uint32 _origin, bytes32 _sender, bytes calldata _body) external onlyMailbox {
    require(_origin == TRUSTED_CHAIN, "Wrong Chain");
    require(_sender == TRUSTED_SENDER, "Wrong Sender");
    // ...
}
```

## Keywords for Code Search

```bash
# Handle Logic
grep "handle" . -r

# Mailbox
grep "Mailbox" . -r

# Sender Conversion
grep "bytes32ToAddress" . -r
```

---

## References

- Use the [Hyperlane Agent](../hyperlane-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/bridge/hyperlane/`
