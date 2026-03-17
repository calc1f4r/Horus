---
# Core Classification
protocol: generic
chain: everychain
category: proxy_pattern
vulnerability_type: proxy_implementation

# Attack Vector Details
attack_type: implementation_exploit
affected_component: proxy_contract_system

# Technical Primitives
primitives:
  - upgradeable_proxy
  - delegatecall
  - storage_layout
  - initialization
  - access_control
  - implementation_contract
  - transparent_proxy
  - UUPS_proxy
  - beacon_proxy
  - diamond_proxy
  - minimal_proxy
  - clone_factory

# Impact Classification
severity: high
impact: contract_takeover
exploitability: 0.7
financial_impact: critical

# Context Tags
tags:
  - proxy_pattern
  - upgradeable_contracts
  - initialization_vulnerability
  - storage_collision
  - implementation_security
  - delegatecall_pattern
  - EIP1967
  - OpenZeppelin
  - metamorphic_contracts
  - clone_validation

language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: storage_layout_error
pattern_key: storage_layout_error | proxy_contract_system | proxy_implementation

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - UUPS_proxy
  - _authorizeUpgrade
  - _getImplementation
  - access_control
  - addToWhitelist
  - address
  - admin
  - approve
  - batch
  - beacon_proxy
  - clone_factory
  - createGauge
  - delegatecall
  - deployCounterfactualWallet
  - deployFor
  - diamond_proxy
  - emergencyWithdraw
  - execute
  - executeAction
  - executeOnWhitelisted
---

## Reference
- [proxy_findings] : /home/calc1f4r/vuln-database/reports/proxy_findings/

## Proxy Pattern Implementation Vulnerabilities

**Comprehensive Security Issues in Upgradeable Proxy Architectures**

### Overview

Proxy patterns enable contract upgradeability in Ethereum smart contracts, but introduce complex security challenges spanning initialization vulnerabilities, storage collisions, access control bypasses, implementation destruction, selector clashing, clone validation flaws, and metamorphic contract risks. These vulnerabilities can lead to complete protocol compromise, fund loss, or contract bricking across transparent proxies, UUPS (Universal Upgradeable Proxy Standard), beacon proxies, diamond patterns (EIP-2535), and minimal proxy clones.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of storage_layout_error"
- Pattern key: `storage_layout_error | proxy_contract_system | proxy_implementation`
- Interaction scope: `multi_contract`
- Primary affected component(s): `proxy_contract_system`
- High-signal code keywords: `UUPS_proxy`, `_authorizeUpgrade`, `_getImplementation`, `access_control`, `addToWhitelist`, `address`, `admin`, `approve`
- Typical sink / impact: `contract_takeover`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `BeaconDS.function -> CLGaugeFactory.function -> CustomProxy.function`
- Trust boundary crossed: `callback / external call`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Storage slot collision between proxy and implementation contracts
- Signal 2: Upgrade changes storage layout order, corrupting existing state
- Signal 3: Diamond proxy selector collision between facets
- Signal 4: Inherited contract storage layout breaks upgrade compatibility

#### False Positive Guards

- Not this bug when: Storage gaps used in all upgradeable base contracts
- Safe if: Upgrade tested with storage layout comparison tooling
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Proxy pattern vulnerabilities stem from the separation of contract logic (implementation) and state (proxy), combined with the use of delegatecall for forwarding calls. This architectural pattern creates multiple attack surfaces:

1. **Uninitialized Implementation Contracts**: Implementation contracts lack constructor-based initialization since constructors don't execute in delegatecall context, requiring initialize() functions that can be vulnerable to front-running or direct exploitation
2. **Storage Layout Misalignment**: Proxy and implementation contracts share storage space via delegatecall, but must maintain identical storage layouts - any mismatch causes state corruption
3. **Missing Storage Gaps**: Upgradeable base contracts without storage gaps prevent safe addition of new state variables in future versions
4. **Implementation Access Control**: Implementation contracts callable directly (not through proxy) may have unprotected critical functions
5. **Selector Clashing**: Malicious or accidental matching of function selectors between proxy and implementation can redirect execution
6. **Non-EIP1967 Compliance**: Custom storage slots for implementation address can collide with application storage
7. **Incorrect Library Versions**: Using non-upgradeable OpenZeppelin libraries in upgradeable contracts prevents proper initialization
8. **Unprotected UUPS Upgrade Functions**: Missing access control on _authorizeUpgrade allows anyone to upgrade
9. **Delegatecall Nonce Reset**: Delegatecall can reset initialization nonce, allowing re-initialization attacks
10. **Clone Validation Bypass**: Minimal proxy verification checking insufficient bytes allows malicious clones
11. **Metamorphic Implementation Risk**: Implementation contracts deployed via CREATE2 can be replaced with malicious code
12. **Module Upgrade State Loss**: Upgrading modules without migrating state locks all existing assets
13. **Persisted msg.value in Batch Delegatecalls**: Reusing msg.value across multiple delegatecalls drains funds
14. **Plugin Selector Collision**: Plugins with colliding selectors override legitimate functionality

---

## VULNERABILITY PATTERNS

---

### Pattern 1: Missing disableInitializers in Implementation Constructor

**Severity**: MEDIUM-HIGH | **Frequency**: Very Common (15+ reports)

```solidity
// ❌ VULNERABLE: Implementation contract constructor doesn't disable initializers
// Source: reports/proxy_findings/missing-disableinitializers-call-in-proxy-upgradeable-contract-constructor.md

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract VaultImplementation is Initializable, OwnableUpgradeable {
    uint256 public totalAssets;
    
    // ❌ VULNERABLE: No constructor with _disableInitializers()
    // Attacker can call initialize() directly on implementation
    
    function initialize(address _owner) public initializer {
        __Ownable_init();
        transferOwnership(_owner);
    }
}
```

**✅ SECURE:**
```solidity
contract SecureVaultImplementation is Initializable, OwnableUpgradeable {
    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();  // ✅ Prevents initialization on implementation
    }
    
    function initialize(address _owner) public initializer {
        __Ownable_init();
        transferOwnership(_owner);
    }
}
```

---

### Pattern 2: Implementation Destruction via Selfdestruct

**Severity**: HIGH-CRITICAL | **Frequency**: Common (8+ reports)

```solidity
// ❌ VULNERABLE: Anyone can destroy implementation contract
// Source: reports/proxy_findings/anyone-can-destroy-morphos-implementation.md
// Source: reports/proxy_findings/h-01-vault-implementation-can-be-destroyed-leading-to-loss-of-all-assets.md

contract MorphoImplementation is OwnableUpgradeable {
    IInterestRatesManager public interestRatesManager;
    
    function initialize() public initializer {
        __Ownable_init(); // Owner will be msg.sender on implementation
    }
    
    function setReserveFactor(address poolToken, uint16 newFactor) 
        external 
        onlyOwner  // ❌ Attacker becomes owner by calling initialize()
    {
        updateP2PIndexes(poolToken);
    }
    
    function updateP2PIndexes(address poolToken) public {
        // ❌ VULNERABLE: Delegatecall to user-controlled address
        address(interestRatesManager).functionDelegateCall(
            abi.encodeWithSelector(
                interestRatesManager.updateP2PIndexes.selector,
                poolToken
            )
        );
    }
}

// Attack flow:
// 1. Attacker calls initialize() directly on implementation
// 2. Attacker becomes owner of implementation contract
// 3. Attacker sets interestRatesManager to malicious contract with selfdestruct
// 4. Attacker calls setReserveFactor() → updateP2PIndexes()
// 5. Delegatecall executes selfdestruct
// 6. Implementation destroyed, ALL proxies bricked permanently
```

---

### Pattern 3: Unprotected UUPS Upgrade Function

**Severity**: HIGH-CRITICAL | **Frequency**: Common (10+ reports)

