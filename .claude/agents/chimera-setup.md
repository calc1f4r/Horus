---
name: chimera-setup
description: Scaffolds a complete Chimera-based property testing suite from an invariant-writer spec. Generates all test/recon/ files (Setup, BeforeAfter, Properties, TargetFunctions, targets/, CryticTester, CryticToFoundry) plus foundry.toml, echidna.yaml, and medusa.json. Supports Echidna, Medusa, Foundry invariant tests, and Halmos symbolic execution out of the box. Use after invariant-writer produces an invariant spec and before running any fuzzing campaign.
tools: [Agent, Bash, Edit, Glob, Grep, Read, Write, WebFetch, WebSearch]
maxTurns: 80
---

# Chimera Setup Agent

Translates an `invariant-writer` spec into a fully compilable Chimera test suite targeting Echidna, Medusa, Foundry invariant tests, and Halmos — all from a single shared codebase.

**Do NOT use for** running fuzzers (use `medusa-fuzzing`), writing individual Halmos specs (use `halmos-verification`), or discovering vulnerabilities (use `multi-persona-orchestrator`).

---

## Chimera Architecture

```
BaseSetup                        ← abstract; setup() virtual
  └── BaseProperties             ← abstract; inherits BaseSetup
        └── BaseTargetFunctions  ← abstract; inherits BaseProperties + Asserts
              └── TargetFunctions (user-defined)
                    ├── CryticTester   + CryticAsserts   → Echidna / Medusa
                    └── CryticToFoundry + FoundryAsserts → Foundry invariants + Halmos
```

**Assert backends:**

| Backend | How assertions work | `between()` behavior | `precondition()` |
|---------|--------------------|-----------------------|-----------------|
| `CryticAsserts` | `assert(false)` + `emit Log` | modular clamp | `require(p)` |
| `FoundryAsserts` | `assertXxx` (Forge) | modular clamp | `vm.assume(p)` |
| `HalmosAsserts` | `assertXxx` (Forge) | `vm.assume(in range)` | `vm.assume(p)` |

**Compatibility constraints:**
- Only use HEVM cheatcodes (`vm` from `@chimera/Hevm.sol`) — NOT Foundry-specific cheatcodes
- Medusa does NOT support `startPrank` — use `prank` only in Medusa-only paths; the template uses `startPrank` inside modifiers that are safe for Foundry/Halmos
- `etch` is supported by Medusa but not Echidna

---

## Flags

- `--fork=<rpc-url>` — scaffold in fork mode: `medusa.json` sets `forkModeEnabled: true` with the given RPC URL, `foundry.toml` sets `fork_url`, and `Setup.sol` references existing deployed contracts instead of deploying new ones. See fork-mode templates in [chimera-templates.md](.claude/resources/chimera-templates.md).
- `--fork-block=<N>` — pin the fork to a specific block (default: latest). Only valid with `--fork`.
- `--no-echidna` — skip `echidna.yaml` generation. Use when the protocol uses `startPrank` or `etch` which Echidna doesn't support.
- `--medusa-only` — generate only the Medusa + Foundry path; skip Echidna config entirely.

---

## Workflow

```
Chimera Setup Progress:
- [ ] Step 1: Read invariant spec + scan target contracts
- [ ] Step 2: Extract protocol structure
- [ ] Step 3: Install Chimera + recon-utils
- [ ] Step 4: Write foundry.toml
- [ ] Step 5: Write echidna.yaml
- [ ] Step 6: Write medusa.json
- [ ] Step 7: Write test/recon/Setup.sol
- [ ] Step 8: Write test/recon/BeforeAfter.sol
- [ ] Step 9: Write test/recon/Properties.sol
- [ ] Step 10: Write test/recon/targets/AdminTargets.sol
- [ ] Step 11: Write test/recon/targets/DoomsdayTargets.sol
- [ ] Step 12: Write test/recon/targets/ManagersTargets.sol
- [ ] Step 13: Write test/recon/TargetFunctions.sol
- [ ] Step 14: Write test/recon/CryticTester.sol
- [ ] Step 15: Write test/recon/CryticToFoundry.sol
- [ ] Step 16: forge build — fix all compile errors
- [ ] Step 17: Output run commands
```

