---
# Core Classification (Required)
protocol: generic
chain: everychain
category: governance
vulnerability_type: proposal_lifecycle_manipulation

# Attack Vector Details (Required)
attack_type: logical_error|griefing|access_control
affected_component: proposal_creation|proposal_cancellation|proposal_execution|state_machine

# Technical Primitives (Required)
primitives:
  - proposal
  - cancellation
  - threshold
  - state_machine
  - expiration
  - execution
  - griefing

# Impact Classification (Required)
severity: medium
impact: governance_dos|proposal_manipulation|griefing
exploitability: 0.60
financial_impact: medium_to_high

# Context Tags
tags:
  - defi
  - dao
  - governance
  - proposal
  - cancellation
  - griefing
  - state_machine

# Version Info
language: solidity
version: all

# Pattern Identity (Required)
root_cause_family: missing_validation
pattern_key: missing_validation | proposal_creation | proposal_lifecycle_manipulation

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - _isExpired
  - block.number
  - block.timestamp
  - cancel
  - cancellation
  - execute
  - execution
  - expiration
  - griefing
  - mint
  - msg.sender
  - proposal
  - propose
  - queue
  - spam
  - state
  - state_machine
  - threshold
  - updateProposal
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Unrestricted Proposal Cancellation
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| RAAC - Unrestricted Cancellation | `reports/dao_governance_findings/unrestricted-proposal-cancellation-allows-governance-process-manipulation.md` | MEDIUM | Codehawks |
| GMX - Proposals Can Be Cancelled | `reports/dao_governance_findings/h-04-proposals-can-be-cancelled.md` | HIGH | Code4rena |

### Proposal Threshold Bypass/Griefing
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Y2K Finance - Threshold Bypass for Spam | `reports/dao_governance_findings/bypassing-the-governances-proposal-threshold-to-spam-malicious-proposal-as-a-gri.md` | MEDIUM | Code4rena |

### Proposal Expiration Logic Errors
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Autonomint - Incorrect Expiration Logic | `reports/dao_governance_findings/m-03-the-proposal-expiration-logic-is-incorrect.md` | MEDIUM | Code4rena |

### State Machine Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Farcaster - Ties Approved | `reports/dao_governance_findings/m09-ties-in-governance-proposals-are-approved.md` | MEDIUM | Code4rena |
| Usual Money - Majority Not Required | `reports/dao_governance_findings/m-28-state-function-does-not-require-majority-of-votes-for-supporting-and-passin.md` | MEDIUM | Code4rena |

---

# Proposal Lifecycle Manipulation - Comprehensive Database

**A Complete Pattern-Matching Guide for Proposal Lifecycle Security Audits**

---

## Table of Contents