```solidity
// ❌ VULNERABLE: Anyone can upgrade the contract
// Source: reports/proxy_findings/h-01-wellupgradeable-can-be-upgraded-by-anyone.md

contract WellUpgradeable is UUPSUpgradeable, OwnableUpgradeable {
    
    function initialize(address _owner) public initializer {
        __Ownable_init();
        __UUPSUpgradeable_init();
        transferOwnership(_owner);
    }
    
    // ❌ VULNERABLE: Missing onlyOwner modifier!
    function _authorizeUpgrade(address newImplementation) internal view override {
        // Only checks delegatecall context, NOT authorization
        require(address(this) != ___self, "Must be delegatecall");
    }
}

// Attack: Anyone can call upgradeTo() and replace implementation with malicious contract
```

**✅ SECURE:**
```solidity
contract SecureWellUpgradeable is UUPSUpgradeable, OwnableUpgradeable {
    
    function _authorizeUpgrade(address newImplementation) 
        internal 
        view 
        override 
        onlyOwner  // ✅ Access control required
    {
        require(address(this) != ___self, "Must be delegatecall");
        require(newImplementation.code.length > 0, "Must be contract");
    }
}
```

---

### Pattern 4: No Storage Gap in Upgradeable Base Contract

**Severity**: MEDIUM | **Frequency**: Very Common (20+ reports)

```solidity
// ❌ VULNERABLE: Base contract has no storage gap
// Source: reports/proxy_findings/m-07-no-storage-gap-for-upgradeable-contracts.md

contract SimpleMarket {
    mapping(uint => Offer) public offers;  // Slot 0
    uint public lastOfferId;                // Slot 1
    // ❌ VULNERABLE: No storage gap
}

contract ExpiringMarket is SimpleMarket {
    bool public stopped;      // Slot 2
    uint64 public expiration; // Slot 2 (packed)
}

// Future upgrade of SimpleMarket:
contract SimpleMarketV2 {
    mapping(uint => Offer) public offers;  // Slot 0
    uint public lastOfferId;                // Slot 1
    uint256 public newFeature;              // Slot 2 ⚠️ OVERWRITES stopped!
}
// Result: ExpiringMarket.stopped silently corrupted
```

**✅ SECURE:**
```solidity
contract SimpleMarket {
    mapping(uint => Offer) public offers;
    uint public lastOfferId;
    
    // ✅ SECURE: Reserve 50 slots for future variables
    uint256[50] private __gap;
}
```

---

### Pattern 5: Storage Collision - Non-EIP1967 Implementation Slot

**Severity**: HIGH | **Frequency**: Common (6+ reports)

```solidity
// ❌ VULNERABLE: Implementation address stored at predictable slot
// Source: reports/proxy_findings/h-06-storage-collision-between-proxy-and-implementation-lack-eip-1967.md
// Source: reports/proxy_findings/risk-of-storage-collision-in-proxy-contract.md

contract CustomProxy is Ownable {
    address private _implement;  // Slot 1 (after Ownable._owner at slot 0)
    
    fallback() external payable {
        address impl = _implement;
        assembly {
            calldatacopy(0, 0, calldatasize())
            let result := delegatecall(gas(), impl, 0, calldatasize(), 0, 0)
            returndatacopy(0, 0, returndatasize())
            switch result
            case 0 { revert(0, returndatasize()) }
            default { return(0, returndatasize()) }
        }
    }
}

contract Implementation is Ownable {
    // _owner at slot 0 collides with proxy's _owner
    mapping(address => uint) public balances;  // Slot 1 collides with proxy's _implement!
}
```

**✅ SECURE:**
```solidity
contract EIP1967Proxy {
    // ✅ EIP-1967 standard slot - cannot collide with application storage
    bytes32 private constant _IMPLEMENTATION_SLOT = 
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
    
    function _getImplementation() internal view returns (address impl) {
        bytes32 slot = _IMPLEMENTATION_SLOT;
        assembly { impl := sload(slot) }
    }
}
```

---

### Pattern 6: Initialization Front-Running

**Severity**: HIGH | **Frequency**: Common (10+ reports)

```solidity
// ❌ VULNERABLE: Two-step deployment allows front-running
// Source: reports/proxy_findings/initialization-functions-can-be-front-run.md

// Deployment script (vulnerable pattern):
// Transaction 1: Deploy proxy
const proxy = await deploy("MyProxy", [implementationAddress]);

// Transaction 2: Initialize (SEPARATE transaction!)
await proxy.initialize(owner, rewardAddress, feeCollector);
// ❌ Attacker can front-run between tx1 and tx2

contract DeFiVault is Initializable {
    address public rewardDistributor;
    address public feeCollector;
    
    function initialize(address _owner, address _rewards, address _fees) 
        public 
        initializer 
    {
        transferOwnership(_owner);
        rewardDistributor = _rewards;  // ⚠️ Attacker sets their address
        feeCollector = _fees;          // ⚠️ Attacker sets their address
    }
}
```

**✅ SECURE:**
```solidity
// ✅ SECURE: Atomic deployment + initialization
const vault = await upgrades.deployProxy(
    VaultImplementation,
    [owner, rewardAddress, feeCollector],
    { initializer: 'initialize' }
);

// Or pass initialization data to proxy constructor
const proxy = new TransparentUpgradeableProxy(
    implementationAddress,
    proxyAdminAddress,
    abi.encodeCall(Implementation.initialize, (owner, rewards, fees))
);
```

---

### Pattern 7: Wrong Ownable Library in Upgradeable Contract

**Severity**: HIGH | **Frequency**: Common (5+ reports)

```solidity
// ❌ VULNERABLE: Using non-upgradeable Ownable in proxy pattern
// Source: reports/proxy_findings/h-01-usage-of-an-incorrect-version-of-ownbale-library-can-potentially-malfunctio.md

import "@openzeppelin/contracts/access/Ownable.sol";  // ❌ WRONG!
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";

contract DelegatedStaking is Ownable, Initializable {
    function initialize(uint128 _minStake) public initializer {
        // ❌ Ownable sets owner in constructor (never called in proxy)
        // Result: owner is address(0), all onlyOwner functions inaccessible
        minStakedRequired = _minStake;
    }
    
    function emergencyWithdraw() external onlyOwner {
        // ⚠️ CAN NEVER BE CALLED - funds permanently locked
    }
}
```

**✅ SECURE:**
```solidity
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract SecureStaking is OwnableUpgradeable, Initializable {
    function initialize(uint128 _minStake) public initializer {
        __Ownable_init();  // ✅ Sets owner via initializer
        minStakedRequired = _minStake;
    }
}
```

---

### Pattern 8: Delegatecall Nonce Reset Allowing Re-initialization

**Severity**: MEDIUM-HIGH | **Frequency**: Uncommon (3+ reports)

```solidity
// ❌ VULNERABLE: Delegatecall can reset nonce variable
// Source: reports/proxy_findings/m-01-delegate-call-in-vault_execute-can-alter-vaults-ownership.md

contract Vault is Initializable {
    address public owner;
    bytes32 public merkleRoot;
    uint256 public nonce;  // Used by Initializable to track initialization
    
    function init(address _owner, bytes32 _merkleRoot) external initializer {
        owner = _owner;
        merkleRoot = _merkleRoot;
    }
    
    function execute(address _target, bytes calldata _data, bytes32[] calldata _proof) 
        external 
        returns (bool, bytes memory) 
    {
        // Check authorization...
        address owner_ = owner;
        
        // ❌ VULNERABLE: Delegatecall can modify ANY storage including nonce
        (bool success, bytes memory response) = _target.delegatecall(_data);
        
        // Only checks owner wasn't changed
        if (owner_ != owner) revert OwnerChanged();
        // ⚠️ But doesn't check if nonce was reset to 0!
        
        return (success, response);
    }
}

// Attack: Delegatecall to contract that resets slot where nonce is stored
// Result: init() becomes callable again, attacker takes ownership
```