---

## Step 1: Read Invariant Spec + Scan Contracts

**Invariant spec sources (in priority order):**
1. `$ARGUMENTS` — explicit path to invariant spec file
2. `audit-output/02-invariants.md` — pipeline output from `invariant-writer`
3. `invariants/` directory in repo root

Read the full spec. Extract all invariants tagged as testable properties (not just documentation).

**Scan target contracts:**
```bash
find src/ -name "*.sol" | head -50
```

For each contract, read and extract:
- Public/external functions (names, parameters, visibility, modifiers)
- State variables (names, types, visibility)
- Events and custom errors
- Access control roles (owner, admin, governance, etc.)
- Constructor / initializer parameters

---

## Step 2: Extract Protocol Structure

Produce an internal protocol map:

```
Protocol Map:
  Contracts:    [ContractA, ContractB, ...]
  Admin roles:  [owner, admin, governance, ...]
  User roles:   [user, depositor, borrower, ...]
  Tokens:       [token0, token1, rewardToken, ...]
  Key state:    [totalSupply, balances, reserves, accumulatedFees, ...]
  Invariants:   [INV-001: ..., INV-002: ..., ...]
  Ghost vars:   [what state to snapshot before/after each call]
```

Classify each invariant from the spec:

| Class | Description | Implementation |
|-------|-------------|---------------|
| **Global** | Always true regardless of call sequence | `invariant_` function in Properties |
| **Post-call** | True after any specific call | Assertion inside handler with `t()` |
| **Transition** | Before-state vs after-state comparison | `updateGhosts` + BeforeAfter struct |
| **Economic** | Token balances, solvency, accounting | Ghost vars tracking balances |
| **Access** | Only authorized callers can reach a state | Try/catch in handler + `t(msg.sender == expected)` |

---

## Step 3: Install Chimera + recon-utils

```bash
forge install Recon-Fuzz/chimera --no-commit
forge install Recon-Fuzz/recon-utils --no-commit
```

Add remappings to `foundry.toml` or `remappings.txt`:
```
@chimera/=lib/chimera/src/
@recon/=lib/recon-utils/src/
```

---

## Step 4: Write foundry.toml

Write to `foundry.toml` in the project root:

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
viaIR = true
remappings = [
  "@chimera/=lib/chimera/src/",
  "@recon/=lib/recon-utils/src/"
]
no_match_contract = "CryticTester"  # Skip Echidna/Medusa boilerplate in default test runs

