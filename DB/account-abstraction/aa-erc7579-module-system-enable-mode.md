---
# Core Classification
protocol: generic
chain: everychain
category: account_abstraction
vulnerability_type: module_system_misconfiguration

# Attack Vector Details
attack_type: logical_error
affected_component: module_installation

# Technical Primitives
primitives:
  - ERC-7579
  - ERC-7484
  - ERC-7739
  - withRegistry
  - enableMode
  - moduleType
  - _getEnableModeDataHash
  - _installFallbackHandler
  - onUninstall
  - postCheck
  - hook
  - validator
  - executor
  - fallback

# Impact Classification
severity: high
impact: unauthorized_module_installation
exploitability: 0.65
financial_impact: high

# Context Tags
tags:
  - account-abstraction
  - ERC-7579
  - ERC-7484
  - modular-account
  - module-installation
  - enable-mode
  - registry
  - hook
  - fallback
  - Biconomy
  - Nexus

language: solidity
version: ">=0.8.0"
---

## References

| Tag | Report Path |
|-----|-------------|
| [MOD-1] | `reports/account_abstraction_findings/erc-7484-registry-checks-missing-on-calls-to-modules.md` |
| [MOD-2] | `reports/account_abstraction_findings/installing-validators-with-enable-mode-in-validateuserop-doesnt-check-moduletype.md` |
| [MOD-3] | `reports/account_abstraction_findings/enable-mode-signature-ignores-module-type.md` |
| [MOD-4] | `reports/account_abstraction_findings/fallback-logic-prevents-hooks-postcheck-from-getting-executed.md` |
| [MOD-5] | `reports/account_abstraction_findings/missing-call-type-validation-in-_installfallbackhandler.md` |
| [MOD-6] | `reports/account_abstraction_findings/cannot-install-fallback-handler-for-empty-calldata.md` |
| [MOD-7] | `reports/account_abstraction_findings/cannot-install-fallback-handler-for-nft-token-callbacks.md` |
| [MOD-8] | `reports/account_abstraction_findings/module-can-prevent-itself-from-uninstalling.md` |
| [MOD-9] | `reports/account_abstraction_findings/timelock-on-emergencyuninstallhook-can-be-bypassed.md` |
| [MOD-10] | `reports/account_abstraction_findings/uninstalling-the-fallback-submodule-of-smartsession-will-break-the-whole-validat.md` |
| [MOD-11] | `reports/account_abstraction_findings/setting-the-erc-7484-registry-may-put-modules-in-a-insecure-state.md` |
| [MOD-12] | `reports/account_abstraction_findings/registryfactoryaddattester-allows-duplicate-and-unsorted-attesters-breaking-erc-.md` |
| [MOD-13] | `reports/account_abstraction_findings/incorrect-check-in-_enablemode-prevents-installing-module-types-other-than-valid.md` |
| [MOD-14] | `reports/account_abstraction_findings/modules-other-than-validators-cannot-be-installed-in-enable-mode.md` |
| [MOD-15] | `reports/account_abstraction_findings/in-nexuscheckerc7739support-only-the-last-validator-is-checked-to-determine-if-t.md` |
| [MOD-16] | `reports/account_abstraction_findings/fallback-can-be-used-for-direct-unauthorised-calls-to-fallback-handlers.md` |
| [MOD-17] | `reports/account_abstraction_findings/m-02-the-prepostcheck-is-not-checking-the-hook-initialization-of-the-sender.md` |

## Vulnerability Title

**ERC-7579 Module System Vulnerabilities — Registry Bypass, moduleType Confusion, Hook PostCheck Skip, and Fallback Logic Flaws**

### Overview

ERC-7579 modular smart accounts (e.g., Biconomy Nexus) expose a rich surface of bugs in the module lifecycle: the ERC-7484 security registry is not consistently applied at call-time (only at install), `moduleType` is not committed to in the enable-mode signature hash, fallback execution paths skip hook `postCheck`, and re-entrancy in `onUninstall` hooks can permanently lock modules in place.

### ERC-7579 Module System — Registry Bypass, moduleType Confusion, Hook PostCheck Skip, Fallback Flaws

#### Root Cause

ERC-7579 module management has multiple independent failure modes:

