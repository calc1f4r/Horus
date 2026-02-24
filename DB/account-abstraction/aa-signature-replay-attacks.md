---
# Core Classification
protocol: generic
chain: everychain
category: signature
vulnerability_type: replay_attack

# Attack Vector Details
attack_type: signature_replay
affected_component: signature_validation

# Technical Primitives
primitives:
  - userOpHash
  - enableModeDataHash
  - entryPoint
  - nonce
  - chainId
  - EIP-712
  - ERC-4337
  - ERC-7579
  - validateUserOp
  - _getEnableModeDataHash

# Impact Classification
severity: high
impact: fund_loss
exploitability: 0.70
financial_impact: high

# Context Tags
tags:
  - account-abstraction
  - ERC-4337
  - ERC-7579
  - smart-wallet
  - signature
  - replay
  - cross-chain
  - enable-mode
  - bundler

language: solidity
version: ">=0.8.0"
---

## References

| Tag | Report Path |
|-----|-------------|
| [REPLAY-1] | `reports/account_abstraction_findings/entrypoint-not-included-in-user-operation-hash-for-validateuserop-allowing-signature-to-be-replayed-on-upgraded-entrypoint.md` |
| [REPLAY-2] | `reports/account_abstraction_findings/enable-mode-signature-can-be-replayed.md` |
| [REPLAY-3] | `reports/account_abstraction_findings/missing-nonce-in-_getenablemodedatahash-enables-replay-attacks-after-module-is-re-installed.md` |
| [REPLAY-4] | `reports/account_abstraction_findings/h-07-replay-attack-eip712-signed-transaction.md` |
| [REPLAY-5] | `reports/account_abstraction_findings/h-06-malicious-relayer-can-replay-execute-calldata-on-different-chains-using-the-same-signature.md` |
| [REPLAY-6] | `reports/account_abstraction_findings/replay-attacks-on-co-signer-signed-invocations.md` |
| [REPLAY-7] | `reports/account_abstraction_findings/operations-are-vulnerable-to-signature-replay-via-reentrancy.md` |
| [REPLAY-8] | `reports/account_abstraction_findings/m-03-cross-chain-signature-replay-attack.md` |
| [REPLAY-9] | `reports/account_abstraction_findings/verifier-signatures-can-be-replayed.md` |
| [REPLAY-10] | `reports/account_abstraction_findings/signature-is-replayable.md` |
| [REPLAY-11] | `reports/account_abstraction_findings/m-2-signatures-missing-some-parameters-allows-for-signature-replay-attack-on-different-chainid.md` |

## Vulnerability Title

**AA Signature Replay Attacks — Missing EntryPoint / Nonce / ChainId in UserOperation and Enable Mode Hashes**

### Overview

Account abstraction wallets (ERC-4337 / ERC-7579) that compute their own `userOp` signature hash instead of reusing the hash passed by the EntryPoint, or that produce inner hashes (e.g., `enableModeDataHash`) without binding them to the current nonce / `userOpHash` / `chainId`, are vulnerable to cross-EntryPoint replay, cross-chain replay, and cross-module-install replay attacks.

### AA Signature Replay — Missing Binding Fields in UserOperation and Enable Mode Hashes

#### Root Cause

This vulnerability exists because **inner EIP-712 hashes computed by the smart account omit one or more domain-binding fields** (`entryPoint` address, `nonce`, `chainId`, `userOpHash`) that would make the signature valid for exactly one operation. Without these anchors:

1. **Missing `entryPoint` in `getPackedUserOperationHash`** — The signed hash is identical across different deployed EntryPoint versions. When the protocol upgrades its EntryPoint, an attacker can re-submit old signed operations against the new EntryPoint.
2. **Missing `userOpHash` (or nonce) in `_getEnableModeDataHash`** — The hash that authorises module enablement is not tied to any specific userOp. A bundler can copy the `enableModeSignature` from one userOp and attach it to another, or replay it after the module is uninstalled and reinstalled (no nonce rotation).
3. **Missing `chainId` in cross-chain relayer payloads** — Signed calldata that does not include `chainId` can be submitted on any chain where the contract is deployed.
4. **Missing `chainId`/`nonce` in co-signer invocation hashes** — A co-signer approval can be re-submitted on another network or in a later transaction.
5. **Reentrancy-based replay** — State is not updated before external calls inside `validateUserOp`, allowing the same signature to pass validation twice in the same block.

#### Attack Scenario