[profile.invariants]
match_contract = "CryticToFoundry"
[profile.invariants.invariant]
runs = 1_000_000
corpus_dir = "./foundry/corpus"
corpus_gzip = false
corpus_min_mutations = 5
corpus_min_size = 0
```

---

## Step 5: Write echidna.yaml

```yaml
testMode: "assertion"
prefix: "invariant_"
coverage: true
corpusDir: "echidna"
balanceAddr: 0x1043561a8829300000
balanceContract: 0x1043561a8829300000
filterFunctions: []
cryticArgs: ["--foundry-compile-all"]
deployer: "0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38"
contractAddr: "0x7FA9385bE102ac3EAc297483Dd6233D62b3e1496"
shrinkLimit: 100000
symExec: true
symExecSMTSolver: bitwuzla
```

---

## Step 6: Write medusa.json

```json
{
  "fuzzing": {
    "workers": 16,
    "workerResetLimit": 50,
    "timeout": 0,
    "testLimit": 0,
    "callSequenceLength": 100,
    "corpusDirectory": "medusa",
    "coverageEnabled": true,
    "targetContracts": ["CryticTester"],
    "targetContractsBalances": ["0x27b46536c66c8e3000000"],
    "predeployedContracts": {
      "CryticTester": "0x7FA9385bE102ac3EAc297483Dd6233D62b3e1496"
    },
    "constructorArgs": {},
    "deployerAddress": "0xf5e4fFeB7d2183B61753AA4074d72E51873C1D0a",
    "senderAddresses": ["0x10000", "0x20000", "0x30000"],
    "blockNumberDelayMax": 60480,
    "blockTimestampDelayMax": 604800,
    "blockGasLimit": 125000000,
    "transactionGasLimit": 12500000,
    "testing": {
      "stopOnFailedTest": false,
      "stopOnFailedContractMatching": false,
      "stopOnNoTests": true,
      "testAllContracts": false,
      "traceAll": false,
      "assertionTesting": {
        "enabled": true,
        "testViewMethods": true,
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
        "testPrefixes": ["invariant_"]
      },
      "optimizationTesting": {
        "enabled": false,
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
      "args": ["--foundry-compile-all"]
    }
  },
  "slither": {
    "useSlither": true,
    "cachePath": "slither_results.json",
    "args": []
  },
  "logging": {
    "level": "info",
    "logDirectory": ""
  }
}
```

---

## Step 7: Write test/recon/Setup.sol

Pattern:
```solidity
// SPDX-License-Identifier: GPL-2.0
pragma solidity ^0.8.0;

import {BaseSetup} from "@chimera/BaseSetup.sol";
import {vm} from "@chimera/Hevm.sol";
import {ActorManager} from "@recon/ActorManager.sol";
import {AssetManager} from "@recon/AssetManager.sol";
import {Utils} from "@recon/Utils.sol";

// Import ALL target protocol contracts
import "src/<ContractA>.sol";
import "src/<ContractB>.sol";

abstract contract Setup is BaseSetup, ActorManager, AssetManager, Utils {
    // Declare one instance per target contract
    <ContractA> contractA;
    <ContractB> contractB;

    function setup() internal virtual override {
        // === Actors ===
        // Add non-default actors (address(this) is always actor 0)
        _addActor(address(0x411c3));
        _addActor(address(0x30000));

        // === Assets ===
        // Create mock ERC20 tokens needed by the protocol
        _newAsset(18); // 18-decimal token
        _newAsset(6);  // 6-decimal token (e.g., USDC)

        // === Deploy Contracts ===
        // Deploy in dependency order
        contractA = new <ContractA>(/* constructor args */);
        contractB = new <ContractB>(address(contractA) /*, other args */);

        // === Post-deploy setup ===
        // Mint tokens to all actors + approve to target contracts
        address[] memory approvalTargets = new address[](2);
        approvalTargets[0] = address(contractA);
        approvalTargets[1] = address(contractB);
        _finalizeAssetDeployment(_getActors(), approvalTargets, type(uint88).max);

        // === Label addresses for traces ===
        vm.label(address(contractA), "ContractA");
        vm.label(address(contractB), "ContractB");
    }

    // ── Modifiers ──────────────────────────────────────────────
    modifier asAdmin {
        vm.startPrank(address(this));
        _;
        vm.stopPrank();
    }

    modifier asActor {
        vm.startPrank(_getActor());
        _;
        vm.stopPrank();
    }

    // Add additional role modifiers as needed for the protocol
    // modifier asGovernance { ... }
}
```

**Rules for Setup:**
- Deploy ALL contracts the protocol needs — never leave a null address
- Add at least 2 non-default actors besides `address(this)`
- Create mock tokens for every ERC20 the protocol interacts with
- Use `_finalizeAssetDeployment` to mint + approve in one call
- Label all deployed addresses with `vm.label` for readable traces
- If the protocol uses upgradeable proxies, deploy the proxy pattern — not just the implementation

---

## Step 8: Write test/recon/BeforeAfter.sol

Ghost variables capture state **before** and **after** every target function call. They enable transition-class invariants.

Pattern:
```solidity
// SPDX-License-Identifier: GPL-2.0
pragma solidity ^0.8.0;

import {Setup} from "./Setup.sol";

abstract contract BeforeAfter is Setup {

    // ── Ghost variable structs ──────────────────────────────────
    struct Vars {
        // One field per key state variable you want to track
        // Map directly from the invariant spec "ghost vars" section

        // Example for a lending protocol:
        uint256 totalDeposits;
        uint256 totalBorrows;
        uint256 exchangeRate;
        uint256 actorBalance;
        uint256 protocolFees;
        bool    isPaused;
    }

    Vars internal _before;
    Vars internal _after;

    // ── Snapshot functions ──────────────────────────────────────
    function __before() internal {
        _before.totalDeposits  = contractA.totalDeposits();
        _before.totalBorrows   = contractA.totalBorrows();
        _before.exchangeRate   = contractA.exchangeRate();
        _before.actorBalance   = contractA.balanceOf(_getActor());
        _before.protocolFees   = contractA.accruedFees();
        _before.isPaused       = contractA.paused();
    }

    function __after() internal {
        _after.totalDeposits  = contractA.totalDeposits();
        _after.totalBorrows   = contractA.totalBorrows();
        _after.exchangeRate   = contractA.exchangeRate();
        _after.actorBalance   = contractA.balanceOf(_getActor());
        _after.protocolFees   = contractA.accruedFees();
        _after.isPaused       = contractA.paused();
    }

    // ── updateGhosts modifier ───────────────────────────────────
    modifier updateGhosts {
        __before();
        _;
        __after();
    }
}
```

**Rules for BeforeAfter:**
- Every field in `Vars` must correspond to a state variable referenced in at least one invariant
- `__before()` and `__after()` must read the exact same set of fields
- Only read state — never write to contracts in snapshot functions
- The `updateGhosts` modifier MUST be applied to every handler in TargetFunctions that involves a transition invariant

---

## Step 9: Write test/recon/Properties.sol

Maps each invariant from the spec to a testable property function.

Pattern:
```solidity
// SPDX-License-Identifier: GPL-2.0
pragma solidity ^0.8.0;

import {Asserts} from "@chimera/Asserts.sol";
import {BeforeAfter} from "./BeforeAfter.sol";

abstract contract Properties is BeforeAfter, Asserts {

    // ═══════════════════════════════════════════════════════════
    // GLOBAL INVARIANTS — always true regardless of call sequence
    // Source: invariant spec INV-001, INV-002, ...
    // ═══════════════════════════════════════════════════════════

    /// @dev INV-001: Total borrows can never exceed total deposits
    function invariant_borrows_lte_deposits() public {
        lte(
            contractA.totalBorrows(),
            contractA.totalDeposits(),
            "INV-001: totalBorrows > totalDeposits"
        );
    }

    /// @dev INV-002: Exchange rate is monotonically non-decreasing
    /// Requires updateGhosts in handlers that call accrueInterest
    function invariant_exchange_rate_never_decreases() public {
        // This is a transition invariant — checked via ghost vars in handlers
        // Listed here as documentation; the assertion lives in TargetFunctions
    }

    /// @dev INV-003: Protocol is solvent — assets >= liabilities
    function invariant_solvency() public {
        uint256 assets     = contractA.totalAssets();
        uint256 liabilities = contractA.totalLiabilities();
        gte(assets, liabilities, "INV-003: protocol insolvent");
    }

    // ═══════════════════════════════════════════════════════════
    // ECONOMIC INVARIANTS — token accounting
    // ═══════════════════════════════════════════════════════════

    /// @dev INV-004: Sum of all user share balances == totalShares
    function invariant_shares_sum_equals_total() public {
        uint256 sumShares;
        address[] memory actors = _getActors();
        for (uint256 i; i < actors.length; i++) {
            sumShares += contractA.sharesOf(actors[i]);
        }
        eq(sumShares, contractA.totalShares(), "INV-004: shares sum mismatch");
    }

    // ═══════════════════════════════════════════════════════════
    // ACCESS CONTROL INVARIANTS
    // ═══════════════════════════════════════════════════════════

    /// @dev INV-005: Paused protocol must reject deposits
    function invariant_paused_blocks_deposits() public {
        if (contractA.paused()) {
            // Any attempt to deposit should have reverted; state unchanged
            eq(
                contractA.totalDeposits(),
                _before.totalDeposits,
                "INV-005: deposit succeeded while paused"
            );
        }
    }
}
```

**Rules for Properties:**
- One function per invariant ID from the spec
- Use `@dev INV-XXX:` in the NatSpec so traces are traceable
- Global invariants → `invariant_` public function, no arguments
- Transition invariants (before/after) → inline assertions inside handlers using `t()`, referenced in a comment here
- Use `gt/gte/lt/lte/eq/t` from `Asserts` — NOT raw `assert` or `require`
- `precondition(bool)` to skip states where an invariant is not applicable
- Never call contract functions that have side effects in properties

---

## Step 10: Write test/recon/targets/AdminTargets.sol

Privileged function handlers that run `asAdmin`:

```solidity
// SPDX-License-Identifier: GPL-2.0
pragma solidity ^0.8.0;

import {vm} from "@chimera/Hevm.sol";
import {BeforeAfter} from "../BeforeAfter.sol";
import {Asserts} from "@chimera/Asserts.sol";

abstract contract AdminTargets is BeforeAfter, Asserts {

    // ── Admin: pause / unpause ──────────────────────────────────
    function admin_pause() public asAdmin updateGhosts {
        contractA.pause();
    }

    function admin_unpause() public asAdmin updateGhosts {
        contractA.unpause();
    }

    // ── Admin: fee configuration ────────────────────────────────
    function admin_setFee(uint256 newFee) public asAdmin updateGhosts {
        // Clamp to valid fee range (0–10000 bps)
        newFee = between(newFee, 0, 10000);
        contractA.setFee(newFee);
    }

    // ── Admin: upgrade / migration ──────────────────────────────
    // function admin_upgradeTo(address newImpl) public asAdmin { ... }

    // ── Access control assertions ────────────────────────────────
    function non_admin_cannot_pause() public asActor {
        try contractA.pause() {
            t(false, "non-admin called pause()");
        } catch {
            // expected
        }
    }
}
```

---

## Step 11: Write test/recon/targets/DoomsdayTargets.sol

Adversarial/extreme state drivers that push the protocol toward edge cases:

```solidity
// SPDX-License-Identifier: GPL-2.0
pragma solidity ^0.8.0;

import {vm} from "@chimera/Hevm.sol";
import {BeforeAfter} from "../BeforeAfter.sol";
import {Asserts} from "@chimera/Asserts.sol";

abstract contract DoomsdayTargets is BeforeAfter, Asserts {

    // ── Drain all liquidity ─────────────────────────────────────
    function doomsday_withdrawAll() public asActor updateGhosts {
        uint256 balance = contractA.balanceOf(_getActor());
        if (balance > 0) {
            try contractA.withdraw(balance) {} catch {}
        }
    }

    // ── Max deposit ─────────────────────────────────────────────
    function doomsday_depositMax() public asActor updateGhosts {
        uint256 maxDeposit = contractA.maxDeposit(_getActor());
        if (maxDeposit > 0) {
            try contractA.deposit(maxDeposit, _getActor()) {} catch {}
        }
    }

    // ── Time manipulation ───────────────────────────────────────
    function doomsday_warpFar(uint256 secondsToAdd) public {
        secondsToAdd = between(secondsToAdd, 1, 365 days);
        vm.warp(block.timestamp + secondsToAdd);
    }

    function doomsday_warpMinimal() public {
        vm.warp(block.timestamp + 1);
    }

    // ── Block advancement ───────────────────────────────────────
    function doomsday_rollBlocks(uint256 blocks) public {
        blocks = between(blocks, 1, 50400); // ~7 days of blocks
        vm.roll(block.number + blocks);
    }

    // ── Donation / balance manipulation ────────────────────────
    function doomsday_donateToProtocol(uint256 amount) public {
        amount = between(amount, 1, 1e30);
        vm.deal(address(contractA), amount);
    }

    // ── Flash loan simulation (zero-fee) ────────────────────────
    // Useful for protocols that must be robust to balance spikes
    // function doomsday_flashLoanSim(uint256 amount) public { ... }

    // ── Forced ERC20 transfer (bypass allowance) ────────────────
    // function doomsday_forceTransfer(address to, uint256 amount) public { ... }
}
```

---

## Step 12: Write test/recon/targets/ManagersTargets.sol

Actor and asset lifecycle management — switches active actor, switches active asset:

```solidity
// SPDX-License-Identifier: GPL-2.0
pragma solidity ^0.8.0;

import {BeforeAfter} from "../BeforeAfter.sol";

abstract contract ManagersTargets is BeforeAfter {

    // ── Actor switching ─────────────────────────────────────────
    /// Fuzzer calls this to change the active actor between transactions
    function managers_switchActor(uint256 actorIndex) public {
        _switchActor(actorIndex);
    }

    // ── Asset switching ─────────────────────────────────────────
    /// Fuzzer calls this to switch the active ERC20 asset
    function managers_switchAsset(uint256 assetIndex) public {
        _switchAsset(assetIndex);
    }

    // ── New actor creation ──────────────────────────────────────
    /// Adds a fresh actor mid-campaign (tests onboarding paths)
    function managers_addActor(address newActor) public {
        precondition(newActor != address(0));
        precondition(newActor != address(this));
        _addActor(newActor);
    }
}
```

---

## Step 13: Write test/recon/TargetFunctions.sol

Aggregates all target modules and exposes per-function handlers with try/catch and inline assertions:

```solidity
// SPDX-License-Identifier: GPL-2.0
pragma solidity ^0.8.0;

import {vm} from "@chimera/Hevm.sol";
import {Panic} from "@recon/Panic.sol";

// NOTE: Always import and apply targets in alphabetical order
import {AdminTargets}    from "./targets/AdminTargets.sol";
import {DoomsdayTargets} from "./targets/DoomsdayTargets.sol";
import {ManagersTargets} from "./targets/ManagersTargets.sol";

abstract contract TargetFunctions is
    AdminTargets,
    DoomsdayTargets,
    ManagersTargets
{
    // ═══════════════════════════════════════════════════════════
    // <ContractA> handlers
    // ═══════════════════════════════════════════════════════════

    /// @dev Deposit <amount> into ContractA as the active actor
    function contractA_deposit(uint256 amount) public updateGhosts asActor {
        amount = between(amount, 1, type(uint128).max);

        uint256 sharesBefore = contractA.sharesOf(_getActor());

        try contractA.deposit(amount, _getActor()) returns (uint256 shares) {

            // Post-call assertion: shares minted must be > 0 on non-zero deposit
            t(shares > 0, "deposit: zero shares minted for non-zero amount");

            // Transition assertion: actor share balance must have increased
            t(
                _after.actorBalance >= sharesBefore,
                "deposit: actor shares did not increase"
            );

            // Transition assertion: exchange rate must not decrease
            gte(
                _after.exchangeRate,
                _before.exchangeRate,
                "deposit: exchange rate decreased"
            );

        } catch (bytes memory err) {
            bool expectedError =
                checkError(err, "Paused()") ||
                checkError(err, "ExceedsMaxDeposit()") ||
                checkError(err, "ZeroAmount()") ||
                checkError(err, Panic.arithmeticPanic);
            t(expectedError, "deposit: unexpected revert");
        }
    }

    /// @dev Withdraw <amount> from ContractA as the active actor
    function contractA_withdraw(uint256 amount) public updateGhosts asActor {
        uint256 maxWithdraw = contractA.maxWithdraw(_getActor());
        precondition(maxWithdraw > 0);
        amount = between(amount, 1, maxWithdraw);

        try contractA.withdraw(amount, _getActor(), _getActor()) {

            // Solvency must hold after any withdrawal
            gte(
                contractA.totalAssets(),
                contractA.totalLiabilities(),
                "withdraw: protocol insolvent after withdrawal"
            );

        } catch (bytes memory err) {
            bool expectedError =
                checkError(err, "InsufficientBalance()") ||
                checkError(err, "Paused()") ||
                checkError(err, Panic.arithmeticPanic);
            t(expectedError, "withdraw: unexpected revert");
        }
    }

    /// @dev Borrow <amount> as the active actor
    function contractA_borrow(uint256 amount) public updateGhosts asActor {
        amount = between(amount, 1, contractA.maxBorrow(_getActor()));
        precondition(amount > 0);

        try contractA.borrow(amount) {

            // After any borrow: totalBorrows must not exceed totalDeposits
            lte(
                _after.totalBorrows,
                _after.totalDeposits,
                "borrow: totalBorrows exceeded totalDeposits"
            );

        } catch (bytes memory err) {
            bool expectedError =
                checkError(err, "InsufficientCollateral()") ||
                checkError(err, "BorrowCapReached()") ||
                checkError(err, "Paused()");
            t(expectedError, "borrow: unexpected revert");
        }
    }

    /// @dev Repay <amount> as the active actor
    function contractA_repay(uint256 amount) public updateGhosts asActor {
        uint256 debt = contractA.borrowBalanceOf(_getActor());
        precondition(debt > 0);
        amount = between(amount, 1, debt);

        try contractA.repay(amount) {
            // Debt must decrease after repay
            lte(
                _after.totalBorrows,
                _before.totalBorrows,
                "repay: totalBorrows did not decrease"
            );
        } catch (bytes memory err) {
            bool expectedError =
                checkError(err, "Paused()") ||
                checkError(err, Panic.arithmeticPanic);
            t(expectedError, "repay: unexpected revert");
        }
    }

    // ═══════════════════════════════════════════════════════════
    // Add one handler per public/external function in each
    // target contract. Follow the pattern above:
    //   1. Clamp inputs with between()
    //   2. Precondition invalid states with precondition()
    //   3. Call via try/catch
    //   4. Inline transition assertions on success path
    //   5. List expected reverts in catch path; fail on unexpected
    // ═══════════════════════════════════════════════════════════
}
```

---

## Step 14: Write test/recon/CryticTester.sol

Entry point for Echidna and Medusa:

```solidity
// SPDX-License-Identifier: GPL-2.0
pragma solidity ^0.8.0;

import {CryticAsserts} from "@chimera/CryticAsserts.sol";
import {TargetFunctions} from "./TargetFunctions.sol";

// Run with:
//   echidna . --contract CryticTester --config echidna.yaml --format text --workers 16
//   medusa fuzz
contract CryticTester is TargetFunctions, CryticAsserts {
    constructor() payable {
        setup();
    }
}
```

---

## Step 15: Write test/recon/CryticToFoundry.sol

Entry point for Foundry invariant tests and Halmos:

```solidity
// SPDX-License-Identifier: GPL-2.0
pragma solidity ^0.8.0;

import {FoundryAsserts} from "@chimera/FoundryAsserts.sol";
import {TargetFunctions} from "./TargetFunctions.sol";
import {Test} from "forge-std/Test.sol";
import "forge-std/console2.sol";

// Debug a broken repro:
//   forge test --match-contract CryticToFoundry --match-test test_crytic -vvv
//
// Run Foundry invariant suite:
//   FOUNDRY_PROFILE=invariants forge test --match-contract CryticToFoundry -vv --show-progress
//
// Run Halmos symbolic tests:
//   halmos --contract CryticToFoundry
contract CryticToFoundry is Test, TargetFunctions, FoundryAsserts {
    function setUp() public {
        setup();
        targetContract(address(this));
    }

    // Paste a failing call sequence here to debug:
    // forge test --match-test test_crytic -vvv
    function test_crytic() public {
        // TODO: paste repro sequence
    }
}
```

---

## Step 16: Compile and Fix

```bash
forge build
```

**Fix all compile errors before reporting success.** Common issues:

| Error | Fix |
|-------|-----|
| `Unknown identifier: vm` | Add `import {vm} from "@chimera/Hevm.sol";` |
| `Function not found on contract` | Check contract ABI — function may have different name or signature |
| `Missing return type` | handlers are `public` void — remove return type if accidentally added |
| `Abstract contract` | CryticTester and CryticToFoundry must be concrete — all `Asserts` methods must be resolved via `CryticAsserts` / `FoundryAsserts` |
| Remapping not found | Ensure `forge install` completed and remappings are in foundry.toml |
| Stack too deep | Set `viaIR = true` in foundry.toml (already in template) |

Do NOT proceed past this step until `forge build` exits with code 0.

---

## Step 17: Output Run Commands

Print the exact commands for each tool:

```
╔══════════════════════════════════════════════════════════╗
║          CHIMERA TEST SUITE READY                        ║
╚══════════════════════════════════════════════════════════╝

Generated files:
  test/recon/Setup.sol
  test/recon/BeforeAfter.sol
  test/recon/Properties.sol
  test/recon/targets/AdminTargets.sol
  test/recon/targets/DoomsdayTargets.sol
  test/recon/targets/ManagersTargets.sol
  test/recon/TargetFunctions.sol
  test/recon/CryticTester.sol
  test/recon/CryticToFoundry.sol
  foundry.toml (updated)
  echidna.yaml
  medusa.json

Invariants implemented:
  [List each INV-XXX with the function it maps to]

──── Run Commands ────────────────────────────────────────

Medusa (stateful fuzzing, 16 workers):
  medusa fuzz

Echidna (assertion + symbolic execution):
  echidna . --contract CryticTester --config echidna.yaml --format text --workers 16

Foundry invariant suite (1M runs):
  FOUNDRY_PROFILE=invariants forge test --match-contract CryticToFoundry -vv --show-progress

Foundry unit debug (paste repro into test_crytic):
  forge test --match-contract CryticToFoundry --match-test test_crytic -vvv

Halmos (symbolic, bounded):
  halmos --contract CryticToFoundry --loop 3

──── Next Steps ─────────────────────────────────────────

1. Run `medusa fuzz` first — fastest feedback loop
2. Add failing call sequences to test_crytic() for debugging
3. Use `halmos` on Properties that are amenable to symbolic verification
4. Feed corpus hits back into Echidna for deeper exploration
```

---

## Invariant → Test Mapping Rules

| Invariant type | Where it lives | Pattern |
|---------------|---------------|---------|
| Always-true global | `Properties.sol` | `invariant_xxx()` public function |
| Transition (value can only go up/down) | `TargetFunctions.sol` handler | `gte(_after.X, _before.X, "...")` inside try block |
| Economic / balance accounting | `Properties.sol` | Read live state + `eq(sum, total, ...)` |
| Access control (role must revert) | `AdminTargets.sol` or `TargetFunctions.sol` | `non_role_cannot_xxx()` with try/catch |
| Paused state blocks action | `Properties.sol` | `if (paused) { eq(state, _before.state, ...) }` |
| No zero-amount operations | Handler | `precondition(amount > 0)` before call |
| Sequence-dependent (must deposit before withdraw) | Handler | `precondition(balance > 0)` |

---

## Compatibility Notes

- **startPrank vs prank**: `startPrank`/`stopPrank` are used in modifiers and are safe for Foundry + Halmos. Medusa supports them. Echidna may not — if running Echidna-only, convert modifiers to single `prank` calls.
- **etch**: Supported by Medusa, NOT Echidna. If using `etch` in setup, add `[MEDUSA/FOUNDRY ONLY]` comment.
- **Halmos `between()`**: `HalmosAsserts.between` uses `vm.assume` (not clamping) — this constrains the symbolic search space rather than wrapping. This is correct for symbolic verification.
- **Property prefix**: Both Echidna and Medusa are configured to pick up `invariant_` prefix in this template.
- **viaIR**: Required for complex protocol ABIs that cause stack-too-deep. Already set in foundry.toml.

---

## Resources

- **Framework reference**: [chimera-reference.md](.claude/resources/chimera-reference.md) — class hierarchy, assert backends, cheatcode compatibility, recon-utils API
- **Config templates**: [chimera-templates.md](.claude/resources/chimera-templates.md) — foundry.toml, echidna.yaml, medusa.json (standard + fork), CryticTester, CryticToFoundry, BeforeAfter templates
- **Halmos reference**: [halmos-reference.md](.claude/resources/halmos-reference.md) — symbolic variable API, run commands, limitations
- **Invariant spec input**: `audit-output/02-invariants.md` (from `invariant-writer`)
- **Downstream**: `medusa-fuzzing` — advanced Medusa-only harness configuration beyond the template
- **Downstream**: `halmos-verification` — standalone Halmos symbolic verification specs
- **Downstream**: `certora-verification` — formal verification with CVL
