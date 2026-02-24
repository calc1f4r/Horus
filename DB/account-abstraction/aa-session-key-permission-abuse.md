---
# Core Classification
protocol: generic
chain: everychain
category: account_abstraction
vulnerability_type: session_key_abuse

# Attack Vector Details
attack_type: logical_error
affected_component: session_key_validation

# Technical Primitives
primitives:
  - session_key
  - sessionData
  - permissionId
  - validateUserOp
  - CredibleAccountModule
  - ResourceLockValidator
  - NativeTokenLimitModule
  - SmartSession
  - ERC-7579
  - ERC-4337
  - _validateSessionKeyParams
  - enableMode

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.70
financial_impact: high

# Context Tags
tags:
  - account-abstraction
  - session-key
  - permission
  - smart-wallet
  - ERC-4337
  - ERC-7579
  - front-running
  - spend-limit
  - cross-wallet

language: solidity
version: ">=0.8.0"
---

## References

| Tag | Report Path |
|-----|-------------|
| [SK-1] | `reports/account_abstraction_findings/c-01-sessionkey-owner-can-drain-the-smart-wallet.md` |
| [SK-2] | `reports/account_abstraction_findings/h-01-session-key-can-be-consumed-by-unauthorized-scw.md` |
| [SK-3] | `reports/account_abstraction_findings/h-01-sessionkey-owner-can-impersonate-another-session-key-owner-for-the-same-sma.md` |
| [SK-4] | `reports/account_abstraction_findings/session-keys-share-and-overwrite-each-others-permissions.md` |
| [SK-5] | `reports/account_abstraction_findings/enable-mode-can-be-frontrun-to-add-policies-for-a-different-permissionid.md` |
| [SK-6] | `reports/account_abstraction_findings/nativetokenlimitmodule-can-be-bypassed.md` |
| [SK-7] | `reports/account_abstraction_findings/h-04-arbitrary-transactions-possible-due-to-insufficient-signature-validation.md` |
| [SK-8] | `reports/account_abstraction_findings/c-07-in-resourcelockvalidator-the-validateuserop-function-is-not-consuming-the-s.md` |
| [SK-9] | `reports/account_abstraction_findings/c-08-in-resourcelockvalidator-the-validateuserop-function-lacks-sufficient-check.md` |

## Vulnerability Title

**AA Session Key & Permission Abuse — Spend Limit Bypass, Cross-Wallet Consumption, Permission Overwrite, and frontrun PermissionId Swap**

### Overview

