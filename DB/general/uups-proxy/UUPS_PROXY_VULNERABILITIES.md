---
# Core Classification (Required)
protocol: generic
chain: everychain
category: upgradeability
vulnerability_type: uups_proxy

# Attack Vector Details (Required)
attack_type: logical_error
affected_component: proxy_implementation

# Technical Primitives (Required)
primitives:
  - UUPSUpgradeable
  - EIP-1822
  - proxy_pattern
  - initialization
  - storage_gap
  - upgradeToAndCall
  - _authorizeUpgrade
  - implementation_contract
  - delegatecall
  - storage_layout

# Impact Classification (Required)
severity: high
impact: implementation_takeover
exploitability: 0.7
financial_impact: high

# Context Tags
tags:
  - defi
  - upgradeable_contracts
  - proxy_pattern
  - openzeppelin
  - initialization
  - storage_management

# Version Info
language: solidity
version: ">=0.8.0"

# Pattern Identity (Required)
root_cause_family: storage_layout_error
pattern_key: storage_layout_error | proxy_implementation | uups_proxy

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - 4
  - EIP-1822
  - UUPSUpgradeable
  - _authorizeUpgrade
  - collisions
  - contract
  - delegatecall
  - deployUUPSProxy
  - implementation_contract
  - initialization
  - initialize
  - proxy
  - proxy_pattern
  - storage_gap
  - storage_layout
  - takeover
  - upgradeAssetFactory
  - upgradeFlashSwapRouter
  - upgradeToAndCall
  - when
---

## References

- [m-1-uupsupgradeable-vulnerability-in-openzeppelin-contracts.md](../../../reports/dao_governance_findings/m-1-uupsupgradeable-vulnerability-in-openzeppelin-contracts.md) - Sherlock audit of KyberSwap
- [storage-collision-risk-in-uups-upgradeable-stakingproxy-due-to-missing-storage-g.md](../../../reports/lst_restaking_findings/storage-collision-risk-in-uups-upgradeable-stakingproxy-due-to-missing-storage-g.md) - Cyfrin audit of StakingProxy
- [m-1-the-uups-proxie-standard-is-implemented-incorrectly-making-the-protocol-not-.md](../../../reports/missing_validations_findings/m-1-the-uups-proxie-standard-is-implemented-incorrectly-making-the-protocol-not-.md) - Sherlock audit of Cork Protocol

## Vulnerability Title

**UUPS Proxy (EIP-1822) Implementation Vulnerabilities**

### Overview

UUPS (Universal Upgradeable Proxy Standard) proxies implementing EIP-1822 introduce security risks when implementation contracts are not properly initialized, storage gaps are missing, or upgrade mechanisms are incorrectly implemented. Vulnerabilities manifest as uninitialized implementation takeover, storage collisions during upgrades, and broken upgradeability due to missing upgrade functions.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of storage_layout_error"
- Pattern key: `storage_layout_error | proxy_implementation | uups_proxy`
- Interaction scope: `multi_contract`
- Primary affected component(s): `proxy_implementation`
- High-signal code keywords: `4`, `EIP-1822`, `UUPSUpgradeable`, `_authorizeUpgrade`, `collisions`, `contract`, `delegatecall`, `deployUUPSProxy`
- Typical sink / impact: `implementation_takeover`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `2.function -> 3.function -> 4.function`
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

UUPS proxy vulnerabilities arise from several fundamental issues:

1. **Uninitialized Implementation Contracts**: OpenZeppelin UUPSUpgradeable versions >= 4.1.0 < 4.3.2 allow attackers to initialize and destroy uninitialized implementation contracts
2. **Missing Storage Gaps**: UUPS contracts without `__gap` arrays risk storage collisions when inherited by external contracts that add new variables
3. **Missing Upgrade Functions**: Owner contracts lacking `upgradeToAndCall()` function prevent proxy upgrades despite inheriting UUPSUpgradeable
4. **Improper Authorization**: `_authorizeUpgrade()` function with `onlyOwner` modifier when owner is a contract without upgrade capabilities

