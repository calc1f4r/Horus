---
# Core Classification
protocol: generic
chain: everychain
category: proxy
vulnerability_type: storage_collision

# Attack Vector Details
attack_type: state_corruption
affected_component: proxy_storage

# Technical Primitives
primitives:
  - proxy_pattern
  - delegatecall
  - storage_slot
  - implementation_address
  - initializer
  - transparent_proxy
  - UUPS
  - diamond
  - EIP1967

# Impact Classification
severity: critical
impact: fund_loss
exploitability: 0.6
financial_impact: critical

# Context Tags
tags:
  - defi
  - proxy
  - upgrade
  - storage
  - real_exploit
  - DeFiHackLabs

# Version Info
language: solidity
version: all

# Source
source: DeFiHackLabs

# Pattern Identity (Required)
root_cause_family: storage_layout_error
pattern_key: storage_layout_error | proxy_storage | storage_collision

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: multi_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - EIP1967
  - UUPS
  - _setImplementation
  - delegatecall
  - diamond
  - fallback
  - implementation_address
  - initialize
  - initializer
  - proxy_pattern
  - setManager
  - storage_slot
  - totalSupply
  - transparent_proxy
  - validateStorageLayout
---

# Storage Collision Vulnerabilities

## Overview

Storage collision vulnerabilities occur when proxy contracts and their implementations share or overwrite storage slots unintentionally, leading to corrupted state, authentication bypasses, or fund loss. These vulnerabilities are particularly dangerous in upgradeable contract systems where the proxy's storage layout must align with all implementation versions.

**Total Historical Losses from Analyzed Exploits: >$12M USD**

---



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of storage_layout_error"
- Pattern key: `storage_layout_error | proxy_storage | storage_collision`
- Interaction scope: `multi_contract`
- Primary affected component(s): `proxy_storage`
- High-signal code keywords: `EIP1967`, `UUPS`, `_setImplementation`, `delegatecall`, `diamond`, `fallback`, `implementation_address`, `initialize`
- Typical sink / impact: `fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `BrokenProxy.function -> EFVaultImpl.function -> EFVaultProxy.function`
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

## Vulnerability Categories

### 1. Proxy-Implementation Storage Collision
Proxy variables collide with implementation's storage layout.

### 2. Implementation Upgrade Storage Mismatch
New implementation has incompatible storage layout with existing data.

### 3. Unstructured Storage Errors
EIP-1967 style slots incorrectly implemented.

### 4. Diamond Storage Conflicts
Facet storage overlaps in diamond proxy pattern.

### 5. Initializer Storage Issues
Initialization flags or data corrupted by storage collisions.

---

## Vulnerable Pattern Examples

### Example 1: Telcoin Storage Collision [CRITICAL]

**Real Exploit: Telcoin (2023-12) - $1.24M Lost**

```solidity
// @PoC: DeFiHackLabs/src/test/2023-12/Telcoin_exp.sol
// ❌ VULNERABLE: Proxy upgrade caused storage collision
// The new implementation had a different storage layout that
// overwrote critical access control variables

// Original Implementation:
contract TelcoinV1 {
    address public owner;           // Slot 0
    mapping(address => uint256) public balances;  // Slot 1
    uint256 public totalSupply;     // Slot 2
}

// New Implementation (VULNERABLE):
contract TelcoinV2 {
    bool public initialized;        // Slot 0 - COLLIDES with owner!
    address public owner;           // Slot 1 - COLLIDES with balances mapping slot
    mapping(address => uint256) public balances;  // Slot 2
    uint256 public totalSupply;     // Slot 3
    uint256 public newFeature;      // Slot 4
}

// @audit When V2 was deployed:
// - `initialized` (bool) was written to slot 0
// - This corrupted the `owner` address from V1
// - `owner` in V2 now reads from slot 1 (balances mapping base)
// - Attacker could exploit the corrupted state
```

**Attack Flow:**
1. Protocol upgrades from V1 to V2
2. Storage layout mismatch corrupts `owner` variable
3. Attacker exploits corrupted access control
4. Unauthorized operations drain funds

---

### Example 2: EFVault Storage Collision [CRITICAL]

**Real Exploit: EFVault (2023-02) - $5.1M Lost**

```solidity
// @PoC: DeFiHackLabs/src/test/2023-02/EFVault_exp.sol
// ❌ VULNERABLE: Storage collision between proxy and implementation