1. [Unrestricted Proposal Cancellation](#1-unrestricted-proposal-cancellation)
2. [Proposal Threshold Bypass for Griefing](#2-proposal-threshold-bypass-for-griefing)
3. [Proposal Expiration Logic Errors](#3-proposal-expiration-logic-errors)
4. [State Machine Transition Vulnerabilities](#4-state-machine-transition-vulnerabilities)
5. [Proposal Execution Vulnerabilities](#5-proposal-execution-vulnerabilities)

---

## 1. Unrestricted Proposal Cancellation

### Overview

Governance proposals should only be cancellable by authorized parties under specific conditions. When cancellation is unrestricted, attackers can repeatedly cancel legitimate proposals, griefing the governance process or preventing critical protocol changes.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/unrestricted-proposal-cancellation-allows-governance-process-manipulation.md` (RAAC - Codehawks)
> - `reports/dao_governance_findings/h-04-proposals-can-be-cancelled.md` (GMX - Code4rena)



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of missing_validation"
- Pattern key: `missing_validation | proposal_creation | proposal_lifecycle_manipulation`
- Interaction scope: `single_contract`
- Primary affected component(s): `proposal_creation|proposal_cancellation|proposal_execution|state_machine`
- High-signal code keywords: `_isExpired`, `block.number`, `block.timestamp`, `cancel`, `cancellation`, `execute`, `execution`, `expiration`
- Typical sink / impact: `governance_dos|proposal_manipulation|griefing`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `proposal_cancellation.function -> proposal_creation.function -> proposal_execution.function`
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

The `cancel()` function lacks proper access control, allowing anyone (or a broader class of users than intended) to cancel proposals. This includes:
- No caller validation
- Checking proposer's current voting power instead of power at proposal time
- Missing proposer-only restrictions

#### Attack Scenario

1. Legitimate proposal passes voting and is queued for execution
2. Attacker (or even proposer's own tokens sold) calls cancel()
3. Proposal is cancelled, negating all voting efforts
4. Attacker repeats for every proposal, griefing entire governance

### Vulnerable Pattern Examples

**Example 1: Anyone Can Cancel** [HIGH]
> 📖 Reference: `reports/dao_governance_findings/h-04-proposals-can-be-cancelled.md`
```solidity
// ❌ VULNERABLE: No access control on cancel
function cancel(uint256 proposalId) external {
    Proposal storage proposal = proposals[proposalId];
    
    // ❌ No check on who is calling!
    require(state(proposalId) != ProposalState.Executed, "Already executed");
    
    proposal.canceled = true;
    emit ProposalCanceled(proposalId);
}
```

**Example 2: Cancellation Based on Current Voting Power** [MEDIUM]
> 📖 Reference: `reports/dao_governance_findings/unrestricted-proposal-cancellation-allows-governance-process-manipulation.md`
```solidity
// ❌ VULNERABLE: Uses current voting power, not snapshot
function cancel(uint256 proposalId) external {
    Proposal storage proposal = proposals[proposalId];
    
    // ❌ BUG: Checks CURRENT voting power, not at proposal time
    if (msg.sender != proposal.proposer) {
        require(
            getVotes(proposal.proposer, block.timestamp) < proposalThreshold,
            "Proposer above threshold"
        );
    }
    
    // Anyone can cancel if proposer sold/transferred tokens!
    _cancel(proposalId);
}

// Attack:
// 1. User A creates proposal with 1000 tokens (above 500 threshold)
// 2. User A sells 600 tokens (now has 400, below threshold)
// 3. Anyone calls cancel() - succeeds because current balance < threshold
```

### Impact Analysis

#### Technical Impact
- Proposals can be cancelled by unauthorized parties
- Governance decisions can be griefed indefinitely
- Even passed and queued proposals can be cancelled

#### Business Impact
- Critical protocol upgrades blocked
- Security patches cannot be deployed
- Complete governance paralysis possible

#### Affected Scenarios
- Any DAO where proposers may sell/delegate tokens
- Protocols with public cancel() functions
- Governance systems without proposer-only cancellation

### Secure Implementation

**Fix 1: Proposer-Only Cancellation**
```solidity
// ✅ SECURE: Only proposer can cancel their own proposal
function cancel(uint256 proposalId) external {
    Proposal storage proposal = proposals[proposalId];
    
    // ✅ Only the original proposer can cancel
    require(msg.sender == proposal.proposer, "Only proposer can cancel");
    require(state(proposalId) == ProposalState.Pending, "Only pending");
    
    _cancel(proposalId);
}
```

**Fix 2: Use Snapshot Voting Power**
```solidity
// ✅ SECURE: Check voting power at proposal creation snapshot
function cancel(uint256 proposalId) external {
    Proposal storage proposal = proposals[proposalId];
    
    if (msg.sender != proposal.proposer) {
        // ✅ Uses SNAPSHOT voting power, not current
        require(
            getVotes(proposal.proposer, proposal.startBlock) < proposalThreshold,
            "Proposer above threshold at snapshot"
        );
    }
    
    _cancel(proposalId);
}
```

---

## 2. Proposal Threshold Bypass for Griefing

### Overview

Proposal thresholds exist to prevent spam proposals. If users can temporarily acquire voting power to meet the threshold (e.g., flash loans, temporary delegation) and then lose it, they can spam governance while circumventing the intended barrier.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/bypassing-the-governances-proposal-threshold-to-spam-malicious-proposal-as-a-gri.md` (Y2K Finance - Code4rena)

### Vulnerability Description

#### Root Cause

Threshold is checked at proposal creation time using current voting power. Proposer can acquire tokens momentarily, create proposals, then dispose of tokens, having never held meaningful stake.

#### Attack Scenario

1. Proposal threshold: 1% of total supply (10,000 tokens)
2. Attacker flash loans 10,000 tokens
3. Attacker creates spam proposal
4. Attacker repays flash loan in same transaction
5. Protocol has no mechanism to cancel (proposer never had real stake)
6. Repeat to spam hundreds of malicious proposals

### Vulnerable Pattern Examples

**Example 1: Threshold Only Checked at Creation** [MEDIUM]
> 📖 Reference: `reports/dao_governance_findings/bypassing-the-governances-proposal-threshold-to-spam-malicious-proposal-as-a-gri.md`
```solidity
// ❌ VULNERABLE: Only checks threshold at creation, no ongoing requirement
function propose(
    address[] memory targets,
    uint256[] memory values,
    bytes[] memory calldatas,
    string memory description
) public returns (uint256) {
    // ❌ Threshold checked only at this moment
    require(
        getVotes(msg.sender, block.number - 1) >= proposalThreshold,
        "Below proposal threshold"
    );
    
    // Proposal created - attacker can now dispose of tokens
    uint256 proposalId = proposalCount++;
    // ...
    
    return proposalId;
}

// Meanwhile, cancel() requires proposer to have dropped below threshold:
function cancel(uint256 proposalId) external {
    Proposal storage proposal = proposals[proposalId];
    
    // ❌ Proposer had flash loan tokens at creation, now has none
    // But this check uses block.number - 1, which shows flash loan balance!
    require(
        getVotes(proposal.proposer, block.number - 1) < proposalThreshold,
        "Proposer above threshold"
    );
    
    // ❌ Can't cancel because snapshot shows they had tokens
    _cancel(proposalId);
}
```

### Secure Implementation

**Fix 1: Guardian-Cancellable Spam Proposals**
```solidity
// ✅ SECURE: Guardian can cancel spam proposals
address public guardian;

function cancel(uint256 proposalId) external {
    Proposal storage proposal = proposals[proposalId];
    
    // ✅ Guardian can always cancel (for emergency/spam protection)
    if (msg.sender == guardian) {
        _cancel(proposalId);
        return;
    }
    
    // Regular cancellation logic
    require(msg.sender == proposal.proposer, "Not proposer");
    _cancel(proposalId);
}
```

**Fix 2: Require Ongoing Stake**
```solidity
// ✅ SECURE: Verify proposer maintains stake
function execute(uint256 proposalId) external {
    Proposal storage proposal = proposals[proposalId];
    
    // ✅ Check proposer still meets threshold at execution
    require(
        getVotes(proposal.proposer, block.number - 1) >= proposalThreshold,
        "Proposer dropped below threshold"
    );
    
    // ... execute proposal
}
```

---

## 3. Proposal Expiration Logic Errors

### Overview

Proposals should expire after a grace period following voting. Incorrect expiration logic can cause proposals to be permanently executable (never expire) or expire immediately (always fail).

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/m-03-the-proposal-expiration-logic-is-incorrect.md` (Autonomint - Code4rena)

### Vulnerability Description

#### Root Cause

Expiration timestamp calculation errors:
- Wrong base timestamp (start instead of end)
- Off-by-one errors in comparison
- Missing grace period addition
- Inverted comparison operators

#### Attack Scenario

1. Proposal passes voting on day 1
2. Grace period: 7 days to execute
3. Bug: Expiration = startTime + gracePeriod (should be endTime + gracePeriod)
4. If voting period is 3 days, proposal expires on day 8
5. But execution window is only days 4-8, then days 9-14 expected
6. Users miss execution window, proposal lost

### Vulnerable Pattern Examples

**Example 1: Wrong Base for Expiration** [MEDIUM]
> 📖 Reference: `reports/dao_governance_findings/m-03-the-proposal-expiration-logic-is-incorrect.md`
```solidity
// ❌ VULNERABLE: Uses startTime instead of endTime
function _isExpired(uint256 proposalId) internal view returns (bool) {
    Proposal storage proposal = proposals[proposalId];
    
    // ❌ BUG: Should be endTime + gracePeriod
    return block.timestamp > proposal.startTime + gracePeriod;
    
    // If voting period is 7 days and grace period is 7 days:
    // - Proposal starts: day 0
    // - Voting ends: day 7
    // - Expected expiration: day 14
    // - Actual expiration: day 7 (immediately after voting!)
}
```

**Example 2: Never Expires (Missing Expiration Check)** [MEDIUM]
```solidity
// ❌ VULNERABLE: Proposals never expire
function state(uint256 proposalId) public view returns (ProposalState) {
    Proposal storage proposal = proposals[proposalId];
    
    if (proposal.executed) return ProposalState.Executed;
    if (proposal.canceled) return ProposalState.Canceled;
    
    if (block.timestamp < proposal.endTime) {
        return ProposalState.Active;
    }
    
    if (_quorumReached(proposalId) && _voteSucceeded(proposalId)) {
        // ❌ No expiration check - proposal succeeds forever!
        return ProposalState.Succeeded;
    }
    
    return ProposalState.Defeated;
}
```

### Secure Implementation

**Fix 1: Correct Expiration Calculation**
```solidity
// ✅ SECURE: Proper expiration based on voting end time
function _isExpired(uint256 proposalId) internal view returns (bool) {
    Proposal storage proposal = proposals[proposalId];
    
    // ✅ Grace period starts from END of voting
    return block.timestamp > proposal.endTime + gracePeriod;
}

function state(uint256 proposalId) public view returns (ProposalState) {
    // ... other checks ...
    
    if (_quorumReached(proposalId) && _voteSucceeded(proposalId)) {
        // ✅ Check expiration for succeeded proposals
        if (_isExpired(proposalId)) {
            return ProposalState.Expired;
        }
        return ProposalState.Succeeded;
    }
    
    return ProposalState.Defeated;
}
```

---

## 4. State Machine Transition Vulnerabilities

### Overview

Governance proposal state machines define the valid transitions between states (Pending → Active → Succeeded/Defeated → Queued → Executed). Bugs in state logic can allow invalid transitions or skip required states.

### Vulnerability Description

#### Root Cause

State machine implementation errors:
- Missing state checks before transitions
- Wrong state returned from state() function
- Race conditions between state checks and actions

### Vulnerable Pattern Examples

**Example 1: Execute Without Queueing** [HIGH]
```solidity
// ❌ VULNERABLE: Can execute without going through queue
function execute(uint256 proposalId) external {
    Proposal storage proposal = proposals[proposalId];
    
    // ❌ Only checks if succeeded, not if queued
    require(state(proposalId) == ProposalState.Succeeded, "Not succeeded");
    
    // Skips timelock queue entirely!
    _execute(proposal.targets, proposal.values, proposal.calldatas);
    proposal.executed = true;
}
```

**Example 2: Re-execution After Expiration** [MEDIUM]
```solidity
// ❌ VULNERABLE: Expired proposals can be re-queued
function queue(uint256 proposalId) external {
    // ❌ No check for expiration
    require(state(proposalId) == ProposalState.Succeeded, "Not succeeded");
    
    // Even if proposal expired, state() might still return Succeeded
    _queue(proposalId);
}
```

### Secure Implementation

**Fix 1: Enforce Complete State Machine**
```solidity
// ✅ SECURE: Proper state machine with all transitions validated
function queue(uint256 proposalId) external {
    ProposalState currentState = state(proposalId);
    require(currentState == ProposalState.Succeeded, "Must be succeeded");
    require(!_proposals[proposalId].queued, "Already queued");
    
    _queue(proposalId);
    _proposals[proposalId].queued = true;
}

function execute(uint256 proposalId) external {
    ProposalState currentState = state(proposalId);
    require(currentState == ProposalState.Queued, "Must be queued");
    require(block.timestamp >= _proposals[proposalId].eta, "Timelock not passed");
    
    _execute(proposalId);
}
```

---

## 5. Proposal Execution Vulnerabilities

### Overview

Proposal execution is the final critical step. Vulnerabilities at this stage can lead to unauthorized execution, failed execution with state corruption, or execution of modified proposal content.

### Vulnerability Description

#### Root Cause

Execution-related issues:
- Proposal content modified after creation
- Execution without proper state checks
- Partial execution with no rollback
- Reentrancy during execution

### Vulnerable Pattern Examples

**Example 1: Proposal Content Modified** [CRITICAL]
```solidity
// ❌ VULNERABLE: Proposal data not immutable
struct Proposal {
    address[] targets;  // ❌ Mutable array
    uint256[] values;
    bytes[] calldatas;
}

function updateProposal(uint256 proposalId, address[] calldata newTargets) external {
    // ❌ Allows changing proposal after voting!
    proposals[proposalId].targets = newTargets;
}
```

**Example 2: Partial Execution Corruption** [HIGH]
```solidity
// ❌ VULNERABLE: No atomic execution
function execute(uint256 proposalId) external {
    Proposal storage proposal = proposals[proposalId];
    
    for (uint256 i = 0; i < proposal.targets.length; i++) {
        // ❌ If one call fails, previous calls still executed
        (bool success,) = proposal.targets[i].call{value: proposal.values[i]}(
            proposal.calldatas[i]
        );
        require(success, "Call failed");  // Reverts but damage may be done
    }
    
    proposal.executed = true;
}
```

### Secure Implementation

**Fix 1: Immutable Proposal Content**
```solidity
// ✅ SECURE: Proposal content stored by hash
function propose(...) external returns (uint256) {
    bytes32 proposalHash = keccak256(abi.encode(targets, values, calldatas));
    
    Proposal storage proposal = proposals[proposalId];
    proposal.contentHash = proposalHash;
    // ✅ Content passed at execution must match hash
}

function execute(uint256 proposalId, address[] calldata targets, ...) external {
    bytes32 proposalHash = keccak256(abi.encode(targets, values, calldatas));
    
    // ✅ Verify content matches original proposal
    require(proposals[proposalId].contentHash == proposalHash, "Content mismatch");
    
    _execute(targets, values, calldatas);
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- cancel() with no access control or weak access control
- Threshold checks using current voting power instead of snapshot
- Expiration calculated from startTime instead of endTime
- Missing expiration check in state() function
- execute() without checking for Queued state
- Mutable proposal content after creation
- Partial execution without atomicity
- Missing guardian/admin override for spam protection
```

### Audit Checklist
- [ ] Can only authorized parties cancel proposals?
- [ ] Does cancellation use snapshot voting power, not current?
- [ ] Is there a guardian role for spam/griefing protection?
- [ ] Is expiration based on voting END time + grace period?
- [ ] Does state() return Expired for old succeeded proposals?
- [ ] Must proposals be queued before execution?
- [ ] Is proposal content immutable after creation?
- [ ] Is execution atomic (all-or-nothing)?

---

## Prevention Guidelines

### Development Best Practices
1. Restrict cancellation to proposer or guardian only
2. Use snapshot voting power for threshold checks
3. Calculate expiration from voting end time
4. Implement complete state machine with all transitions
5. Store proposal content by hash, verify at execution
6. Make execution atomic or implement proper rollback

### Testing Requirements
- Unit tests for: cancellation access control, expiration edge cases
- Integration tests for: state machine transitions, execution atomicity
- Fuzzing targets: cancel() with various callers, expiration boundaries

---

## Keywords for Search

`proposal`, `cancel`, `cancellation`, `threshold`, `expiration`, `grace_period`, `state_machine`, `execute`, `queue`, `griefing`, `spam_proposal`, `proposal_hash`, `atomic_execution`, `proposer`, `guardian`, `voting_power_snapshot`

---

## Related Vulnerabilities

- [Voting Power Manipulation](./voting-power-manipulation.md)
- [Timelock Bypass](./timelock-bypass.md)
- [Quorum Manipulation](./quorum-manipulation.md)

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

`_isExpired`, `block.number`, `block.timestamp`, `cancel`, `cancellation`, `dao`, `defi`, `execute`, `execution`, `expiration`, `governance`, `griefing`, `mint`, `msg.sender`, `proposal`, `proposal_lifecycle_manipulation`, `propose`, `queue`, `spam`, `state`, `state_machine`, `threshold`, `updateProposal`