#### Attack Scenario

**Scenario 1: Uninitialized Implementation Takeover (MEDIUM-HIGH)**
1. Protocol deploys UUPS proxy with OZ 4.3.1 but forgets to initialize implementation contract
2. Attacker calls `initialize()` on implementation contract directly (not through proxy)
3. Attacker becomes owner of implementation contract
4. Attacker calls `upgradeTo()` or `upgradeToAndCall()` with malicious implementation
5. Attacker can `selfdestruct` implementation, bricking all proxies pointing to it

**Scenario 2: Storage Collision via Missing Gap (LOW-MEDIUM)**
1. `StakingProxy` inherits `UUPSUpgradeable` and `OwnableUpgradeable` with 7 state variables
2. Third-party DAO inherits `StakingProxy` and adds their own state variables
3. Protocol upgrades `StakingProxy` adding new variable at end
4. New variable collides with DAO's inherited variables
5. Storage corruption causes contract malfunction

**Scenario 3: Broken Upgradeability (MEDIUM)**
1. `AssetFactory` and `FlashSwapRouter` inherit UUPSUpgradeable
2. `initialize()` sets owner to `ModuleCore` contract
3. `_authorizeUpgrade()` has `onlyOwner` modifier
4. `ModuleCore` contract has no `upgradeToAndCall()` function
5. Upgrades impossible; contracts effectively non-upgradeable

#### Vulnerable Pattern Examples

**Example 1: Uninitialized Implementation (OZ 4.1.0-4.3.1)** [MEDIUM]
```solidity
// ❌ VULNERABLE: Implementation contract not initialized after deployment
// OpenZeppelin UUPSUpgradeable 4.3.1
contract PoolOracle is UUPSUpgradeable, OwnableUpgradeable {
    // NO constructor with _disableInitializers()!
    
    function initialize(address _owner) external initializer {
        __Ownable_init();
        __UUPSUpgradeable_init();
        transferOwnership(_owner);
    }
    
    function _authorizeUpgrade(address newImplementation) 
        internal override onlyOwner 
    {}
}

// Attack:
// 1. Deploy proxy pointing to PoolOracle implementation
// 2. Initialize proxy: proxy.initialize(protocolOwner) ✓
// 3. Implementation still uninitialized!
// 4. Attacker: implementation.initialize(attacker) ✓
// 5. Attacker: implementation.upgradeTo(maliciousImpl) ✓
// 6. All proxies now point to malicious implementation
```

**Example 2: Missing Storage Gap in Inherited Contract** [LOW]
```solidity
// ❌ VULNERABLE: No storage gap for future upgrades
contract StakingProxy is UUPSUpgradeable, OwnableUpgradeable {
    IERC20Upgradeable public token;
    IStakingPool public lst;
    IPriorityPool public priorityPool;
    IWithdrawalPool public withdrawalPool;
    ISDLPool public sdlPool;
    address public staker;
    
    // NO __gap array!
    // If external contract inherits this and we add variables, collision occurs
}

// External DAO inherits:
contract DAOStaking is StakingProxy {
    uint256 public daoVariable1;  // Slot 256
    uint256 public daoVariable2;  // Slot 257
}

// Future StakingProxy upgrade adds:
contract StakingProxyV2 is UUPSUpgradeable, OwnableUpgradeable {
    // ... existing 6 variables
    address public staker;
    uint256 public newFeature;  // COLLISION with daoVariable1!
}
```