**✅ SECURE:**
```solidity
function execute(address _target, bytes calldata _data, bytes32[] calldata _proof) 
    external 
    returns (bool, bytes memory) 
{
    address owner_ = owner;
    uint256 nonce_ = nonce;  // ✅ Cache nonce too
    
    (bool success, bytes memory response) = _target.delegatecall(_data);
    
    if (owner_ != owner) revert OwnerChanged();
    if (nonce_ != nonce) revert NonceChanged();  // ✅ Check nonce
    
    return (success, response);
}
```

---

### Pattern 9: Constructor State Not Available in Proxy

**Severity**: HIGH | **Frequency**: Common (5+ reports)

```solidity
// ❌ VULNERABLE: Constructor sets state, but proxy never sees it
// Source: reports/proxy_findings/h-04-the-constructor-caveat-leads-to-bricking-of-configurator-contract.md

contract LybraConfigurator {
    address public governance;
    address public curvePool;
    
    // ❌ VULNERABLE: Constructor state only exists in implementation, not proxy
    constructor(address _governance, address _curvePool) {
        governance = _governance;
        curvePool = _curvePool;
    }
    
    function initToken(address eusd, address peUsd) external {
        // ❌ governance is address(0) in proxy - this always reverts
        require(msg.sender == governance, "Not governance");
        // ...
    }
}

// Proxy delegates to implementation but has its own storage
// Constructor ran on implementation's storage, not proxy's
// Result: governance = address(0) in proxy, all governance functions broken
```

**✅ SECURE:**
```solidity
contract SecureConfigurator is Initializable {
    address public governance;
    address public curvePool;
    
    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();
    }
    
    // ✅ SECURE: Use initializer instead of constructor
    function initialize(address _governance, address _curvePool) 
        external 
        initializer 
    {
        governance = _governance;
        curvePool = _curvePool;
    }
}
```

---

### Pattern 10: Clone Validation Checking Insufficient Bytes

**Severity**: CRITICAL | **Frequency**: Uncommon (2+ reports)

```solidity
// ❌ VULNERABLE: Only checks first 54 bytes of clone
// Source: reports/proxy_findings/clones-with-malicious-extradata-are-also-considered-valid-clones.md

function isETHPairClone(address implementation, address query) 
    internal 
    view 
    returns (bool result) 
{
    assembly {
        let ptr := mload(0x40)
        mstore(ptr, /* expected bytecode prefix */)
        
        let other := add(ptr, 0x40)
        extcodecopy(query, other, 0, 0x36)  // Only copies 54 bytes!
        
        result := and(
            eq(mload(ptr), mload(other)),
            eq(mload(add(ptr, 0x16)), mload(add(other, 0x16)))
        )
        // ❌ VULNERABLE: Only checks proxy code prefix
        // Does NOT verify factory, bondingCurve, nft, poolType parameters!
    }
}

// Attack:
// 1. Attacker deploys clone with valid 54-byte prefix but malicious extradata
// 2. Clone passes isPair() validation
// 3. Attacker calls pairTransferERC20From() - router trusts malicious clone
// 4. Attacker steals tokens from users who approved router
```

**✅ SECURE:**
```solidity
function isValidPair(address implementation, address query) 
    internal 
    view 
    returns (bool) 
{
    // ✅ Check full clone bytecode including immutable args
    bytes32 expectedHash = keccak256(
        abi.encodePacked(
            CLONE_PREFIX,
            implementation,
            CLONE_SUFFIX,
            expectedFactory,
            expectedBondingCurve,
            expectedNft,
            expectedPoolType
        )
    );
    
    return query.codehash == expectedHash;
}
```

---

### Pattern 11: Metamorphic Implementation Contract Risk

**Severity**: MEDIUM-HIGH | **Frequency**: Uncommon (3+ reports)

```solidity
// ❌ VULNERABLE: Implementation deployed via CREATE2 can be replaced
// Source: reports/proxy_findings/implementations-of-clones-could-be-metamorphic-and-lead-to-exploit.md

contract CLGaugeFactory {
    address public implementation;
    
    constructor(address _impl) {
        // ❌ VULNERABLE: If _impl was deployed via CREATE2 and can be 
        // selfdestructed, attacker can redeploy malicious code at same address
        implementation = _impl;
    }
    
    function createGauge() external returns (address) {
        return Clones.clone(implementation);
        // All clones delegate to implementation
        // If implementation is replaced with malicious code, all clones compromised
    }
}

// Metamorphic attack:
// 1. Deploy implementation via CREATE2 with factory that can selfdestruct
// 2. Wait for many clones to be created
// 3. Selfdestruct implementation
// 4. Redeploy malicious code at same address via CREATE2 (same salt)
// 5. All existing clones now delegate to malicious implementation
```

**✅ SECURE:**
```solidity
contract SecureGaugeFactory {
    address public immutable implementation;
    bytes32 public immutable implementationCodehash;
    
    constructor(address _impl) {
        // ✅ Verify implementation is not metamorphic
        require(!isMetamorphic(_impl), "Metamorphic impl");
        
        implementation = _impl;
        implementationCodehash = _impl.codehash;
    }
    
    function isMetamorphic(address addr) internal view returns (bool) {
        // Check for metamorphic indicators:
        // - Deployed by CREATE2
        // - Contains SELFDESTRUCT or DELEGATECALL opcodes
        // - Deployer is a factory contract
        // Use tools like metamorphic-contract-detector
    }
}
```

---

### Pattern 12: Plugin Selector Collision Override

**Severity**: HIGH | **Frequency**: Uncommon (2+ reports)

```solidity
// ❌ VULNERABLE: Plugin selectors can collide and override each other
// Source: reports/proxy_findings/plugins-can-be-maliciously-overridden-by-colliding-signatures.md

contract PRBProxyAnnex {
    // Plugins mapped by 4-byte selector
    mapping(bytes4 method => IPRBProxyPlugin plugin) public plugins;
    
    function installPlugin(IPRBProxyPlugin plugin) external {
        bytes4[] memory methodList = plugin.methodList();
        
        for (uint256 i = 0; i < methodList.length; i++) {
            // ❌ VULNERABLE: Silently overwrites existing plugin
            plugins[methodList[i]] = plugin;
        }
    }
}

// Attack on Sablier integration:
// 1. Legitimate plugin handles onStreamCanceled (selector 0xabc12345)
// 2. Attacker creates "InnocentLookingPlugin" with function that has same selector:
//    function onAddictionFeesRefunded(...) // selector 0xabc12345 (collision!)
// 3. Attacker installs malicious plugin - overrides legitimate one
// 4. When stream is canceled, attacker's function executes instead
// 5. Attacker steals refund tokens meant for legitimate users
```

**✅ SECURE:**
```solidity
function installPlugin(IPRBProxyPlugin plugin) external {
    bytes4[] memory methodList = plugin.methodList();
    
    for (uint256 i = 0; i < methodList.length; i++) {
        bytes4 selector = methodList[i];
        
        // ✅ SECURE: Prevent overwriting existing plugins
        require(
            address(plugins[selector]) == address(0),
            "Plugin already installed for selector"
        );
        
        plugins[selector] = plugin;
    }
}
```

---

### Pattern 13: Persisted msg.value in Batch Delegatecalls

**Severity**: MEDIUM-HIGH | **Frequency**: Uncommon (3+ reports)

