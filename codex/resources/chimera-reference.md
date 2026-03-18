<!-- AUTO-GENERATED from `.claude/resources/chimera-reference.md`; source_sha256=ef6a70631018f6484e85781597c0e217944f2d5734e23f3cd8944aa537fcb068 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/chimera-reference.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Chimera Framework Reference

Chimera is a "write once, run everywhere" smart contract property-testing framework.
Install: `forge install Recon-Fuzz/chimera --no-commit`
Repo: https://github.com/Recon-Fuzz/chimera

## Class Hierarchy

```
BaseSetup                        ← abstract; setup() virtual
  └── BaseProperties             ← abstract; inherits BaseSetup
        └── BaseTargetFunctions  ← abstract; inherits BaseProperties + Asserts (abstract)
              └── TargetFunctions  (user-defined handlers)
                    ├── CryticTester   + CryticAsserts   → Echidna / Medusa
                    └── CryticToFoundry + FoundryAsserts → Foundry invariants / Halmos
```

## Assert Backends

| Contract | Target tool | Assertion mechanism | `between()` | `precondition()` |
|----------|------------|---------------------|-------------|-----------------|
| `CryticAsserts` | Echidna / Medusa | `assert(false)` + `emit Log` | modular clamp | `require(p)` |
| `FoundryAsserts` | Foundry / Halmos | `assertXxx` from forge-std | modular clamp | `vm.assume(p)` |
| `HalmosAsserts` | Halmos only | `assertXxx` from forge-std | `vm.assume(in range)` | `vm.assume(p)` |

`HalmosAsserts.between()` constrains the symbolic search space (does not wrap/clamp).

## Asserts API

```solidity
gt(uint256 a, uint256 b, string reason)   // a > b
gte(uint256 a, uint256 b, string reason)  // a >= b
lt(uint256 a, uint256 b, string reason)   // a < b
lte(uint256 a, uint256 b, string reason)  // a <= b
eq(uint256 a, uint256 b, string reason)   // a == b
t(bool b, string reason)                  // generic boolean assertion

between(uint256 value, uint256 low, uint256 high) returns (uint256)
between(int256 value, int256 low, int256 high) returns (int256)

precondition(bool p)  // skip invalid states
```

## recon-utils Managers

Install: `forge install Recon-Fuzz/recon-utils --no-commit`

### ActorManager
```solidity
_addActor(address actor)         // add actor to pool
_getActor() returns (address)    // get currently active actor
_getActors() returns (address[]) // get all actors
_switchActor(uint256 index)      // switch active actor (call this from ManagersTargets)
```

### AssetManager
```solidity
_newAsset(uint8 decimals)           // deploy new mock ERC20
_switchAsset(uint256 index)         // switch active asset
_finalizeAssetDeployment(
  address[] actors,
  address[] approvalTargets,
  uint256 maxAmount
)                                   // mint to all actors + approve all targets
```

### Utils (error matching)
```solidity
checkError(bytes memory err, string memory reason) returns (bool)
checkError(bytes memory err, bytes4 selector) returns (bool)
// Panic codes available via Panic library:
//   Panic.arithmeticPanic  → bytes4(0x4e487b71) with code 0x11
```

## Hevm Cheatcodes

Import: `import {vm} from "@chimera/Hevm.sol";`

Only use HEVM-supported cheatcodes — NOT Foundry-specific cheatcodes.

```solidity
vm.warp(uint256 timestamp)
vm.roll(uint256 blockNumber)
vm.deal(address user, uint256 amount)
vm.prank(address sender)
vm.startPrank(address sender)   // NOT supported by Echidna — use in Foundry/Medusa only
vm.stopPrank()
vm.assume(bool condition)
vm.load(address, bytes32) returns (bytes32)
vm.store(address, bytes32, bytes32)
vm.label(address, string)
vm.etch(address, bytes)         // NOT supported by Echidna — Medusa/Foundry only
```

## Remappings

```toml
# foundry.toml or remappings.txt
@chimera/=lib/chimera/src/
@recon/=lib/recon-utils/src/
```

## Compatibility Matrix

| Feature | Echidna | Medusa | Foundry | Halmos |
|---------|---------|--------|---------|--------|
| `startPrank` / `stopPrank` | ✗ | ✓ | ✓ | ✓ |
| `etch` | ✗ | ✓ | ✓ | ✓ |
| `between()` clamp | ✓ | ✓ | ✓ | `vm.assume` |
| `precondition()` | `require` | `require` | `vm.assume` | `vm.assume` |
| Property prefix | `echidna_`/`invariant_` | `invariant_` | `invariant_` | `check_` |
| Fork mode | ✗ | ✓ | ✓ | partial |

## File Layout Convention

```
test/recon/
  Setup.sol             — deploy contracts; ActorManager; AssetManager; prank modifiers
  BeforeAfter.sol       — Vars struct + __before() / __after() + updateGhosts modifier
  Properties.sol        — invariant_* public functions
  targets/
    AdminTargets.sol    — privileged function wrappers (asAdmin)
    DoomsdayTargets.sol — extreme state drivers (warp, roll, max drain)
    ManagersTargets.sol — _switchActor / _switchAsset
  TargetFunctions.sol   — aggregates targets; per-function handlers with try/catch
  CryticTester.sol      — Echidna + Medusa entry (CryticAsserts)
  CryticToFoundry.sol   — Foundry + Halmos entry (FoundryAsserts)
```

## updateGhosts Pattern

```solidity
modifier updateGhosts {
    __before();
    _;
    __after();
}

// Apply to every handler that tests a transition invariant:
function protocol_deposit(uint256 amount) public updateGhosts asActor {
    ...
}
```

## Handler Template

```solidity
function contract_functionName(uint256 param) public updateGhosts asActor {
    // 1. Clamp inputs
    param = between(param, 1, type(uint128).max);
    // 2. Skip invalid pre-states
    precondition(contract.someCondition());
    // 3. Call via try/catch
    try contract.functionName(param) {
        // 4. Inline transition assertions on success
        t(/* post-condition */, "reason");
    } catch (bytes memory err) {
        // 5. List expected reverts; fail on unexpected
        bool expected = checkError(err, "ExpectedRevert()") ||
                        checkError(err, Panic.arithmeticPanic);
        t(expected, "unexpected revert");
    }
}
```

## Run Commands

```bash
# Medusa
medusa fuzz

# Echidna
echidna . --contract CryticTester --config echidna.yaml --format text --workers 16

# Foundry invariant suite (1M runs)
FOUNDRY_PROFILE=invariants forge test --match-contract CryticToFoundry -vv --show-progress

# Debug a repro
forge test --match-contract CryticToFoundry --match-test test_crytic -vvv

# Halmos
halmos --contract CryticToFoundry --loop 3
```
