# Chimera Configuration Templates

Ready-to-use configuration files for Chimera-based test suites.

---

## foundry.toml

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
no_match_contract = "CryticTester"  # Skip Echidna/Medusa boilerplate in default runs

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

## echidna.yaml

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

## medusa.json (standard — no fork)

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

## medusa.json (fork mode — replace forkConfig block)

When using `--fork=<rpc-url>`, replace the `forkConfig` block with:

```json
"forkConfig": {
  "forkModeEnabled": true,
  "rpcUrl": "<RPC_URL>",
  "rpcBlock": 0,
  "poolSize": 20
}
```

And update `foundry.toml` to add the fork URL:

```toml
[profile.default]
# ... existing config ...
fork_url = "<RPC_URL>"
```

Also update `Setup.sol` to avoid re-deploying contracts that already exist on the fork:

```solidity
function setup() internal virtual override {
    // In fork mode: reference existing deployed contracts instead of deploying new ones
    contractA = <ContractA>(0x<DEPLOYED_ADDRESS>);
    // Label for traces
    vm.label(address(contractA), "ContractA");
    // Only deploy mock actors/assets as needed
}
```

---

## CryticTester.sol template

```solidity
// SPDX-License-Identifier: GPL-2.0
pragma solidity ^0.8.0;

import {CryticAsserts} from "@chimera/CryticAsserts.sol";
import {TargetFunctions} from "./TargetFunctions.sol";

// echidna . --contract CryticTester --config echidna.yaml --format text --workers 16
// medusa fuzz
contract CryticTester is TargetFunctions, CryticAsserts {
    constructor() payable {
        setup();
    }
}
```

---

## CryticToFoundry.sol template

```solidity
// SPDX-License-Identifier: GPL-2.0
pragma solidity ^0.8.0;

import {FoundryAsserts} from "@chimera/FoundryAsserts.sol";
import {TargetFunctions} from "./TargetFunctions.sol";
import {Test} from "forge-std/Test.sol";
import "forge-std/console2.sol";

// forge test --match-contract CryticToFoundry --match-test test_crytic -vvv
// FOUNDRY_PROFILE=invariants forge test --match-contract CryticToFoundry -vv --show-progress
// halmos --contract CryticToFoundry --loop 3
contract CryticToFoundry is Test, TargetFunctions, FoundryAsserts {
    function setUp() public {
        setup();
        targetContract(address(this));
    }

    function test_crytic() public {
        // Paste failing call sequence here for debugging
    }
}
```

---

## BeforeAfter.sol template

```solidity
// SPDX-License-Identifier: GPL-2.0
pragma solidity ^0.8.0;

import {Setup} from "./Setup.sol";

abstract contract BeforeAfter is Setup {

    struct Vars {
        // Add one field per key state variable referenced in transition invariants
        // e.g.:
        // uint256 totalDeposits;
        // uint256 exchangeRate;
        // uint256 actorBalance;
    }

    Vars internal _before;
    Vars internal _after;

    function __before() internal {
        // _before.totalDeposits = contract.totalDeposits();
    }

    function __after() internal {
        // _after.totalDeposits = contract.totalDeposits();
    }

    modifier updateGhosts {
        __before();
        _;
        __after();
    }
}
```