```solidity
// ❌ VULNERABLE: msg.value reused across multiple delegatecalls
// Source: reports/proxy_findings/m-04-persisted-msgvalue-in-a-loop-of-delegate-calls-can-be-used-to-drain-eth-fro.md

contract MIMOProxy {
    // Inherits BoringBatchable
    
    function batch(bytes[] calldata calls, bool revertOnFail) 
        external 
        payable  // ❌ VULNERABLE: Accepts ETH
    {
        for (uint256 i = 0; i < calls.length; i++) {
            // ❌ Each delegatecall sees the SAME msg.value!
            (bool success, bytes memory result) = address(this).delegatecall(calls[i]);
            if (!success && revertOnFail) {
                revert(string(result));
            }
        }
    }
    
    function execute(address target, bytes calldata data) 
        external 
        payable  // ❌ Also payable
        returns (bytes memory)
    {
        // msg.value is same for ALL batch iterations
        return target.functionCallWithValue(data, msg.value);
    }
}

// Attack:
// 1. Proxy has 100 ETH balance from deposits
// 2. Attacker calls batch() with 1 ETH and array of 100 execute() calls
// 3. Each execute() sends 1 ETH from proxy's balance (not attacker's!)
// 4. Attacker drains 100 ETH by sending only 1 ETH
```

**✅ SECURE:**
```solidity
function batch(bytes[] calldata calls, bool revertOnFail) 
    external  // ✅ Remove payable from batch
{
    for (uint256 i = 0; i < calls.length; i++) {
        (bool success, bytes memory result) = address(this).delegatecall(calls[i]);
        if (!success && revertOnFail) {
            revert(string(result));
        }
    }
}
```

---

### Pattern 14: Module Upgrade Without State Migration

**Severity**: MEDIUM-HIGH | **Frequency**: Uncommon (3+ reports)

```solidity
// ❌ VULNERABLE: Module upgrade doesn't migrate state or assets
// Source: reports/proxy_findings/m-07-upgrading-modules-via-executeaction-will-brick-all-existing-rentals.md

contract Kernel {
    function executeAction(Actions action, address target) external {
        if (action == Actions.UpgradeModule) {
            Module oldModule = getModule[moduleKeycode];
            
            // Deactivate old module
            oldModule.deactivate();
            
            // Install new module
            Module newModule = Module(target);
            newModule.initialize(address(this));
            getModule[moduleKeycode] = newModule;
            
            // ❌ VULNERABLE: No state migration!
            // Old module still holds all rental data and escrowed funds
            // New module has empty state
            // All existing rentals cannot be stopped - assets locked forever
        }
    }
}

// Impact:
// 1. PaymentEscrow holds user deposits
// 2. Kernel upgrades PaymentEscrow module
// 3. New module deployed with empty state
// 4. Old module is deactivated, cannot process withdrawals
// 5. All escrowed funds permanently locked
```

**✅ SECURE:**
```solidity
contract SecureKernel {
    function executeAction(Actions action, address target, bytes calldata migrationData) 
        external 
    {
        if (action == Actions.UpgradeModule) {
            Module oldModule = getModule[moduleKeycode];
            Module newModule = Module(target);
            
            // ✅ SECURE: Migrate state before deactivation
            if (migrationData.length > 0) {
                newModule.migrateFrom(address(oldModule), migrationData);
            }
            
            // ✅ Transfer any held assets
            oldModule.transferAssetsTo(address(newModule));
            
            oldModule.deactivate();
            newModule.initialize(address(this));
            getModule[moduleKeycode] = newModule;
        }
    }
}
```

---

### Pattern 15: Storage Layout Change on Upgrade Breaks Roles

**Severity**: HIGH | **Frequency**: Uncommon (2+ reports)

```solidity
// ❌ VULNERABLE: Upgrade changes storage layout, corrupting access control
// Source: reports/proxy_findings/h-01-lost-roles-after-the-proxy-upgrade.md

// Current version (deployed):
contract GNSMultiCollatDiamond {
    // Slot 0-1: Initializable
    // Slot 2: accessControl mapping <-- CURRENT LOCATION
    struct Addresses {
        address gns;  // Slot 2
    }
    mapping(address => mapping(Role => bool)) accessControl;  // Slot 3
}

// New version (upgrade):
contract GNSMultiCollatDiamondV2 {
    // Slot 0-1: Initializable
    struct Addresses {
        address gns;         // Slot 2
        address gnsStaking;  // Slot 3 ⚠️ NEW
        address linkErc677;  // Slot 4 ⚠️ NEW
    }
    mapping(address => mapping(Role => bool)) accessControl;  // Slot 5 ⚠️ MOVED!
}

// Result: accessControl moved from slot 3 to slot 5
// All role assignments are lost
// All role-gated functions become inaccessible
```

**✅ SECURE:**
```solidity
contract GNSMultiCollatDiamondV2 {
    struct Addresses {
        address gns;  // Keep at original position
    }
    mapping(address => mapping(Role => bool)) accessControl;  // Keep at slot 3
    
    // ✅ Add new variables AFTER existing ones
    address public gnsStaking;   // Slot 4
    address public linkErc677;   // Slot 5
    
    uint256[47] private __gap;  // Reserve remaining slots
}
```

---

### Pattern 16: Missing Contract Existence Check Before Delegatecall

**Severity**: MEDIUM | **Frequency**: Common (5+ reports)

```solidity
// ❌ VULNERABLE: Delegatecall to address with no code silently succeeds
// Source: reports/proxy_findings/lack-of-contract-existence-check-on-delegatecall-will-result-in-unexpected-behav.md

contract ProxyWithDelegatecall {
    address public implementation;
    
    function execute(bytes memory data) external returns (bytes memory) {
        // ❌ VULNERABLE: No check if implementation has code
        (bool success, bytes memory result) = implementation.delegatecall(data);
        require(success, "Delegatecall failed");
        return result;
    }
    
    // If implementation is:
    // - address(0)
    // - EOA
    // - Contract that was selfdestructed
    // Delegatecall returns success=true but does nothing!
}
```

**✅ SECURE:**
```solidity
function execute(bytes memory data) external returns (bytes memory) {
    require(implementation != address(0), "Implementation not set");
    require(implementation.code.length > 0, "Implementation not a contract");
    
    (bool success, bytes memory result) = implementation.delegatecall(data);
    require(success, "Delegatecall failed");
    return result;
}
```

---

### Pattern 17: Proxy Shadowing Implementation Functions

**Severity**: MEDIUM | **Frequency**: Uncommon (2+ reports)

```solidity
// ❌ VULNERABLE: Proxy has public methods that shadow implementation
// Source: reports/proxy_findings/proxy-has-public-methods-that-shadow-implementation.md

contract TransparentProxy {
    address public admin;
    address public implementation;
    
    // ❌ VULNERABLE: These public getters can be called by anyone
    // If implementation has functions with same selectors, they're shadowed
    
    function admin() external view returns (address) {
        return admin;
    }
    
    function implementation() external view returns (address) {
        return implementation;
    }
    
    fallback() external payable {
        // Only forwards if caller is not admin
        if (msg.sender != admin) {
            _delegate(implementation);
        }
    }
}

// Problem: User calls admin() expecting implementation's admin function
// Instead gets proxy's admin - completely different result
```

**✅ SECURE:**
```solidity
contract SecureTransparentProxy {
    // ✅ Use EIP-1967 slots and no public getters
    bytes32 private constant _ADMIN_SLOT = 
        0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103;
    
    // Admin functions only callable by admin via ifAdmin modifier
    modifier ifAdmin() {
        if (msg.sender == _getAdmin()) {
            _;
        } else {
            _delegate(_getImplementation());
        }
    }
    
    // No public getters that could shadow implementation functions
}
```

---

### Pattern 18: Permissions/Allowances Not Reset on Proxy Ownership Transfer

**Severity**: MEDIUM-HIGH | **Frequency**: Uncommon (3+ reports)

