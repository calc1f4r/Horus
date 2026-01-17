---
# Core Classification (Required)
protocol: generic
chain: everychain
category: governance
vulnerability_type: quorum_manipulation

# Attack Vector Details (Required)
attack_type: logical_error|state_manipulation
affected_component: quorum_calculation|dynamic_quorum|voting_threshold

# Technical Primitives (Required)
primitives:
  - quorum
  - voting_power
  - threshold
  - delegation
  - proposal_passing
  - dynamic_quorum
  - supply_based_quorum

# Impact Classification (Required)
severity: medium_to_high
impact: governance_bypass|proposal_manipulation
exploitability: 0.65
financial_impact: high

# Context Tags
tags:
  - defi
  - dao
  - governance
  - quorum
  - voting_threshold
  - delegation

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Quorum Lowering via Delegation Abuse
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Nouns DAO - Abuse Delegating to Lower Quorum | `reports/dao_governance_findings/m-8-adversary-can-abuse-delegating-to-lower-quorum.md` | MEDIUM | Code4rena |
| Reserve Protocol - Coordinated Quorum Attack | `reports/dao_governance_findings/cordinated-group-of-attacker-can-artificially-lower-quorum-threshold-during-acti.md` | MEDIUM | Code4rena |

### Quorum/Threshold Miscalculations
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Venus - Winning with 4% Voting Power | `reports/dao_governance_findings/h-01-adversary-can-win-proposals-with-voting-power-as-low-as-4.md` | HIGH | Code4rena |
| Usual Money - Quorum Has No Effect | `reports/dao_governance_findings/m-01-quorum-votes-have-no-effect-for-determining-whether-proposal-is-defeated-or.md` | MEDIUM | Code4rena |

### Vote Counting Errors
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Farcaster - Ties Approved Instead of Rejected | `reports/dao_governance_findings/m09-ties-in-governance-proposals-are-approved.md` | MEDIUM | Code4rena |
| Usual Money - Majority Not Required | `reports/dao_governance_findings/m-28-state-function-does-not-require-majority-of-votes-for-supporting-and-passin.md` | MEDIUM | Code4rena |

---

# Quorum Manipulation Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for Governance Quorum Security Audits**

---

## Table of Contents

