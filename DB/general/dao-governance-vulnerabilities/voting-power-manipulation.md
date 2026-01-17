---
# Core Classification (Required)
protocol: generic
chain: everychain
category: governance
vulnerability_type: voting_power_manipulation

# Attack Vector Details (Required)
attack_type: economic_exploit|logical_error
affected_component: voting_system|delegation_logic|checkpoint_system

# Technical Primitives (Required)
primitives:
  - voting_power
  - delegation
  - checkpoints
  - flash_loans
  - vote_escrow
  - governance_token
  - snapshot
  - quorum
  - proposal

# Impact Classification (Required)
severity: high
impact: governance_hijacking|fund_loss|manipulation
exploitability: 0.80
financial_impact: high

# Context Tags
tags:
  - defi
  - dao
  - governance
  - voting
  - delegation
  - time_dependent

# Version Info
language: solidity
version: all
---

## References & Source Reports

> **For Agents**: If you need more detailed information about any vulnerability pattern, read the full report from the referenced file path.

### Double Voting / Vote Multiplication
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Tracer - Double Voting by Delegaters | `reports/dao_governance_findings/double-voting-by-delegaters.md` | HIGH | SigmaPrime |
| Golom - Old Delegatee Not Deleted | `reports/dao_governance_findings/h-04-old-delegatee-not-deleted-when-delegating-to-new-tokenid.md` | HIGH | Code4rena |
| Golom - Delegation Updates Both Checkpoints | `reports/dao_governance_findings/h-10-upon-changing-of-delegate-votedelegation-updates-both-the-previous-and-the-.md` | HIGH | Code4rena |

### Flash Loan Voting Attacks
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Vader Protocol - Flash Loans in DAO | `reports/dao_governance_findings/h-05-flash-loans-can-affect-governance-voting-in-daosol.md` | HIGH | Code4rena |

### Unlimited Vote Minting
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Tokensoft - Votes Increased Indefinitely | `reports/dao_governance_findings/h-1-votes-balance-can-be-increased-indefinitely-in-multiple-contracts.md` | HIGH | Sherlock |

### Missing Voting Power Snapshots
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| RAAC - Voting Power Snapshot Missing | `reports/dao_governance_findings/voting-power-snapshot-missing.md` | HIGH | Codehawks |

---

# Voting Power Manipulation Vulnerabilities - Comprehensive Database

**A Complete Pattern-Matching Guide for DAO Governance Security Audits**

---

## Table of Contents