```solidity
// ❌ VULNERABLE: Permissions and allowances persist after ownership transfer
// Source: reports/proxy_findings/permission-and-plugins-not-reset-on-proxy-ownership-transfer.md
// Source: reports/proxy_findings/token-allowances-stay-in-effect-on-proxy-ownership-transfer.md

contract PRBProxyRegistry {
    // Plugins and permissions stored per proxy
    mapping(bytes4 => IPRBProxyPlugin) public plugins;
    mapping(address => mapping(address => bool)) public permissions;
    
    function transferOwnership(address newOwner) external onlyOwner {
        // ❌ VULNERABLE: Only transfers ownership
        owner = newOwner;
        // plugins mapping stays intact
        // permissions mapping stays intact
        // ERC20 token approvals stay intact
    }
}

// Attack scenario:
// 1. Alice owns proxy with installed plugins and permissions
// 2. Alice sells/transfers proxy to Bob
// 3. Alice's malicious plugin still installed - can execute arbitrary code
// 4. Alice's ERC20 approvals still valid - can drain Bob's tokens via approved contracts
// 5. Alice still has envoy permissions - can call targets on Bob's behalf
```

**✅ SECURE:**
```solidity
function transferOwnership(address newOwner) external onlyOwner {
    // ✅ Reset all plugins
    _clearAllPlugins();
    
    // ✅ Reset all permissions
    _clearAllPermissions();
    
    // ✅ Revoke token approvals (or warn new owner)
    _revokeCommonTokenApprovals();
    
    owner = newOwner;
}
```

---

### Pattern 19: Temporary Owner Change During Delegatecall

**Severity**: HIGH | **Frequency**: Uncommon (2+ reports)

```solidity
// ❌ VULNERABLE: Owner can be changed during delegatecall execution
// Source: reports/proxy_findings/owner-can-be-temporarily-changed-within-proxy-calls-allowing-complete-control-of.md

contract PRBProxy {
    address public owner;
    
    function execute(address target, bytes calldata data) 
        external 
        onlyOwner 
        returns (bytes memory) 
    {
        // ❌ VULNERABLE: delegatecall can modify owner storage slot
        (bool success, bytes memory result) = target.delegatecall(data);
        
        // Owner could have been changed during delegatecall
        // Attacker temporarily becomes owner, performs malicious actions
        // Then restores original owner to hide attack
        
        require(success, "Call failed");
        return result;
    }
}

// Attack:
// 1. Legitimate owner calls execute() with malicious target
// 2. Target changes owner to attacker via delegatecall storage modification
// 3. Attacker (now temporary owner) drains funds, installs backdoors
// 4. Target restores original owner
// 5. Original owner unaware of theft
```

**✅ SECURE:**
```solidity
function execute(address target, bytes calldata data) 
    external 
    onlyOwner 
    returns (bytes memory) 
{
    address ownerBefore = owner;
    
    (bool success, bytes memory result) = target.delegatecall(data);
    
    // ✅ Verify owner unchanged
    require(owner == ownerBefore, "Owner changed during call");
    
    require(success, "Call failed");
    return result;
}
```

---

### Pattern 20: Proxy Reuse Without Implementation Version Check

**Severity**: MEDIUM | **Frequency**: Uncommon (2+ reports)

```solidity
// ❌ VULNERABLE: Reusing old proxy clones without checking implementation version
// Source: reports/proxy_findings/proxy-reuse-without-implementation-check-inside-unstakecooldown-leads-to-executi.md

contract UnstakeCooldown {
    mapping(address => address) public implementations;
    mapping(address => address[]) public userProxyPools;
    
    function processTransfer(address user, address token) external {
        address[] storage pool = userProxyPools[user];
        
        if (pool.length > 0) {
            // ❌ VULNERABLE: Reuses old proxy without checking implementation
            address proxy = pool[pool.length - 1];
            pool.pop();
            
            // This proxy might point to old/vulnerable implementation!
            IProxy(proxy).execute(token);
        } else {
            // Create new proxy with current implementation
            address proxy = Clones.clone(implementations[token]);
            IProxy(proxy).execute(token);
        }
    }
    
    function setImplementation(address token, address newImpl) external onlyOwner {
        // Updates implementation, but pooled proxies still use old one
        implementations[token] = newImpl;
    }
}

// Impact:
// 1. Implementation V1 has bug
// 2. Owner upgrades to V2 (bug fixed)
// 3. User with pooled V1 proxies continues using vulnerable version
// 4. Inconsistent behavior across users
```

**✅ SECURE:**
```solidity
function processTransfer(address user, address token) external {
    address currentImpl = implementations[token];
    address[] storage pool = userProxyPools[user];
    
    if (pool.length > 0) {
        address proxy = pool[pool.length - 1];
        
        // ✅ Verify proxy uses current implementation
        if (_getProxyImplementation(proxy) == currentImpl) {
            pool.pop();
            IProxy(proxy).execute(token);
            return;
        }
        // Old implementation - discard and create new
    }
    
    address proxy = Clones.clone(currentImpl);
    IProxy(proxy).execute(token);
}
```

---

### Pattern 21: CREATE2 Salt Predictability/Front-Running

**Severity**: MEDIUM-HIGH | **Frequency**: Common (5+ reports)

```solidity
// ❌ VULNERABLE: CREATE2 salt based only on tx.origin, not owner
// Source: reports/proxy_findings/create2-salt-based-on-txorigin-alone.md
// Source: reports/proxy_findings/issues-with-create2-salt-in-supervaultaggregatorcreatevault.md
// Source: reports/proxy_findings/deploychain-calls-can-be-front-run-to-deny-chain-deployments.md

contract ProxyRegistry {
    mapping(address => uint256) public nonces;
    
    function deployFor(address owner) external returns (address proxy) {
        // ❌ VULNERABLE: Salt only uses tx.origin and nonce
        bytes32 salt = keccak256(abi.encode(tx.origin, nonces[tx.origin]++));
        
        proxy = address(new PRBProxy{salt: salt}(owner));
        // Problem: Anyone can front-run and use up the nonce
        // Problem: Meta-transaction relayers can hijack predicted addresses
    }
    
    function predict(address deployer) external view returns (address) {
        bytes32 salt = keccak256(abi.encode(deployer, nonces[deployer]));
        return _computeCreate2Address(salt);
    }
}

// Attack scenarios:
// 1. Relayer predicts address for Alice, Alice signs meta-tx
// 2. Bob front-runs with same deployer, gets Alice's predicted address
// 3. Alice's signature now points to Bob's proxy
```

**✅ SECURE:**
```solidity
function deployFor(address owner) external returns (address proxy) {
    // ✅ Include owner in salt to prevent address hijacking
    bytes32 salt = keccak256(abi.encode(
        owner,           // Owner address
        msg.sender,      // Actual caller (not tx.origin)
        nonces[owner]++  // Per-owner nonce
    ));
    
    proxy = address(new PRBProxy{salt: salt}(owner));
}
```

---

### Pattern 22: Counterfactual Wallet Deployment Hijacking

**Severity**: HIGH | **Frequency**: Uncommon (3+ reports)

```solidity
// ❌ VULNERABLE: Entrypoint not included in address generation
// Source: reports/proxy_findings/h-03-attacker-can-gain-control-of-counterfactual-wallet.md

contract SmartAccountFactory {
    function getAddressForCounterfactualWallet(
        address owner,
        uint256 index
    ) external view returns (address) {
        // ❌ VULNERABLE: Address doesn't depend on entrypoint
        bytes32 salt = keccak256(abi.encode(owner, index));
        return _computeCreate2Address(salt);
    }
    
    function deployCounterfactualWallet(
        address owner,
        address entryPoint,  // ⚠️ Attacker can provide any entrypoint!
        uint256 index
    ) external returns (address) {
        bytes32 salt = keccak256(abi.encode(owner, index));
        
        // Attacker deploys with malicious entrypoint at predicted address
        return address(new SmartWallet{salt: salt}(owner, entryPoint));
    }
}

// Attack:
// 1. User pre-generates wallet address and funds it
// 2. Attacker calls deployCounterfactualWallet with malicious entrypoint
// 3. Wallet deployed at correct address but controlled by attacker's entrypoint
// 4. Attacker drains pre-funded assets
```