Session keys in ERC-4337 / ERC-7579 smart accounts are meant to grant restricted, time-limited execution rights. Across 9+ audit reports, session key implementations consistently fail to enforce their own restrictions: session keys can approve arbitrary spenders (draining the wallet entirely), be consumed by any wallet instead of just the intended one, share storage slots with other keys (overwriting each other's permissions), and have their `permissionId` swapped via frontrunning during enable-mode installation.

### Session Key Abuse — Spend Limit Bypass, Cross-Wallet Consumption, Permission Overwrite, PermissionId Frontrun

#### Root Cause

Session key security depends on correct enforcement of four invariants:
1. The key's allowed spenders, targets, and amounts are validated during every call.
2. The key is bound to a specific smart wallet (not consumable by others).
3. Each key has an isolated storage slot (no aliasing with other keys).
4. The `permissionId` associated with the key is committed to in the signed hash.

Common failures:
- **Invariant 1 violated** — `_validateSingleCall` returns `true` for `ERC20.approve` without checking *who* is being approved as spender, letting the session key owner approve themselves and drain the wallet.
- **Invariant 2 violated** — `validateUserOp` recovers a `sessionKeySigner` address but never verifies it belongs to the calling wallet (`msg.sender`). Any SCW that installed the module can use any session key from any other wallet.
- **Invariant 3 violated** — Storage key derivation erroneously slices off 4 bytes of the `sessionKeyId` counter, causing the first ~4 billion keys to share the same `SessionKeyData` slot.
- **Invariant 4 violated** — `permissionId` is parsed from `userOp.signature` (which is NOT part of `userOpHash` and therefore not signed by EntryPoint). Bundler can swap it to redirect policies to a different permission.

Additionally:
- **NativeTokenLimitModule bypass** — The module enforces a spend limit by checking call value, but certain execution paths (e.g., batch calls or specific call types) bypass the per-session limit check.
- **ResourceLockValidator** — Does not consume (invalidate) the session after use, allowing it to be used repeatedly; also lacks sufficient checks on the signed user operation fields.

#### Attack Scenario

**Scenario A — Session key drains entire wallet** [SK-1] (Shieldify, CRITICAL):
1. Alice's smart wallet has a `CredibleAccountModule` with a session key `SK` authorized for specific locked tokens.
2. `SK` is permitted to call `ERC20.approve()` — but the spender address is never checked.
3. `SK` owner calls `ERC20.approve(attacker, type(uint256).max)` on every token in the wallet.
4. Attacker calls `ERC20.transferFrom(aliceWallet, attacker, balance)` to drain all tokens.

**Scenario B — Session key consumed by unauthorized SCW** [SK-2] (Shieldify, HIGH):
1. Module is installed on both Alice's wallet and Bob's wallet.
2. Alice's session key `SK_A` is stored under `sessionData[SK_A][aliceWallet]`.
3. Bob calls `validateUserOp` with `userOp.sender = bobWallet` but signs with `SK_A`.
4. The module recovers `SK_A`, checks `sessionData[SK_A][msg.sender]` = `sessionData[SK_A][bobWallet]`.
5. If Bob had previously set up any session data at that slot, validation passes — Bob consumed Alice's session key on his wallet.

**Scenario C — Session key impersonation within same wallet** [SK-3] (Shieldify, HIGH):
1. Two session keys SK_A and SK_B are registered for the same smart wallet.
2. SK_A owner signs a userOp but submits it claiming to be SK_B (or vice-versa).
3. Due to missing cross-key binding in the hash, the validation passes for the wrong session key identity.

**Scenario D — Session key permission overwrite** [SK-4] (Quantstamp, HIGH):
1. Account registers 5 session keys (IDs 0–4). Due to the last-4-bytes slicing bug, all share the same `SessionKeyData` storage slot.
2. Each `updateKeyPermissions` call silently overwrites the previous key's permissions.
3. The last-registered key's permissions apply to ALL keys, destroying per-key isolation.

**Scenario E — Enable mode frontrun swaps permissionId** [SK-5] (Cantina/Rhinestone, HIGH):
1. Alice sends a userOp enabling policies for `permissionId = X`.
2. Bundler/attacker sees the pending transaction and replaces `permissionId` in `userOp.signature` with their own `permissionId = Y` (which they also have installed with the same nonce).
3. Alice's policies get installed on `permissionId = Y` instead of X — attacker gains Alice's policy permissions.

**Scenario F — NativeTokenLimitModule bypass** [SK-6] (Quantstamp, HIGH):
1. Session key is granted a `nativeTokenLimit = 0.1 ETH`.
2. Attacker constructs a batch call routed through an execution path not covered by the limit check.
3. The session key transfers more than `0.1 ETH` without triggering a revert.

#### Vulnerable Pattern Examples

**Example 1: approve() allowed without spender check** [CRITICAL] — Source: [SK-1]
```solidity
// ❌ VULNERABLE: ERC20.approve selector accepted unconditionally
// Session key can approve any address — including itself

function _validateSingleCall(bytes calldata _callData) internal view returns (bool) {
    bytes4 selector = bytes4(_callData[:4]);

    if (selector == IERC20.approve.selector) {
        return true; // ← NO check on _callData[4:36] (spender address)
    }
    if (target != address(this)) return false;
    return true;
}

function _validateBatchCall(bytes calldata _callData) internal view returns (bool) {
    Execution[] calldata execs = ExecutionLib.decodeBatch(_callData[EXEC_OFFSET:]);
    for (uint256 i; i < execs.length; ++i) {
        bytes4 selector = bytes4(execs[i].callData[:4]);
        if (selector == IERC20.approve.selector) continue; // ← same issue
        if (execs[i].target != address(this)) return false;
    }
    return true;
}
```

**Example 2: Session key not bound to specific wallet** [HIGH] — Source: [SK-2]
```solidity
// ❌ VULNERABLE: Recovers sessionKeySigner but never checks it belongs to msg.sender

function validateUserOp(
    PackedUserOperation calldata userOp,
    bytes32 userOpHash,
    uint256 missingAccountFunds
) external returns (uint256) {
    bytes memory sig = _digestSignature(userOp.signature);
    address sessionKeySigner = ECDSA.recover(
        ECDSA.toEthSignedMessageHash(userOpHash), sig
    );

    // ← Checks that the session is valid for (sessionKeySigner, msg.sender),
    //   but there is no check that sessionKeySigner was registered BY msg.sender specifically.
    //   Any wallet that installed the module can look up ANY key.
    if (!_validateSessionKeyParams(sessionKeySigner, userOp)) {
        return VALIDATION_FAILED;
    }
    SessionData memory sd = sessionData[sessionKeySigner][msg.sender];
    return _packValidationData(false, sd.validUntil, sd.validAfter);
}
```

**Example 3: SessionKeyData storage collision — shared slot for first 4B keys** [HIGH] — Source: [SK-4]
```solidity
// ❌ VULNERABLE: sessionKeyDataKey slices off 4 least-significant bytes of sessionKeyId
// All session IDs 0..4294967295 produce the same storage key

function sessionKeyDataKey(
    SessionKeyId id,
    address account,
    uint256 batchIndex
) internal pure returns (bytes32) {
    return keccak256(abi.encodePacked(
        bytes12(0),                    // 12 bytes padding
        account,                       // 20 bytes
        SESSION_KEY_DATA_PREFIX,       // 4 bytes
        batchIndex                     // 32 bytes
    ))
    // The original code appended:
    // + bytes32(abi.encodePacked(SESSION_KEY_DATA_PREFIX, SessionKeyId.unwrap(id)))
    //   ↑ This slices off the 4 right-most bytes of id (least significant bytes of uint256 counter)
    //   ↑ Result: ids 0..0xFFFFFFFF map to SAME key
    ;
}
```

**Example 4: permissionId not in signed hash — frontrun possible** [HIGH] — Source: [SK-5]
```solidity
// ❌ VULNERABLE: permissionId decoded from userOp.signature which is NOT signed by EntryPoint
// Bundler can modify permissionId without invalidating the signature

function validateUserOp(
    PackedUserOperation calldata userOp,
    bytes32 userOpHash,
    ...
) external returns (uint256) {
    // permissionId parsed from userOp.signature — NOT part of userOpHash
    (PermissionId permId, SmartSessionMode mode, bytes calldata sigData) =
        userOp.signature.decodeSmartSessionSignature();

    if (mode == SmartSessionMode.ENABLE) {
        // permId is used to install policies but is NOT in the signed digest
        _enablePolicies(permId, userOpHash, sigData);
        // ← attacker replaced permId in the mempool before this executes
    }
}

function getAndVerifyDigest(
    PermissionId permId,          // ← not signed!
    bytes32 userOpHash,
    bytes calldata enableSessionSig
) internal view returns (address signer, PermissionId id) {
    bytes32 digest = _hashTypedData(keccak256(abi.encode(
        ENABLE_SESSION_TYPEHASH,
        // permId absent here
        keccak256(abi.encode(session)),
        userOpHash
    )));
    // Signature verifies but permId can be anything the bundler chooses
}
```

**Example 5: ResourceLockValidator does not consume session** [CRITICAL] — Source: [SK-8]
```solidity
// ❌ VULNERABLE: Session is validated but never consumed (invalidated)
// Same session can be replayed indefinitely

function validateUserOp(
    PackedUserOperation calldata userOp,
    bytes32 userOpHash
) external override returns (uint256) {
    ResourceLockSessionData memory session = _decodeSession(userOp);
    _validateSession(session, userOp);
    // ← Missing: _consumeSession(session) or nonce increment
    // Session remains valid for future replay
    return VALIDATION_SUCCESS;
}
```

**Example 6: Insufficient checks in ResourceLockValidator** [CRITICAL] — Source: [SK-9]
```solidity
// ❌ VULNERABLE: validateUserOp does not verify critical fields of the userOp
// against the session constraints (trusted limits, target addresses, selectors)

function validateUserOp(...) external returns (uint256) {
    ResourceLockSessionData memory session = _decodeSession(userOp);
    // Checks expiry and basic format
    require(block.timestamp < session.validUntil, "expired");
    // ← Missing: check that userOp.callData target matches session.allowedTarget
    // ← Missing: check that value <= session.nativeTokenLimit
    // ← Missing: check that callData selector is in session.allowedSelectors
    return VALIDATION_SUCCESS;
}
```

### Impact Analysis

#### Technical Impact
- Session keys with `approve` bypass can drain all ERC-20 tokens in the wallet — even non-whitelisted ones
- Cross-wallet key consumption means compromising one wallet's key compromises all wallets with the same module
- Storage collision destroys per-key permission isolation; last-registered key overwrites all others
- `permissionId` frontrun misdirects session policy installation silently

#### Business Impact
- Full wallet drain with no on-chain evidence of misbehavior (session key used as authorized)
- User trust in session key "security escrow" model catastrophically broken
- Protocol liability for stolen funds when advertised restrictions do not hold

#### Affected Scenarios
- Approve-based session keys (drain via unlimited approval): Uncommon setup but CRITICAL when present (1/9 reports)
- Cross-wallet key consumption: Specific to module-sharing architectures (2/9 reports)
- Storage collision: Unique to incorrect `keccak256` key derivation (1/9 reports, HIGH)
- frontrun permissionId: Requires mempool visibility + specific preconditions (1/9 reports, HIGH)
- NativeTokenLimit bypass: Execution-path specific (1/9 reports, HIGH)
- ResourceLock insufficient validation: Incomplete implementation (2/9 reports, CRITICAL)

### Secure Implementation

**Fix 1: Validate spender address in approve calls**
```solidity
// ✅ SECURE: When approve is detected, verify the spender is the module itself (or a whitelist)

function _validateSingleCall(bytes calldata _callData) internal view returns (bool) {
    bytes4 selector = bytes4(_callData[:4]);

    if (selector == IERC20.approve.selector) {
        // Extract spender from ABI-encoded approve(address,uint256)
        address spender = abi.decode(_callData[4:36], (address));
        // Only allow approvals to the module contract
        require(spender == address(this), "UnauthorizedSpender");
        return true;
    }
    if (target != address(this)) return false;
    return true;
}
```

**Fix 2: Bind session key to specific wallet during validation**
```solidity
// ✅ SECURE: After recovering sessionKeySigner, verify it was registered by msg.sender

function validateUserOp(
    PackedUserOperation calldata userOp,
    bytes32 userOpHash,
    uint256 missingAccountFunds
) external returns (uint256) {
    bytes memory sig = _digestSignature(userOp.signature);
    address sessionKeySigner = ECDSA.recover(
        ECDSA.toEthSignedMessageHash(userOpHash), sig
    );

    // ✅ Must verify this session key was registered by this specific wallet
    SessionData memory sd = sessionData[sessionKeySigner][msg.sender];
    require(sd.registeredBy == msg.sender, "KeyNotOwnedByWallet"); // ← explicit ownership
    if (!_validateSessionKeyParams(sessionKeySigner, userOp)) {
        return VALIDATION_FAILED;
    }
    return _packValidationData(false, sd.validUntil, sd.validAfter);
}
```

**Fix 3: Correct storage key derivation — do not slice sessionKeyId**
```solidity
// ✅ SECURE: Full sessionKeyId bytes, no truncation

function sessionKeyDataKey(
    SessionKeyId id,
    address account,
    uint256 batchIndex
) internal pure returns (bytes32) {
    return keccak256(abi.encodePacked(
        bytes12(0),
        account,
        SESSION_KEY_DATA_PREFIX,
        batchIndex,
        SessionKeyId.unwrap(id)   // ← full 32 bytes, no truncation
    ));
}
```

**Fix 4: Include permissionId in the signed enable-session digest**
```solidity
// ✅ SECURE: permissionId must be part of the hash signed by the account owner

bytes32 constant ENABLE_SESSION_TYPEHASH = keccak256(
    "EnableSession(bytes32 permissionId,bytes32 sessionHash,bytes32 userOpHash)"
);

function getAndVerifyDigest(
    PermissionId permId,
    bytes32 userOpHash,
    SmartSessionMode mode,
    Session memory session,
    bytes calldata enableSessionSig
) internal view returns (address signer) {
    bytes32 digest = _hashTypedData(keccak256(abi.encode(
        ENABLE_SESSION_TYPEHASH,
        PermissionId.unwrap(permId),       // ← now signed
        keccak256(abi.encode(session)),
        userOpHash
    )));
    signer = ECDSA.recover(digest, enableSessionSig);
    require(signer == ISmartAccount(msg.sender).owner(), "InvalidSigner");
}
```

**Fix 5: Consume session after successful validation**
```solidity
// ✅ SECURE: Invalidate / consume session to prevent replay

function validateUserOp(
    PackedUserOperation calldata userOp,
    bytes32 userOpHash
) external override returns (uint256) {
    ResourceLockSessionData memory session = _decodeSession(userOp);
    _validateSession(session, userOp); // validates constraints

    // Consume: increment nonce or mark session as spent
    _usedSessions[keccak256(abi.encode(session, msg.sender))] = true; // ← mark used
    // OR: session.nonce++ (if session has sequence counter)

    return VALIDATION_SUCCESS;
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- IERC20.approve.selector check that returns true without checking decoded spender address
- sessionData[sessionKeySigner][msg.sender] lookup without verifying key ownership by msg.sender
- keccak256 storage key derivation with abi.encodePacked(..., PREFIX, id) where id is uint256 counter
- permissionId / permId decoded from userOp.signature (not userOpHash) fed into a hash without being signed
- validateUserOp returning VALIDATION_SUCCESS without consuming / marking the session
- nativeTokenLimit or spendLimit checks inside conditional branches that can be bypassed
- _validateSessionKeyParams without explicit target/selector/spender allowlist enforcement
```

#### Audit Checklist
- [ ] Does each session key's validation explicitly check the spender address in `approve` calls?
- [ ] Is the session key bound to a specific wallet — can't a different wallet's user consume this key?
- [ ] Is the storage key for `SessionKeyData` derived using the full, untruncated session key ID?
- [ ] Is `permissionId` included in the signed digest (not just parsed from unsigned `userOp.signature`)?
- [ ] Is the session consumed / nonce incremented after a single use (for one-time sessions)?
- [ ] Does the spend limit module cover ALL execution paths including batch and delegatecall?
- [ ] Are all session constraints (target, selector, value, token, amount) verified against actual calldata?

### Real-World Examples

#### Known Issues from Audit Reports
- **Etherspot GasTankPaymasterModule (Shieldify)** — Session key can approve arbitrary spender and drain wallet [SK-1] — CRITICAL
- **Etherspot CredibleAccountModule Mitigation (Shieldify)** — Session key consumed by unauthorized SCW [SK-2] — HIGH
- **Etherspot CredibleAccountModule (Shieldify)** — Session key owner impersonates another key for same wallet [SK-3] — HIGH
- **Alchemy Modular Account (Quantstamp)** — Session keys overwrite each other's permissions via storage collision [SK-4] — HIGH
- **Rhinestone SmartSessions (Cantina)** — Enable mode frontrun swaps permissionId [SK-5] — HIGH
- **Alchemy Modular Account V2 (Quantstamp)** — NativeTokenLimitModule spend limit bypass [SK-6] — HIGH
- **Custom smart wallet (Sherlock)** — Insufficient signature validation allows arbitrary transactions [SK-7] — HIGH
- **Etherspot ResourceLockValidator (Shieldify)** — Session not consumed after use [SK-8] — CRITICAL
- **Etherspot ResourceLockValidator (Shieldify)** — Insufficient field validation in `validateUserOp` [SK-9] — CRITICAL

### Prevention Guidelines

#### Development Best Practices
1. **Validate EVERY field in calldata against session constraints** — target, selector, spender, amount, token. Session key validation is only secure if it's exhaustive.
2. **Bind session keys to specific wallets** — use `registeredBy` or a wallet-keyed mapping for all session key lookups.
3. **Test storage key derivation with many keys** — create 5+ session keys and verify each has a separate storage slot with distinct data.
4. **Include `permissionId` in the enabled session signature** — any parameter that affects session scope must be in the EIP-712 struct.
5. **Mark sessions consumed after first use** (for single-use sessions) — use a `usedNonces` bitmap or mapping.
6. **Cover all execution paths in spend limit checks** — batch, single, delegate, try-catch; ensure limits apply to every variant.

#### Testing Requirements
- Unit test: session key calls `approve(attacker, MAX)` → must revert
- Unit test: wallet B tries to consume a session key registered by wallet A → must revert
- Unit test: create 10 session keys, verify each has independent permissions
- Unit test: enable mode with frontrunned `permissionId` → must revert
- Unit test: replay the same session key in two sequential userOps → second must fail
- Fuzz: vary calldata in `_validateSessionKeyParams` with random target/selector/amount combinations

### Keywords for Search

`session key drain`, `session key approve bypass`, `session key cross-wallet`, `session key unauthorized consumption`, `SessionKeyData storage collision`, `session key id truncation`, `permissionId frontrun`, `permissionId unsigned`, `enable mode frontrun`, `NativeTokenLimitModule bypass`, `spend limit bypass`, `session not consumed`, `ResourceLockValidator`, `CredibleAccountModule`, `SmartSession`, `_validateSessionKeyParams`, `session key permission overwrite`, `session key impersonation`, `session key replay`, `ERC-7579 session`, `ERC-4337 session key`, `smart wallet session abuse`, `sessionData mapping collision`

### Related Vulnerabilities

- `DB/account-abstraction/aa-signature-replay-attacks.md` — cross-chain and enable mode replay
- `DB/account-abstraction/aa-erc7579-module-system-enable-mode.md` — enable mode module type confusion
- `DB/account-abstraction/aa-paymaster-gas-accounting-vulnerabilities.md` — paymaster approval drain
- `DB/general/access-control/` — missing authorization checks

---
