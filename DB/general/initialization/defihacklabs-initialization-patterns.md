---
protocol: generic
chain: ethereum, bsc
category: initialization
vulnerability_type: unprotected_initialization

attack_type: initialization_hijack
affected_component: proxy_initialization, constructor

primitives:
  - unprotected_init
  - reinit_during_flashloan
  - uninitialized_library
  - missing_initializer

severity: critical
impact: fund_loss, total_control
exploitability: 0.85
financial_impact: critical

tags:
  - initialization
  - init_hijack
  - proxy
  - self_destruct
  - access_control
  - constructor
  - real_exploit
  - DeFiHackLabs

source: DeFiHackLabs
total_exploits_analyzed: 4
total_losses: "$500M+"
---

## DeFiHackLabs Unprotected Initialization Compendium

### Overview

Unprotected initialization functions are the most devastating access control vulnerability in smart contracts. This entry catalogs **4 landmark exploits** spanning 2017-2021 totaling over **$500M in losses** (at time of exploit). The pattern: critical `init()` or `initialize()` functions lack access control, allowing anyone to claim ownership or re-initialize state.

### Root Cause Categories

1. **Public init() with No Access Control** — Anyone can call after deployment to set themselves as owner
2. **Re-Initialization During Flash Loan** — `init()` callable again during mid-transaction state change
3. **Uninitialized Library Contract** — Library's `init()` never called, attacker claims ownership + `selfdestruct`

---

### Vulnerable Pattern Examples

#### Category 1: Public init() — No Access Control [CRITICAL]

**Example 1: DAO Maker — Unguarded init() Steals Deposits ($4M, 2021-09)** [CRITICAL]
```solidity
// ❌ VULNERABLE: init() has NO access control — anyone can re-set depositToken
contract DaoMakerVault {
    address public depositToken;
    address public owner;
    bool private initialized;

    // @audit MISSING: onlyOwner modifier, initialized check
    function init(address _depositToken) external {
        // @audit No `require(!initialized)` check!
        // @audit No `require(msg.sender == owner)` check!
        depositToken = _depositToken;
        initialized = true;
    }

    function emergencyWithdraw(uint256 amount) external {
        IERC20(depositToken).transfer(msg.sender, amount);
    }
}

// Attack: Call init() with attacker-controlled fake token
// Then call emergencyWithdraw to extract real deposited funds
interface IDAOMaker {
    function init(
        address _stakingToken,
        address _rewardToken,
        uint256 _rewardPerBlock,
        uint256 _startBlock,
        uint256 _bonusEndBlock,
        uint256 _poolLimitPerUser,
        address _admin,
        address _walletAddress
    ) external;
}

// @audit Attacker calls init() with a new stakingToken and themselves as admin
daomaker.init(fakeToken, fakeReward, 0, 0, 0, type(uint256).max, attacker, attacker);
// Now attacker controls the vault
```
- **PoC**: `DeFiHackLabs/src/test/2021-09/DAOMaker_exp.sol`
- **Root Cause**: `init()` had no `onlyOwner` or `initialized` guard. Called by attacker to change deposit token and admin, enabling withdrawal of real user deposits.

**Example 2: 88mph — init() Never Called After Deploy ($6.5M at risk, 2021-06)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Deploy creates a proxy but init() is never called in the same tx
// The init() function is left open for anyone to front-run

contract EightyEightMPH {
    address public owner;
    bool private _initialized;

    function init() external {
        require(!_initialized, "already initialized");
        owner = msg.sender;          // @audit First caller becomes owner
        _initialized = true;
    }

    function setRewards(address _rewardToken, uint256 _rate) external onlyOwner {
        // Owner can drain protocol by setting attacker-controlled reward token
    }
}