**✅ SECURE:**
```solidity
function getAddressForCounterfactualWallet(
    address owner,
    address entryPoint,  // ✅ Include entrypoint in prediction
    uint256 index
) external view returns (address) {
    bytes32 salt = keccak256(abi.encode(owner, entryPoint, index));
    return _computeCreate2Address(salt);
}

function deployCounterfactualWallet(
    address owner,
    address entryPoint,
    uint256 index
) external returns (address) {
    // ✅ Same entrypoint must be used for deployment
    bytes32 salt = keccak256(abi.encode(owner, entryPoint, index));
    return address(new SmartWallet{salt: salt}(owner, entryPoint));
}
```

---

### Pattern 23: Variable Initialization at Declaration in Upgradeable Contract

**Severity**: MEDIUM | **Frequency**: Common (5+ reports)

```solidity
// ❌ VULNERABLE: Variables initialized at declaration, not in initialize()
// Source: reports/proxy_findings/incorrect-proxy-implementation-by-declaring-initial-values-in-storage.md
// Source: reports/proxy_findings/blast-is-conﬁgured-in-the-implementation-contract-constructor-not-the-proxy.md

contract StreamedVesting is Initializable {
    // ❌ VULNERABLE: These values set in implementation bytecode
    // Proxy storage will have default values (0, address(0))
    address public dead = address(0xdead);
    uint256 public duration = 3 * 30 days;  // 90 days
    
    function initialize() external initializer {
        // dead and duration NOT set here
        // Proxy sees duration = 0, not 90 days!
    }
    
    function penalty(uint256 startTime, uint256 nowTime) public view returns (uint256) {
        // ❌ BUG: duration is 0 in proxy, so no penalty ever applies
        if (nowTime > startTime + duration) return 0;  // Always true!
        // ...
    }
}
```

**✅ SECURE:**
```solidity
contract SecureStreamedVesting is Initializable {
    address public dead;
    uint256 public duration;
    
    function initialize() external initializer {
        // ✅ Set values in initialize(), not at declaration
        dead = address(0xdead);
        duration = 3 * 30 days;
    }
}
```

---

### Pattern 24: Beacon Implementation Without Contract Existence Check

**Severity**: MEDIUM-HIGH | **Frequency**: Uncommon (2+ reports)

```solidity
// ❌ VULNERABLE: Beacon doesn't verify implementation exists
// Source: reports/proxy_findings/beaconds-can-create-broken-margin-accounts-via-an-undeployed-account-implementat.md

contract BeaconDS {
    bytes32 constant IMPLEMENTATION_SLOT = keccak256("beacon.implementation");
    
    function setImplementation(address newImplementation) external onlyOwner {
        // ❌ VULNERABLE: Only checks non-zero, not contract existence
        if (newImplementation == address(0)) revert ImplementationAddressIsZero();
        if (_implementation() == newImplementation) revert AlreadyUpToDate();
        
        assembly {
            sstore(IMPLEMENTATION_SLOT, newImplementation)
        }
        // If deployment to newImplementation fails silently, all proxies break
    }
}

// Exploit scenario:
// 1. Owner updates implementation to new address (deployment pending)
// 2. Deployment transaction fails/reverts
// 3. Implementation slot points to address with no code
// 4. All beacon proxy calls succeed silently but do nothing
// 5. Critical state changes lost, funds potentially stuck
```

**✅ SECURE:**
```solidity
function setImplementation(address newImplementation) external onlyOwner {
    require(newImplementation != address(0), "Zero address");
    require(newImplementation.code.length > 0, "No code at address");  // ✅ Check code exists
    require(_implementation() != newImplementation, "Already set");
    
    assembly {
        sstore(IMPLEMENTATION_SLOT, newImplementation)
    }
}
```

---

### Pattern 25: Approval Set in Constructor for Proxy Contract

**Severity**: MEDIUM | **Frequency**: Uncommon (3+ reports)

```solidity
// ❌ VULNERABLE: Approval set in constructor, not available to proxy
// Source: reports/proxy_findings/cross-chain-token-transfer-from-spokevault-fails-due-to-approval-from-implementa.md

contract SpokeVault {
    address public mToken;
    address public spokePortal;
    
    constructor(address _mToken, address _spokePortal) {
        mToken = _mToken;
        spokePortal = _spokePortal;
        
        // ❌ VULNERABLE: This approval is on IMPLEMENTATION, not proxy
        IERC20(mToken).approve(spokePortal, type(uint256).max);
    }
    
    function transferExcessM(uint256 amount) external {
        // This fails! Proxy never has the approval
        // Tokens stuck in proxy forever
        ISpokePortal(spokePortal).transfer(mToken, amount);
    }
}

// Deployed as:
// proxy = new TransparentUpgradeableProxy(
//     address(new SpokeVault(mToken, spokePortal)),
//     admin,
//     ""  // No initialization!
// );
// Result: proxy has tokens but can't transfer them
```

**✅ SECURE:**
```solidity
contract SecureSpokeVault is Initializable {
    address public mToken;
    address public spokePortal;
    
    constructor() {
        _disableInitializers();
    }
    
    function initialize(address _mToken, address _spokePortal) external initializer {
        mToken = _mToken;
        spokePortal = _spokePortal;
        
        // ✅ Approval set via proxy's context
        IERC20(mToken).approve(spokePortal, type(uint256).max);
    }
}
```

---

### Pattern 26: Proxy Cannot Redeploy After Selfdestruct

**Severity**: MEDIUM | **Frequency**: Uncommon (2+ reports)

```solidity
// ❌ VULNERABLE: Destroyed proxy address permanently blocked in registry
// Source: reports/proxy_findings/m-08-if-a-mimoproxy-owner-destroys-their-proxy-they-cannot-deploy-another-from-t.md

contract MIMOProxyRegistry {
    mapping(address => IMIMOProxy) public _currentProxies;
    
    function deployFor(address owner) public returns (IMIMOProxy proxy) {
        IMIMOProxy currentProxy = _currentProxies[owner];
        
        // ❌ VULNERABLE: If proxy was selfdestructed, this call reverts
        if (address(currentProxy) != address(0) && currentProxy.owner() == owner) {
            revert PROXY_ALREADY_EXISTS(owner);
        }
        
        // Deploy never reached if destroyed proxy exists in mapping
        proxy = factory.deployFor(owner);
        _currentProxies[owner] = proxy;
    }
}

// Scenario:
// 1. User deploys proxy, address stored in _currentProxies
// 2. User accidentally triggers selfdestruct on their proxy
// 3. Proxy destroyed but mapping still has address
// 4. currentProxy.owner() reverts (no code)
// 5. User permanently blocked from deploying new proxy
```

**✅ SECURE:**
```solidity
function deployFor(address owner) public returns (IMIMOProxy proxy) {
    IMIMOProxy currentProxy = _currentProxies[owner];
    
    if (address(currentProxy) != address(0)) {
        // ✅ Check if proxy still has code (not selfdestructed)
        if (address(currentProxy).code.length > 0) {
            // Safe to call - proxy exists
            if (currentProxy.owner() == owner) {
                revert PROXY_ALREADY_EXISTS(owner);
            }
        }
        // Proxy was destroyed - allow new deployment
    }
    
    proxy = factory.deployFor(owner);
    _currentProxies[owner] = proxy;
}
```

---

### Pattern 27: Whitelist Bypass via Upgradeable Proxy

**Severity**: MEDIUM | **Frequency**: Uncommon (2+ reports)