**Example 3: Owner Contract Missing Upgrade Function** [MEDIUM]
```solidity
// ❌ VULNERABLE: ModuleCore cannot call upgradeToAndCall()
contract AssetFactory is UUPSUpgradeable, OwnableUpgradeable {
    function initialize(address moduleCore) external initializer {
        __Ownable_init();
        __UUPSUpgradeable_init();
        transferOwnership(moduleCore);  // ModuleCore is now owner
    }
    
    function _authorizeUpgrade(address newImplementation) 
        internal override onlyOwner  // Only ModuleCore can upgrade
    {}
}

contract ModuleCore {
    // NO upgradeToAndCall() function!
    // AssetFactory cannot be upgraded despite being UUPSUpgradeable
}
```

**Example 4: Duplicate Reports - Same KyberSwap Issue** [MEDIUM]
```solidity
// ❌ VULNERABLE: KyberSwap using OZ 4.3.1
// package.json
{
    "@openzeppelin/contracts": "4.3.1",
    "@openzeppelin/contracts-upgradeable": "4.3.1"
}

// Affected contracts:
// 1. PoolOracle.sol
// 2. TokenPositionDescriptor.sol

// Both inherit UUPSUpgradeable 4.3.1 without initializing implementation
// Vulnerable to GHSA-5vp3-v4hc-gx76
```

### Impact Analysis

#### Technical Impact
- **Implementation Takeover**: Attacker can initialize uninitialized implementation contracts (OZ 4.1.0-4.3.1)
- **Implementation Destruction**: Attacker can `selfdestruct` implementation, bricking all proxies
- **Storage Corruption**: Missing storage gaps cause variable collisions in inherited contracts
- **Broken Upgradeability**: Missing upgrade functions prevent contract upgrades
- **Permanent Lock**: Contracts become non-upgradeable despite UUPSUpgradeable inheritance

#### Business Impact
- **Consensus Severity**: MEDIUM (3/5 reports), LOW (1/5 reports), CRITICAL per OpenZeppelin
- **Financial Loss**: Implementation destruction bricks all proxies; potential total loss
- **Operational Disruption**: Non-upgradeable contracts cannot fix bugs or add features
- **Trust Damage**: Known OZ vulnerability (GHSA-5vp3-v4hc-gx76) missed in audits
- **Recovery Complexity**: No on-chain recovery if implementation destroyed

#### Affected Scenarios
- **OZ Version 4.1.0-4.3.1**: All UUPS contracts using these versions vulnerable to takeover
- **Third-Party Inheritance**: Contracts intended for external inheritance without storage gaps
- **Multi-Contract Ownership**: Owner contracts without upgrade function implementation
- **Deployment Errors**: Forgetting to initialize implementation contracts post-deployment

### Secure Implementation

**Fix 1: Disable Initializers in Constructor (OZ >= 4.3.2)**
```solidity
// ✅ SECURE: Constructor disables initialization on implementation
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";

contract PoolOracle is UUPSUpgradeable, OwnableUpgradeable {
    /// @custom:oz-upgrades-unsafe-allow constructor
    constructor() {
        _disableInitializers();  // Implementation cannot be initialized
    }
    
    function initialize(address _owner) external initializer {
        __Ownable_init();
        __UUPSUpgradeable_init();
        transferOwnership(_owner);
    }
    
    function _authorizeUpgrade(address newImplementation) 
        internal override onlyOwner 
    {}
}
```

**Fix 2: Add Storage Gap for Future Upgrades**
```solidity
// ✅ SECURE: Storage gap reserves slots for future variables
contract StakingProxy is UUPSUpgradeable, OwnableUpgradeable {
    IERC20Upgradeable public token;
    IStakingPool public lst;
    IPriorityPool public priorityPool;
    IWithdrawalPool public withdrawalPool;
    ISDLPool public sdlPool;
    address public staker;
    
    // Reserve 50 slots for future variables (OpenZeppelin recommendation)
    uint256[50] private __gap;
}

// Future upgrade can safely add variables:
contract StakingProxyV2 is UUPSUpgradeable, OwnableUpgradeable {
    // ... existing 6 variables
    address public staker;
    uint256 public newFeature;  // Uses gap slot - no collision!
    
    uint256[49] private __gap;  // Reduced gap
}
```

