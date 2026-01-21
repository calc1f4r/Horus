---
# Core Classification (Required)
protocol: generic
chain: everychain
category: upgradeability
vulnerability_type: diamond_proxy

# Attack Vector Details (Required)
attack_type: logical_error
affected_component: proxy_storage

# Technical Primitives (Required)
primitives:
  - EIP-2535
  - diamondCut
  - facet_management
  - storage_layout
  - delegatecall
  - proxy_upgrade
  - storage_collision
  - reentrancy_guard
  - access_control
  - initialization

# Impact Classification (Required)
severity: medium_to_high
impact: state_corruption
exploitability: 0.5
financial_impact: high

# Context Tags
tags:
  - defi
  - upgradeable_contracts
  - proxy_pattern
  - diamond_standard
  - multi_facet
  - storage_management

# Version Info
language: solidity
version: ">=0.8.0"
---

## References

- [storage-collision-leads-to-failure-of-the-system.md](../../../reports/diamond_proxy_findings/storage-collision-leads-to-failure-of-the-system.md) - OpenZeppelin audit of zkSync
- [h-01-lost-roles-after-the-proxy-upgrade.md](../../../reports/diamond_proxy_findings/h-01-lost-roles-after-the-proxy-upgrade.md) - Pashov audit of GainsNetwork
- [accesscontrolds-uses-accesscontrol-which-has-storage-collision-risks.md](../../../reports/diamond_proxy_findings/accesscontrolds-uses-accesscontrol-which-has-storage-collision-risks.md) - TrailOfBits audit of Arkis
- [m-18-future-upgrades-may-be-difficult-or-impossible.md](../../../reports/diamond_proxy_findings/m-18-future-upgrades-may-be-difficult-or-impossible.md) - Sherlock audit of Elfi
- [farmfacet-functions-are-susceptible-to-the-draining-of-intermediate-value-sent-b.md](../../../reports/diamond_proxy_findings/farmfacet-functions-are-susceptible-to-the-draining-of-intermediate-value-sent-b.md) - Cyfrin audit of Beanstalk
- [intermediate-value-sent-by-the-caller-can-be-drained-via-reentrancy-when-pipelin.md](../../../reports/diamond_proxy_findings/intermediate-value-sent-by-the-caller-can-be-drained-via-reentrancy-when-pipelin.md) - Cyfrin audit of Beanstalk
- [h-2-all-taker-collateral-and-collected-fees-can-be-stolen-by-re-entering-via-rft.md](../../../reports/diamond_proxy_findings/h-2-all-taker-collateral-and-collected-fees-can-be-stolen-by-re-entering-via-rft.md) - Sherlock audit of Ammplify
- [failure-to-add-modified-facets-and-facets-with-modified-dependencies-to-bipsbips.md](../../../reports/diamond_proxy_findings/failure-to-add-modified-facets-and-facets-with-modified-dependencies-to-bipsbips.md) - Cyfrin audit of Beanstalk
- [anyone-can-remove-the-template-contract-for-threednsregcontrol-and-threednsresol.md](../../../reports/diamond_proxy_findings/anyone-can-remove-the-template-contract-for-threednsregcontrol-and-threednsresol.md) - Cantina audit of 3DNS
- [m-01-freezed-chain-will-never-be-unfreeze-since-statetransitionmanagerunfreezech.md](../../../reports/diamond_proxy_findings/m-01-freezed-chain-will-never-be-unfreeze-since-statetransitionmanagerunfreezech.md) - Code4rena audit of zkSync
- [a-newly-created-chain-that-has-been-migrated-to-the-gateway-will-be-lost-if-trie.md](../../../reports/diamond_proxy_findings/a-newly-created-chain-that-has-been-migrated-to-the-gateway-will-be-lost-if-trie.md) - Codehawks audit of zkSync Era
- [priority-operation-reexecution-for-era-chain-in-gw-and-l1-when-migrating-from-gw.md](../../../reports/diamond_proxy_findings/priority-operation-reexecution-for-era-chain-in-gw-and-l1-when-migrating-from-gw.md) - Codehawks audit of zkSync Era

## Vulnerability Title