1. [Double Voting via Delegation Abuse](#1-double-voting-via-delegation-abuse)
2. [Flash Loan Voting Attacks](#2-flash-loan-voting-attacks)
3. [Unlimited Vote Minting](#3-unlimited-vote-minting)
4. [Missing Voting Power Snapshots](#4-missing-voting-power-snapshots)
5. [Delegation Logic Errors](#5-delegation-logic-errors)

---

## 1. Double Voting via Delegation Abuse

### Overview

Delegation systems allow users to transfer their voting power to another address. When delegation state is not properly tracked or cleaned up during transfers, users can vote multiple times with the same tokens by exploiting the delegation lifecycle.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/double-voting-by-delegaters.md` (Tracer - SigmaPrime)
> - `reports/dao_governance_findings/h-04-old-delegatee-not-deleted-when-delegating-to-new-tokenid.md` (Golom - Code4rena)

### Vulnerability Description

#### Root Cause

When a user delegates their voting power and later withdraws/transfers their stake, there are no restrictions preventing the delegated stake from being used again. Additionally, when re-delegating to a new address, the old delegation is not properly removed.

#### Attack Scenario

1. Alice delegates her voting power (100 tokens) to Bob
2. Bob votes on a proposal with 100 + his own votes
3. Alice withdraws her stake during the voting period
4. Alice transfers tokens to a new account or re-stakes
5. Alice (or new account) votes on the same proposal
6. The 100 tokens have now been counted twice

### Vulnerable Pattern Examples

**Example 1: No Withdrawal Lock During Active Votes** [HIGH]
> 📖 Reference: `reports/dao_governance_findings/double-voting-by-delegaters.md`
```solidity
// ❌ VULNERABLE: No restriction on withdrawing delegated stake after vote
contract VotingContract {
    mapping(address => address) public delegates;
    mapping(address => uint256) public stakedBalance;
    
    function delegate(address delegatee) external {
        delegates[msg.sender] = delegatee;
        // Delegatee now has voting power of msg.sender
    }
    
    function withdraw(uint256 amount) external {
        // ❌ No check if user's stake was used in active votes
        // ❌ No cooldown period after delegation
        stakedBalance[msg.sender] -= amount;
        token.transfer(msg.sender, amount);
    }
    
    function vote(uint256 proposalId, bool support) external {
        uint256 votingPower = getVotingPower(msg.sender);
        // Voting power includes delegated tokens that can be withdrawn
        _castVote(proposalId, support, votingPower);
    }
}
```

**Example 2: Old Delegatee Not Removed on Re-Delegation** [HIGH]
> 📖 Reference: `reports/dao_governance_findings/h-04-old-delegatee-not-deleted-when-delegating-to-new-tokenid.md`
```solidity
// ❌ VULNERABLE: Delegating to new tokenId doesn't remove from old
contract VoteEscrowDelegation {
    mapping(uint256 => uint256[]) public delegatedTokenIds;
    mapping(uint256 => uint256) public delegatee;
    
    function delegate(uint256 tokenId, uint256 toTokenId) external {
        require(ownerOf(tokenId) == msg.sender);
        
        // ❌ Missing: Remove tokenId from old delegatee's list
        // delegatee[tokenId] still points to old, and new gets added
        
        delegatee[tokenId] = toTokenId;
        delegatedTokenIds[toTokenId].push(tokenId);
        // Now tokenId voting power is counted for BOTH old and new delegatees!
    }
    
    function getVotes(uint256 tokenId) public view returns (uint256) {
        uint256 votes = balanceOf(tokenId);
        for (uint256 i = 0; i < delegatedTokenIds[tokenId].length; i++) {
            votes += balanceOf(delegatedTokenIds[tokenId][i]);
        }
        return votes;
    }
}
```

**Example 3: Storage vs Memory Bug in Checkpoint Updates** [HIGH]
> 📖 Reference: `reports/dao_governance_findings/h-10-upon-changing-of-delegate-votedelegation-updates-both-the-previous-and-the-.md`
```solidity
// ❌ VULNERABLE: Using storage modifies previous checkpoint
function delegate(uint256 tokenId, uint256 toTokenId) internal {
    uint256 nCheckpoints = numCheckpoints[toTokenId];
    
    if (nCheckpoints > 0) {
        // ❌ VULNERABLE: This is a storage reference - modifies previous checkpoint!
        Checkpoint storage checkpoint = checkpoints[toTokenId][nCheckpoints - 1];
        checkpoint.delegatedTokenIds.push(tokenId);
        _writeCheckpoint(toTokenId, nCheckpoints, checkpoint.delegatedTokenIds);
        // Both old AND new checkpoint now contain tokenId
    }
}
```

### Impact Analysis

#### Technical Impact
- Voting power can be multiplied arbitrarily
- Historical vote records become corrupted
- Checkpoints contain duplicate entries

#### Business Impact
- Governance decisions manipulated by minority holders
- Proposals pass/fail against true voter intent
- Complete breakdown of democratic governance

#### Affected Scenarios
- DAOs with transferable governance tokens
- Vote escrow systems with delegation
- Any governance with withdrawal during voting

### Secure Implementation

**Fix 1: Lock Delegated Stake During Active Proposals**
```solidity
// ✅ SECURE: Stake locked while used in active votes
function withdraw(uint256 amount) external {
    require(!hasActiveVotes(msg.sender), "Cannot withdraw: active votes");
    require(
        block.timestamp > lastVoteTime[msg.sender] + votingLockPeriod,
        "Cooldown period not elapsed"
    );
    stakedBalance[msg.sender] -= amount;
    token.transfer(msg.sender, amount);
}
```

**Fix 2: Properly Remove Old Delegation**
```solidity
// ✅ SECURE: Remove from old delegatee before adding to new
function delegate(uint256 tokenId, uint256 toTokenId) external {
    require(ownerOf(tokenId) == msg.sender);
    
    uint256 oldDelegatee = delegatee[tokenId];
    if (oldDelegatee != 0) {
        // ✅ Remove from old delegatee's list
        _removeDelegation(oldDelegatee, tokenId);
    }
    
    delegatee[tokenId] = toTokenId;
    delegatedTokenIds[toTokenId].push(tokenId);
    
    _writeCheckpoint(oldDelegatee, ...);
    _writeCheckpoint(toTokenId, ...);
}
```

**Fix 3: Use Memory for Reading, Storage for Writing**
```solidity
// ✅ SECURE: Use memory to read checkpoint, only write new one
function delegate(uint256 tokenId, uint256 toTokenId) internal {
    uint256 nCheckpoints = numCheckpoints[toTokenId];
    
    if (nCheckpoints > 0) {
        // ✅ SECURE: Use memory - doesn't modify storage
        Checkpoint memory oldCheckpoint = checkpoints[toTokenId][nCheckpoints - 1];
        uint256[] memory newDelegated = new uint256[](oldCheckpoint.delegatedTokenIds.length + 1);
        // Copy and add new
        for (uint i = 0; i < oldCheckpoint.delegatedTokenIds.length; i++) {
            newDelegated[i] = oldCheckpoint.delegatedTokenIds[i];
        }
        newDelegated[newDelegated.length - 1] = tokenId;
        _writeCheckpoint(toTokenId, nCheckpoints, newDelegated);
    }
}
```

---

## 2. Flash Loan Voting Attacks

### Overview

Flash loans enable attackers to borrow massive amounts of governance tokens within a single transaction, artificially inflate their voting power, cast decisive votes, and return the tokens - all atomically.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/h-05-flash-loans-can-affect-governance-voting-in-daosol.md` (Vader Protocol - Code4rena)

### Vulnerability Description

#### Root Cause

Voting power is calculated based on current token balance at vote time, rather than a historical snapshot taken before the proposal was created. This allows instantaneous balance changes to affect voting outcomes.

#### Attack Scenario

1. Attacker takes a flash loan of governance tokens
2. In the same transaction, attacker votes on a critical proposal
3. Voting power is calculated based on current (borrowed) balance
4. Attacker returns flash loan
5. Proposal outcome is manipulated without real token ownership

### Vulnerable Pattern Examples

**Example 1: Voting with Current Balance** [HIGH]
> 📖 Reference: `reports/dao_governance_findings/h-05-flash-loans-can-affect-governance-voting-in-daosol.md`
```solidity
// ❌ VULNERABLE: Uses current balance, not snapshot
contract DAO {
    function countMemberVotes(address member) public view returns (uint256) {
        // ❌ Current balance can be manipulated via flash loan
        return governanceToken.balanceOf(member);
    }
    
    function vote(uint256 proposalId, bool support) external {
        uint256 weight = countMemberVotes(msg.sender);
        // Attacker can flash loan tokens, vote, return tokens
        proposals[proposalId].votes += weight;
    }
}
```

**Example 2: No Block Delay for Voting** [HIGH]
```solidity
// ❌ VULNERABLE: Voting allowed immediately after receiving tokens
function castVote(uint256 proposalId, bool support) external {
    ProposalCore storage proposal = _proposals[proposalId];
    
    // ❌ No check that voter had tokens BEFORE proposal creation
    uint256 weight = _veToken.getVotingPower(msg.sender);
    
    if (support) {
        proposal.forVotes += weight;
    } else {
        proposal.againstVotes += weight;
    }
}
```

### Secure Implementation

**Fix 1: Use Historical Snapshots at Proposal Creation**
```solidity
// ✅ SECURE: Voting power based on snapshot at proposal creation
function vote(uint256 proposalId, bool support) external {
    Proposal storage proposal = proposals[proposalId];
    
    // ✅ Use voting power from BEFORE proposal was created
    uint256 weight = governanceToken.getPastVotes(
        msg.sender, 
        proposal.snapshotBlock
    );
    
    require(weight > 0, "No voting power at snapshot");
    proposal.votes[support] += weight;
}

function propose(...) external returns (uint256) {
    uint256 proposalId = proposalCount++;
    // ✅ Lock snapshot at proposal creation time
    proposals[proposalId].snapshotBlock = block.number - 1;
    return proposalId;
}
```

**Fix 2: Voting Delay After Token Acquisition**
```solidity
// ✅ SECURE: Require tokens held for minimum period
function getVotingPower(address account) public view returns (uint256) {
    // Only count tokens held for at least votingDelay blocks
    return token.getPastVotes(account, block.number - votingDelay);
}
```

---

## 3. Unlimited Vote Minting

### Overview

Some governance systems mint voting tokens to represent vesting or distribution rights. If the initialization or minting function can be called multiple times, attackers can mint unlimited voting tokens.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/h-1-votes-balance-can-be-increased-indefinitely-in-multiple-contracts.md` (Tokensoft - Sherlock)

### Vulnerability Description

#### Root Cause

Public initialization functions that mint voting tokens lack proper access control or single-use enforcement, allowing repeated calls to inflate voting power.

#### Attack Scenario

1. Attacker calls `initializeDistributionRecord()` with valid merkle proof
2. Function mints voting tokens equal to their total claimable amount
3. Attacker calls the function again (and again)
4. Each call mints additional voting tokens
5. Attacker now has unlimited voting power

### Vulnerable Pattern Examples

**Example 1: Reusable Initialization Function** [HIGH]
> 📖 Reference: `reports/dao_governance_findings/h-1-votes-balance-can-be-increased-indefinitely-in-multiple-contracts.md`
```solidity
// ❌ VULNERABLE: Can be called multiple times to mint infinite votes
contract AdvancedDistributor is ERC20Votes {
    function initializeDistributionRecord(
        uint32 _domain,
        address _beneficiary,
        uint256 _amount,
        bytes32[] calldata merkleProof
    ) external validMerkleProof(_getLeaf(_beneficiary, _amount, _domain), merkleProof) {
        // ❌ No check if already initialized for this beneficiary
        _initializeDistributionRecord(_beneficiary, _amount);
    }
    
    function _initializeDistributionRecord(
        address beneficiary,
        uint256 totalAmount
    ) internal virtual override {
        super._initializeDistributionRecord(beneficiary, totalAmount);
        // ❌ Mints voting tokens every time - can be called repeatedly!
        _mint(beneficiary, tokensToVotes(totalAmount));
    }
}
```

### Secure Implementation

**Fix 1: Track Initialization Status**
```solidity
// ✅ SECURE: Only allow initialization once per beneficiary
mapping(address => bool) private initialized;

function initializeDistributionRecord(
    uint32 _domain,
    address _beneficiary,
    uint256 _amount,
    bytes32[] calldata merkleProof
) external validMerkleProof(...) {
    require(!initialized[_beneficiary], "Already initialized");
    initialized[_beneficiary] = true;
    _initializeDistributionRecord(_beneficiary, _amount);
}
```

**Fix 2: Mint Based on Delta, Not Total**
```solidity
// ✅ SECURE: Only mint votes for unclaimed portion
function _initializeDistributionRecord(
    address beneficiary,
    uint256 totalAmount
) internal virtual override {
    uint256 existingVotes = balanceOf(beneficiary);
    uint256 targetVotes = tokensToVotes(totalAmount);
    
    if (targetVotes > existingVotes) {
        _mint(beneficiary, targetVotes - existingVotes);
    }
}
```

---

## 4. Missing Voting Power Snapshots

### Overview

When voting power is calculated at vote time rather than at proposal creation, it creates opportunities for manipulation by acquiring or transferring tokens during the voting period.

> **📚 Source Reports for Deep Dive:**
> - `reports/dao_governance_findings/voting-power-snapshot-missing.md` (RAAC - Codehawks)

### Vulnerability Description

#### Root Cause

The governance contract uses current voting power (`getVotingPower(msg.sender)`) instead of historical voting power at a specific snapshot block.

#### Attack Scenario

1. User sees a proposal they want to pass/fail
2. User increases their locked tokens (or acquires more)
3. User votes with inflated voting power
4. After voting, user withdraws or sells tokens
5. Voting outcome influenced without genuine long-term stake

### Vulnerable Pattern Examples

**Example 1: Current Voting Power Used** [HIGH]
> 📖 Reference: `reports/dao_governance_findings/voting-power-snapshot-missing.md`
```solidity
// ❌ VULNERABLE: Uses current voting power, not snapshot
function castVote(uint256 proposalId, bool support) external override returns (uint256) {
    ProposalCore storage proposal = _proposals[proposalId];
    
    // ❌ Current voting power - can be manipulated during voting period
    uint256 weight = _veToken.getVotingPower(msg.sender);
    
    if (weight == 0) {
        revert NoVotingPower(msg.sender, block.number);
    }
    
    proposalVote.hasVoted[msg.sender] = true;
    
    if (support) {
        proposalVote.forVotes += weight;
    } else {
        proposalVote.againstVotes += weight;
    }
    
    return weight;
}
```

### Secure Implementation

**Fix 1: Store Snapshot at Proposal Creation**
```solidity
// ✅ SECURE: Use snapshot from proposal creation
function propose(...) external returns (uint256) {
    uint256 proposalId = ++proposalCount;
    
    _proposals[proposalId].snapshotBlock = block.number;
    _proposals[proposalId].startTime = block.timestamp + votingDelay;
    _proposals[proposalId].endTime = block.timestamp + votingDelay + votingPeriod;
    
    return proposalId;
}

function castVote(uint256 proposalId, bool support) external returns (uint256) {
    ProposalCore storage proposal = _proposals[proposalId];
    
    // ✅ Use voting power at snapshot block
    uint256 weight = _veToken.getPastVotingPower(
        msg.sender, 
        proposal.snapshotBlock
    );
    
    // Rest of voting logic...
}
```

---

## 5. Delegation Logic Errors

### Overview

Complex delegation systems with nested delegations, re-delegation, or self-delegation can contain logic errors that corrupt vote accounting.

### Vulnerable Pattern Examples

**Example 1: Self-Delegation Community Power Exploit** [MEDIUM]
```solidity
// ❌ VULNERABLE: Self-delegation toggles community power
function _delegate(address _delegator, address _delegatee) internal {
    address currentDelegate = delegates[_delegator];
    
    // ❌ Toggling between self and others manipulates total power
    if (_delegator == _delegatee) {
        _updateTotalCommunityVotingPower(_delegator, true);  // Add power
    } else if (currentDelegate == _delegator) {
        _updateTotalCommunityVotingPower(_delegator, false); // Remove power
    }
    
    delegates[_delegator] = _delegatee;
}
```

---

## Detection Patterns

### Code Patterns to Look For
```
- getPriceUnsafe() equivalent for voting: getVotingPower() without snapshot
- Public initialize/mint functions for voting tokens
- Delegation without cleanup of previous delegatee
- storage variable used when reading checkpoints for modification
- No withdrawal lock during active voting periods
- Voting based on current balance rather than historical snapshot
```

### Audit Checklist
- [ ] Is voting power snapshotted at proposal creation?
- [ ] Can voting tokens be flash loaned?
- [ ] Is delegation cleanup complete on re-delegation?
- [ ] Are initialization functions protected against repeated calls?
- [ ] Is there a withdrawal lock during active votes?
- [ ] Are checkpoint operations using correct storage/memory semantics?
- [ ] Can community/total voting power be manipulated via self-delegation?

---

## Prevention Guidelines

### Development Best Practices
1. Always use historical snapshots (ERC20Votes pattern) for voting power
2. Implement withdrawal locks during voting periods
3. Use OpenZeppelin's Governor and Votes extensions as reference
4. Ensure delegation cleanup removes from previous delegatee
5. Make initialization functions single-use per address

### Testing Requirements
- Unit tests for: double voting scenarios, flash loan attacks, re-delegation
- Integration tests for: full proposal lifecycle with delegation changes
- Fuzzing targets: delegation operations, vote casting with balance changes

---

## Keywords for Search

`voting_power`, `delegation`, `double_voting`, `flash_loan_attack`, `governance`, `dao`, `checkpoint`, `snapshot`, `vote_escrow`, `quorum`, `proposal`, `delegate`, `re-delegation`, `vote_multiplication`, `unlimited_minting`, `voting_token`, `governance_token`, `ERC20Votes`, `getPastVotes`, `voting_delay`, `voting_period`

---

## Related Vulnerabilities

- [Quorum Manipulation](./quorum-manipulation.md)
- [Checkpoint Vulnerabilities](./checkpoint-vulnerabilities.md)
- [Timelock Bypass](./timelock-bypass.md)
- [Proposal Lifecycle Manipulation](./proposal-lifecycle-manipulation.md)