**Fix 3: Implement Upgrade Function in Owner Contract**
```solidity
// ✅ SECURE: ModuleCore can call upgradeToAndCall()
contract ModuleCore is Ownable {
    function upgradeAssetFactory(
        address assetFactoryProxy,
        address newImplementation,
        bytes memory data
    ) external onlyOwner {
        UUPSUpgradeable(assetFactoryProxy).upgradeToAndCall(
            newImplementation,
            data
        );
    }
    
    function upgradeFlashSwapRouter(
        address routerProxy,
        address newImplementation,
        bytes memory data
    ) external onlyOwner {
        UUPSUpgradeable(routerProxy).upgradeToAndCall(
            newImplementation,
            data
        );
    }
}
```

**Fix 4: Upgrade to OpenZeppelin >= 4.3.2**
```json
// ✅ SECURE: Use patched OpenZeppelin version
{
    "@openzeppelin/contracts": "4.9.0",
    "@openzeppelin/contracts-upgradeable": "4.9.0"
}
```

**Fix 5: Initialize Implementation Immediately After Deployment**
```javascript
// ✅ SECURE: Initialize implementation in deployment script
async function deployUUPSProxy() {
    // 1. Deploy implementation
    const Implementation = await ethers.getContractFactory("PoolOracle");
    const implementation = await Implementation.deploy();
    await implementation.deployed();
    
    // 2. Initialize implementation to prevent takeover
    await implementation.initialize(BURN_ADDRESS);  // Lock implementation
    
    // 3. Deploy proxy
    const ERC1967Proxy = await ethers.getContractFactory("ERC1967Proxy");
    const initData = implementation.interface.encodeFunctionData(
        "initialize",
        [protocolOwner]
    );
    const proxy = await ERC1967Proxy.deploy(implementation.address, initData);
    await proxy.deployed();
    
    return proxy.address;
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: UUPSUpgradeable without constructor calling _disableInitializers()
- Pattern 2: OpenZeppelin version >= 4.1.0 < 4.3.2 in package.json
- Pattern 3: UUPSUpgradeable contract without __gap array
- Pattern 4: _authorizeUpgrade() with onlyOwner when owner is external contract
- Pattern 5: Owner contract without upgradeToAndCall() implementation
- Pattern 6: Deployment scripts not initializing implementation contracts
- Pattern 7: Contracts intended for inheritance without storage gaps
- Pattern 8: UUPS proxies without initialization in constructor
```

#### Audit Checklist
- [ ] Verify OpenZeppelin version >= 4.3.2 or implementation has _disableInitializers()
- [ ] Check deployment scripts initialize implementation contracts
- [ ] Confirm UUPS contracts have __gap array (size 50 recommended)
- [ ] Validate owner contracts implement upgradeToAndCall() if they own UUPS proxies
- [ ] Test upgrade flow end-to-end before mainnet deployment
- [ ] Verify _authorizeUpgrade() authorization logic is correct
- [ ] Check for storage layout changes between upgrade versions
- [ ] Ensure no direct calls to implementation contract are possible

### Real-World Examples

#### Known Protocol Findings
- **KyberSwap (Sherlock 2023)** - PoolOracle and TokenPositionDescriptor using OZ 4.3.1 vulnerable to GHSA-5vp3-v4hc-gx76
- **StakingProxy (Cyfrin 2025)** - Missing storage gap in UUPS contract intended for third-party inheritance
- **Cork Protocol (Sherlock 2024)** - AssetFactory and FlashSwapRouter non-upgradeable due to missing upgradeToAndCall() in ModuleCore