**Diamond Proxy (EIP-2535) Implementation Vulnerabilities**

### Overview

Diamond proxies implementing EIP-2535 introduce unique security challenges due to their multi-facet architecture, shared storage model, and complex upgrade mechanisms. Vulnerabilities manifest as storage collisions during upgrades, reentrancy through facet callbacks, improper facet management, and initialization oversights that can lead to fund loss, privilege escalation, or complete system failure.

### Vulnerability Description

#### Root Cause

Diamond proxy vulnerabilities arise from several fundamental issues:

1. **Storage Layout Mismanagement**: When structs within `AppStorage` are modified (added/removed members), subsequent variables shift storage slots, causing data corruption
2. **Non-Upgrade-Aware Contracts**: Using OpenZeppelin's `AccessControl` instead of `AccessControlUpgradeable` in facets creates slot 0 collisions
3. **Missing Reentrancy Protection**: Facet functions with external callbacks (e.g., ERC1155 safe transfers, RFT callbacks) lack reentrancy guards on Diamond-level state
4. **Incomplete Upgrade Scripts**: Modified facets and their library dependencies not included in `diamondCut` calls
5. **Uninitialized Template Contracts**: `initialize()` callable on template contracts allows malicious authority takeover
6. **Nested Struct Limitations**: Directly nested structs cannot be safely extended in future upgrades

#### Attack Scenario

**Scenario 1: Storage Collision Leading to System Failure (HIGH)**
1. Protocol upgrades Diamond with new struct that changes size from 7 to 2 slots
2. All subsequent variables in `AppStorage` shift their storage positions
3. `governor` address now reads from old `lastDiamondFreezeTimestamp` slot
4. Protocol loses governor privilege; no recovery mechanism exists
5. Validators mapped incorrectly; block commitment becomes impossible

**Scenario 2: Reentrancy via Facet Callback Draining Funds (HIGH)**
1. Victim calls `FarmFacet::advancedFarm{value: 10 ether}` with ERC1155 transfer
2. Malicious recipient receives ERC1155 via safe transfer acceptance check
3. In callback, attacker calls `advancedFarm{value: 1 wei}` with empty data
4. Execution falls through to ETH refund; entire Diamond balance sent to attacker
5. Original victim receives no refund; funds stolen

**Scenario 3: Lost Roles After Upgrade (HIGH)**
1. Current `accessControl` mapping occupies slot 2 (after 2 slots from Initializable + Addresses)
2. New version adds 2 addresses to `Addresses` struct, putting `accessControl` at slot 4
3. Post-upgrade, `hasRole` addresses wrong slot; all roles appear revoked
4. Role-gated functionality inaccessible; emergency upgrade required

#### Vulnerable Pattern Examples

**Example 1: Storage Slot Shift from Struct Modification** [HIGH]
```solidity
// ❌ VULNERABLE: Changing struct size shifts all subsequent storage
// BEFORE: DiamondCutStorage occupies slots 0-6 (7 slots)
struct DiamondCutStorage {
    uint256 proposedUpgradeTimestamp;
    address proposedUpgradeAddress;
    bytes32 approvedData;
    uint256 currentProposalId;
    bool isFrozen;
    address securityCouncil;
    uint256 lastDiamondFreezeTimestamp;
}

// AFTER: UpgradeStorage occupies only slots 0-1 (2 slots)
struct UpgradeStorage {
    bytes32 proposedUpgradeHash;
    uint256 proposedUpgradeTimestamp;
}

struct AppStorage {
    UpgradeStorage upgradeStorage;  // Now 2 slots instead of 7
    address governor;               // SHIFTED: was slot 7, now slot 2
    Verifier verifier;              // SHIFTED: was slot 8, now slot 3
    // All data corrupted after upgrade!
}
```

