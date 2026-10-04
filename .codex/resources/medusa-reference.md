# Medusa Fuzzer Reference

## Contents
- [Cheatcode interface](#cheatcode-interface)
- [Supported cheatcodes](#supported-cheatcodes)
- [Input bounding utilities](#input-bounding-utilities)
- [Property test conventions](#property-test-conventions)
- [Assertion vs property testing](#assertion-vs-property-testing)
- [medusa.json template](#medusajson-template)
- [Configuration recipes](#configuration-recipes)
- [Console logging](#console-logging)
- [Compilation platform notes](#compilation-platform-notes)

---

## Cheatcode Interface

The cheatcode contract is deployed at `0x7109709ECfa91a80626fF3989D68f67F5b1DD12D`. If using Foundry as compilation platform, `forge-std` provides this via `Vm`. Otherwise, declare the interface inline:

```solidity
interface IHevm {
    function warp(uint256) external;
    function roll(uint256) external;
    function fee(uint256) external;
    function prevrandao(bytes32) external;
    function chainId(uint256) external;
    function coinbase(address) external;
    function load(address, bytes32) external returns (bytes32);
    function store(address, bytes32, bytes32) external;
    function prank(address) external;
    function startPrank(address) external;
    function stopPrank() external;
    function prankHere(address) external;
    function deal(address, uint256) external;
    function etch(address, bytes calldata) external;
    function label(address, string calldata) external;
    function sign(uint256, bytes32) external returns (uint8, bytes32, bytes32);
    function addr(uint256) external returns (address);
    function getCode(string calldata) external returns (bytes memory);
    function getNonce(address) external returns (uint64);
    function setNonce(address, uint64) external;
    function ffi(string[] calldata) external returns (bytes memory);
    function snapshot() external returns (uint256);
    function revertTo(uint256) external returns (bool);
    function toString(address) external returns (string memory);
    function toString(uint256) external returns (string memory);
    function toString(int256) external returns (string memory);
    function toString(bool) external returns (string memory);
    function toString(bytes calldata) external returns (string memory);
    function toString(bytes32) external returns (string memory);
    function parseBytes(string memory) external returns (bytes memory);
    function parseBytes32(string memory) external returns (bytes32);
    function parseAddress(string memory) external returns (address);
    function parseUint(string memory) external returns (uint256);
    function parseInt(string memory) external returns (int256);
    function parseBool(string memory) external returns (bool);
}
```

**Important**: `prankHere(address)` sets `msg.sender` for the remainder of the current call frame only (NOT a Foundry cheatcode — Medusa-specific).

---

## Supported Cheatcodes

| Cheatcode | Purpose | Notes |
|-----------|---------|-------|
| `warp(uint256)` | Set `block.timestamp` | Use for time-dependent invariants |
| `roll(uint256)` | Set `block.number` | Use for block-dependent logic |
| `fee(uint256)` | Set `block.basefee` | |
| `prevrandao(bytes32)` | Set `block.prevrandao` | |
| `chainId(uint256)` | Set `block.chainid` | |
| `coinbase(address)` | Set `block.coinbase` | |
| `load(address, bytes32)` | Read storage slot | Useful for verifying packed storage |
| `store(address, bytes32, bytes32)` | Write storage slot | Setup only — never to fabricate invalid states |
| `prank(address)` | Set next call's `msg.sender` | Single-call override |
| `startPrank(address)` | Set `msg.sender` until `stopPrank()` | Multi-call override |
| `stopPrank()` | Clear prank | |
| `prankHere(address)` | Set `msg.sender` for current frame | Medusa-specific |
| `deal(address, uint256)` | Set ETH balance | For test setup — realistic amounts only |
| `etch(address, bytes)` | Set contract code | Setup only |
| `snapshot()` / `revertTo(uint256)` | EVM state snapshots | Useful for before/after comparisons |
| `getNonce(address)` / `setNonce(address, uint64)` | Nonce management | New nonce must be ≥ current |
| `ffi(string[])` | Execute shell command | Disabled by default (`enableFFI: false`) |

---

## Input Bounding Utilities

Include these helpers directly in the harness contract. Do NOT import from external libraries — this eliminates dependency-related compilation failures:

```solidity
// Clamp value to [low, high]
function clampBetween(uint256 value, uint256 low, uint256 high) internal pure returns (uint256) {
    if (value < low || value > high) {
        return low + (value % (high - low + 1));
    }
    return value;
}

// Clamp value to [0, upper]
function clampLte(uint256 value, uint256 upper) internal pure returns (uint256) {
    if (value > upper) {
        return value % (upper + 1);
    }
    return value;
}

// Clamp value to [lower, type(uint256).max]
function clampGte(uint256 value, uint256 lower) internal pure returns (uint256) {
    if (value < lower) {
        return lower;
    }
    return value;
}

// Clamp to strictly less than upper
function clampLt(uint256 value, uint256 upper) internal pure returns (uint256) {
    if (upper == 0) return 0;
    if (value >= upper) {
        return value % upper;
    }
    return value;
}

// Clamp to strictly greater than lower
function clampGt(uint256 value, uint256 lower) internal pure returns (uint256) {
    if (value <= lower) {
        return lower + 1;
    }
    return value;
}
```

### Bounding Strategy

| Input Type | Recommended Bound | Rationale |
|-----------|-------------------|-----------|
| Token amounts | `clampBetween(x, 1, type(uint128).max)` | Avoids zero (often trivial) and extreme overflow territory |
| Array indices | `clampLt(x, array.length)` | Prevents OOB |
| Percentages (BPS) | `clampBetween(x, 0, 10_000)` | Valid basis point range |
| Timestamps | Let Medusa's `blockTimestampDelayMax` handle | Fuzzer jumps time automatically |
| Addresses | Use `senderAddresses` from config | Default: `0x10000`, `0x20000`, `0x30000` |
| ETH values | `clampBetween(x, 0, address(this).balance)` | Cannot send more than available |

---

## Property Test Conventions

### Naming

- **Prefix**: `property_` (default, configured via `testing.propertyTesting.testPrefixes`)
- **Format**: `property_{what}_{condition}` — descriptive, no abbreviations
- **Examples**:
  - `property_totalSupply_equals_sum_of_balances()`
  - `property_share_price_never_decreases()`
  - `property_only_owner_can_pause()`

### Signature Rules

1. **System-level properties**: `function property_X() public view` — no parameters, queries contract state, called after every transaction in the sequence
2. **Function-level properties**: `function property_X(uint256 a, uint256 b) public` — fuzzed parameters, calls target contracts, asserts post-conditions
3. **Visibility**: Must be `public` or `external`
4. **Return type**: `void` — no return value
5. **Success**: Function completes without reverting = property HOLDS
6. **Failure**: `assert(false)` or any revert inside the function = property VIOLATED — medusa reports failing sequence

### Critical Rule

**`assert()` for invariant checks, NEVER `require()` or `revert()`.**

`require()` causes the transaction to revert, which Medusa treats as "call didn't execute" — it does NOT flag it as a failing property. Only `assert()` failures (panic code `0x01`) are caught by property testing.

---

## Assertion vs Property Testing

Medusa supports two invariant testing modes simultaneously:

| Feature | Property Testing | Assertion Testing |
|---------|-----------------|-------------------|
| Function prefix | `property_` | Any function |
| Trigger | Called by fuzzer after each tx | Triggered when `assert()` fails in any call |
| Input source | Fuzzer generates inputs | Fuzzer generates inputs for all functions |
| Use case | System-wide invariants | Per-function correctness |
| Config | `propertyTesting.enabled` | `assertionTesting.enabled` |

**When to use which**:
- **Property tests**: Global state invariants (solvency, supply conservation, monotonicity)
- **Assertion tests**: Pre/post condition checks within functions the fuzzer calls directly

Both are enabled by default. Both can coexist in the same harness.

---

## medusa.json Template

```json
{
  "fuzzing": {
    "workers": 10,
    "workerResetLimit": 50,
    "timeout": 0,
    "testLimit": 0,
    "shrinkLimit": 5000,
    "callSequenceLength": 100,
    "pruneFrequency": 5,
    "corpusDirectory": "corpus",
    "coverageEnabled": true,
    "coverageFormats": ["html", "lcov"],
    "revertReporterEnabled": false,
    "targetContracts": ["REPLACE_WITH_HARNESS_NAME"],
    "predeployedContracts": {},
    "targetContractsBalances": [],
    "constructorArgs": {},
    "deployerAddress": "0x30000",
    "senderAddresses": ["0x10000", "0x20000", "0x30000"],
    "blockNumberDelayMax": 60480,
    "blockTimestampDelayMax": 604800,
    "transactionGasLimit": 12500000,
    "testing": {
      "stopOnFailedTest": true,
      "stopOnFailedContractMatching": false,
      "stopOnNoTests": true,
      "testAllContracts": false,
      "testViewMethods": true,
      "verbosity": 1,
      "targetFunctionSignatures": [],
      "excludeFunctionSignatures": [],
      "assertionTesting": {
        "enabled": true,
        "panicCodeConfig": {
          "failOnCompilerInsertedPanic": false,
          "failOnAssertion": true,
          "failOnArithmeticUnderflow": false,
          "failOnDivideByZero": false,
          "failOnEnumTypeConversionOutOfBounds": false,
          "failOnIncorrectStorageAccess": false,
          "failOnPopEmptyArray": false,
          "failOnOutOfBoundsArrayAccess": false,
          "failOnAllocateTooMuchMemory": false,
          "failOnCallUninitializedVariable": false
        }
      },
      "propertyTesting": {
        "enabled": true,
        "testPrefixes": ["property_"]
      },
      "optimizationTesting": {
        "enabled": true,
        "testPrefixes": ["optimize_"]
      }
    },
    "chainConfig": {
      "codeSizeCheckDisabled": true,
      "cheatCodes": {
        "cheatCodesEnabled": true,
        "enableFFI": false
      },
      "skipAccountChecks": true,
      "forkConfig": {
        "forkModeEnabled": false,
        "rpcUrl": "",
        "rpcBlock": 1,
        "poolSize": 20
      }
    }
  },
  "compilation": {
    "platform": "crytic-compile",
    "platformConfig": {
      "target": ".",
      "solcVersion": "",
      "exportDirectory": "",
      "args": []
    }
  },
  "slither": {
    "useSlither": true,
    "cachePath": "slither_results.json",
    "args": []
  },
  "logging": {
    "level": "info",
    "logDirectory": "",
    "noColor": false
  }
}
```

### Fields to Customize Per Project

| Field | What to Set | Example |
|-------|-------------|---------|
| `targetContracts` | Array of harness contract names | `["InvariantHarness"]` |
| `targetContractsBalances` | Starting ETH if constructor is `payable` | `["100e18"]` |
| `constructorArgs` | Constructor parameters keyed by contract name | See Medusa docs |
| `testLimit` | Transactions before stopping (0 = infinite) | `100_000` for dev, `0` for CI |
| `callSequenceLength` | Tx per sequence before state reset | `100` for protocol, `1` for pure math |
| `corpusDirectory` | Where to persist coverage corpus | `"corpus"` |
| `senderAddresses` | Actor addresses the fuzzer uses | Add more for multi-role protocols |
| `testViewMethods` | Whether to fuzz `view`/`pure` functions | `true` — required for system-level property tests |

---

## Configuration Recipes

### Arithmetic Library Testing
```json
"callSequenceLength": 1,
"testLimit": 100000,
"targetContractsBalances": []
```
State resets after every call — isolates pure function testing.

### Multi-Step Protocol (DeFi)
```json
"callSequenceLength": 100,
"testLimit": 0,
"timeout": 3600,
"senderAddresses": ["0x10000", "0x20000", "0x30000", "0x40000", "0x50000"]
```
Long sequences allow complex interaction patterns. More senders model more actors.

### Fork Mode (Mainnet State)
```json
"chainConfig": {
  "forkConfig": {
    "forkModeEnabled": true,
    "rpcUrl": "https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY",
    "rpcBlock": 19000000,
    "poolSize": 20
  }
}
```

### Strict Panic Detection
```json
"assertionTesting": {
  "enabled": true,
  "panicCodeConfig": {
    "failOnAssertion": true,
    "failOnArithmeticUnderflow": true,
    "failOnDivideByZero": true,
    "failOnOutOfBoundsArrayAccess": true
  }
}
```
Catches compiler-level panics as test failures — use for arithmetic invariants.

---

## Console Logging

Medusa supports Foundry's `console.sol` library. Use `%v` as the recommended format specifier (works for all types).

```solidity
import "forge-std/console.sol";

// During development only — remove before finalizing
console.log("Balance: %v", balance);
```

**Rule**: No `console.log` in the final harness. Logs consume gas and obscure output. Use only during the compile-fix-debug cycle, then delete.

---

## Compilation Platform Notes

### Foundry (Recommended)
- Set `compilation.platform` to `"crytic-compile"` with `target: "."`
- Medusa uses `crytic-compile` which auto-detects Foundry projects
- Run `forge build` first to verify compilation before running `medusa fuzz`
- `forge-std` provides `Vm` interface, `console.sol`, and test utilities

### Hardhat
- Set `compilation.platform` to `"crytic-compile"` with `target: "."`
- `crytic-compile` auto-detects Hardhat projects
- Install `@crytic/properties` for standard property helpers

### Solc Direct
- Set `compilation.platformConfig.solcVersion` to a specific version
- Less common — use only when no framework is available