**Scenario A — EntryPoint upgrade replay [REPLAY-1]:**
1. User signs a userOp against EntryPoint v0.6. The account computes its own hash, omitting the `entryPoint` address.
2. The protocol upgrades to EntryPoint v0.7.
3. Attacker re-submits the old signed operation to EntryPoint v0.7.
4. The signature is still valid (same hash), and the operation executes again.

**Scenario B — Enable mode bundler swap [REPLAY-2]:**
1. Alice signs a userOp that installs module A via enable-mode.
2. Bundler bundles Alice's `enableModeSignature` together with a *different* calldata that installs a malicious module B.
3. Because `_getEnableModeDataHash` only commits to `module+initData` (not to the outer `userOpHash`), the signature validates for the malicious installation.

**Scenario C — Module reinstall replay [REPLAY-3]:**
1. Alice installs module X with enable-mode signature S.
2. Alice later uninstalls module X.
3. Attacker replays signature S to reinstall module X without Alice's current approval.
4. Because `_getEnableModeDataHash` has no nonce, this succeeds.

**Scenario D — Cross-chain relayer replay [REPLAY-5]:**
1. User signs calldata for Ethereum.
2. Attacker submits same signature on Arbitrum / Optimism where the same contract is deployed.
3. `chainId` absent from signed payload → valid on every chain.

#### Vulnerable Pattern Examples

**Example 1: Missing entryPoint in UserOp hash** [HIGH] — Source: [REPLAY-1]
```solidity
// ❌ VULNERABLE: Computes its own userOp hash without entryPoint address
// An upgraded EntryPoint that calls this same account will still accept old signed ops

function validateUserOp(
    PackedUserOperation calldata _userOp,
    bytes32 /* _userOpHash — ignored! */,
    uint256 _missingAccountFunds
) external {
    // Uses internally computed hash, NOT the one passed by EntryPoint
    validationData_ = _validateUserOpSignature(
        _userOp,
        getPackedUserOperationTypedDataHash(_userOp) // ← ignores entryPoint
    );
}

function getPackedUserOperationHash(PackedUserOperation calldata _userOp)
    public pure returns (bytes32)
{
    return keccak256(abi.encode(
        PACKED_USER_OP_TYPEHASH,
        _userOp.sender,
        _userOp.nonce,
        keccak256(_userOp.initCode),
        keccak256(_userOp.callData),
        _userOp.accountGasLimits,
        _userOp.preVerificationGas,
        _userOp.gasFees,
        keccak256(_userOp.paymasterAndData)
        // ← NO entryPoint address → replayable on any EntryPoint
    ));
}
```

**Example 2: Enable mode hash missing userOpHash and nonce** [HIGH] — Source: [REPLAY-2] & [REPLAY-3]
```solidity
// ❌ VULNERABLE: enableModeDataHash does not commit to the outer userOpHash or a nonce
// Bundler can swap enable-mode data between ops; attacker can replay after module uninstall

function _getEnableModeDataHash(
    address module,
    bytes calldata initData
) internal view returns (bytes32) {
    return _hashTypedData(keccak256(abi.encode(
        MODULE_ENABLE_MODE_TYPE_HASH,
        module,
        keccak256(initData)
        // ← NO nonce, NO userOpHash, NO chainId
    )));
}

// Called during validateUserOp — the moduleType is attacker-controlled
function _enableMode(bytes32 userOpHash, bytes calldata modeInitData)
    internal returns (address, bytes calldata)
{
    (uint256 moduleType, address module, bytes calldata initData, bytes calldata sig) =
        modeInitData.decodeEnableModeData();
    require(
        isValidSignatureWithSender(address(0), _getEnableModeDataHash(module, initData), sig) ==
            EIP1271_SUCCESS,
        "InvalidEnableSig"
    );
    // moduleType is not part of the hash ← attacker picks any type
    _installModule(moduleType, module, initData);
}
```

**Example 3: Cross-chain relayer replay — missing chainId** [HIGH] — Source: [REPLAY-5]
```solidity
// ❌ VULNERABLE: Signed payload lacks chainId; replayable on any chain

function _hashExecution(
    address target,
    uint256 value,
    bytes calldata callData,
    uint256 nonce
) internal pure returns (bytes32) {
    return keccak256(abi.encodePacked(
        target,
        value,
        callData,
        nonce
        // ← NO block.chainid → same signature valid on ETH, ARB, OP, etc.
    ));
}
```

