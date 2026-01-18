# Wormhole Bridge - Quick Knowledge Reference

> **Purpose**: Fast lookup reference for the `wormhole-reasoning-agent`. Contains condensed reasoning prompts, checklists, and vulnerability signatures.

---

## Core Security Requirements

| Check | Required | Attack If Missing |
|-------|----------|-------------------|
| VAA Verify | ✓ | Fake Message Injection |
| Emitter Check | ✓ | Spoofing from other App |
| Replay Guard | ✓ | Double Spending |
| Chain ID | ✓ | Wrong Source Chain |
| Consistency | ✓ | Reorg Attack |

---

## Vulnerability Quick Checklist

### ⚠️ Category 1: Emitter Validation

**One-liner**: Verifying the VAA signature only proves *someone* on *some* chain signed it. You MUST check *who* (`emitterAddress`) and *where* (`emitterChainId`).

**Quick Checks:**
- [ ] `vm.emitterAddress == trustedRemote`?
- [ ] `vm.emitterChainId == trustedChain`?
- [ ] Are addresses converted correctly? (Bytes32).

**Exploit Signature:**
```solidity
// ❌ VULNERABLE: Signature valid, but from WRONG app
(bool valid, string memory reason) = wormhole.verifyVM(vm);
require(valid, reason);
_process(vm.payload); // Attacker deployed their own emitter
```

---

### ⚠️ Category 2: Replay Protection

**One-liner**: VAAs are valid forever. You must remember if you've seen the `hash` before.

**Quick Checks:**
- [ ] `processed[vm.hash] = true` executed?
- [ ] `require(!processed[vm.hash])` checked?
- [ ] Is the map persistent (State variable)?

---

### ⚠️ Category 3: Token Bridge Integration

**One-liner**: `transferTokensWithPayload` allows attached data. If the target isn't a contract, the tokens are stuck.

**Quick Checks:**
- [ ] Sending to EOA? Use `transferTokens`.
- [ ] Sending to Contract? Use `transferTokensWithPayload`.

---

## Secure Implementation Pattern

```solidity
// ✅ SECURE: Full Verification
function receiveMessage(bytes calldata vaa) external {
    IWormhole.VM memory vm = wormhole.parseVM(vaa);
    (bool valid, string memory reason) = wormhole.verifyVM(vm);
    require(valid, reason);
    
    // 1. Check Source
    require(vm.emitterChainId == SOURCE_CHAIN_ID, "Wrong Chain");
    require(vm.emitterAddress == TRUSTED_EMITTER, "Wrong Emitter");
    
    // 2. Check Replay
    require(!processed[vm.hash], "Replay");
    processed[vm.hash] = true;
    
    // 3. Process
    // ...
}
```

## Keywords for Code Search

```bash
# VAA Logic
grep "parseVM" . -r
grep "verifyVM" . -r

# Replay Logic
grep "hash" . -r

# Emitter Logic
grep "emitterAddress" . -r
```

---

## References

- Use the [Wormhole Agent](../wormhole-reasoning-agent.md) for deep analysis.
- Full DB Path: `DB/bridge/wormhole/`