// @audit Attack vector:
// 1. Monitor mempool for deploy tx
// 2. Front-run the team's init() call
// 3. Attacker becomes owner
// 4. Call setRewards() to drain protocol
```
- **PoC**: `DeFiHackLabs/src/test/2021-06/88mph_exp.sol`
- **Root Cause**: `init()` was supposed to be called immediately after deploy but was in a separate transaction. Attacker could front-run it to become owner.

---

#### Category 2: Re-Initialization During Flash Loan [CRITICAL]

**Example 3: DODO — init() Re-Callable During Flashloan ($700K, 2021-03)** [CRITICAL]
```solidity
// ❌ VULNERABLE: DODO V2 pool init() can be called AGAIN during a flash loan
// Normal state: pool is initialized
// During flash loan: tokens are temporarily removed → state looks uninitialized

// DODO V2 Pool Implementation
contract DODOPool {
    address public _BASE_TOKEN_;
    address public _QUOTE_TOKEN_;
    bool public _INITIALIZED_;

    function init(
        address baseToken,
        address quoteToken,
        uint256 lpFee
    ) external {
        // @audit Checks _INITIALIZED_ flag BUT:
        // During flash loan, attacker can point to a NEW, uninitialized clone
        require(!_INITIALIZED_, "already init");
        _BASE_TOKEN_ = baseToken;
        _QUOTE_TOKEN_ = quoteToken;
        _INITIALIZED_ = true;
    }

    function flashLoan(uint256 amount, bytes calldata data) external {
        IERC20(_BASE_TOKEN_).transfer(msg.sender, amount);
        // @audit Callback to attacker during flash loan
        IFlashLoanReceiver(msg.sender).executeOperation(amount, data);
        // Check repayment...
    }
}

// Attack flow:
// 1. Flash loan from pool A
// 2. In callback: find an uninitialized DODO pool clone
// 3. Call init() on the clone with attacker-controlled tokens
// 4. Drain the clone's actual token balances
function DPPFlashLoanCall(address sender, uint256 amount, bytes calldata data) external {
    // @audit Call init() on uninitialized clone during callback
    IDODOPool(uninitClone).init(attackerToken, attackerQuote, 0);
    IDODOPool(uninitClone).flashLoan(stolenAmount, "");
}
```
- **PoC**: `DeFiHackLabs/src/test/2021-03/DODO_exp.sol`
- **Root Cause**: DODO V2 had factory-created pool clones. Some clones were deployed but never initialized. Attacker found these and called `init()` with attacker-controlled parameters during a flash loan callback.

---

#### Category 3: Uninitialized Library — selfdestruct [CRITICAL]

**Example 4: Parity Multisig — Library Kill (514K ETH / ~$157M, 2017-11)** [CRITICAL]
```solidity
// ❌ VULNERABLE: Multisig library contract's initWallet() was never called
// Global library that ALL Parity multisigs delegatecall into

contract WalletLibrary {
    address[] public m_owners;
    bool public initialized;

    // @audit This function controls ownership of ALL multisigs
    function initWallet(address[] _owners, uint _required) external {
        // @audit No `initialized` check in original code!
        // @audit Called via delegatecall from each multisig, BUT:
        // The LIBRARY CONTRACT ITSELF was never initialized
        m_owners = _owners;
        initialized = true;
    }

    // @audit If attacker becomes owner of the LIBRARY, they can kill it
    function kill(address _to) external onlyOwner {
        selfdestruct(payable(_to));
        // @audit This DESTROYS the library that all multisigs depend on
        // All multisig wallets instantly become unusable
    }
}

// Attack sequence:
// 1. Call initWallet() directly on the LIBRARY contract (not a multisig)
library_contract.initWallet([attacker], 1);
// @audit Attacker is now owner of the shared library