**Example 2: Non-Upgrade-Aware AccessControl in Facet** [MEDIUM]
```solidity
// ❌ VULNERABLE: AccessControl stores _roles mapping at slot 0
// When new facet also uses slot 0, storage collision occurs
abstract contract AccessControlDS is AccessControl, OwnableReadonlyDS {
    // OpenZeppelin AccessControl stores:
    // mapping(bytes32 role => RoleData) private _roles;  // at slot 0
    
    function hasRole(bytes32 _role, address _account) public view virtual override
        returns (bool) {
            return (isOwnerRole(_role) && _owner() == _account) || 
                   super.hasRole(_role, _account);  // Reads from slot 0
    }
}

// Any new facet with its own slot 0 variable will collide
contract NewFacet {
    uint256 public myVariable;  // Also slot 0 - COLLISION!
}
```

**Example 3: FarmFacet Reentrancy via ERC1155 Callback** [HIGH]
```solidity
// ❌ VULNERABLE: No reentrancy guard on Diamond-level state
modifier withEth() {
    if (msg.value > 0) s.isFarm = 2;  // Set flag
    _;
    if (msg.value > 0) {
       s.isFarm = 1;                   // Clear flag
        LibEth.refundEth();            // Refund entire balance
    }
}

function advancedFarm(AdvancedFarmCall[] calldata data) 
    external payable withEth 
{
    for (uint256 i = 0; i < data.length; ++i) {
        // External call allows reentrancy
        _advancedFarm(data[i]);  // May call ERC1155 safeTransfer -> onERC1155Received
    }
}

// LibEth.refundEth() sends entire balance when s.isFarm != 2
function refundEth() internal {
    AppStorage storage s = LibAppStorage.diamondStorage();
    if (address(this).balance > 0 && s.isFarm != 2) {
        (bool success, ) = msg.sender.call{value: address(this).balance}("");
        require(success, "Eth transfer Failed.");
    }
}
```

**Example 4: Nested Structs Blocking Future Upgrades** [MEDIUM]
```solidity
// ❌ VULNERABLE: Nested structs cannot be extended safely
struct Props {
    bytes32 key;
    TokenBalance baseTokenBalance;     // NESTED STRUCT - cannot add fields!
    EnumerableSet.AddressSet stableTokens;
    mapping(address => TokenBalance) stableTokenBalances;
    BorrowingFee borrowingFee;         // NESTED STRUCT - cannot add fields!
    uint256 apr;
    uint256 totalClaimedRewards;
}

// Future upgrade attempt:
struct TokenBalance {
    uint256 amount;
    uint256 timestamp;
    uint256 newField;  // BREAKS STORAGE: shifts stableTokens and everything after!
}
```

**Example 5: Missing Facet Upgrade Breaking Protocol** [HIGH]
```solidity
// ❌ VULNERABLE: bipSeedGauge missing modified facets
async function bipSeedGauge() {
    // Missing: FieldFacet, BDVFacet, ConvertFacet, WhitelistFacet, SiloFacet
    // All were modified but not included in diamondCut
    
    const facets = [
        'SeasonFacet',
        'SeasonGettersFacet',
        'GaugePointFacet',
        // FieldFacet MISSING - has LibTokenSilo changes
        // SiloFacet MISSING - has stemTipForToken changes
    ];
    
    await diamondCut(facets);  // Incomplete upgrade
}

// Result: Old stemTipForToken implementation used
// Deposits before upgrade receive significantly more grown stalk than intended
```

**Example 6: Template Contract Initialization Takeover** [MEDIUM]
```solidity
// ❌ VULNERABLE: Template contract can be initialized by anyone
contract ThreeDNSRegControl {
    // NO constructor with _disableInitializers()!
    
    function initialize(
        address _authority,
        address resolver_,
        string memory domainName_,
        string memory domainVersion_,
        uint64 chainId_,
        string memory _baseUri,
        address _usdc
    ) external {
        // Attacker can call on template, set malicious _authority
        // Then use diamondCut to add selfdestruct facet
    }
}

// Attack:
template.initialize(address(attacker), ...);  // Take control
diamondCut([selfDestructFacet]);              // Add malicious facet
fallback() -> selfdestruct(attacker);         // Destroy template
```