```solidity
// ❌ VULNERABLE: Whitelisted proxy can be upgraded to malicious implementation
// Source: reports/proxy_findings/whitelist-is-incompatible-with-proxies.md

contract TrustedContractWhitelist {
    mapping(address => bool) public isWhitelisted;
    
    function addToWhitelist(address contractAddr) external onlyOwner {
        // ❌ VULNERABLE: No check if contract is upgradeable
        isWhitelisted[contractAddr] = true;
    }
    
    function executeOnWhitelisted(address target, bytes calldata data) external {
        require(isWhitelisted[target], "Not whitelisted");
        
        // If target is a proxy, owner can upgrade to malicious implementation
        // Whitelist check passes but execution is now malicious
        (bool success, ) = target.call(data);
        require(success);
    }
}

// Attack:
// 1. USDC (proxy) whitelisted as safe token contract
// 2. Circle upgrades USDC (legitimate or compromised)
// 3. New implementation has backdoor/different behavior
// 4. All interactions with "trusted" USDC now exploitable
```

**✅ SECURE:**
```solidity
contract SecureWhitelist {
    mapping(address => bool) public isWhitelisted;
    mapping(address => bytes32) public whitelistedCodehash;
    
    function addToWhitelist(address contractAddr) external onlyOwner {
        require(!_isProxy(contractAddr), "Cannot whitelist proxies");
        
        isWhitelisted[contractAddr] = true;
        whitelistedCodehash[contractAddr] = contractAddr.codehash;
    }
    
    function executeOnWhitelisted(address target, bytes calldata data) external {
        require(isWhitelisted[target], "Not whitelisted");
        // ✅ Verify code hasn't changed (detect upgrades)
        require(target.codehash == whitelistedCodehash[target], "Code changed");
        
        (bool success, ) = target.call(data);
        require(success);
    }
}
```

---

### Pattern 28: Re-Initializable Proxy Due to Missing Modifier

**Severity**: HIGH-CRITICAL | **Frequency**: Common (8+ reports)

```solidity
// ❌ VULNERABLE: Initialize can be called multiple times
// Source: reports/proxy_findings/c-01-anyone-can-re-initialize-the-swapproxy.md

contract SwapImpl {
    address public router;
    address public permit2;
    
    // ❌ VULNERABLE: No initializer modifier, no access control
    function initialize(
        address _universalRouter,
        address _permit2,
        address _weth
    ) external {
        // Can be called by anyone, multiple times!
        router = _universalRouter;
        permit2 = _permit2;
    }
}

// Attack:
// 1. Legitimate deployment initializes with correct addresses
// 2. Attacker calls initialize() again with malicious router/permit2
// 3. All swaps now route through attacker's contracts
// 4. Attacker steals all tokens passing through
```

**✅ SECURE:**
```solidity
contract SecureSwapImpl is Initializable {
    address public router;
    address public permit2;
    
    function initialize(
        address _universalRouter,
        address _permit2,
        address _weth
    ) external initializer {  // ✅ Can only be called once
        router = _universalRouter;
        permit2 = _permit2;
    }
}
```

---

## Impact Analysis

### Technical Impact

**Immediate Contract State Effects:**
- **Complete Protocol Takeover**: Unprotected initialize() or upgrade functions allow attackers to gain admin privileges
- **Implementation Destruction**: selfdestruct permanently bricks all dependent proxies with no recovery
- **Storage Corruption**: Layout misalignment corrupts security flags and accounting
- **Function Redirection**: Selector clashing and plugin override redirect execution to attacker code
- **Permanent Lock**: Wrong library versions result in address(0) owner, permanent function inaccessibility
- **Clone Exploitation**: Insufficient clone validation allows malicious clones to steal approved tokens
- **State Loss**: Module upgrades without migration lock all existing assets

### Business Impact

**Financial Consequences:**
- **Total Fund Loss**: Implementation destruction locks all funds permanently
- **Gradual Drainage**: Malicious initialization extracts value via fee/reward redirects
- **Upgrade Failure**: Missing storage gaps force redeployment, losing all state
- **Governance Capture**: Unauthorized upgrades install malicious logic

### Severity Distribution from Reports

| Pattern | Severity | Frequency |
|---------|----------|-----------|
| Implementation Destruction | CRITICAL-HIGH | 8+ reports |
| Unprotected UUPS Upgrade | HIGH | 10+ reports |
| Missing disableInitializers | MEDIUM-HIGH | 15+ reports |
| Storage Collision | HIGH | 6+ reports |
| No Storage Gap | MEDIUM | 20+ reports |
| Initialization Front-run | HIGH | 10+ reports |
| Wrong Library Version | HIGH | 5+ reports |
| Clone Validation Bypass | CRITICAL | 2+ reports |
| Metamorphic Risk | MEDIUM-HIGH | 3+ reports |
| Plugin Collision | HIGH | 2+ reports |
| msg.value Reuse | MEDIUM-HIGH | 3+ reports |
| State Loss on Upgrade | MEDIUM-HIGH | 3+ reports |
| Permissions Not Reset on Transfer | MEDIUM-HIGH | 3+ reports |
| Temporary Owner Change | HIGH | 2+ reports |
| Proxy Reuse (Wrong Implementation) | MEDIUM | 2+ reports |
| CREATE2 Salt Predictability | MEDIUM-HIGH | 5+ reports |
| Counterfactual Wallet Hijacking | HIGH | 3+ reports |
| Variables at Declaration | MEDIUM | 5+ reports |
| Beacon No Code Check | MEDIUM-HIGH | 2+ reports |
| Constructor Approval (No Proxy) | MEDIUM | 3+ reports |
| Selfdestruct Blocks Redeploy | MEDIUM | 2+ reports |
| Whitelist Bypass via Upgrade | MEDIUM | 2+ reports |
| Re-Initializable (Missing Modifier) | HIGH-CRITICAL | 8+ reports |

---

## Audit Checklist

### Initialization Security
- [ ] Constructor calls `_disableInitializers()`
- [ ] `initialize()` has `initializer` modifier
- [ ] Deployment script initializes atomically with proxy creation
- [ ] All inherited base contracts properly initialized (`__Contract_init()`)
- [ ] Variables NOT initialized at declaration time (use initialize())
- [ ] Constructor does NOT set approvals/configurations meant for proxy

### Storage Safety
- [ ] All upgradeable base contracts have `uint256[50] private __gap`
- [ ] Using `@openzeppelin/contracts-upgradeable` (not `/contracts`)
- [ ] EIP-1967 compliant storage slots for implementation/admin
- [ ] No variables initialized at declaration time
- [ ] Inheritance order unchanged between versions
- [ ] New variables added at end only

### Access Control
- [ ] `_authorizeUpgrade()` has `onlyOwner` or role check (UUPS)
- [ ] Implementation cannot be called directly for sensitive operations
- [ ] ProxyAdmin ownership properly configured
- [ ] Plugin installation prevents selector collision

### Delegatecall Safety
- [ ] Target address validated (non-zero, has code)
- [ ] Critical storage (owner, nonce, initialized) checked post-delegatecall
- [ ] No `payable` on batch functions that loop delegatecalls
- [ ] Delegatecall targets restricted to trusted contracts
- [ ] Owner cannot be temporarily changed during delegatecall execution

### Clone/Factory Safety
- [ ] Clone validation checks full bytecode including immutable args
- [ ] Implementation address verified not metamorphic
- [ ] Factory checks implementation codehash
- [ ] Module upgrades include state migration

### CREATE2 and Counterfactual Deployment
- [ ] CREATE2 salt includes owner address (not just tx.origin)
- [ ] CREATE2 salt includes msg.sender to prevent front-running
- [ ] Counterfactual wallet address depends on entrypoint
- [ ] No abi.encodePacked collisions in salt generation

### Proxy Ownership Transfer
- [ ] Permissions and plugins cleared on ownership transfer
- [ ] Token allowances handled on ownership transfer (revoke or warn)
- [ ] Envoy/delegate access revoked on ownership transfer