1. [Quorum Lowering via Delegation Abuse](#1-quorum-lowering-via-delegation-abuse)
2. [Dynamic Quorum Manipulation](#2-dynamic-quorum-manipulation)
3. [Quorum Threshold Miscalculation](#3-quorum-threshold-miscalculation)
4. [Quorum Not Enforced in State Transitions](#4-quorum-not-enforced-in-state-transitions)
5. [Tie Handling Vulnerabilities](#5-tie-handling-vulnerabilities)

---

## 1. Quorum Lowering via Delegation Abuse

### Overview

Dynamic quorum systems calculate quorum as a percentage of current total voting power. When users can delegate to external accounts or abstain during active proposals, they can artificially reduce total voting supply, making quorum easier to reach.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/m-8-adversary-can-abuse-delegating-to-lower-quorum.md` (Nouns DAO - Code4rena)
> - `reports/dao_governance_findings/cordinated-group-of-attacker-can-artificially-lower-quorum-threshold-during-acti.md` (Reserve Protocol - Code4rena)

### Vulnerability Description

#### Root Cause

Quorum is calculated based on total adjusted supply at a snapshot block. If delegation changes can affect what counts as "adjusted" supply after the snapshot, attackers can lower the quorum requirement during active proposals.

#### Attack Scenario

1. Proposal starts with 100 ETH total adjusted supply
2. Quorum = 20% of adjusted supply = 20 ETH required
3. Coordinated group holds 15 ETH of voting power
4. Group delegates 50 ETH to addresses that "don't count" as adjusted supply
5. Adjusted supply drops to 50 ETH
6. Quorum = 20% of 50 ETH = 10 ETH required
7. Attacker's 15 ETH now exceeds quorum - proposal passes

### Vulnerable Pattern Examples

**Example 1: Dynamic Quorum Based on Adjusted Supply** [MEDIUM]
> 📖 Reference: `reports/dao_governance_findings/m-8-adversary-can-abuse-delegating-to-lower-quorum.md`
```solidity
// ❌ VULNERABLE: Adjusted supply can change after proposal creation
function quorumVotes(uint256 proposalId) public view returns (uint256) {
    Proposal storage proposal = _proposals[proposalId];
    // ❌ Uses adjustedTotalSupply which can be manipulated
    return bps2Uint(proposal.quorumVotesBPS, adjustedTotalSupply(proposalId));
}

function adjustedTotalSupply(uint256 proposalId) public view returns (uint256) {
    Proposal storage proposal = _proposals[proposalId];
    // ❌ Excludes delegated tokens - attackers can delegate to lower this
    return nouns.totalSupply() - nouns.balanceOf(address(this)) 
                               - delegatedTokenCount(proposal.creationBlock);
}
```

**Example 2: Coordinated Delegation Attack** [MEDIUM]
> 📖 Reference: `reports/dao_governance_findings/cordinated-group-of-attacker-can-artificially-lower-quorum-threshold-during-acti.md`
```solidity
// ❌ VULNERABLE: Quorum reads current delegations, not snapshot
function _quorumReached(uint256 proposalId) internal view returns (bool) {
    (uint256 againstVotes, uint256 forVotes, uint256 abstainVotes) = proposalVotes(proposalId);
    
    // ❌ Uses current total votes, which is affected by delegations
    uint256 totalVotingPower = getTotalVotingPower();  // Can be lowered!
    uint256 quorumRequired = totalVotingPower * quorumBPS / 10000;
    
    return forVotes + abstainVotes >= quorumRequired;
}

// Attack: Before proposal
// - Total voting power: 1,000,000
// - Quorum (10%): 100,000 votes required

// Attack: During proposal
// - Attacker group undelegates 800,000 votes
// - Total voting power: 200,000
// - Quorum (10%): 20,000 votes required  
// - Attacker's 50,000 votes now pass quorum!
```

### Impact Analysis

#### Technical Impact
- Quorum requirement can be artificially lowered
- Proposals pass with minority support
- Dynamic quorum defeats its own purpose

#### Business Impact
- Minority token holders can pass proposals
- Governance decisions don't reflect community will
- Protocol can be taken over by coordinated minority

#### Affected Scenarios
- Any DAO with dynamic quorum based on current supply
- Protocols with delegation mechanisms
- Governance systems without snapshot-locked quorum

### Secure Implementation

**Fix 1: Lock Quorum at Proposal Creation**
```solidity
// ✅ SECURE: Quorum locked at proposal creation time
struct Proposal {
    // ... other fields
    uint256 snapshotQuorum;  // ✅ Stored at creation, immutable
}

function propose(...) external returns (uint256) {
    uint256 proposalId = proposalCount++;
    Proposal storage proposal = _proposals[proposalId];
    
    // ✅ Lock quorum based on snapshot, not current supply
    proposal.snapshotQuorum = calculateQuorum(block.number);
    // ... rest of proposal creation
}

function quorumVotes(uint256 proposalId) public view returns (uint256) {
    // ✅ Returns stored value, cannot be manipulated
    return _proposals[proposalId].snapshotQuorum;
}
```

**Fix 2: Use Fixed Quorum or Total Supply (Not Adjusted)**
```solidity
// ✅ SECURE: Quorum based on total token supply, not adjusted
function quorumVotes(uint256 proposalId) public view returns (uint256) {
    Proposal storage proposal = _proposals[proposalId];
    
    // ✅ Uses total supply at snapshot - delegation doesn't affect this
    uint256 totalSupplyAtSnapshot = token.getPastTotalSupply(proposal.startBlock);
    return totalSupplyAtSnapshot * quorumNumerator / quorumDenominator;
}
```

---

## 2. Dynamic Quorum Manipulation

### Overview

Dynamic quorum systems adjust quorum based on past proposal participation. If quorum automatically decreases when participation is low, attackers can boycott proposals to lower quorum, then pass malicious proposals with minimal votes.

### Vulnerability Description

#### Root Cause

Automatic quorum adjustment algorithms that lower quorum when participation drops can be gamed by coordinated non-participation.

#### Attack Scenario

1. Normal quorum: 40% of voting power
2. Attacker group controls 15% of tokens
3. Group boycotts multiple proposals, reducing participation
4. Dynamic quorum algorithm lowers quorum to 10%
5. Attacker's 15% is now sufficient to pass any proposal

### Vulnerable Pattern Examples

**Example 1: Participation-Based Dynamic Quorum** [MEDIUM]
```solidity
// ❌ VULNERABLE: Quorum decreases based on low participation
function updateQuorum() internal {
    uint256 lastParticipation = getLastProposalParticipation();
    
    if (lastParticipation < targetParticipation) {
        // ❌ Automatically lowers quorum if participation drops
        currentQuorum = currentQuorum * 95 / 100;  // Decrease by 5%
    } else {
        currentQuorum = currentQuorum * 105 / 100;  // Increase by 5%
    }
    
    // ❌ No minimum floor - quorum can go arbitrarily low
}
```

### Secure Implementation

**Fix 1: Enforce Minimum Quorum Floor**
```solidity
// ✅ SECURE: Quorum has a minimum floor
uint256 public constant MIN_QUORUM = 4 * 1e16;  // 4% minimum

function updateQuorum() internal {
    uint256 lastParticipation = getLastProposalParticipation();
    uint256 newQuorum;
    
    if (lastParticipation < targetParticipation) {
        newQuorum = currentQuorum * 95 / 100;
    } else {
        newQuorum = currentQuorum * 105 / 100;
    }
    
    // ✅ Never go below minimum
    currentQuorum = newQuorum < MIN_QUORUM ? MIN_QUORUM : newQuorum;
}
```

---

## 3. Quorum Threshold Miscalculation

### Overview

Incorrect quorum calculations can result in proposals passing with far less support than intended. Off-by-one errors, wrong denominators, or missing divisions can make quorum trivially easy to reach.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/h-01-adversary-can-win-proposals-with-voting-power-as-low-as-4.md` (Venus - Code4rena)

### Vulnerability Description

#### Root Cause

Mathematical errors in quorum calculation - using wrong base values, missing percentage conversions, or comparing against wrong vote tallies.

#### Attack Scenario

1. Intended quorum: 51% of total votes FOR to pass
2. Bug: Code checks if forVotes > totalVotes * 0.04 (4%)
3. Attacker with only 5% voting power can pass any proposal
4. Governance completely compromised

### Vulnerable Pattern Examples

**Example 1: Wrong Percentage Calculation** [HIGH]
> 📖 Reference: `reports/dao_governance_findings/h-01-adversary-can-win-proposals-with-voting-power-as-low-as-4.md`
```solidity
// ❌ VULNERABLE: Uses FOR_PERCENTAGE (4%) instead of requiring majority
function _isProposalSucceeded(uint256 proposalId) private view returns (bool) {
    uint256 forVotes = _getForVotes(proposalId);
    uint256 againstVotes = _getAgainstVotes(proposalId);
    
    // ❌ BUG: Only requires 4% of votes to be FOR, not majority!
    uint256 threshold = (forVotes + againstVotes) * FOR_PERCENTAGE / DENOMINATOR;
    
    return forVotes > threshold;  // ❌ Passes with only 4% support!
}

// Intended behavior: forVotes > againstVotes (majority)
// Actual behavior: forVotes > 4% of total votes cast
```

**Example 2: Quorum Check Against Wrong Value** [MEDIUM]
```solidity
// ❌ VULNERABLE: Quorum checked against FOR votes only, not total participation
function _quorumReached(uint256 proposalId) internal view returns (bool) {
    uint256 forVotes = proposalVote[proposalId].forVotes;
    
    // ❌ Only counts FOR votes toward quorum
    // Abstain and Against don't contribute!
    return forVotes >= quorum(proposalSnapshot(proposalId));
}

// Correct: forVotes + againstVotes + abstainVotes >= quorum
```

### Impact Analysis

#### Technical Impact
- Proposals pass without required support
- Quorum check is effectively disabled
- Minority can control governance

#### Business Impact
- Critical protocol changes with 4% support
- Treasury drains through minority votes
- Complete governance takeover possible

### Secure Implementation

**Fix 1: Correct Percentage Calculations**
```solidity
// ✅ SECURE: Proper majority calculation
function _isProposalSucceeded(uint256 proposalId) private view returns (bool) {
    uint256 forVotes = _getForVotes(proposalId);
    uint256 againstVotes = _getAgainstVotes(proposalId);
    
    // ✅ Requires majority (more FOR than AGAINST)
    return forVotes > againstVotes;
}

// ✅ SECURE: Proper quorum check
function _quorumReached(uint256 proposalId) internal view returns (bool) {
    uint256 forVotes = proposalVote[proposalId].forVotes;
    uint256 againstVotes = proposalVote[proposalId].againstVotes;
    uint256 abstainVotes = proposalVote[proposalId].abstainVotes;
    
    // ✅ Total participation must meet quorum
    uint256 totalVotes = forVotes + againstVotes + abstainVotes;
    return totalVotes >= quorum(proposalSnapshot(proposalId));
}
```

---

## 4. Quorum Not Enforced in State Transitions

### Overview

Even when quorum is calculated correctly, bugs in proposal state machine logic can bypass quorum checks entirely.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/m-01-quorum-votes-have-no-effect-for-determining-whether-proposal-is-defeated-or.md` (Usual Money - Code4rena)

### Vulnerability Description

#### Root Cause

The `state()` function determines proposal outcome but fails to check quorum in the success path, or quorum check is placed in wrong branch of conditional logic.

#### Attack Scenario

1. Proposal receives 10 FOR votes, 5 AGAINST votes
2. Quorum requirement: 1000 votes
3. Bug: State function only checks forVotes > againstVotes
4. Proposal marked as SUCCEEDED despite not meeting quorum
5. Proposal can be queued and executed

### Vulnerable Pattern Examples

**Example 1: Missing Quorum Check in State Function** [MEDIUM]
> 📖 Reference: `reports/dao_governance_findings/m-01-quorum-votes-have-no-effect-for-determining-whether-proposal-is-defeated-or.md`
```solidity
// ❌ VULNERABLE: Quorum not checked for SUCCEEDED state
function state(uint256 proposalId) public view returns (ProposalState) {
    Proposal memory proposal = proposals[proposalId];
    
    if (block.timestamp < proposal.startTime) {
        return ProposalState.Pending;
    }
    
    if (block.timestamp < proposal.endTime) {
        return ProposalState.Active;
    }
    
    // ❌ BUG: Only checks vote counts, not quorum!
    if (proposal.forVotes <= proposal.againstVotes) {
        return ProposalState.Defeated;
    }
    
    // ❌ Proposal succeeds even without meeting quorum
    return ProposalState.Succeeded;
}
```

### Secure Implementation

**Fix 1: Enforce Quorum in State Function**
```solidity
// ✅ SECURE: Quorum enforced in state transitions
function state(uint256 proposalId) public view returns (ProposalState) {
    Proposal memory proposal = proposals[proposalId];
    
    if (block.timestamp < proposal.startTime) {
        return ProposalState.Pending;
    }
    
    if (block.timestamp < proposal.endTime) {
        return ProposalState.Active;
    }
    
    // ✅ Check quorum FIRST
    uint256 totalVotes = proposal.forVotes + proposal.againstVotes + proposal.abstainVotes;
    if (totalVotes < quorum(proposalId)) {
        return ProposalState.Defeated;  // ✅ Fails if quorum not met
    }
    
    // ✅ Then check majority
    if (proposal.forVotes <= proposal.againstVotes) {
        return ProposalState.Defeated;
    }
    
    return ProposalState.Succeeded;
}
```

---

## 5. Tie Handling Vulnerabilities

### Overview

When FOR and AGAINST votes are equal, the outcome should typically be rejection. However, bugs in comparison operators can cause ties to be approved.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/m09-ties-in-governance-proposals-are-approved.md` (Farcaster - Code4rena)
> - `reports/dao_governance_findings/m-28-state-function-does-not-require-majority-of-votes-for-supporting-and-passin.md` (Usual Money - Code4rena)

### Vulnerability Description

#### Root Cause

Using `>=` instead of `>` when comparing FOR votes to AGAINST votes causes ties to pass. This is often an intentional design choice but frequently inconsistent with governance documentation.

#### Attack Scenario

1. Proposal: Transfer 1M tokens to attacker address
2. Voting: 500,000 FOR, 500,000 AGAINST (tie)
3. Bug: Code uses `forVotes >= againstVotes`
4. Proposal passes despite no majority support
5. Attacker receives tokens

### Vulnerable Pattern Examples

**Example 1: Ties Approved** [MEDIUM]
> 📖 Reference: `reports/dao_governance_findings/m09-ties-in-governance-proposals-are-approved.md`
```solidity
// ❌ VULNERABLE: Ties pass (uses >=)
function _isSucceeded(uint256 proposalId) internal view returns (bool) {
    ProposalData memory proposal = proposals[proposalId];
    
    // ❌ BUG: >= means ties pass
    return proposal.forVotes >= proposal.againstVotes;
}

// If forVotes == againstVotes, this returns true!
```

**Example 2: Incorrect Majority Definition** [MEDIUM]
> 📖 Reference: `reports/dao_governance_findings/m-28-state-function-does-not-require-majority-of-votes-for-supporting-and-passin.md`
```solidity
// ❌ VULNERABLE: Doesn't require strict majority
function state(uint256 proposalId) public view returns (ProposalState) {
    // ... other checks ...
    
    // ❌ Only checks that forVotes is not less than againstVotes
    if (proposal.forVotes < proposal.againstVotes) {
        return ProposalState.Defeated;
    }
    
    return ProposalState.Succeeded;  // ❌ Ties and equal votes pass!
}
```

### Secure Implementation

**Fix 1: Require Strict Majority**
```solidity
// ✅ SECURE: Ties fail (uses >)
function _isSucceeded(uint256 proposalId) internal view returns (bool) {
    ProposalData memory proposal = proposals[proposalId];
    
    // ✅ Strict majority required
    return proposal.forVotes > proposal.againstVotes;
}
```

**Fix 2: Explicit Tie Handling**
```solidity
// ✅ SECURE: Explicit tie handling
function state(uint256 proposalId) public view returns (ProposalState) {
    // ... other checks ...
    
    if (proposal.forVotes > proposal.againstVotes) {
        return ProposalState.Succeeded;
    } else if (proposal.forVotes < proposal.againstVotes) {
        return ProposalState.Defeated;
    } else {
        // ✅ Explicit: Ties are defeated
        return ProposalState.Defeated;
    }
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- adjustedTotalSupply() or similar functions affecting quorum denominator
- Quorum calculated at voting time instead of proposal creation
- Automatic quorum reduction without minimum floor
- Wrong percentage calculations (e.g., 4% instead of 51%)
- Quorum checked against forVotes only (not total participation)
- Missing quorum check in state() function
- >= instead of > for majority comparison
- Dynamic quorum without minimum bounds
```

### Audit Checklist
- [ ] Is quorum locked at proposal creation (snapshot)?
- [ ] Can delegations affect quorum calculation after snapshot?
- [ ] Does dynamic quorum have a minimum floor?
- [ ] Are percentage calculations correct?
- [ ] Is quorum checked against total participation (not just FOR)?
- [ ] Does state() function enforce quorum before SUCCEEDED?
- [ ] Are ties explicitly handled and rejected?
- [ ] Is majority defined as strictly greater than (not >=)?

---

## Prevention Guidelines

### Development Best Practices
1. Lock quorum at proposal snapshot block
2. Use total token supply for quorum base, not "adjusted" supply
3. Enforce minimum quorum floor in dynamic systems
4. Check quorum BEFORE checking majority
5. Use strict inequality (>) for majority, not >=
6. Test with edge cases: ties, minimal participation, delegation changes

### Testing Requirements
- Unit tests for: tie scenarios, quorum edge cases, delegation during voting
- Integration tests for: dynamic quorum manipulation, coordinated attacks
- Fuzzing targets: quorum calculations, state transitions, vote counting

---

## Keywords for Search

`quorum`, `threshold`, `majority`, `dynamic_quorum`, `adjusted_supply`, `delegation`, `voting_power`, `proposal_passing`, `tie_handling`, `quorum_manipulation`, `vote_counting`, `governance_threshold`, `minimum_quorum`, `quorum_reached`, `_isSucceeded`, `state_function`

---

## Related Vulnerabilities

- [Voting Power Manipulation](./voting-power-manipulation.md)
- [Timelock Bypass](./timelock-bypass.md)
- [Proposal Lifecycle Manipulation](./proposal-lifecycle-manipulation.md)