#### Related CVEs/Advisories
- **GHSA-5vp3-v4hc-gx76**: OpenZeppelin UUPSUpgradeable uninitialized implementation vulnerability (Critical)
- **OpenZeppelin Advisory**: [Initialize UUPS Implementation Contracts](https://forum.openzeppelin.com/t/security-advisory-initialize-uups-implementation-contracts/15301)

### Prevention Guidelines

#### Development Best Practices
1. **Always** use OpenZeppelin >= 4.3.2 for new UUPS deployments
2. **Add** `_disableInitializers()` in constructor for all UUPS implementations
3. **Include** storage gap (`uint256[50] private __gap`) in all UUPS contracts
4. **Implement** `upgradeToAndCall()` in owner contracts that manage UUPS proxies
5. **Initialize** implementation contracts immediately after deployment
6. **Test** upgrade flow in testnet before mainnet deployment
7. **Document** storage layout for each version to prevent collisions
8. **Use** OpenZeppelin Upgrades Plugin to validate storage layout

#### Testing Requirements
- Unit tests for: Implementation initialization prevention; storage gap preservation
- Integration tests for: Complete upgrade flow from owner contract
- Upgrade simulation: Fork mainnet state and test upgrade with production data
- Invariant tests: Implementation cannot be initialized; proxy upgrade succeeds
- Deployment tests: Verify implementation initialized in deployment script

### References

#### Technical Documentation
- [EIP-1822: Universal Upgradeable Proxy Standard](https://eips.ethereum.org/EIPS/eip-1822)
- [OpenZeppelin UUPS Proxies](https://docs.openzeppelin.com/contracts/4.x/api/proxy#UUPSUpgradeable)
- [OpenZeppelin Upgrades Plugin](https://docs.openzeppelin.com/upgrades-plugins/1.x/)
- [Storage Gaps in Upgradeable Contracts](https://docs.openzeppelin.com/contracts/4.x/upgradeable#storage_gaps)

#### Security Research
- [GHSA-5vp3-v4hc-gx76: UUPSUpgradeable Vulnerability](https://github.com/OpenZeppelin/openzeppelin-contracts/security/advisories/GHSA-5vp3-v4hc-gx76)
- [OpenZeppelin Security Advisory](https://forum.openzeppelin.com/t/security-advisory-initialize-uups-implementation-contracts/15301)

### Keywords for Search

`UUPS proxy`, `UUPSUpgradeable`, `EIP-1822`, `uninitialized implementation`, `implementation takeover`, `_disableInitializers`, `storage gap`, `__gap`, `upgradeToAndCall`, `_authorizeUpgrade`, `onlyOwner`, `proxy upgrade`, `OpenZeppelin 4.3.1`, `GHSA-5vp3-v4hc-gx76`, `implementation destruction`, `selfdestruct implementation`, `storage collision`, `upgradeable contract`, `proxy pattern`, `delegatecall`, `ERC1967Proxy`, `initialize`, `initializer`, `OwnableUpgradeable`, `upgrade mechanism`, `broken upgradeability`, `ModuleCore`, `AssetFactory`, `FlashSwapRouter`, `PoolOracle`, `TokenPositionDescriptor`, `StakingProxy`

### Related Vulnerabilities

- [Diamond Proxy Vulnerabilities](../diamond-proxy/DIAMOND_PROXY_VULNERABILITIES.md)
- [Proxy Initialization Vulnerabilities](../initialization/proxy-initialization.md)
- [Upgradeable Contract Storage Gaps](../storage/storage-gaps.md)
- [Transparent Proxy Vulnerabilities](../transparent-proxy/transparent-proxy.md)

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

`4`, `EIP-1822`, `UUPSUpgradeable`, `_authorizeUpgrade`, `collisions`, `contract`, `defi`, `delegatecall`, `deployUUPSProxy`, `implementation_contract`, `initialization`, `initialize`, `openzeppelin`, `proxy`, `proxy_pattern`, `storage_gap`, `storage_layout`, `storage_management`, `takeover`, `upgradeAssetFactory`, `upgradeFlashSwapRouter`, `upgradeToAndCall`, `upgradeability`, `upgradeable_contracts`, `uups_proxy`, `when`