### Beacon Proxy Safety
- [ ] Beacon validates implementation has code (`code.length > 0`)
- [ ] Beacon cannot point to undeployed addresses

### Whitelist and Registry Safety
- [ ] Whitelists verify contracts are not upgradeable proxies
- [ ] Registries handle selfdestructed proxies (check code existence)
- [ ] Codehash verification for whitelist integrity

---

## Real-World Examples

| Protocol | Issue | Severity | Reference |
|----------|-------|----------|-----------|
| Morpho Protocol | Implementation destruction via unprotected initialize + delegatecall | HIGH | anyone-can-destroy-morphos-implementation.md |
| Fractional V2 | Vault implementation destruction, all assets lost | HIGH | h-01-vault-implementation-can-be-destroyed-leading-to-loss-of-all-assets.md |
| Basin | WellUpgradeable missing onlyOwner on _authorizeUpgrade | HIGH | h-01-wellupgradeable-can-be-upgraded-by-anyone.md |
| Covalent | Non-upgradeable Ownable in upgradeable contract | HIGH | h-01-usage-of-an-incorrect-version-of-ownbale-library-can-potentially-malfunctio.md |
| Rubicon | Missing storage gaps in base contracts | MEDIUM | m-07-no-storage-gap-for-upgradeable-contracts.md |
| 88mph | Initialization front-running | HIGH | initialization-functions-can-be-front-run.md |
| Joyn | Storage collision from non-EIP1967 slots | HIGH | h-06-storage-collision-between-proxy-and-implementation-lack-eip-1967.md |
| Sudoswap | Clone validation only checks 54 bytes | CRITICAL | clones-with-malicious-extradata-are-also-considered-valid-clones.md |
| Velodrome | Metamorphic implementation risk | MEDIUM | implementations-of-clones-could-be-metamorphic-and-lead-to-exploit.md |
| Sablier | Plugin selector collision override | HIGH | plugins-can-be-maliciously-overridden-by-colliding-signatures.md |
| Mimo DeFi | msg.value reuse in batch delegatecalls | MEDIUM | m-04-persisted-msgvalue-in-a-loop-of-delegate-calls-can-be-used-to-drain-eth-fro.md |
| reNFT | Module upgrade without state migration | MEDIUM | m-07-upgrading-modules-via-executeaction-will-brick-all-existing-rentals.md |
| GainsNetwork | Storage layout change breaks roles | HIGH | h-01-lost-roles-after-the-proxy-upgrade.md |
| Lybra | Constructor state unavailable in proxy | HIGH | h-04-the-constructor-caveat-leads-to-bricking-of-configurator-contract.md |
| Notional | UUPS implementation destruction DoS | HIGH | h-09-potential-dos-in-contracts-inheriting-uupsupgradeablesol.md |
| Sablier V2 | Permissions/plugins not reset on proxy transfer | MEDIUM | permission-and-plugins-not-reset-on-proxy-ownership-transfer.md |
| Sablier V2 | Token allowances persist after proxy transfer | MEDIUM | token-allowances-stay-in-effect-on-proxy-ownership-transfer.md |
| Sablier V2 | Owner temporarily changed within delegatecalls | HIGH | owner-can-be-temporarily-changed-within-proxy-calls-allowing-complete-control-of.md |
| Sablier V2 | CREATE2 salt based on tx.origin alone | MEDIUM | create2-salt-based-on-txorigin-alone.md |
| Biconomy | Counterfactual wallet hijack (entrypoint not in salt) | HIGH | h-03-attacker-can-gain-control-of-counterfactual-wallet.md |
| Strata | Proxy reuse without implementation version check | MEDIUM | proxy-reuse-without-implementation-check-inside-unstakecooldown-leads-to-executi.md |
| Arkis | Beacon with undeployed implementation | MEDIUM | beaconds-can-create-broken-margin-accounts-via-an-undeployed-account-implementat.md |
| M Protocol | Approval in constructor unavailable to proxy | MEDIUM | cross-chain-token-transfer-from-spokevault-fails-due-to-approval-from-implementa.md |
| Mimo DeFi | Selfdestruct proxy blocks new deployment | MEDIUM | m-08-if-a-mimoproxy-owner-destroys-their-proxy-they-cannot-deploy-another-from-t.md |
| Retro/Thena | Whitelist incompatible with proxies | MEDIUM | whitelist-is-incompatible-with-proxies.md |
| WishWish | Re-initializable SwapProxy | CRITICAL | c-01-anyone-can-re-initialize-the-swapproxy.md |
| Superform | CREATE2 salt collision from encodePacked | MEDIUM | issues-with-create2-salt-in-supervaultaggregatorcreatevault.md |
| ZeroLend | Storage variables initialized at declaration | MEDIUM | incorrect-proxy-implementation-by-declaring-initial-values-in-storage.md |

---

## Keywords for Search

**Primary Terms:** proxy_pattern, upgradeable_contracts, implementation_contract, delegatecall, initialization, storage_layout, EIP1967, UUPS, transparent_proxy, beacon_proxy, diamond_proxy, minimal_proxy, clone_factory, proxy_upgrade, storage_gap, disableInitializers, storage_collision, selector_clashing, proxy_ownership_transfer, CREATE2_salt, counterfactual_wallet

**Attack Vectors:** initialization_frontrun, implementation_destruction, storage_corruption, unauthorized_upgrade, proxy_takeover, ownership_hijack, selfdestruct_implementation, clone_validation_bypass, metamorphic_attack, plugin_collision, msgvalue_reuse, state_migration_loss, nonce_reset_attack, permission_persistence, allowance_persistence, temporary_owner_change, create2_hijacking, counterfactual_hijack, proxy_reuse_exploit, beacon_no_code, constructor_approval, selfdestruct_block_redeploy, whitelist_bypass, re_initialization

**OpenZeppelin Terms:** Initializable, UUPSUpgradeable, TransparentUpgradeableProxy, BeaconProxy, ProxyAdmin, OwnableUpgradeable, __gap, _disableInitializers, initializer_modifier, Clones, ClonesUpgradeable, reinitializer

**Code Patterns:** constructor_disable_initializers, storage_gap_declaration, upgradeable_library_import, EIP1967_storage_slot, authorize_upgrade, proxy_fallback, delegatecall_forwarding, clone_verification, batch_delegatecall, ownership_transfer_reset, create2_salt_composition, entrypoint_in_salt, code_length_check, codehash_verification, variable_declaration_initialization

**Impact Keywords:** contract_bricked, funds_locked, storage_overwrite, upgrade_failure, initialization_exploit, implementation_compromised, proxy_admin_capture, total_value_locked, permanent_dos, token_drainage, permission_abuse, allowance_exploit, address_hijack, broken_accounts, stuck_tokens, registry_block

### Detection Patterns

#### Code Patterns to Look For
```
- See vulnerable pattern examples above for specific code smells
- Check for missing validation on critical state-changing operations
- Look for assumptions about external component behavior
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`EIP1967`, `OpenZeppelin`, `UUPS_proxy`, `_authorizeUpgrade`, `_getImplementation`, `access_control`, `addToWhitelist`, `address`, `admin`, `approve`, `batch`, `beacon_proxy`, `clone_factory`, `clone_validation`, `createGauge`, `delegatecall`, `delegatecall_pattern`, `deployCounterfactualWallet`, `deployFor`, `diamond_proxy`, `emergencyWithdraw`, `execute`, `executeAction`, `executeOnWhitelisted`, `implementation_contract`, `implementation_security`, `initialization`, `initialization_vulnerability`, `metamorphic_contracts`, `minimal_proxy`, `proxy_implementation`, `proxy_pattern`, `storage_collision`, `storage_layout`, `transparent_proxy`, `upgradeable_contracts`, `upgradeable_proxy`