**Example 7: Copy-Paste Error in Freeze/Unfreeze Functions** [MEDIUM]
```solidity
// ❌ VULNERABLE: Both functions call freezeDiamond()
function freezeChain(uint256 _chainId) external onlyOwner {
    IZkSyncStateTransition(stateTransition[_chainId]).freezeDiamond();  // Correct
}

/// @dev freezes the specified chain  // WRONG COMMENT
function unfreezeChain(uint256 _chainId) external onlyOwner {
    IZkSyncStateTransition(stateTransition[_chainId]).freezeDiamond();  // WRONG!
    // Should call unfreezeDiamond() instead
}

// Result: Frozen chain can never be unfrozen via this function
```

### Impact Analysis

#### Technical Impact
- **Storage Corruption**: All state variables after modified struct read incorrect data (3/13 reports)
- **Role System Failure**: Access control mappings address wrong slots; all permissions lost (2/13 reports)
- **Fund Drainage**: Reentrancy allows stealing intermediate ETH from Diamond (3/13 reports)
- **Incomplete Upgrades**: Stale facet code leads to accounting errors, broken functionality (1/13 reports)
- **Template Destruction**: Attacker can initialize and selfdestruct implementation contracts (1/13 reports)
- **Migration Failures**: Chains permanently lost when migrating between layers (2/13 reports)

#### Business Impact
- **Consensus Severity**: HIGH (7/13 reports), MEDIUM (6/13 reports)
- **Financial Loss**: Direct fund theft possible via reentrancy; all taker collateral at risk
- **Operational Disruption**: Protocol halt if governor privilege lost; no upgrade path available
- **Trust Damage**: Failed upgrades require emergency patches, eroding user confidence
- **Recovery Complexity**: Some failures have no on-chain recovery mechanism

#### Affected Scenarios
- **Version Upgrades**: When modifying `AppStorage` structs without preserving slot layout
- **Multi-Call Operations**: Farm/Pipeline/Depot facets with external callbacks
- **Cross-Layer Migrations**: Moving chains between L1 and Gateway settlement layers
- **Facet Dependencies**: When libraries used by facets are modified but facets not recut
- **Access Control Integration**: Using standard OpenZeppelin contracts in Diamond context

### Secure Implementation

**Fix 1: Preserve Storage Layout with Gaps and Deprecation**
```solidity
// ✅ SECURE: Keep deprecated structs, add new fields at end
struct AppStorage {
    DiamondCutStorage __deprecated_diamondCutStorage;  // DO NOT REMOVE - preserves slots 0-6
    uint256[5] __gap_upgradeStorage;                    // Gap for future UpgradeStorage
    address governor;                                   // Still at slot 12
    Verifier verifier;                                  // Still at slot 13
    
    // New fields ONLY at the end
    UpgradeStorage upgradeStorage;                      // New location
}

// Document storage layout for CI validation
// Create machine-readable artifact describing deployed AppStorage
```

**Fix 2: Use EIP-7201 Namespaced Storage**
```solidity
// ✅ SECURE: EIP-7201 prevents slot collisions entirely
abstract contract AccessControlUpgradeable {
    // keccak256(abi.encode(uint256(keccak256("openzeppelin.storage.AccessControl")) - 1))
    bytes32 private constant ACCESS_CONTROL_STORAGE_LOCATION = 
        0x02dd7bc7dec4dceedda775e58dd541e08a116c6c53815c0bd028192f7b626800;
    
    struct AccessControlStorage {
        mapping(bytes32 role => RoleData) _roles;
    }
    
    function _getAccessControlStorage() private pure returns (AccessControlStorage storage $) {
        assembly {
            $.slot := ACCESS_CONTROL_STORAGE_LOCATION
        }
    }
}
```

**Fix 3: Reentrancy Guard on Diamond State**
```solidity
// ✅ SECURE: Reentrancy guard prevents callback exploitation
modifier nonReentrantFarm() {
    AppStorage storage s = LibAppStorage.diamondStorage();
    require(s.farmReentrancyStatus != 2, "ReentrancyGuard: reentrant call");
    s.farmReentrancyStatus = 2;
    _;
    s.farmReentrancyStatus = 1;
}

function advancedFarm(AdvancedFarmCall[] calldata data) 
    external payable 
    nonReentrantFarm  // Prevent reentrancy
    withEth 
{
    for (uint256 i = 0; i < data.length; ++i) {
        _advancedFarm(data[i]);
    }
}

// Also verify amounts spent match amounts charged
function _settleWithAmountCheck(uint256 expectedX, uint256 expectedY) internal {
    uint256 actualX = amountX;
    uint256 actualY = amountY;
    require(actualX == expectedX && actualY == expectedY, "Amount mismatch");
}
```