**Example 4: EIP-712 transaction without domain chainId** [HIGH] — Source: [REPLAY-4]
```solidity
// ❌ VULNERABLE: EIP-712 domain separator missing chainId field
bytes32 private constant DOMAIN_TYPEHASH =
    keccak256("EIP712Domain(string name,string version,address verifyingContract)");
    // ← chainId absent from domain → cross-chain replay

function _buildDomainSeparator() internal view returns (bytes32) {
    return keccak256(abi.encode(
        DOMAIN_TYPEHASH,
        keccak256(bytes(name)),
        keccak256(bytes(version)),
        address(this)
        // ← no block.chainid
    ));
}
```

**Example 5: Co-signer invocation replay — missing nonce & chainId** [HIGH] — Source: [REPLAY-6]
```solidity
// ❌ VULNERABLE: Co-signer signs only (target, value, calldata) without nonce or chainId

function _getCoSignerHash(
    address target,
    uint256 value,
    bytes calldata data
) internal pure returns (bytes32) {
    return keccak256(abi.encode(target, value, keccak256(data)));
    // ← no nonce (replay same op twice) and no chainId (replay cross-chain)
}
```

**Example 6: Reentrancy-based signature replay** [HIGH] — Source: [REPLAY-7]
```solidity
// ❌ VULNERABLE: External call made before nonce invalidation in validateUserOp
// Attacker's contract calls back into the account during validation, reusing same sig

function validateUserOp(
    UserOperation calldata userOp,
    bytes32 userOpHash,
    uint256 missingFunds
) external returns (uint256) {
    // External call BEFORE state update — reentrancy window
    if (missingFunds > 0) {
        payable(msg.sender).call{value: missingFunds}("");
    }
    _validateSignature(userOp, userOpHash); // ← nonce not yet invalidated
    _validateAndUpdateNonce(userOp);         // ← too late
    return 0;
}
```

### Impact Analysis

#### Technical Impact
- Attacker can re-execute previously authorised operations without the owner's current approval
- Module installation can be manipulated by the bundler (wrong module type, wrong module address)
- After module uninstall, attacker can reinstall the same module without new authorization
- Cross-chain replay allows draining wallets on every chain where the account is deployed

#### Business Impact
- Full wallet drain if replayed operation involves token transfers or approvals
- Silent installation of malicious modules giving attacker persistent execution access
- Loss of user trust in smart wallet security guarantees

#### Affected Scenarios
- Protocols that deploy to multiple chains with same bytecode (same address)
- Protocols that plan EntryPoint migrations (v0.6 → v0.7)
- Modular accounts using ERC-7579 enable-mode for module installation
- Any account with a custom userOp hash that bypasses the EntryPoint-supplied hash
- Frequency in reports: Cross-chain replay (5/11 reports), enable mode replay (3/11), reentrancy replay (1/11), co-signer (1/11), EIP-712 domain (1/11)

### Secure Implementation

**Fix 1: Use the EntryPoint-supplied userOpHash directly** — Source: [REPLAY-1]
```solidity
// ✅ SECURE: Use the userOpHash passed by EntryPoint — it already includes entryPoint address,
// chainId, nonce, and all UserOperation fields. Do NOT recompute.

function validateUserOp(
    PackedUserOperation calldata userOp,
    bytes32 userOpHash,    // ← use this directly
    uint256 missingFunds
) external onlyEntryPoint returns (uint256 validationData) {
    validationData = _validateSignature(userOp, userOpHash); // ← pass EntryPoint hash
    _payPrefund(missingFunds);
}
```

**Fix 2: Bind enableModeDataHash to the outer userOpHash**
```solidity
// ✅ SECURE: Include userOpHash (and optionally a nonce) in the enable mode data hash.
// EntryPoint's per-account nonce already prevents the outer userOp from replaying;
// binding enableModeDataHash to userOpHash prevents bundler swapping.

function _getEnableModeDataHash(
    bytes32 userOpHash,   // ← passed from validateUserOp
    address module,
    uint256 moduleType,   // ← must be committed to prevent type confusion
    bytes calldata initData
) internal view returns (bytes32) {
    return _hashTypedData(keccak256(abi.encode(
        MODULE_ENABLE_MODE_TYPE_HASH,
        userOpHash,        // ← binds to specific op
        module,
        moduleType,        // ← binds module type
        keccak256(initData)
    )));
}
```

