---
# Core Classification
protocol: generic
chain: cosmos
category: governance
vulnerability_type: voting_manipulation

# Attack Vector Details
attack_type: economic_exploit
affected_component: governance_module

# Technical Primitives
primitives:
  - quorum_calculation
  - voting_power
  - delegation
  - offboarding
  - commission_rate
  - proposal_lifecycle

# Impact Classification
severity: medium
impact: governance_bypass
exploitability: 0.6
financial_impact: medium

# Context Tags
tags:
  - governance
  - voting
  - quorum
  - delegation
  - dao
  - commission
  - proposal

# Version Info
language: solidity
version: all
---

## References
- [ref-1]: reports/cosmos_cometbft_findings/m-8-adversary-can-abuse-delegating-to-lower-quorum.md
- [ref-2]: reports/cosmos_cometbft_findings/m-06-re-triggering-the-canoffboardterm-flag-to-bypass-the-dao-vote-of-the-lendin.md
- [ref-3]: reports/cosmos_cometbft_findings/validators-can-manipulate-commission-rates.md
- [ref-4]: reports/cosmos_cometbft_findings/validators-manipulating-commission-rates.md

## Vulnerability Title

**Governance Voting and Parameter Manipulation Vulnerabilities**

### Overview

Governance systems in DAOs and staking protocols are vulnerable to manipulation when quorum calculations, voting power snapshots, poll state management, and parameter changes are not properly secured. Attackers can artificially lower quorum thresholds, bypass DAO votes for critical actions, or manipulate commission rates to steal from delegators. These vulnerabilities affect voting-based decision making across DeFi lending, staking, and governance protocols.

### Vulnerability Description

#### Root Cause

The fundamental issues are:
1. **Quorum calculated at proposal creation** - Allows manipulation before snapshot
2. **Poll state not invalidated after action** - Stale polls can re-trigger flags
3. **No lockup period for parameter changes** - Instant changes trap delegators
4. **Delegation affects total voting power** - Temporary delegation lowers quorum

#### Attack Scenario

**Scenario 1: Quorum Lowering via Delegation (MEDIUM)**

1. Protocol has 1000 total votes, 20% quorum requirement (200 votes needed)
2. 5 colluding users each have 35 votes (10 base + 25 community)
3. Users delegate to each other, reducing their community voting power
4. Total votes drop to 875 (125 community votes removed from quorum calculation)
5. Users create proposal - quorum now only 175 votes (875 * 20%)
6. Users self-delegate to recover all 175 votes
7. Proposal passes with votes that couldn't meet original quorum

**Scenario 2: DAO Vote Bypass via Poll Re-triggering (MEDIUM)**

1. Lending term offboarded via proper voting mechanism
2. `cleanup()` resets `canOffboard[term]` flag
3. But original poll still has ~7 days validity
4. Term re-onboarded through proper governance
5. Attacker calls `supportOffboard()` on old poll to re-trigger flag
6. Attacker immediately calls `offboard()` bypassing new vote
7. Borrowers' loans force-called, stakers slashed

**Scenario 3: Commission Rate Manipulation (MEDIUM)**

1. Validator sets low commission rate (1%) to attract delegators
2. Stakes are locked for 30 days lockup period
3. Validator increases commission to maximum (50%+) immediately
4. Delegators cannot exit - locked funds lose rewards to high commission
5. Validator profits from trapped delegators

#### Vulnerable Pattern Examples

