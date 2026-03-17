---
# Core Classification (Required)
protocol: generic
chain: everychain
category: governance
vulnerability_type: timelock_bypass

# Attack Vector Details (Required)
attack_type: logical_error|access_control
affected_component: timelock_controller|governance_admin|delay_enforcement

# Technical Primitives (Required)
primitives:
  - timelock
  - delay
  - governor
  - admin
  - execution
  - cancellation
  - scheduling
  - grace_period

# Impact Classification (Required)
severity: high
impact: governance_bypass|unauthorized_execution|fund_loss
exploitability: 0.75
financial_impact: critical

# Context Tags
tags:
  - defi
  - dao
  - governance
  - timelock
  - access_control
  - admin_privilege

# Version Info
language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | timelock_controller | timelock_bypass

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _timelockMint
  - admin
  - block.timestamp
  - cancel
  - cancellation
  - delay
  - emergencyWithdraw
  - execute
  - executeBatch
  - execution
  - governor
  - grace_period
  - initialize
  - mint
  - msg.sender
  - onlyAdmin
  - onlyTimelock
  - re
  - scheduling
  - setAdmin
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Timelock Bypass via Privileged Functions
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Malt Finance - Timelock Can Be Bypassed | `reports/dao_governance_findings/h-01-timelock-can-be-bypassed.md` | HIGH | Code4rena |
| Coinbase Solady - Cancelling bytes32(0) | `reports/dao_governance_findings/cancelling-bytes320-allows-timelock-takeover.md` | HIGH | Spearbit |

### Zero Delay Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Moonwell - Timelock Delay Set to Zero | `reports/dao_governance_findings/timelock-delay-is-set-to-zero-in-the-constructor.md` | MEDIUM | Halborn |

### Timelock Reduction/Override
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| NFTX - Bypass Zap Timelock | `reports/dao_governance_findings/m-09-bypass-zap-timelock.md` | MEDIUM | Code4rena |

### Canceled Proposal Execution
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| RAAC - Timelock Retains Canceled Proposals | `reports/dao_governance_findings/timelock-controller-retains-canceled-proposals-enabling-unauthorized-execution-a.md` | MEDIUM | Codehawks |

---

# Timelock Bypass Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Governance Timelock Security Audits**

---

## Table of Contents