**Fix 3: Include chainId and nonce in all signed cross-chain payloads**
```solidity
// ✅ SECURE: Full EIP-712 domain separator with chainId; include nonce in struct

bytes32 private constant DOMAIN_TYPEHASH = keccak256(
    "EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"
);

function _buildDomainSeparator() internal view returns (bytes32) {
    return keccak256(abi.encode(
        DOMAIN_TYPEHASH,
        keccak256(bytes(NAME)),
        keccak256(bytes(VERSION)),
        block.chainid,       // ← chain-specific
        address(this)
    ));
}

function _hashExecution(
    address target,
    uint256 value,
    bytes calldata callData,
    uint256 nonce           // ← one-time use
) internal view returns (bytes32) {
    return _hashTypedData(keccak256(abi.encode(
        EXECUTION_TYPEHASH,
        target,
        value,
        keccak256(callData),
        nonce,
        block.chainid   // ← explicit chain binding
    )));
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- getPackedUserOperationHash / getPackedUserOperationTypedDataHash not referencing block.chainid or entryPoint address
- _getEnableModeDataHash with only (module, initData) — no userOpHash, no nonce
- validateUserOp that ignores the _userOpHash parameter passed by EntryPoint
- keccak256(abi.encode(...)) inside signature validation that lacks chainId
- EIP712Domain without chainId field
- External calls (transfer, call) inside validateUserOp before nonce update
- abi.encodePacked(target, value, callData, nonce) without chainId
```

#### Audit Checklist
- [ ] Does `validateUserOp` use the `userOpHash` passed by EntryPoint, or does it recompute its own?
- [ ] Does every inner hash (`enableModeDataHash`, co-signer hash, relayer hash) include `chainId`?
- [ ] Does the enable-mode hash commit to `moduleType`, `userOpHash`, and a nonce?
- [ ] Are all EIP-712 domain separators constructed with `chainId`?
- [ ] Are nonces invalidated **before** any external calls inside validation?
- [ ] Are cross-chain contracts protected against same-signature replay on sibling deployments?

### Real-World Examples

#### Known Issues from Audit Reports
- **Metamask Smart Transactions (Cyfrin)** — Missing entryPoint in userOp hash; replayable on EntryPoint upgrade [REPLAY-1] — HIGH
- **Biconomy Nexus (Spearbit)** — enableModeSignature not tied to userOpHash; bundler can swap enable-mode data [REPLAY-2] — HIGH
- **Biconomy Nexus (Codehawks)** — Missing nonce in `_getEnableModeDataHash`; module reinstall replay [REPLAY-3] — HIGH
- **Cross-chain wallet (multiple)** — Missing chainId in signed execution payloads [REPLAY-5, REPLAY-8] — HIGH/MEDIUM
- **Co-signer wallet (Cyfrin)** — Missing nonce and chainId in co-signer invocation [REPLAY-6] — HIGH
- **Reentrancy replay (Sherlock)** — State update after external call in validateUserOp [REPLAY-7] — HIGH

### Prevention Guidelines

#### Development Best Practices
1. **Always use the `userOpHash` parameter passed by `validateUserOp`** — it is computed by EntryPoint and already binds `entryPoint`, `chainId`, `nonce`, and all UserOperation fields.
2. **Bind all inner hashes to `userOpHash`** — any hash signed during validation (enable mode, module config) must include `userOpHash` to prevent bundler manipulation.
3. **Commit to `moduleType` in every hash that authorises module installation** — prevents type-confusion installs.
4. **Include `block.chainid` in every EIP-712 domain separator** — prevents cross-chain replay.
5. **Invalidate nonces before external calls** — follow checks-effects-interactions in `validateUserOp`.
6. **Add a separate nonce for enable-mode signatures** — even when outer userOp nonce is invalidated, a dedicated enable-mode nonce prevents reinstall replay.

#### Testing Requirements
- Unit tests: replay same signed userOp after execution → must revert
- Unit tests: replay enable-mode signature after module uninstall → must revert
- Integration tests: submit same signed op to two different EntryPoint versions → must fail on second
- Fuzzing: vary `chainId` in domain separator, confirm signature invalidity

### Keywords for Search

`signature replay`, `userOp hash`, `entryPoint not included`, `getPackedUserOperationHash`, `enableModeDataHash`, `_getEnableModeDataHash`, `missing nonce`, `missing chainId`, `cross-chain replay`, `enable mode replay`, `ERC-4337 replay`, `ERC-7579 replay`, `validateUserOp signature`, `bundler replay`, `module reinstall replay`, `co-signer replay`, `EIP-712 domain chainId`, `reentrancy replay`, `inner hash binding`, `account abstraction signature`, `smart account replay`, `session hash reuse`

### Related Vulnerabilities

- `DB/general/signature/` — general EIP-712 signature vulnerabilities
- `DB/account-abstraction/aa-erc7579-module-system-enable-mode.md` — enable mode module type confusion
- `DB/account-abstraction/aa-session-key-permission-abuse.md` — session key cross-wallet replay

---