**Fix 4: Use Mappings Instead of Nested Structs**
```solidity
// ✅ SECURE: Mappings allow safe extension of inner structures
struct Props {
    bytes32 key;
    
    // Replace nested structs with indexed mappings
    mapping(uint256 => TokenBalance) tokenBalances;
    mapping(uint256 => BorrowingFee) borrowingFees;
    
    uint256 constant BASE_TOKEN_BALANCE = 0;
    uint256 constant BORROWING_FEE = 1;
}

// Access via constants - can add new struct fields safely
TokenBalance storage baseTokenBalance = props.tokenBalances[BASE_TOKEN_BALANCE];
BorrowingFee storage borrowingFee = props.borrowingFees[BORROWING_FEE];
```

**Fix 5: Comprehensive Upgrade Script with CI Validation**
```javascript
// ✅ SECURE: Automatically detect all modified facets
async function getModifiedFacets(fromCommit, toCommit) {
    // Use git diff to find all modified .sol files
    const modifiedFiles = execSync(
        `git diff --stat ${fromCommit}..${toCommit} -- "*.sol" | grep "Facet.sol"`
    );
    
    // Also include facets whose library dependencies changed
    const modifiedLibs = execSync(
        `git diff --stat ${fromCommit}..${toCommit} -- "*.sol" | grep "Lib.*\\.sol"`
    );
    
    // Find facets importing modified libraries
    const affectedFacets = findFacetsUsingLibs(modifiedLibs);
    
    return [...modifiedFiles, ...affectedFacets];
}

// CI integration
async function validateUpgrade() {
    const expectedFacets = await getModifiedFacets(PREVIOUS_COMMIT, CURRENT_COMMIT);
    const upgradeScriptFacets = parseUpgradeScript('bips.js');
    
    for (const facet of expectedFacets) {
        assert(upgradeScriptFacets.includes(facet), `Missing facet: ${facet}`);
    }
}
```

**Fix 6: Disable Initializers in Template Constructors**
```solidity
// ✅ SECURE: Prevent initialization of template contracts
contract ThreeDNSRegControl {
    constructor() {
        _disableInitializers();  // Template cannot be initialized
    }
    
    function initialize(
        address _authority,
        address resolver_,
        string memory domainName_,
        string memory domainVersion_,
        uint64 chainId_,
        string memory _baseUri,
        address _usdc
    ) external initializer {  // Only callable on proxy once
        _authority = _authority;
        // ...
    }
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: Struct modifications in storage libraries without gap preservation
- Pattern 2: OpenZeppelin AccessControl (not Upgradeable) in Diamond facets
- Pattern 3: External calls within payable facet functions without reentrancy guards
- Pattern 4: `withEth` or similar modifiers that refund address(this).balance
- Pattern 5: Nested structs in upgradeable storage (not using mappings)
- Pattern 6: diamondCut calls in upgrade scripts - verify all modified facets included
- Pattern 7: Template contracts missing _disableInitializers() in constructor
- Pattern 8: Copy-paste function pairs (freeze/unfreeze, pause/unpause) with same implementation
- Pattern 9: Migration functions without historical root validation
- Pattern 10: ERC1155/ERC721 safe transfers in facets enabling callback reentrancy
```

#### Audit Checklist
- [ ] Verify storage layout preserved when upgrading structs (use Slither `--print variable-order`)
- [ ] Confirm all facets use EIP-7201 namespaced storage or gap patterns
- [ ] Check for reentrancy guards on all facet functions with external calls
- [ ] Validate diamondCut scripts include all modified facets and library dependencies
- [ ] Ensure template contracts have _disableInitializers() in constructor
- [ ] Verify no nested structs exist that may need future extension
- [ ] Test freeze/unfreeze and similar paired functions actually call different implementations
- [ ] Confirm ETH refund logic cannot be exploited via reentrancy
- [ ] Check migration functions validate historical roots and state consistency
- [ ] Verify Diamond holds no user funds directly accessible via facet callbacks