1. [Timelock Bypass via Privileged Functions](#1-timelock-bypass-via-privileged-functions)
2. [Zero/Minimal Delay Vulnerabilities](#2-zerominimal-delay-vulnerabilities)
3. [Timelock Reduction During Active Lock](#3-timelock-reduction-during-active-lock)
4. [Canceled Proposal Still Executable](#4-canceled-proposal-still-executable)
5. [Storage Collision Attacks](#5-storage-collision-attacks)

---

## 1. Timelock Bypass via Privileged Functions

### Overview

Timelocks are designed to force a delay between proposal approval and execution, giving users time to exit if they disagree with a governance decision. When administrative functions like `setGovernor()` or `setDelay()` are not themselves subject to the timelock, the entire security model collapses.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/h-01-timelock-can-be-bypassed.md` (Malt Finance - Code4rena)



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | timelock_controller | timelock_bypass`
- Interaction scope: `single_contract`
- Primary affected component(s): `timelock_controller|governance_admin|delay_enforcement`
- High-signal code keywords: `_timelockMint`, `admin`, `block.timestamp`, `cancel`, `cancellation`, `delay`, `emergencyWithdraw`, `execute`
- Typical sink / impact: `governance_bypass|unauthorized_execution|fund_loss`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `4.function -> Governance.function -> GovernanceTimelock.function`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: Critical input parameter not validated against expected range or format
- Signal 2: Oracle data consumed without staleness check or sanity bounds
- Signal 3: User-supplied address or calldata forwarded without validation
- Signal 4: Missing check allows operation under invalid or stale state

#### False Positive Guards

- Not this bug when: Validation exists but is in an upstream function caller
- Safe if: Parameter range is inherently bounded by the type or protocol invariant
- Requires attacker control of: specific conditions per pattern

### Vulnerability Description

#### Root Cause

Critical governance functions that control the timelock parameters (delay, governor, admin) can be called directly by privileged addresses without going through the timelock delay mechanism themselves.

#### Attack Scenario

1. Governor/Admin key is compromised or turns malicious
2. Attacker calls `setGovernor(attackerAddress)` - takes effect IMMEDIATELY
3. New attacker-controlled governor calls `setDelay(0)` - takes effect IMMEDIATELY
4. Attacker now has unrestricted access to all timelocked functions
5. Attacker drains treasury, mints tokens, or executes other privileged actions

### Vulnerable Pattern Examples

**Example 1: setGovernor Without Timelock** [HIGH]
> 📖 Reference: `reports/dao_governance_findings/h-01-timelock-can-be-bypassed.md`
```solidity
// ❌ VULNERABLE: Governor can set new governor immediately
contract Timelock {
    address public governor;
    uint256 public delay;
    
    function setGovernor(address _governor) 
        public 
        onlyRole(GOVERNOR_ROLE, "Must have governor role") 
    {
        // ❌ No timelock delay for this critical function!
        _swapRole(_governor, governor, GOVERNOR_ROLE);
        governor = _governor;
        emit NewGovernor(_governor);
    }
    
    function setDelay(uint256 _delay) 
        public 
        onlyRole(GOVERNOR_ROLE, "Must have governor role") 
    {
        // ❌ Delay can be changed to 0 immediately!
        require(_delay >= 0 && _delay < gracePeriod);
        delay = _delay;
        emit NewDelay(delay);
    }
}
```

**Example 2: Admin Role Not Subject to Timelock** [HIGH]
```solidity
// ❌ VULNERABLE: Admin can bypass all timelock protections
contract GovernanceTimelock {
    address public admin;
    
    modifier onlyAdmin() {
        require(msg.sender == admin, "Not admin");
        _;
    }
    
    // ❌ These functions bypass the timelock entirely
    function emergencyWithdraw(address to, uint256 amount) external onlyAdmin {
        token.transfer(to, amount);
    }
    
    function setAdmin(address _admin) external onlyAdmin {
        admin = _admin;  // Immediate effect
    }
}
```

### Impact Analysis

#### Technical Impact
- Complete bypass of all timelock security guarantees
- Privileged functions executable without warning period
- Users have no time to react to malicious governance

#### Business Impact
- Treasury can be drained instantly
- Minter roles can be assigned to attackers
- Contract upgrades can be pushed maliciously
- Total loss of user funds possible

#### Affected Scenarios
- Any protocol with timelocked governance
- Multi-sig controlled treasuries
- Upgradeable proxy systems with time delays

### Secure Implementation

**Fix 1: Administrative Functions Through Timelock**
```solidity
// ✅ SECURE: All administrative actions go through timelock
contract SecureTimelock {
    modifier onlyTimelock() {
        require(msg.sender == address(this), "Must go through timelock");
        _;
    }
    
    function setGovernor(address _governor) external onlyTimelock {
        // Can only be called by executing a timelocked proposal
        governor = _governor;
    }
    
    function setDelay(uint256 _delay) external onlyTimelock {
        // Can only be called by executing a timelocked proposal
        require(_delay >= MINIMUM_DELAY, "Delay too short");
        delay = _delay;
    }
}
```

**Fix 2: Self-Administered Timelock**
```solidity
// ✅ SECURE: Timelock is its own admin
function initialize(address _admin) external initializer {
    // ✅ Timelock administers itself - all changes require delay
    _adminSetup(address(this));  // NOT _admin!
    
    // Governor can only propose, not directly execute
    _grantRole(PROPOSER_ROLE, _admin);
    _grantRole(EXECUTOR_ROLE, _admin);
}
```

---

## 2. Zero/Minimal Delay Vulnerabilities

### Overview

If the timelock delay is set to zero during initialization or can be reduced below a safe minimum, the timelock provides no security benefit.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/timelock-delay-is-set-to-zero-in-the-constructor.md` (Moonwell - Halborn)

### Vulnerability Description

#### Root Cause

Constructor or initialization code sets the delay to zero, or validation logic allows zero/minimal delays, effectively disabling the timelock.

#### Attack Scenario

1. Protocol deploys timelock with delay = 0 (by accident or design flaw)
2. Proposals can be executed immediately after creation
3. Malicious proposals cannot be detected or prevented
4. Users have no time to exit before harmful actions execute

### Vulnerable Pattern Examples

**Example 1: Zero Delay in Constructor** [MEDIUM]
> 📖 Reference: `reports/dao_governance_findings/timelock-delay-is-set-to-zero-in-the-constructor.md`
```solidity
// ❌ VULNERABLE: Delay hardcoded to 0 despite parameter
constructor(address admin_, uint delay_) public {
    require(delay_ >= MINIMUM_DELAY, "Delay must exceed minimum");
    require(delay_ <= MAXIMUM_DELAY, "Delay must not exceed maximum");
    admin = admin_;
    delay = 0;  // ❌ BUG: Should be delay = delay_;
}
```

**Example 2: No Minimum Delay Enforcement** [MEDIUM]
```solidity
// ❌ VULNERABLE: Allows setting delay to 0
function setDelay(uint256 _delay) external onlyGovernor {
    require(_delay >= 0, "Invalid delay");  // ❌ Zero is allowed!
    delay = _delay;
}
```

### Secure Implementation

**Fix 1: Enforce Minimum Delay**
```solidity
// ✅ SECURE: Minimum delay enforced
uint256 public constant MINIMUM_DELAY = 1 days;

constructor(address admin_, uint256 delay_) {
    require(delay_ >= MINIMUM_DELAY, "Delay must exceed minimum");
    admin = admin_;
    delay = delay_;  // ✅ Uses parameter, not hardcoded
}

function setDelay(uint256 _delay) external onlyTimelock {
    require(_delay >= MINIMUM_DELAY, "Delay must exceed minimum");
    delay = _delay;
}
```

---

## 3. Timelock Reduction During Active Lock

### Overview

When a new timelock duration is applied retroactively to existing locks, users can reduce their lock periods by triggering re-calculation with a shorter global timelock.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/m-09-bypass-zap-timelock.md` (NFTX - Code4rena)

### Vulnerability Description

#### Root Cause

Timelock end timestamp is calculated as `block.timestamp + timelockLength` every time a minting/locking function is called, rather than taking the maximum of existing and new timelocks.

#### Attack Scenario

1. User locks tokens via StakingZap with 7-day timelock
2. User immediately deposits a tiny amount via a different path with 2ms timelock
3. Timelock is recalculated: `block.timestamp + 2ms`
4. User's 7-day lock is now only 2ms
5. User can withdraw immediately

### Vulnerable Pattern Examples

**Example 1: Timelock Always Overwrites** [MEDIUM]
> 📖 Reference: `reports/dao_governance_findings/m-09-bypass-zap-timelock.md`
```solidity
// ❌ VULNERABLE: Always overwrites timelock, even if shorter
function _timelockMint(address account, uint256 amount, uint256 timelockLength) internal {
    uint256 timelockFinish = block.timestamp + timelockLength;
    timelock[account] = timelockFinish;  // ❌ Overwrites longer existing lock!
    emit Timelocked(account, timelockFinish);
    _mint(account, amount);
}

// Contract A uses 7 days
uint256 public inventoryLockTime = 7 days;

// Contract B uses 2 milliseconds (default)
uint256 public constant DEFAULT_LOCKTIME = 2;  // ❌ Effectively no lock
```

### Secure Implementation

**Fix 1: Use Maximum of Existing and New Timelock**
```solidity
// ✅ SECURE: Only extend timelock, never reduce
function _timelockMint(address account, uint256 amount, uint256 timelockLength) internal {
    uint256 timelockFinish = block.timestamp + timelockLength;
    
    // ✅ Only update if new lock is further in future
    if (timelockFinish > timelock[account]) {
        timelock[account] = timelockFinish;
        emit Timelocked(account, timelockFinish);
    }
    
    _mint(account, amount);
}
```

---

## 4. Canceled Proposal Still Executable

### Overview

When a proposal is canceled in the governance contract but not canceled in the underlying timelock controller, the proposal remains executable in the timelock.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/timelock-controller-retains-canceled-proposals-enabling-unauthorized-execution-a.md` (RAAC - Codehawks)

### Vulnerability Description

#### Root Cause

The `cancel()` function in the governance contract only updates the governance state but does not call `cancel()` on the TimelockController, leaving the operation still queued for execution.

#### Attack Scenario

1. Proposal is created and passes voting
2. Proposal is scheduled in TimelockController
3. Proposer or guardian cancels proposal in Governance contract
4. Users believe proposal is canceled
5. Malicious executor calls `TimelockController.executeBatch()`
6. Proposal executes despite being "canceled"

### Vulnerable Pattern Examples

**Example 1: Cancel Doesn't Propagate to Timelock** [MEDIUM]
> 📖 Reference: `reports/dao_governance_findings/timelock-controller-retains-canceled-proposals-enabling-unauthorized-execution-a.md`
```solidity
// ❌ VULNERABLE: Cancel only updates governance state, not timelock
contract Governance {
    function cancel(uint256 proposalId) external override {
        ProposalCore storage proposal = _proposals[proposalId];
        require(proposal.startTime != 0, "Proposal doesn't exist");
        
        ProposalState currentState = state(proposalId);
        require(currentState != ProposalState.Executed, "Cannot cancel executed");
        
        // ❌ Only marks as canceled in governance contract
        proposal.canceled = true;
        emit ProposalCanceled(proposalId, msg.sender, "Canceled");
        
        // ❌ MISSING: Does NOT cancel in TimelockController!
        // timelock.cancel(operationId);  <- This is missing
    }
}

// Meanwhile in TimelockController...
contract TimelockController {
    function executeBatch(...) external {
        bytes32 id = hashOperationBatch(...);
        Operation storage op = _operations[id];
        
        // ❌ No check that operation was canceled in governance
        require(op.timestamp != 0, "Operation not found");
        require(!op.executed, "Already executed");
        require(block.timestamp >= op.timestamp, "Not ready");
        
        // Executes even though governance shows "canceled"!
        _execute(...);
        op.executed = true;
    }
}
```

### Secure Implementation

**Fix 1: Cancel in Both Contracts**
```solidity
// ✅ SECURE: Cancel propagates to timelock
function cancel(uint256 proposalId) external override {
    ProposalCore storage proposal = _proposals[proposalId];
    require(proposal.startTime != 0, "Proposal doesn't exist");
    
    ProposalState currentState = state(proposalId);
    require(currentState != ProposalState.Executed, "Cannot cancel executed");
    
    proposal.canceled = true;
    
    // ✅ Also cancel in TimelockController if scheduled
    if (currentState == ProposalState.Queued) {
        bytes32 operationId = _getOperationId(proposalId);
        timelock.cancel(operationId);
    }
    
    emit ProposalCanceled(proposalId, msg.sender, "Canceled");
}
```

---

## 5. Storage Collision Attacks

### Overview

Specialized attacks that exploit storage layout to corrupt timelock state, such as using `cancel(bytes32(0))` to clear the minimum delay storage slot.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/cancelling-bytes320-allows-timelock-takeover.md` (Coinbase Solady - Spearbit)

### Vulnerability Description

#### Root Cause

The `cancel()` function takes a raw `bytes32` id as input without validation. When XORed with internal storage slot calculations, arbitrary storage slots can be cleared if the id matches certain patterns.

#### Attack Scenario

1. Attacker with CANCELLER_ROLE calls `cancel(bytes32(0))`
2. Storage slot for minimum delay is cleared (if it has LSB = 0)
3. Contract now has zero minimum delay
4. `initialize()` can be called again (relies on zero-check)
5. Attacker reinitializes with themselves as admin with zero delay
6. Complete timelock takeover

### Vulnerable Pattern Examples

**Example 1: Arbitrary Storage Slot Clearing** [CRITICAL]
> 📖 Reference: `reports/dao_governance_findings/cancelling-bytes320-allows-timelock-takeover.md`
```solidity
// ❌ VULNERABLE: cancel() takes raw id, allowing storage manipulation
function cancel(bytes32 id) public virtual onlyRole(CANCELLER_ROLE) {
    assembly {
        // Storage slot = XOR of id and _TIMELOCK_SLOT
        let s := xor(shl(72, id), _TIMELOCK_SLOT)  // ❌ id not validated!
        let p := sload(s)
        
        // ❌ If id = 0, clears the _TIMELOCK_SLOT itself (minimum delay)
        if or(and(1, p), iszero(p)) {
            mstore(0x00, 0xd639b0bf)  // TimelockInvalidOperation
            revert(0x1c, 0x44)
        }
        
        sstore(s, 0)  // ❌ Clears whatever storage slot was computed
        log2(0x00, 0x00, _CANCELLED_EVENT_SIGNATURE, id)
    }
}
```

### Secure Implementation

**Fix 1: Compute ID from Operation Data**
```solidity
// ✅ SECURE: ID is computed, not provided directly
function cancel(
    address[] calldata targets,
    uint256[] calldata values,
    bytes[] calldata calldatas,
    bytes32 predecessor,
    bytes32 salt
) public virtual onlyRole(CANCELLER_ROLE) {
    // ✅ ID is derived from operation data, cannot be arbitrary
    bytes32 id = hashOperationBatch(targets, values, calldatas, predecessor, salt);
    
    _cancel(id);
}

// Alternative: Use keccak256 for storage slot calculation
function cancel(bytes32 id) public virtual onlyRole(CANCELLER_ROLE) {
    assembly {
        mstore(0x09, _TIMELOCK_SLOT)
        mstore(0x00, id)
        let s := keccak256(0x00, 0x29)  // ✅ Hash-based slot prevents collisions
        // ... rest of logic
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- setGovernor(), setAdmin(), setDelay() callable by non-timelock addresses
- MINIMUM_DELAY constant set to 0 or very low value
- delay = 0 hardcoded in constructor despite parameter
- timelock[account] = newValue without max() check
- Governance.cancel() not calling TimelockController.cancel()
- cancel(bytes32 id) taking raw id input without validation
- initialize() checking for zero delay to prevent re-init
```

### Audit Checklist
- [ ] Are setGovernor/setAdmin/setDelay subject to timelock delay?
- [ ] Is MINIMUM_DELAY enforced and reasonable (e.g., 1+ day)?
- [ ] Is delay properly assigned in constructor (not hardcoded to 0)?
- [ ] Does new timelock use max(existing, new) logic?
- [ ] Does cancel() propagate to TimelockController?
- [ ] Is the cancel() id parameter validated/derived?
- [ ] Can initialize() be called multiple times?

---

## Prevention Guidelines

### Development Best Practices
1. Make timelock its own admin - all changes require delay
2. Enforce meaningful MINIMUM_DELAY (e.g., 24-48 hours)
3. Timelock should only extend, never reduce
4. Cancel should propagate to all relevant contracts
5. Validate or derive operation IDs, never accept raw bytes32

### Testing Requirements
- Unit tests for: governor/admin change flows, delay reduction attempts
- Integration tests for: cancel propagation, re-initialization attempts
- Fuzzing targets: cancel() with various id patterns, delay modification flows

---

## Keywords for Search

`timelock`, `delay`, `governor`, `admin`, `bypass`, `setDelay`, `setGovernor`, `cancel`, `execute`, `minimum_delay`, `grace_period`, `timelock_controller`, `proposal_execution`, `storage_collision`, `re-initialization`, `zero_delay`, `timelock_takeover`, `governance_bypass`

---

## Related Vulnerabilities

- [Voting Power Manipulation](./voting-power-manipulation.md)
- [Quorum Manipulation](./quorum-manipulation.md)
- [Proposal Lifecycle Manipulation](./proposal-lifecycle-manipulation.md)

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

`_timelockMint`, `access_control`, `admin`, `admin_privilege`, `block.timestamp`, `cancel`, `cancellation`, `dao`, `defi`, `delay`, `emergencyWithdraw`, `execute`, `executeBatch`, `execution`, `governance`, `governor`, `grace_period`, `initialize`, `mint`, `msg.sender`, `onlyAdmin`, `onlyTimelock`, `re`, `scheduling`, `setAdmin`, `timelock`, `timelock_bypass`