1. **ERC-7484 registry not checked at call-time** — The `withRegistry` modifier is only applied during module installation. At execution time (when a validator signs a userOp, a hook's `preCheck` runs, or a fallback handler processes a call), the registry attestation is never re-verified. A module that loses its attestation after install can still execute indefinitely.

2. **`moduleType` absent from `_getEnableModeDataHash`** — Enable mode allows installing a module during `validateUserOp`. The owner signs a hash committing to `(module, initData)` but NOT to `moduleType`. An attacker can re-use the signature to install the same module as a different type (e.g., executor instead of validator), escalating its privileges.

3. **Fallback path skips hook `postCheck`** — When the fallback handler is invoked and the execution itself triggers an additional fallback (nested), the outer hook's `postCheck()` call is unreachable or skipped, breaking the hook invariant.

4. **Module can block its own uninstall** — `onUninstall` is a hook called on the module being uninstalled. A malicious or buggy module can revert in `onUninstall`, preventing removal. Combined with missing emergency paths, this permanently locks the module.

5. **Emergency uninstall timelock bypassed** — The `emergencyUninstallHook` path intended to force-remove stuck hooks can be called with crafted parameters that skip the timelock.

6. **ERC-7739 verifying contract check only on last validator** — `INexus.checkERC7739Support` iterates over installed validators but only calls `checkNestingERC7739Support` on the last one; if earlier validators do not support ERC-7739, the check falsely passes.

#### Attack Scenario

**Scenario A — Registry bypass via compromised module [MOD-1]:**
1. Attacker submits a malicious module that passes ERC-7484 attestation checks at install time.
2. Registry revokes the module's attestation after it's installed (e.g., a security team flags it).
3. Because `withRegistry` is not called during `validateUserOp` or fallback execution, the module continues operating.
4. The malicious module can sign arbitrary userOps or manipulate all calls through the account.

**Scenario B — moduleType confusion via enable mode [MOD-2] & [MOD-3]:**
1. Account owner signs an enable-mode approval for module M as `MODULE_TYPE_VALIDATOR`.
2. Attacker intercepts and re-submits the same `enableModeSignature` but with `moduleType = MODULE_TYPE_EXECUTOR`.
3. `_getEnableModeDataHash` does not include `moduleType` → hash is unchanged → signature verifies.
4. Module M is installed as an executor with `onlyExecutorModule` access → can call `executeFromExecutor` on behalf of the account.

**Scenario C — Hook postCheck skipped in fallback [MOD-4]:**
1. A hook's `preCheck` executes and records state (e.g., balance snapshot, invariant check).
2. The fallback execution path encounters a condition that bypasses the `postCheck` call.
3. The hook's post-execution invariant is never verified, allowing balance drains or state corruption to slip through.

**Scenario D — Module griefs uninstall process [MOD-8]:**
1. Attacker or buggy module reverts at `onUninstall(address, bytes)`.
2. Account owner cannot remove the module through the normal uninstall path.
3. The module persists indefinitely, continuing to intercept validation or execution.

**Scenario E — Attester deduplication breaks ERC-7484 threshold [MOD-12]:**
1. Registry is deployed with 3 required attesters.
2. `addAttester` is called with the same address twice — duplicates not rejected.
3. Effective unique attesters < 3 → security threshold becomes unachievable or trivially bypassable.

#### Vulnerable Pattern Examples

**Example 1: withRegistry not applied at execution time** [HIGH] — Source: [MOD-1]
```solidity
// ❌ VULNERABLE: withRegistry only on install and executeFromExecutor,
// NOT on validateUserOp, fallback handling, or preCheck/postCheck invocation

// Install path: ✓ registry enforced
function installModule(uint256 moduleType, address module, bytes calldata initData)
    external onlyEntryPointOrSelf withRegistry(module, moduleType) { ... }

// Execute path: ✓ registry checked
function executeFromExecutor(...)
    external payable onlyExecutorModule withRegistry(msg.sender, MODULE_TYPE_EXECUTOR) { ... }

// Validation path: ✗ NO registry check
function validateUserOp(PackedUserOperation calldata userOp, bytes32 userOpHash, ...)
    external onlyEntryPoint returns (uint256) {
    address validator = _resolveValidator(userOp.nonce);
    // ← validator could have lost attestation; no re-check
    return IValidator(validator).validateUserOp(userOp, userOpHash);
}

// Fallback path: ✗ NO registry check
function _handleFallback(address handler, bytes calldata callData)
    internal returns (bytes memory) {
    // ← handler could be deattested; no re-check
    return IFallback(handler).handle(address(this), msg.value, callData);
}
```

**Example 2: moduleType not in enable mode hash** [HIGH] — Source: [MOD-2] & [MOD-3]
```solidity
// ❌ VULNERABLE: Hash commits to module+initData only; moduleType is attacker-controlled

function _getEnableModeDataHash(
    address module,
    bytes calldata initData
) internal view returns (bytes32) {
    return _hashTypedData(keccak256(abi.encode(
        MODULE_ENABLE_MODE_TYPE_HASH,
        module,
        keccak256(initData)
        // ← moduleType missing — attacker can change it freely
    )));
}

// During enable mode processing:
function _enableMode(bytes32 /* userOpHash */, bytes calldata modeData) internal {
    (uint256 moduleType, address module, bytes calldata initData, bytes calldata sig) =
        modeData.decodeEnableModeData();

    // Hash does not include moduleType → sig valid for any moduleType
    require(
        isValidSignatureWithSender(address(0), _getEnableModeDataHash(module, initData), sig)
            == EIP1271_SUCCESS, "bad sig"
    );
    _installModule(moduleType, module, initData); // ← moduleType unchecked
}
```

**Example 3: Fallback path skips hook postCheck** [HIGH] — Source: [MOD-4]
```solidity
// ❌ VULNERABLE: postCheck not reached when nested fallback triggers

function _handleFallbackWithHook(address handler, bytes calldata data)
    external returns (bytes memory result)
{
    address hook = _getHook();
    bytes memory hookContext = IHook(hook).preCheck(msg.sender, msg.value, data);

    // Execute fallback handler
    result = IFallback(handler).handle(address(this), msg.value, data);

    // ← If handler itself calls back into this contract (nested fallback),
    //   execution may return here with a revert in a try/catch,
    //   and the catch branch does NOT call postCheck
    try IHook(hook).postCheck(hookContext) {} catch {
        revert PostCheckFailed(); // ← postCheck is called, but only in try branch
        // Nested reentrant path can bypass this entirely
    }
}
```

**Example 4: Module blocking its own uninstallation** [MEDIUM] — Source: [MOD-8]
```solidity
// ❌ VULNERABLE: No try/catch around onUninstall — malicious module can revert

function uninstallModule(uint256 moduleType, address module, bytes calldata deInitData)
    external onlyEntryPointOrSelf
{
    _moduleStorage[moduleType][module].installed = false;
    IModule(module).onUninstall(deInitData); // ← revert here blocks uninstall
    emit ModuleUninstalled(moduleType, module);
}
```

**Example 5: ERC-7739 only checks last validator** [MEDIUM] — Source: [MOD-15]
```solidity
// ❌ VULNERABLE: Only last element of validators array is checked for ERC-7739 support

function checkERC7739Support(...)
    external view returns (string memory)
{
    address[] memory validators = _getInstalledValidators();
    for (uint256 i; i < validators.length; i++) {
        try IValidator(validators[i]).checkNestingERC7739Support() returns (string memory) {
            // Overwrites result on every iteration — only last validator's result matters
            // Earlier validators lacking ERC-7739 support silently pass
        } catch { }
    }
}
```

**Example 6: Unauthorized direct calls to fallback handlers** [MEDIUM] — Source: [MOD-16]
```solidity
// ❌ VULNERABLE: Fallback handler can be called directly by anyone via the fallback function
// without going through the account's access control

fallback(bytes calldata data) external payable returns (bytes memory result) {
    bytes4 selector = bytes4(data[:4]);
    address handler = _fallbackHandlers[selector];
    require(handler != address(0), "no handler");
    // ← No check that msg.sender is authorized
    // Direct callers (not the account itself via executeFromExecutor) can reach modules
    (bool success, bytes memory ret) = handler.delegatecall(data);
    require(success);
    return ret;
}
```

### Impact Analysis

#### Technical Impact
- Deattested modules continue executing indefinitely after registry revocation (bypasses ERC-7484 security guarantee)
- `moduleType` confusion allows escalating a validator-level module to executor-level privileges
- Hook invariants unenforceable if `postCheck` is skippable
- Modules can permanently entrench themselves, making accounts unmanageable
- True attestation threshold unreachable if duplicates are allowed in attester list

#### Business Impact
- Critical trust failure: security registry becomes decorative
- Account fully compromised via malicious executor module installed with attacker-chosen type
- Governance of modular accounts undermined when key modules cannot be removed

#### Affected Scenarios
- Protocols relying on ERC-7484 registry for post-install security guarantees (3/17 reports)
- Enable-mode module installation in Biconomy Nexus (5/17 reports)
- Fallback hooks in any ERC-7579 account (3/17 reports)
- Module lifecycle (install/uninstall) management (4/17 reports)
- Edge cases in fallback handler routing (2/17 reports)

### Secure Implementation

**Fix 1: Apply withRegistry at call-time, not just at install-time**
```solidity
// ✅ SECURE: Re-verify attestation before delegating to validator / hook / fallback

modifier withRegistryAtRuntime(address module, uint256 moduleType) {
    _registry.check(module, moduleType); // revert if deattested
    _;
}

function validateUserOp(PackedUserOperation calldata userOp, bytes32 userOpHash, ...)
    external onlyEntryPoint withRegistryAtRuntime(_resolveValidator(userOp.nonce), MODULE_TYPE_VALIDATOR)
    returns (uint256) { ... }

function _handleFallback(address handler, bytes calldata callData)
    internal withRegistryAtRuntime(handler, MODULE_TYPE_FALLBACK)
    returns (bytes memory) { ... }
```

**Fix 2: Include `moduleType` in `_getEnableModeDataHash`**
```solidity
// ✅ SECURE: Commit to moduleType so the owner's approval is type-bound

bytes32 constant MODULE_ENABLE_MODE_TYPE_HASH = keccak256(
    "EnableMode(bytes32 userOpHash,address module,uint256 moduleType,bytes initData)"
);

function _getEnableModeDataHash(
    bytes32 userOpHash,
    address module,
    uint256 moduleType,      // ← new field
    bytes calldata initData
) internal view returns (bytes32) {
    return _hashTypedData(keccak256(abi.encode(
        MODULE_ENABLE_MODE_TYPE_HASH,
        userOpHash,
        module,
        moduleType,           // ← attacker cannot change
        keccak256(initData)
    )));
}
```

**Fix 3: Use try/catch around onUninstall to prevent griefing**
```solidity
// ✅ SECURE: Always remove internal bookkeeping; best-effort onUninstall call

function uninstallModule(uint256 moduleType, address module, bytes calldata deInitData)
    external onlyEntryPointOrSelf
{
    // Remove from storage FIRST (prevents re-entrancy reinstall)
    _moduleStorage[moduleType][module].installed = false;

    // Best-effort notification; module cannot block its own removal
    try IModule(module).onUninstall(deInitData) {} catch {}

    emit ModuleUninstalled(moduleType, module);
}
```

**Fix 4: Ensure postCheck is always called after hook-guarded execution**
```solidity
// ✅ SECURE: Use a try/finally equivalent (Solidity doesn't have finally,
// so structure to guarantee postCheck via explicit error propagation)

function _handleFallbackWithHook(address handler, bytes calldata data)
    external returns (bytes memory result)
{
    address hook = _getHook();
    bytes memory hookContext = IHook(hook).preCheck(msg.sender, msg.value, data);

    bool success;
    bytes memory ret;
    (success, ret) = handler.call{value: msg.value}(data);

    // Always call postCheck regardless of execution success
    IHook(hook).postCheck(hookContext); // ← unconditional

    if (!success) {
        assembly { revert(add(ret, 32), mload(ret)) }
    }
    return ret;
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- withRegistry modifier present on installModule but ABSENT on validateUserOp
- _getEnableModeDataHash(address module, bytes calldata initData) — only 2 params, no moduleType
- postCheck() inside try/catch where catch branch does NOT call postCheck
- IModule(module).onUninstall(deInitData) called directly without try/catch
- emergencyUninstallHook / emergency path that can be invoked before timelock expiry
- addAttester without deduplication check
- fallback() function that delegatecalls handlers without msg.sender authorization
- only last element of validators array checked for ERC-7739 support
```

#### Audit Checklist
- [ ] Does `withRegistry` apply to ALL execution-time module calls (validator, hook, executor, fallback)?
- [ ] Does `_getEnableModeDataHash` include `moduleType`?
- [ ] Is `postCheck` called unconditionally after every `preCheck`?
- [ ] Is `onUninstall` wrapped in a try/catch so modules cannot block removal?
- [ ] Does the emergency uninstall path enforce its timelock fully?
- [ ] Does `addAttester` reject duplicate addresses?
- [ ] Are fallback handlers protected from direct external calls?
- [ ] Does ERC-7739 support checking cover ALL installed validators?

### Real-World Examples

#### Known Issues from Audit Reports
- **Biconomy Nexus (Spearbit)** — ERC-7484 registry checks missing during execution [MOD-1] — HIGH
- **Biconomy Nexus (Codehawks/Cyfrin)** — `moduleType` not in enable mode hash [MOD-2] — HIGH
- **Biconomy Nexus (Spearbit)** — Enable mode signature ignores module type [MOD-3] — HIGH
- **Biconomy Nexus (Code4rena)** — Fallback prevents hooks `postCheck` execution [MOD-4] — HIGH
- **Biconomy Nexus (Code4rena)** — Module can prevent its own uninstall [MOD-8] — MEDIUM
- **Biconomy Nexus (Code4rena)** — Emergency uninstall timelock bypass [MOD-9] — MEDIUM
- **Biconomy Nexus (Code4rena)** — ERC-7739 only checks last validator [MOD-15] — MEDIUM
- **Biconomy Nexus (Code4rena)** — Unauthorized direct calls to fallback handlers [MOD-16] — MEDIUM
- **Biconomy Nexus (Code4rena)** — RegistryFactory allows duplicate attesters [MOD-12] — MEDIUM

### Prevention Guidelines

#### Development Best Practices
1. **Apply `withRegistry` at every module invocation point**, not just install — validator resolution in `validateUserOp`, hook invocation in fallback, executor calls in `executeFromExecutor`.
2. **Include `moduleType` in every hash that authorises module installation** — prevents type confusion in enable mode and any other installation path.
3. **Wrap `onUninstall` in try/catch** — modules must not have veto power over their own removal; security-critical invariants must be upheld even when modules misbehave.
4. **Write `postCheck` as guaranteed** — treat it like a `finally` block; any code path that calls `preCheck` must unconditionally call `postCheck`.
5. **Add access control to fallback routing** — only `self` (via `execute*` paths) should be able to reach fallback handlers; external direct calls must be rejected.
6. **Enforce attester deduplication in registry factory** — use a mapping or sorted array with duplicate check.

#### Testing Requirements
- Unit test: install module, revoke attestation, attempt `validateUserOp` → must revert
- Unit test: enable-mode install with changed `moduleType` → must revert
- Unit test: `preCheck` + execution that reverts → `postCheck` must still be called
- Unit test: malicious module that reverts in `onUninstall` → account owner can still remove
- Unit test: add same attester twice → must revert
- Unit test: direct external call to fallback → must revert

### Keywords for Search

`ERC-7579 module`, `ERC-7484 registry`, `withRegistry missing`, `module type confusion`, `enableMode moduleType`, `_getEnableModeDataHash`, `enable mode signature`, `postCheck skipped`, `hook postCheck`, `onUninstall revert`, `module griefing`, `fallback handler unauthorized`, `emergencyUninstallHook bypass`, `ERC-7739 support check`, `attester deduplication`, `modular account vulnerabilities`, `Biconomy Nexus`, `module lifecycle`, `validator delegation`, `executor escalation`, `install module hash`, `registry attestation bypass`, `smart account module security`

### Related Vulnerabilities

- `DB/account-abstraction/aa-signature-replay-attacks.md` — enable mode signature replay
- `DB/account-abstraction/aa-session-key-permission-abuse.md` — module-level permission abuse
- `DB/general/access-control/` — missing authorization checks
- `DB/general/reentrancy/` — reentrancy in module lifecycle hooks

---