// 2. Kill the library — permanently freezes 514,000 ETH across ALL Parity multisigs
library_contract.kill(attacker);
// @audit selfdestruct destroys library code
// All delegatecall-dependent multisigs are now BRICKED forever
```
- **PoC**: `DeFiHackLabs/src/test/2017-11/Parity_exp.sol`
- **Root Cause**: WalletLibrary was deployed as a standalone contract. Its `initWallet()` was only called via `delegatecall` from individual multisigs, but the library contract itself was never initialized. Attacker directly called `initWallet()` on the library, became its owner, and called `kill()` which `selfdestruct`-ed the library, permanently freezing 514K ETH ($157M).

---

### Impact Analysis

#### Technical Impact
- **Total contract takeover**: Attacker becomes owner/admin with full control
- **Permanent fund lock**: Parity's `selfdestruct` locked 514K ETH permanently (still frozen today)
- **Protocol-wide cascading failure**: Library kill affects ALL dependent contracts

#### Business Impact
| Protocol | Loss | Initialization Flaw |
|----------|------|---------------------|
| Parity Multisig | 514K ETH (~$157M) | Library `initWallet()` never called + `selfdestruct` |
| DAO Maker | $4M | `init()` with no access control |
| 88mph | $6.5M (at risk) | `init()` in separate tx from deploy |
| DODO | $700K | Uninitialized pool clones |

---

### Secure Implementation

**Fix 1: OpenZeppelin Initializable Pattern**
```solidity
// ✅ SECURE: Use OpenZeppelin's initializer modifier
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract SecureVault is Initializable {
    address public owner;
    address public depositToken;

    // @audit `initializer` modifier prevents re-initialization
    function initialize(address _depositToken, address _owner) external initializer {
        owner = _owner;
        depositToken = _depositToken;
    }
}
```

**Fix 2: Constructor + Initializer in Same Tx**
```solidity
// ✅ SECURE: Initialize in constructor or factory in same tx
contract SecureFactory {
    function createVault(address depositToken) external returns (address) {
        Vault vault = new Vault();
        // @audit Initialize in SAME transaction as deploy — no front-run window
        vault.initialize(depositToken, msg.sender);
        return address(vault);
    }
}
```

**Fix 3: Disable Library Initialization**
```solidity
// ✅ SECURE: Disable initialization on implementation/library contracts
contract WalletLibrary is Initializable {
    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();  // @audit Library itself cannot be initialized
    }

    function initialize(address[] memory _owners) external initializer {
        // Only callable via proxy delegatecall
    }
}
```

---

### Detection Patterns

```bash
# Unprotected init/initialize functions
grep -rn "function init\|function initialize" --include="*.sol" | \
  xargs grep -L "initializer\|onlyOwner\|_initialized\|require.*!.*init"

# selfdestruct in library contracts
grep -rn "selfdestruct\|suicide" --include="*.sol"

# Factory contracts that don't initialize in same tx
grep -rn "new.*Vault\|new.*Pool\|create\|clone" --include="*.sol" | \
  xargs grep -L "initialize\|init("

# Proxy patterns without initializer guard
grep -rn "delegatecall\|_implementation" --include="*.sol" | \
  xargs grep -L "Initializable\|initializer"
```

---

### Audit Checklist

1. **Does every `init()`/`initialize()` have an `initializer` modifier or equivalent guard?**
2. **Is initialization done in the SAME transaction as deployment?** — Front-run window if separate
3. **Are implementation/library contracts themselves initialized (or initialization disabled)?**
4. **Can `init()` be called again after state changes (e.g., during flash loan callbacks)?**
5. **Does any contract use `selfdestruct`?** — If so, who can trigger it?
6. **Are factory-created clones initialized before being registered?**

---

### Keywords

- initialization
- init_hijack
- unprotected_init
- reinitialize
- proxy_initialization
- selfdestruct
- library_kill
- front_run_init
- constructor
- initializer_modifier
- clone_factory
- DeFiHackLabs

---

### Related Vulnerabilities

- [Proxy Vulnerabilities](../../general/proxy-vulnerabilities/proxy-vulnerabilities.md)
- [UUPS Proxy](../../general/uups-proxy/uups-proxy-vulnerabilities.md)
- [Access Control](../../general/access-control/access-control-vulnerabilities.md)