// Proxy Contract:
contract EFVaultProxy {
    address public admin;           // Slot 0
    address public implementation;  // Slot 1
    
    fallback() external {
        address impl = implementation;
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

// Implementation Contract:
contract EFVaultImpl {
    address public manager;         // Slot 0 - COLLIDES with proxy's admin!
    address public asset;           // Slot 1 - COLLIDES with implementation address!
    uint256 public totalAssets;     // Slot 2
    
    // @audit When implementation writes to `manager`, it overwrites proxy's admin
    // When implementation writes to `asset`, it overwrites implementation address!
    
    function setManager(address _manager) external onlyAdmin {
        manager = _manager;  // Overwrites proxy admin!
    }
}
```

**Attack Flow:**
1. Implementation's storage variables overlap with proxy's critical slots
2. Writing to implementation variables corrupts proxy state
3. Attacker manipulates proxy's `implementation` pointer
4. Proxy now delegates to attacker-controlled contract

---

### Example 3: Audius Governance Storage Collision [CRITICAL]

**Real Exploit: Audius (2022-07) - $6M Lost**

```solidity
// @PoC: DeFiHackLabs/src/test/2022-07/Audius_exp.sol
// ❌ VULNERABLE: Governance proxy storage collision allowed malicious proposal

// The storage collision allowed attacker to:
// 1. Submit a malicious proposal that appeared valid
// 2. Storage collision caused governance checks to pass incorrectly
// 3. Execute arbitrary code through governance mechanism

// Simplified vulnerability pattern:
contract GovernanceProxy {
    // EIP-1967 slots SHOULD be used but weren't properly
    address internal _implementation;  // Collided with implementation storage
    
    // ...
}

contract GovernanceImpl {
    mapping(uint256 => Proposal) public proposals;  // Base slot collided
    
    // @audit Proposal storage collided with proxy metadata
    // Attacker crafted proposal that exploited the collision
}
```

---

### Example 4: Unstructured Storage Errors [HIGH]

```solidity
// ❌ VULNERABLE: Incorrect EIP-1967 implementation
contract BrokenProxy {
    // Attempting EIP-1967 but with errors
    bytes32 private constant IMPL_SLOT = keccak256("my.implementation.slot");
    // @audit Should be: keccak256("eip1967.proxy.implementation") - 1
    // Wrong slot calculation can collide with implementation storage
    
    function _setImplementation(address impl) internal {
        assembly {
            sstore(IMPL_SLOT, impl)
        }
    }
}

// ✅ SECURE: Correct EIP-1967 slot
contract SecureProxy {
    // EIP-1967: keccak256("eip1967.proxy.implementation") - 1
    bytes32 private constant IMPL_SLOT = 
        0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
    
    function _setImplementation(address impl) internal {
        assembly {
            sstore(IMPL_SLOT, impl)
        }
    }
}
```

---

### Example 5: Diamond Storage Collision [HIGH]

```solidity
// ❌ VULNERABLE: Facets with overlapping storage
library FacetAStorage {
    bytes32 constant STORAGE_POSITION = keccak256("facet.a.storage");
    
    struct Storage {
        uint256 value1;
        address admin;
    }
}

library FacetBStorage {
    // @audit Same storage position as FacetA - will collide!
    bytes32 constant STORAGE_POSITION = keccak256("facet.a.storage");
    
    struct Storage {
        address token;  // Collides with value1
        uint256 balance; // Collides with admin
    }
}

// ✅ SECURE: Unique storage positions
library FacetAStorageSecure {
    bytes32 constant STORAGE_POSITION = keccak256("diamond.facet.a.storage");
}

library FacetBStorageSecure {
    bytes32 constant STORAGE_POSITION = keccak256("diamond.facet.b.storage");
}
```

---

## Secure Implementation Guidelines

### 1. Use EIP-1967 Standard Slots
```solidity
// Standard slots that won't collide with implementation storage
bytes32 constant IMPLEMENTATION_SLOT = 
    0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc;
bytes32 constant ADMIN_SLOT = 
    0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103;
bytes32 constant BEACON_SLOT = 
    0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50;
```

### 2. Inherit Storage Layout Properly
```solidity
// ✅ SECURE: Maintain storage layout across upgrades
contract ImplementationV1 {
    address public owner;           // Slot 0
    uint256 public value;           // Slot 1
    mapping(address => uint256) public balances;  // Slot 2
    
    uint256[47] private __gap;      // Reserve slots for upgrades
}

contract ImplementationV2 is ImplementationV1 {
    // Add new variables AFTER inherited ones
    uint256 public newFeature;      // Uses gap slot
    
    // Reduce gap by 1
    uint256[46] private __gap;
}
```

### 3. Use OpenZeppelin's Upgradeable Contracts
```solidity
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract SecureVault is Initializable, OwnableUpgradeable {
    // Storage automatically managed with gaps
    
    function initialize(address owner_) public initializer {
        __Ownable_init(owner_);
    }
}
```

### 4. Storage Validation Before Upgrade
```solidity
// Include in upgrade process
function validateStorageLayout(address newImpl) internal view {
    // Check critical slots haven't moved
    bytes32 currentOwner = _getStorageAt(OWNER_SLOT);
    
    // Simulate upgrade and verify
    // ... validation logic
}
```

---

## Real-World Exploits Summary

| Protocol | Date | Loss | Vulnerability Type |
|----------|------|------|-------------------|
| Telcoin | 2023-12 | $1.24M | Upgrade storage mismatch |
| EFVault | 2023-02 | $5.1M | Proxy-impl collision |
| Audius | 2022-07 | $6M | Governance storage collision |
| Multiple Proxies | Various | >$5M | Unstructured storage errors |

---

## Detection Patterns

### Storage Layout Comparison Tool
```bash
# Compare storage layouts between versions
slither-check-upgradeability project/ --new-version ImplementationV2
```

### Manual Checklist
- [ ] Are proxy storage slots EIP-1967 compliant?
- [ ] Is storage layout preserved across upgrades?
- [ ] Are `__gap` arrays used for future storage?
- [ ] Does new implementation inherit from old correctly?
- [ ] Are diamond facets using unique storage positions?
- [ ] Has slither/storage-check been run before upgrade?

### Semgrep Rule
```yaml
rules:
  - id: proxy-storage-collision-risk
    patterns:
      - pattern: |
          contract $PROXY {
              address $VAR1;
              ...
          }
      - pattern-inside: |
          fallback() ... {
              ... delegatecall(...) ...
          }
    message: "Proxy with direct storage variables - collision risk"
    severity: WARNING
```

---

## Keywords for Search

`storage collision`, `proxy storage`, `delegatecall storage`, `EIP-1967`, `storage slot`, `implementation storage`, `upgrade storage`, `storage layout`, `storage gap`, `diamond storage`, `facet storage`, `transparent proxy`, `UUPS storage`, `initializer collision`, `unstructured storage`

---

## DeFiHackLabs Real-World Exploits (4 incidents)

**Category**: Storage Collision | **Total Losses**: $129.5M | **Sub-variants**: 1

### Sub-variant Breakdown

#### Storage-Collision/Generic (4 exploits, $129.5M)

- **Telcoin** (2023-12, $124.0M, polygon) | PoC: `DeFiHackLabs/src/test/2023-12/Telcoin_exp.sol`
- **EFVault** (2023-02, $5.1M, ethereum) | PoC: `DeFiHackLabs/src/test/2023-02/EFVault_exp.sol`
- **LeverageSIR** (2025-03, $354K, ethereum) | PoC: `DeFiHackLabs/src/test/2025-03/LeverageSIR_exp.sol`
- *... and 1 more exploits*

### Complete DeFiHackLabs Exploit Table

| Protocol | Date | Loss | Vulnerability Sub-type | Chain |
|----------|------|------|----------------------|-------|
| Telcoin | 2023-12-25 | $124.0M | Storage Collision | polygon |
| EFVault | 2023-02-24 | $5.1M | Storage Collision | ethereum |
| LeverageSIR | 2025-03-30 | $354K | Storage SLOT1 collision | ethereum |
| Audius | 2022-07-23 | $704 | Storage Collision & Malicious Proposal | ethereum |

### Top PoC References

- **Telcoin** (2023-12, $124.0M): `DeFiHackLabs/src/test/2023-12/Telcoin_exp.sol`
- **EFVault** (2023-02, $5.1M): `DeFiHackLabs/src/test/2023-02/EFVault_exp.sol`
- **LeverageSIR** (2025-03, $354K): `DeFiHackLabs/src/test/2025-03/LeverageSIR_exp.sol`
- **Audius** (2022-07, $704): `DeFiHackLabs/src/test/2022-07/Audius_exp.sol`

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

`DeFiHackLabs`, `EIP1967`, `UUPS`, `_setImplementation`, `defi`, `delegatecall`, `diamond`, `fallback`, `implementation_address`, `initialize`, `initializer`, `proxy`, `proxy_pattern`, `real_exploit`, `setManager`, `storage`, `storage_collision`, `storage_slot`, `totalSupply`, `transparent_proxy`, `upgrade`, `validateStorageLayout`