### Real-World Examples

#### Known Protocol Findings
- **zkSync (OpenZeppelin 2023)** - Storage collision in AppStorage struct shift - deployed upgrade would have bricked protocol
- **GainsNetwork (Pashov 2024)** - accessControl mapping shifted from slot 2 to slot 4 during upgrade
- **Beanstalk (Cyfrin 2023)** - FarmFacet and DepotFacet reentrancy via ERC1155 callbacks - all intermediate ETH drainable
- **Arkis (TrailOfBits 2024)** - AccessControlDS using non-upgrade-aware OpenZeppelin base
- **Elfi (Sherlock 2024)** - Nested structs in LpPool.Props blocking future upgrades
- **Beanstalk BIP-39 (Cyfrin 2023)** - Modified facets missing from upgrade script broke Stalk accounting
- **3DNS (Cantina 2024)** - Template contract initialized by attacker enabling selfdestruct
- **zkSync (Code4rena 2024)** - unfreezeChain calling freezeDiamond instead of unfreezeDiamond
- **Ammplify (Sherlock 2025)** - RFTLib.settle reentrancy enabling Uniswap price manipulation

### Prevention Guidelines

#### Development Best Practices
1. **Always** use EIP-7201 namespaced storage for new Diamond implementations
2. **Never** modify struct sizes in existing storage - deprecate and add new at end
3. **Add** reentrancy guards to all facet functions that make external calls
4. **Create** machine-readable storage layout artifacts for CI validation
5. **Automate** facet dependency detection in upgrade scripts
6. **Disable** initializers in template contract constructors
7. **Use** mappings with constant indexes instead of nested structs
8. **Review** all paired functions (enable/disable, freeze/unfreeze) for copy-paste errors

#### Testing Requirements
- Unit tests for: Storage slot consistency before/after simulated upgrades
- Integration tests for: Complete upgrade flow with production fork state
- Fuzzing targets: Facet functions with external callbacks; ETH refund paths
- Invariant tests: No storage slot collisions between facets
- Upgrade simulation: All modified facets detected and included

### References

#### Technical Documentation
- [EIP-2535: Diamond Standard](https://eips.ethereum.org/EIPS/eip-2535)
- [EIP-7201: Namespaced Storage Layout](https://eips.ethereum.org/EIPS/eip-7201)
- [Diamond Upgrades Best Practices](https://eip2535diamonds.substack.com/p/diamond-upgrades)
- [OpenZeppelin Upgradeable Contracts](https://docs.openzeppelin.com/contracts/5.x/upgradeable)

#### Security Research
- [Slither Storage Layout Printer](https://github.com/crytic/slither) - `slither --print variable-order`
- [Diamond Storage Collision Detection](https://github.com/trailofbits/publications)

### Keywords for Search

`diamond proxy`, `EIP-2535`, `diamondCut`, `facet`, `storage collision`, `storage slot`, `AppStorage`, `struct shift`, `upgrade vulnerability`, `reentrancy facet`, `FarmFacet`, `DepotFacet`, `Pipeline`, `withEth modifier`, `refundEth`, `ERC1155 callback`, `onERC1155Received`, `nested struct`, `storage gap`, `AccessControl slot 0`, `AccessControlUpgradeable`, `EIP-7201`, `namespaced storage`, `template initialization`, `_disableInitializers`, `freeze unfreeze`, `facet upgrade`, `modified dependencies`, `library changes`, `upgrade script`, `diamondStorage`, `delegatecall`, `proxy pattern`, `multi-facet`, `loupe functions`, `selector collision`

### Related Vulnerabilities

- [Proxy Initialization Vulnerabilities](../initialization/proxy-initialization.md)
- [Standard Reentrancy Patterns](../reentrancy/reentrancy.md)
- [Upgradeable Contract Storage Gaps](../storage/storage-gaps.md)
- [Access Control Misconfigurations](../access-control/access-control.md)