**Example 1: Quorum Snapshot at Creation Time** [Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: Quorum locked at proposal creation, can be manipulated
function propose(
    address[] memory _targets,
    uint256[] memory _values,
    string[] memory _signatures,
    bytes[] memory _calldatas
) external returns (uint256) {
    // ... validation ...
    
    Proposal storage newProposal = proposals[newProposalId];
    newProposal.id = newProposalId;
    newProposal.proposer = msg.sender;
    
    // VULNERABILITY: Quorum calculated NOW, not at vote time
    // Attacker can temporarily lower total votes before this call
    newProposal.quorumVotes = quorumVotes();  // Uses current totalVotes
    
    newProposal.startTime = block.timestamp + votingDelay;
    newProposal.endTime = block.timestamp + votingDelay + votingPeriod;
    
    return newProposalId;
}

function quorumVotes() public view returns (uint256) {
    // Based on current total - can be manipulated
    return totalCommunityVotingPower * quorumVotesBPS / 10000;
}
```

**Example 2: Delegation Affects Voting Power** [Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: Delegating away reduces total voting power
function delegate(address _delegator, address _delegatee) internal {
    address currentDelegate = delegates[_delegator];
    
    // If delegating back to self, regain community voting power
    if (_delegator == _delegatee) {
        _updateTotalCommunityVotingPower(_delegator, true);  // Add back
    }
    // If delegating away, forfeit community voting power
    else if (currentDelegate == _delegator) {
        _updateTotalCommunityVotingPower(_delegator, false);  // Remove
    }
    
    delegates[_delegator] = _delegatee;
    // Attacker: Delegate away -> create proposal -> self-delegate -> vote
}
```

**Example 3: Stale Poll Re-triggering** [Severity: MEDIUM]
```solidity
// ❌ VULNERABLE: Old poll can re-trigger action flag after cleanup
function supportOffboard(uint256 snapshotBlock, address term) external {
    // Poll only checks age, not if term was cleaned up
    require(
        block.number <= snapshotBlock + POLL_DURATION_BLOCKS,  // ~7 days
        "LendingTermOffboarding: poll expired"
    );
    
    uint256 _weight = polls[snapshotBlock][term];
    require(_weight != 0, "poll not found");
    
    // ... voting logic ...
    
    polls[snapshotBlock][term] = _weight + userWeight;
    
    // VULNERABILITY: Can re-set flag even after cleanup() reset it
    if (_weight + userWeight >= quorum) {
        canOffboard[term] = true;  // Re-triggered!
    }
}

function cleanup(address term) external {
    // ... cleanup logic ...
    canOffboard[term] = false;  // Reset, but poll can re-trigger
}
```

**Example 4: No Lockup for Commission Changes** [Severity: MEDIUM]
```rust
// ❌ VULNERABLE: Commission can be changed instantly
pub fn change_commission(
    pool_owner: &signer,
    new_default_commission: u64,
    new_protocol_commission: u64,
) acquires ManagedStakePool {
    // Only validates max commission limit
    assert!(
        new_default_commission <= managed_stake_pool.max_commission,
        ECOMMISSION_EXCEEDS_MAX
    );
    assert!(
        new_protocol_commission <= new_default_commission,
        EPROTOCOL_COMMISSION_EXCEEDS_DEFAULT
    );
    
    // No timelock! Change is instant
    // Delegators are locked for 30 days but commission changes immediately
    delegation_state::change_commission_internal(
        managed_pool_address,
        new_default_commission,
        new_protocol_commission,
    );
}
```

### Impact Analysis

#### Technical Impact
- **Quorum Bypass**: Proposals pass with artificially lowered thresholds
- **State Inconsistency**: Actions executed based on stale poll state
- **Parameter Manipulation**: Critical parameters changed without notice

#### Business Impact
- **Governance Integrity**: Minority can pass proposals meant to fail
- **User Trust**: Unexpected offboarding or parameter changes
- **Financial Loss**: Delegators trapped with high commission validators
- **Protocol Disruption**: Lending terms force-closed, loans called

#### Affected Scenarios
- DAO governance with delegation-based voting power
- Lending protocol offboarding/onboarding mechanisms
- Staking protocols with validator commission
- Any system where quorum is calculated at snapshot time

### Secure Implementation

**Fix 1: Use Checkpoints for Voting Power**
```solidity
// ✅ SECURE: Use checkpointing to prevent manipulation
function propose(...) external returns (uint256) {
    Proposal storage newProposal = proposals[newProposalId];
    
    // Snapshot at voting start, not proposal creation
    newProposal.startBlock = block.number + votingDelay;
    
    // Quorum calculated at vote time using checkpointed values
    // Cannot be manipulated after proposal creation
    return newProposalId;
}

function castVote(uint256 proposalId, bool support) external {
    Proposal storage proposal = proposals[proposalId];
    
    // Use checkpointed voting power at proposal start block
    uint256 votes = getPriorVotes(msg.sender, proposal.startBlock);
    uint256 quorum = getQuorumAtBlock(proposal.startBlock);
    
    // Vote weight locked at snapshot
    proposal.forVotes += support ? votes : 0;
}
```

**Fix 2: Invalidate Stale Polls**
```solidity
// ✅ SECURE: Invalidate poll after cleanup
mapping(uint256 => mapping(address => bool)) public pollInvalidated;

function cleanup(address term) external {
    // ... cleanup logic ...
    
    canOffboard[term] = false;
    
    // Invalidate all polls for this term
    // Or track cleanup block and reject votes from older polls
    lastCleanupBlock[term] = block.number;
    
    emit Cleanup(block.timestamp, term);
}

function supportOffboard(uint256 snapshotBlock, address term) external {
    require(
        block.number <= snapshotBlock + POLL_DURATION_BLOCKS,
        "poll expired"
    );
    
    // SECURE: Reject votes if term was cleaned up after poll creation
    require(
        lastCleanupBlock[term] < snapshotBlock,
        "term cleaned up - poll invalid"
    );
    
    // ... rest of voting logic ...
}
```

**Fix 3: Add Commission Change Lockup**
```rust
// ✅ SECURE: Add timelock for commission changes
pub fn propose_commission_change(
    pool_owner: &signer,
    new_commission: u64,
) acquires ManagedStakePool {
    // Validate new commission
    assert!(new_commission <= max_commission, ECOMMISSION_EXCEEDS_MAX);
    
    // Queue change with timelock matching stake lockup
    pending_commission[pool_address] = PendingCommission {
        new_rate: new_commission,
        effective_at: timestamp::now_seconds() + STAKE_LOCKUP_PERIOD,
    };
    
    emit_event(CommissionChangeQueued { 
        pool: pool_address,
        new_rate: new_commission,
        effective_at: pending.effective_at 
    });
}

pub fn apply_commission_change(pool_address: address) {
    let pending = pending_commission[pool_address];
    require!(
        timestamp::now_seconds() >= pending.effective_at,
        ETIMESTAMP_NOT_REACHED
    );
    
    delegation_state::change_commission_internal(pool_address, pending.new_rate);
}
```

**Fix 4: Add Voting Cooldown After Delegation**
```solidity
// ✅ SECURE: Prevent vote immediately after delegation change
mapping(address => uint256) public lastDelegationChange;

function delegate(address delegatee) external {
    lastDelegationChange[msg.sender] = block.number;
    _delegate(msg.sender, delegatee);
}

function castVote(uint256 proposalId, bool support) external {
    Proposal storage proposal = proposals[proposalId];
    
    // Must have been delegated before proposal creation
    require(
        lastDelegationChange[msg.sender] < proposal.startBlock,
        "delegation too recent"
    );
    
    // ... voting logic ...
}
```

### Detection Patterns

#### Code Patterns to Look For
```
- quorumVotes() called at propose() rather than at vote counting
- totalVotingPower affected by delegation changes
- Poll/vote state not invalidated after related action completed
- Commission/parameter changes without timelock
- No checkpoint system for voting power snapshots
```

#### Audit Checklist
- [ ] When is quorum calculated - at creation or vote time?
- [ ] Does delegation affect total voting power immediately?
- [ ] Are polls invalidated when their target is modified?
- [ ] Is there timelock for validator parameter changes?
- [ ] Can voters delegate-vote-undelegate in same block?
- [ ] Are there cooldown periods preventing vote manipulation?

### Real-World Examples

#### Known Audit Findings
- **FrankenDAO** (Sherlock 2022) - MEDIUM: Quorum lowering via delegation
- **Ethereum Credit Guild** (Code4rena 2023) - MEDIUM: Poll re-triggering bypasses DAO vote
- **Tortuga** (OtterSec 2022) - MEDIUM: Commission manipulation traps delegators

### Prevention Guidelines

#### Development Best Practices
1. **Use Checkpoints**: Implement ERC20Votes-style checkpointing for voting power
2. **Snapshot at Vote Time**: Calculate quorum based on voting period, not proposal creation
3. **Invalidate Stale State**: Reset poll validity when target state changes
4. **Timelock Parameters**: Commission and critical parameters need change delays
5. **Voting Cooldowns**: Prevent vote immediately after delegation changes
6. **Event Emissions**: Log all governance actions for monitoring

#### Testing Requirements
- Test quorum calculation with delegation changes
- Test poll state after cleanup/reset operations
- Test commission changes with locked delegators
- Simulate collusion attacks for quorum manipulation

### Keywords for Search

`quorum_manipulation`, `voting_power`, `delegation_attack`, `poll_retrigger`, `offboard_bypass`, `dao_vote`, `commission_manipulation`, `validator_commission`, `governance_bypass`, `snapshot_voting`, `checkpoint`, `voting_delay`, `proposal_lifecycle`, `stale_poll`, `quorum_lowering`, `community_votes`, `total_voting_power`

### Related Vulnerabilities

- [Epoch Snapshot Timing Manipulation](../staking-delegation/epoch-snapshot-timing-manipulation.md)
- [Malicious Hook/Callback DoS](../hooks-callbacks/malicious-hook-callback-dos.md)
