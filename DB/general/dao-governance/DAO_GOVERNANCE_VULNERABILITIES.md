---
# Core Classification
protocol: generic
chain: everychain
category: governance
vulnerability_type: governance_manipulation

# Pattern Identity
root_cause_family: governance_mechanism_bypass
pattern_key: governance_bypass | voting_proposal_timelock | manipulation_or_dos | unauthorized_execution_or_fund_theft

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - Governor
  - Timelock
  - VotingToken
  - VoteEscrow
  - Delegation
  - Multisig
  - Treasury
  - ProposalExecutor
path_keys:
  - flash_loan_voting | Governor | VotingToken | inflated_voting_power
  - double_voting_delegation | Delegation→Governor | VotingToken | 2x_vote_weight
  - quorum_manipulation | Governor | VoteEscrow→Governor | proposal_passes_without_majority
  - timelock_bypass | Timelock | Governor→Timelock | unauthorized_immediate_execution
  - proposal_cancellation_abuse | Governor | cancel() | block_legitimate_proposals
  - checkpoint_storage_bug | VoteEscrow | _writeCheckpoint | stale_or_lost_delegation
  - arbitrary_proposal_execution | Governor→ProposalExecutor | arbitrary_call | fund_theft
  - snapshot_missing | Governor | VotingToken | vote_weight_manipulation_mid_proposal

# Attack Vector Details
attack_type: governance_exploit
affected_component: governance_system

# Technical Primitives
primitives:
  - propose
  - castVote
  - execute
  - queue
  - cancel
  - delegate
  - timelock
  - quorum
  - checkpoint
  - votingPower
  - snapshot
  - getVotes
  - proposalThreshold

# Grep / Hunt-Card Seeds
code_keywords:
  - propose
  - castVote
  - execute
  - queue
  - cancel
  - delegate
  - quorum
  - quorumVotes
  - proposalThreshold
  - GovernorVotesQuorumFraction
  - _writeCheckpoint
  - getVotes
  - getPastVotes
  - votingPower
  - timelock
  - setDelay
  - setGovernor
  - scheduleBatch
  - fastTrack
  - ArbitraryCallsProposal
  - countMemberVotes
  - initializeDistributionRecord
  - delegatedTokenIds
  - endorseProposal

# Impact Classification
severity: high
impact: governance_takeover
exploitability: 0.75
financial_impact: critical

# Context Tags
tags:
  - defi
  - governance
  - dao
  - voting
  - timelock
  - delegation
  - quorum
  - proposal
  - multisig
  - treasury

# Version Info
language: solidity
version: ">=0.8.0"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID |
|-------|------|----------|---------|-----------|
| [flash-vote] | reports/dao_governance_findings/h-05-flash-loans-can-affect-governance-voting-in-daosol.md | HIGH | Code4rena | 3908 |
| [double-vote-delegate] | reports/dao_governance_findings/double-voting-by-delegaters.md | HIGH | SigmaPrime | 19733 |
| [quorum-fraction-miscfg] | reports/dao_governance_findings/h-01-adversary-can-win-proposals-with-voting-power-as-low-as-4.md | HIGH | Code4rena | 50064 |
| [timelock-bypass] | reports/dao_governance_findings/h-01-timelock-can-be-bypassed.md | HIGH | Code4rena | 1091 |
| [bytes32-0-cancel] | reports/dao_governance_findings/cancelling-bytes320-allows-timelock-takeover.md | CRITICAL | Spearbit | 45408 |
| [cancel-retains-timelock] | reports/dao_governance_findings/timelock-controller-retains-canceled-proposals-enabling-unauthorized-execution-a.md | MEDIUM | Codehawks | 57143 |
| [unrestricted-cancel] | reports/dao_governance_findings/unrestricted-proposal-cancellation-allows-governance-process-manipulation.md | MEDIUM | Codehawks | 57235 |
| [checkpoint-memory-bug] | reports/dao_governance_findings/h-07-_writecheckpoint-does-not-write-to-storage-on-same-block.md | HIGH | Code4rena | 8733 |
| [checkpoint-both-update] | reports/dao_governance_findings/h-10-upon-changing-of-delegate-votedelegation-updates-both-the-previous-and-the-.md | HIGH | Code4rena | 8736 |
| [quadratic-tally-wrong] | reports/dao_governance_findings/m-19-quadratic-voting-tally-done-wrong.md | MEDIUM | Sherlock | 6316 |
| [arbitrary-call-hijack] | reports/dao_governance_findings/h-05-arbitrarycallsproposalsol-and-listonopenseaproposalsol-safeguards-can-be-by.md | HIGH | Code4rena | 3306 |
| [51-majority-mint-hijack] | reports/dao_governance_findings/h-01-the-51-majority-can-hijack-the-partys-precious-tokens-through-an-arbitrary-.md | HIGH | Code4rena | 29545 |
| [transfer-vote-endorse] | reports/dao_governance_findings/m-06-after-endorsing-a-proposal-user-can-transfer-votes-to-another-user-for-endo.md | MEDIUM | Code4rena | 3210 |
| [votes-infinite-mint] | reports/dao_governance_findings/h-1-votes-balance-can-be-increased-indefinitely-in-multiple-contracts.md | HIGH | Sherlock | 21226 |
| [burn-block-voting] | reports/dao_governance_findings/m-03-burning-an-nft-can-be-used-to-block-voting.md | MEDIUM | Code4rena | 20140 |
| [quorum-delegate-lower] | reports/dao_governance_findings/m-8-adversary-can-abuse-delegating-to-lower-quorum.md | MEDIUM | Sherlock | 3750 |
| [griefing-delegation-fill] | reports/dao_governance_findings/griefing-an-account-from-getting-votes-delegated-to-it.md | MEDIUM | Immunefi | 38120 |
| [griefing-min-power] | reports/dao_governance_findings/m-15-griefer-can-minimize-delegatees-voting-power.md | MEDIUM | Code4rena | 8752 |
| [quorum-withdrawal-lower] | reports/dao_governance_findings/cordinated-group-of-attacker-can-artificially-lower-quorum-threshold-during-acti.md | MEDIUM | Codehawks | 57262 |
| [quorum-deadlock] | reports/dao_governance_findings/m-22-governance-deadlock-potential-in-blackgovernorsol-due-to-quorum-mismatch.md | MEDIUM | Code4rena | 58356 |
| [quorum-low-supply] | reports/dao_governance_findings/m-01-quorum-votes-have-no-effect-for-determining-whether-proposal-is-defeated-or.md | MEDIUM | Code4rena | 3268 |
| [expired-execute] | reports/dao_governance_findings/m-15-l2governorexecute-accepts-expired-defeated-proposals-attacker-front-runs-bl.md | MEDIUM | Code4rena | 58349 |
| [proposal-frontrun-salt] | reports/dao_governance_findings/proposal-front-running-via-predictable-salt-in-timelockcontrollerschedulebatch.md | MEDIUM | Codehawks | 57261 |
| [fasttrack-no-pause] | reports/dao_governance_findings/m-08-fasttrackproposalexecution-should-only-be-callable-when-temporalgovernor-is.md | MEDIUM | Code4rena | 26844 |
| [governance-takeover] | reports/dao_governance_findings/governance-takeover-via-unrestricted-elections_master-deployment.md | HIGH | Quantstamp | 61875 |
| [timelock-delay-zero] | reports/dao_governance_findings/timelock-delay-is-set-to-zero-in-the-constructor.md | MEDIUM | Halborn | 50145 |
| [timelock-emergency-bypass] | reports/dao_governance_findings/timelock-on-emergencyuninstallhook-can-be-bypassed.md | MEDIUM | Spearbit | 43814 |
| [safe-phony-sig] | reports/dao_governance_findings/m-11-if-a-hat-is-owned-by-address0-phony-signatures-will-be-accepted-by-the-safe.md | MEDIUM | Sherlock | 6731 |
| [safe-module-brick] | reports/dao_governance_findings/h-4-if-another-module-adds-a-module-the-safe-will-be-bricked.md | HIGH | Sherlock | 10277 |
| [voter-weight-burn] | reports/dao_governance_findings/voter-weight-manipulation-by-burning-after-vote.md | MEDIUM | OtterSec | 48616 |
| [snapshot-missing] | reports/dao_governance_findings/voting-power-snapshot-missing.md | HIGH | Codehawks | 57249 |
| [tie-approved] | reports/dao_governance_findings/m09-ties-in-governance-proposals-are-approved.md | MEDIUM | OpenZeppelin | 11332 |
| [extraordinary-attack] | reports/dao_governance_findings/m-12-governance-attack-on-extraordinary-proposals.md | MEDIUM | Code4rena | 20091 |
| [state-no-majority] | reports/dao_governance_findings/m-28-state-function-does-not-require-majority-of-votes-for-supporting-and-passin.md | MEDIUM | Code4rena | 3295 |

## Vulnerability Title

**DAO Governance Vulnerabilities** — Voting power manipulation, timelock bypass, proposal execution abuse, delegation exploits, quorum gaming, and checkpoint accounting bugs in on-chain governance systems.

### Overview

On-chain governance systems (Governor contracts, timelocks, voting escrow, delegation, multisigs) are foundational to DeFi protocol control. This entry covers 8 vulnerability families with 34+ unique findings from 15+ independent auditors across 25+ protocols. Core patterns include flash loan voting, double-voting via delegation, quorum manipulation through coordinated withdrawals, timelock bypass, checkpoint storage bugs, arbitrary proposal execution, missing voting snapshots, and proposal cancellation abuse.

#### Agent Quick View

- Root cause statement: "These vulnerabilities exist because governance mechanisms rely on manipulable voting power (flash loans, delegation recycling, missing snapshots), implement flawed quorum calculations (dynamic vs. snapshot, low-supply edge cases), fail to enforce timelock invariants (zero delay, governor can change delay, cancel clears wrong slots), or have checkpoint accounting errors (memory vs storage, stale delegations) — leading to unauthorized proposal execution, treasury theft, governance takeover, or permanent DoS."
- Pattern key: `governance_bypass | voting_proposal_timelock | manipulation_or_dos | unauthorized_execution_or_fund_theft`
- Interaction scope: `multi_contract`
- Primary affected component(s): `Governor, Timelock, VotingToken/VoteEscrow, Delegation, Treasury`
- Contracts / modules involved: `Governor, Timelock, VotingToken, VoteEscrow, Delegation, Multisig, Treasury, ProposalExecutor`
- Path keys: `flash_loan_voting`, `double_voting_delegation`, `quorum_manipulation`, `timelock_bypass`, `proposal_cancellation_abuse`, `checkpoint_storage_bug`, `arbitrary_proposal_execution`, `snapshot_missing`
- High-signal code keywords: `propose, castVote, execute, queue, cancel, delegate, quorum, quorumVotes, proposalThreshold, GovernorVotesQuorumFraction, _writeCheckpoint, getVotes, getPastVotes, timelock, setDelay, setGovernor, scheduleBatch, fastTrack, ArbitraryCallsProposal`
- Typical sink / impact: `governance takeover / treasury theft / proposal DoS / unauthorized execution / permanent fund lock`
- Validation strength: `strong` (34+ unique findings, 15+ auditors, 25+ protocols)

#### Contract / Boundary Map

```
VotingToken / VoteEscrow
     │
     ├── delegate(to) ──→ Delegation tracking (checkpoints)
     │                        │
     │                        └── _writeCheckpoint(tokenId, delegatedIds)
     │
     └── getVotes(account, blockNumber) ──→ voting power for proposal
                                                │
Governor                                        │
     │                                          │
     ├── propose(targets, values, calldatas) ────┘
     │       └── snapshot quorum at proposalSnapshot (if implemented)
     │
     ├── castVote(proposalId, support) ──→ uses getVotes/getPastVotes
     │       └── no snapshot → uses current balance → MANIPULABLE
     │
     ├── queue(proposalId) ──→ Timelock.schedule(operationId, delay)
     │
     ├── execute(proposalId) ──→ Timelock.execute(operationId)
     │       └── ProposalExecutor: ArbitraryCallsProposal, etc.
     │
     └── cancel(proposalId) ──→ should also cancel in Timelock
                                     └── missing → stale operation persists

Timelock
     │
     ├── setDelay(newDelay) ──→ governor can set to 0? → BYPASS
     ├── setGovernor(newGov) ──→ effective immediately? → TAKEOVER
     ├── cancel(bytes32 id) ──→ clears storage slot → can clear wrong slot?
     └── fastTrackProposalExecution() ──→ missing whenPaused? → ABUSE
```

- Entry surface(s): `Governor.propose()`, `Governor.castVote()`, `Governor.execute()`, `Governor.cancel()`, `Timelock.setDelay()`, `VoteEscrow.delegate()`
- Contract hop(s): `Governor → Timelock → Treasury`, `VotingToken → Governor`, `Delegation → VoteEscrow → Governor`
- Trust boundary crossed: `voting power calculated from token balances that change within same block`, `timelock delay modifiable by governor`, `proposal cancellation not propagated to timelock`
- Shared state or sync assumption: `quorum must reflect actual voting power at proposal creation`, `timelock operations and governance state must stay synchronized`, `checkpoint writes must persist to storage`

#### Valid Bug Signals

- Signal 1: `castVote` uses current balance (`getVotes(block.number)`) instead of snapshot at proposal creation (`getPastVotes(proposalSnapshot)`)
- Signal 2: Quorum calculated dynamically from current token supply, not frozen at proposal creation
- Signal 3: Governor can call `Timelock.setDelay(0)` or `Timelock.setGovernor(newAddress)` without going through the timelock itself
- Signal 4: `cancel()` in Governor does not call `Timelock.cancel()` — stale timelock operation can still be executed
- Signal 5: `_writeCheckpoint` uses `memory` instead of `storage` — same-block overwrites lost
- Signal 6: No restriction on delegating the same tokenId multiple times, or withdrawing delegated stake while votes are active
- Signal 7: `GovernorVotesQuorumFraction(4)` — 4 means 4%, not 25% (1/4th)
- Signal 8: Tokens can be burned/withdrawn after voting to reduce max_voter_weight, inflating vote impact

#### False Positive Guards

- Not this bug when: Governance uses `getPastVotes(proposalSnapshot)` from OZ Governor, which snapshots at proposal creation
- Safe if: Timelock's `setDelay` and `setGovernor` can only be called via the timelock itself (`require(msg.sender == address(this))`)
- Safe if: `cancel()` propagates cancellation to both Governor state and Timelock state
- Safe if: Checkpoint updates use `storage` reference and handle same-block overwrites correctly
- Safe if: Quorum is frozen at proposal creation time (OZ GovernorCompatibilityBravo pattern)
- Safe if: Token transfers/delegations are locked during active voting period

---

## Section 1: Flash Loan & Snapshot-Less Voting Power Manipulation

### Root Cause

Governance contracts that use current token balance (instead of a historical snapshot at proposal creation) for voting power allow attackers to temporarily inflate their voting weight via flash loans, large transfers, or vote-and-transfer cycling within a single block or transaction.

### Attack Scenario / Path Variants

**Path A: Flash Loan Voting**
Path key: `flash_loan_voting | Governor | VotingToken | inflated_voting_power`
Entry surface: `Governor.castVote()`
Contracts touched: `FlashLender → VotingToken → Governor`
1. Attacker takes a flash loan of governance tokens (or borrows from pool)
2. Attacker calls `castVote()` with enormous voting weight
3. Attacker repays flash loan in same transaction
4. Proposal outcome determined by temporary, unbacked voting power
5. **Impact**: Governance takeover — any proposal can be forced through (Common — 5/34 findings: flash-vote, snapshot-missing, votes-infinite-mint, double-vote-delegate, transfer-vote-endorse)

**Path B: Missing Voting Power Snapshot**
Path key: `snapshot_missing | Governor | VotingToken | vote_weight_manipulation_mid_proposal`
Entry surface: `Governor.castVote()`
Contracts touched: `Governor → VotingToken`
1. Voting power based on `getVotes(msg.sender)` at current block, not `getPastVotes(proposalSnapshot)`
2. User increases lock/deposit → votes with inflated power → immediately withdraws
3. No record of historical balance at proposal creation time
4. **Impact**: Each voter can temporarily maximize voting power for each vote (Common — 5/34 findings)

**Path C: Indefinite Vote Balance Inflation**
Path key: `vote_balance_inflation | initializeDistributionRecord | VotingToken | unlimited_voting_power`
Entry surface: `initializeDistributionRecord()`
Contracts touched: `MerkleDistributor → VotingToken`
1. `initializeDistributionRecord()` is public and can be called multiple times
2. Each call mints additional voting power tokens to the beneficiary
3. No access control or "already initialized" check
4. **Impact**: Unlimited voting power inflation — complete governance takeover (24 finders on this bug)

### Vulnerable Pattern Examples

**Example 1: No Flash Loan Protection in Voting** [HIGH]
```solidity
// ❌ VULNERABLE: Uses current balance, not snapshot — flash-loanable
// Source: reports/dao_governance_findings/h-05-flash-loans-can-affect-governance-voting-in-daosol.md
function countMemberVotes(address member) public view returns (uint) {
    return VETHER.balanceOf(member);  // ← current balance, not snapshot
    // Flash loan → inflate balance → vote → repay in same tx
}
```

**Example 2: Votes Can Be Increased Indefinitely** [HIGH]
```solidity
// ❌ VULNERABLE: No access control on re-initialization — unlimited voting power mint
// Source: reports/dao_governance_findings/h-1-votes-balance-can-be-increased-indefinitely-in-multiple-contracts.md
function initializeDistributionRecord(
    uint32 _domain, address _beneficiary, uint256 _amount,
    bytes32[] calldata merkleProof
) external validMerkleProof(_getLeaf(_beneficiary, _amount, _domain), merkleProof) {
    _initializeDistributionRecord(_beneficiary, _amount);
    // ← Can be called again and again, minting more voting tokens each time
}
```

---

## Section 2: Quorum Manipulation & Threshold Bypass

### Root Cause

Quorum thresholds calculated dynamically from current total supply (instead of frozen at proposal creation) can be manipulated by coordinated token burns, withdrawals, or delegation changes that reduce the denominator, allowing proposals to pass with fewer absolute votes than intended.

### Attack Scenario / Path Variants

**Path A: Quorum Lowered via Token Withdrawal**
Path key: `quorum_manipulation | Governor | VoteEscrow→Governor | proposal_passes_without_majority`
Entry surface: `VoteEscrow.withdraw()` during active voting
Contracts touched: `VoteEscrow → Governor (quorum calculation)`
1. Attacker coordinates with group to lock tokens and create a proposal
2. After proposal enters voting period, coordinated group withdraws locks (after expiry)
3. Total voting power decreases → quorum threshold drops proportionally
4. Attacker's votes now exceed lowered quorum → proposal passes
5. **Impact**: Minority stakeholders pass malicious proposals (Common — 4/34: quorum-delegate-lower, quorum-withdrawal-lower, quorum-deadlock, quorum-low-supply)

**Path B: Quorum Fraction Misconfiguration**
Path key: `quorum_misconfiguration | Governor | GovernorVotesQuorumFraction | lowered_threshold`
Entry surface: `Governor constructor`
Contracts touched: `Governor (internal)`
1. `GovernorVotesQuorumFraction(4)` — developer intends 25% (1/4th) but parameter means 4%
2. Proposals pass with only 4% of supply supporting
3. **Impact**: Proposals execute at 6.25× lower threshold than intended (1/34 finding, but widespread Compound-fork misconfiguration)

**Path C: Delegation Lowers Quorum**
Path key: `quorum_delegation_manipulation | Delegation→Governor | delegate | lowered_quorum`
Entry surface: `Governor.propose()` / `VotingToken.delegate()`
Contracts touched: `VotingToken → Governor`
1. When users delegate, their community votes are forfeited (reduce total)
2. Attacker delegates to self, then creates a proposal → quorum locked at reduced total
3. Self-delegate restores all community voting power → easily reaches quorum
4. **Impact**: Quorum artificially lowered at proposal creation

### Vulnerable Pattern Examples

**Example 3: Quorum Fraction Parameter Misunderstanding** [HIGH]
```solidity
// ❌ VULNERABLE: `4` means 4%, NOT 1/4th (25%) — proposals pass at 6.25x lower threshold
// Source: reports/dao_governance_findings/h-01-adversary-can-win-proposals-with-voting-power-as-low-as-4.md
constructor(string memory _name, IVotes _token, Agent _agent)
    Governor(_name)
    GovernorVotes(_token)
    GovernorVotesQuorumFraction(4) // ← Dev comment says 25% (1/4th) but 4 = 4%
{
    agent = _agent;
}
```

**Example 4: Quorum Returns 0 at Low Supply** [MEDIUM]
```solidity
// ❌ VULNERABLE: At low supply, quorum rounds to 0 — any vote passes proposal
// Source: reports/dao_governance_findings/m-01-quorum-votes-have-no-effect-for-determining-whether-proposal-is-defeated-or.md
function quorum() public view returns (uint256) {
    unchecked {
        return (settings.token.totalSupply() * settings.quorumThresholdBps) / 10_000;
        // When totalSupply is small → result rounds to 0 → quorum disabled
    }
}
```

---

## Section 3: Timelock Bypass & Unauthorized Execution

### Root Cause

Timelocks are meant to enforce a mandatory delay between proposal approval and execution. When the governor can directly modify the delay or governor address without going through the timelock itself, or when the timelock's cancel function can clear arbitrary storage slots, the delay can be bypassed entirely.

### Attack Scenario / Path Variants

**Path A: Governor Sets Delay to Zero**
Path key: `timelock_bypass | Timelock | Governor→Timelock | unauthorized_immediate_execution`
Entry surface: `Timelock.setGovernor()`, `Timelock.setDelay()`
Contracts touched: `Governor → Timelock`
1. Governor calls `Timelock.setGovernor(attacker)` — effective immediately (no timelock enforcement)
2. Attacker (now governor) calls `Timelock.setDelay(0)` — effective immediately
3. Attacker can now execute any operation instantly, including minting unlimited tokens
4. **Impact**: Complete timelock bypass → protocol takeover (Common — 4/34: timelock-bypass, timelock-delay-zero, timelock-emergency-bypass, bytes32-0-cancel)

**Path B: Cancel bytes32(0) Clears Arbitrary Storage**
Path key: `timelock_storage_clear | Timelock.cancel | bytes32(0) | uninitialized_takeover`
Entry surface: `Timelock.cancel(bytes32(0))`
Contracts touched: `Timelock (internal)`
1. `cancel()` takes `bytes32 id` and clears storage at `xor(shl(72, id), _TIMELOCK_SLOT)`
2. With `id = bytes32(0)`, the slot maps to the minimum delay storage
3. Canceller clears the delay → can reinitialize the timelock with zero delay
4. **Impact**: Timelock takeover — CRITICAL (Spearbit finding, 4 finders)

**Path C: Canceled Proposal Still Executable via Timelock**
Path key: `cancel_state_desync | Governor.cancel() | Timelock | stale_execution`
Entry surface: `Governor.cancel()` / `TimelockController.executeBatch()`
Contracts touched: `Governor → Timelock (state desync)`
1. Proposal canceled in Governor (`proposal.canceled = true`)
2. But `Timelock.cancel(operationId)` never called
3. Stale operation persists in Timelock — any executor can still call `executeBatch()`
4. **Impact**: Canceled proposals executed, governance integrity broken (Common — 3/34)

### Vulnerable Pattern Examples

**Example 5: Governor Can Bypass Timelock via setGovernor** [HIGH]
```solidity
// ❌ VULNERABLE: setGovernor effective immediately — no timelock enforcement
// Source: reports/dao_governance_findings/h-01-timelock-can-be-bypassed.md
function setGovernor(address _governor)
    public
    onlyRole(GOVERNOR_ROLE, "Must have timelock role")
{
    _swapRole(_governor, governor);
    governor = _governor;
    // ← Effective immediately. New governor can setDelay(0) next.
}
```

**Example 6: Cancel bytes32(0) Clears Timelock Delay** [CRITICAL]
```solidity
// ❌ VULNERABLE: id=0x0 maps to delay storage slot — cancel clears delay
// Source: reports/dao_governance_findings/cancelling-bytes320-allows-timelock-takeover.md
function cancel(bytes32 id) public virtual onlyRole(CANCELLER_ROLE) {
    assembly {
        let s := xor(shl(72, id), _TIMELOCK_SLOT) // Operation slot
        let p := sload(s)
        if or(and(1, p), iszero(p)) { revert(...) }
        sstore(s, 0) // ← When id=0, clears the minimum delay storage
    }
}
```

---

## Section 4: Delegation & Checkpoint Accounting Bugs

### Root Cause

Vote delegation and checkpoint systems track historical voting power for governance snapshots. When checkpoints are written to `memory` instead of `storage` (same-block overwrites lost), or when delegation state isn't properly cleaned up on delegate change, votes can be doubled, lost, or permanently corrupted.

### Attack Scenario / Path Variants

**Path A: _writeCheckpoint Memory vs Storage Bug**
Path key: `checkpoint_storage_bug | VoteEscrow | _writeCheckpoint | stale_or_lost_delegation`
Entry surface: `VoteEscrow.delegate()`
Contracts touched: `VoteEscrow (internal)`
1. User delegates tokenA to userB, then delegates tokenA to userC in same block
2. `_writeCheckpoint` reads `oldCheckpoint` as `memory` (not `storage`)
3. Update to `delegatedTokenIds` in same-block branch writes to memory, not storage
4. Only first delegation persists — second is silently lost
5. **Impact**: Incorrect delegation accounting (Common — 2/34: checkpoint-memory-bug, checkpoint-both-update)

**Path B: Double Voting via Delegation Withdrawal**
Path key: `double_voting_delegation | Delegation→Governor | VotingToken | 2x_vote_weight`
Entry surface: `VotingToken.delegate()` / `VotingToken.withdraw()`
Contracts touched: `VotingToken → Delegation → Governor`
1. Alice delegates to Bob → Bob votes with combined weight (Alice + Bob)
2. Alice withdraws delegated stake (no lockup enforcement during voting)
3. Alice transfers tokens to new account → re-stakes → votes on same proposal
4. **Impact**: Same tokens vote twice (Common — 3/34: double-vote-delegate, transfer-vote-endorse, voter-weight-burn)

**Path C: Delegation Griefing — Fill Delegate Array**
Path key: `delegation_griefing | VoteEscrow.delegate | Delegation | block_votes`
Entry surface: `VoteEscrow.delegate()`
Contracts touched: `VoteEscrow (internal)`
1. Victim's delegatedTokenIds array has a max size (e.g., 500)
2. Attacker creates 500 minimum-value lock NFTs, delegates all to victim
3. Victim's array is full of worthless delegations → effective voting power ≈ 0
4. Legitimate delegators can no longer delegate to victim
5. **Impact**: Targeted governance DoS (2/34: griefing-delegation-fill, griefing-min-power)

### Vulnerable Pattern Examples

**Example 7: _writeCheckpoint Memory Bug** [HIGH]
```solidity
// ❌ VULNERABLE: `memory` instead of `storage` — same-block updates lost
// Source: reports/dao_governance_findings/h-07-_writecheckpoint-does-not-write-to-storage-on-same-block.md
Checkpoint memory oldCheckpoint = checkpoints[toTokenId][nCheckpoints - 1];
//         ^^^^^^ should be `storage`
if (nCheckpoints > 0 && oldCheckpoint.fromBlock == block.number) {
    oldCheckpoint.delegatedTokenIds = _delegatedTokenIds;
    // ← Writes to memory copy, never persisted to storage
}
```

**Example 8: Double Voting After Delegation Withdrawal** [HIGH]
```solidity
// ❌ VULNERABLE: No stake lockup during active voting — delegate→vote→withdraw→re-vote
// Source: reports/dao_governance_findings/double-voting-by-delegaters.md
// 1. Bob delegates to Alice → Alice votes with Bob's weight
// 2. Bob withdraws stake (no lock during vote)
// 3. Bob transfers to alt account → re-stakes → votes again
// Conceptual: no code guard prevents withdrawal during active proposal
```

---

## Section 5: Proposal Cancellation & Execution Abuse

### Root Cause

Proposal lifecycle functions (`cancel`, `execute`, `queue`) with insufficient state validation allow: executing defeated/expired proposals, canceling succeeded proposals to block governance, or re-executing via stale timelock operations.

### Attack Scenario / Path Variants

**Path A: Execute Defeated/Expired Proposals**
Path key: `expired_proposal_execution | Governor.execute | ProposalState | malicious_execution`
Entry surface: `Governor.execute()`
Contracts touched: `Governor → Timelock → Target`
1. `execute()` accepts `Succeeded`, `Defeated`, and `Expired` states (too permissive)
2. Attacker front-runs legitimate proposal execution with an expired proposal
3. Target function has one-time-per-period guard → attacker's execution blocks legitimate one
4. **Impact**: Block legitimate governance actions for entire epoch (1/34 finding)

**Path B: Unrestricted Proposal Cancellation**
Path key: `proposal_cancellation_abuse | Governor | cancel() | block_legitimate_proposals`
Entry surface: `Governor.cancel()`
Contracts touched: `Governor (internal)`
1. `cancel()` allows cancellation in all states except `Executed`
2. Proposer (or anyone if proposer's power drops below threshold) can cancel even after successful vote
3. **Impact**: Governance DoS — any voted proposal can be blocked (2/34 findings)

**Path C: Arbitrary Call via 51% Minting Authority**
Path key: `arbitrary_proposal_execution | Governor→ProposalExecutor | arbitrary_call | fund_theft`
Entry surface: `ArbitraryCallsProposal`
Contracts touched: `Governor → AddPartyCardsAuthority → ArbitraryCallsProposal`
1. 51% majority creates ArbitraryCallsProposal to call `AddPartyCardsAuthority.addPartyCards()`
2. Mints new governance NFT with astronomical voting power to attacker
3. Attacker now has 100% voting power → creates unanimously-voted proposal
4. Transfers all precious NFTs out of the party treasury
5. **Impact**: Complete governance hijack and treasury theft (2/34 findings)

### Vulnerable Pattern Examples

**Example 9: Unrestricted Cancellation** [MEDIUM]
```solidity
// ❌ VULNERABLE: Can cancel in all states except Executed — blocks governance
// Source: reports/dao_governance_findings/unrestricted-proposal-cancellation-allows-governance-process-manipulation.md
function cancel(uint256 proposalId) external override {
    ProposalCore storage proposal = _proposals[proposalId];
    ProposalState currentState = state(proposalId);
    if (currentState == ProposalState.Executed) {
        revert InvalidProposalState(...);
    }
    // ← Should also block cancellation of Succeeded and Queued proposals
    proposal.canceled = true;
}
```

---

## Section 6: Quadratic Voting & Tally Errors

### Root Cause

Quadratic voting systems that fail to properly square individual votes before summing them, or that don't enforce majority requirements (ties pass), produce outcomes that don't match the governance specification.

### Attack Scenario / Path Variants

**Path A: Quadratic Sum Not Squared**
Path key: `quadratic_tally_error | Governor | _fundingVote | incorrect_power_distribution`
Entry surface: `StandardFunding._fundingVote()`
Contracts touched: `Governor (internal)`
1. Spec says: sum of squares of votes ≤ square of token holdings
2. Code enforces: sum of absolute votes ≤ square of holdings (votes NOT squared)
3. Attacker concentrates all votes on one proposal instead of distributing
4. **Impact**: Governance hijacked with 10% of tokens instead of 50% (1/34 finding)

**Path B: Ties Approve Proposals**
Path key: `tie_approval | Governor.state | quorum_check | wrong_outcome`
Entry surface: `Governor.state(proposalId)`
Contracts touched: `Governor (internal)`
1. When forVotes == againstVotes, `state()` returns `Succeeded` instead of `Defeated`
2. Contentious proposals that should fail get executed
3. **Impact**: Critical governance changes pass without majority support (2/34 findings: tie-approved, state-no-majority)

### Vulnerable Pattern Examples

**Example 10: Quadratic Voting Sum Not Squared** [MEDIUM]
```solidity
// ❌ VULNERABLE: votes not squared before summing — lower hijack threshold
// Source: reports/dao_governance_findings/m-19-quadratic-voting-tally-done-wrong.md
function _fundingVote(...) internal {
    // Spec: sum(votes_i^2) <= tokenBalance^2
    // Code: sum(|votes_i|) <= tokenBalance^2  ← votes NOT squared
    voter.votesCast += SafeCast.toInt128(voteParams_);
    // ← Checking |sum| ≤ balance^2 instead of sum(each^2) ≤ balance^2
}
```

---

## Section 7: Multisig & Safe Module Exploits

### Root Cause

Gnosis Safe modules and signer gate contracts assume module counts remain consistent and that hat owners are always valid addresses. When external modules bypass the module counter or address(0) is a hat wearer, signatures can be forged or the safe can be permanently bricked.

### Attack Scenario / Path Variants

**Path A: Module Count Desync Bricks Safe**
Path key: `safe_module_desync | HatsSignerGate | enabledModuleCount | permanent_brick`
Entry surface: `Safe.execTransactionFromModule()` (via external module)
Contracts touched: `ExternalModule → Safe → HatsSignerGateBase`
1. External module calls `Safe.enableModule()` directly (bypasses `enableNewModule()`)
2. `enabledModuleCount` not incremented → guard hash check fails
3. `checkAfterExecution()` always reverts → no transaction can execute
4. **Impact**: Safe permanently bricked — all funds stuck forever (3 finders)

**Path B: Phony Signatures via address(0) Hat Wearer**
Path key: `safe_phony_sig | HatsSignerGate | ecrecover | unauthorized_execution`
Entry surface: `Safe.checkNSignatures()`
Contracts touched: `Safe → HatsSignerGateBase`
1. `ecrecover` returns `address(0)` for invalid signatures (wrong v value)
2. Hat owned by `address(0)` → `isValidSigner(address(0))` returns true
3. Anyone can forge a signature that resolves to address(0) and passes validation
4. **Impact**: Non-signers can authorize arbitrary Safe transactions (2 finders)

### Vulnerable Pattern Examples

**Example 11: Module Addition Bricks Safe** [HIGH]
```solidity
// ❌ VULNERABLE: External module adds module → enabledModuleCount desync → safe bricked
// Source: reports/dao_governance_findings/h-4-if-another-module-adds-a-module-the-safe-will-be-bricked.md
function checkAfterExecution(bytes32, bool) external override {
    // Uses enabledModuleCount + 1 for "after" check
    // But if module was added via another module (not through enableNewModule()),
    // enabledModuleCount wasn't incremented → hash mismatch → REVERT
    // ALL future transactions blocked
}
```

---

## Section 8: Governance Takeover via Deployment/Factory Bugs

### Root Cause

When governance contracts accept operations from instances whose deployment origin isn't verified (i.e., anyone can deploy a governance contract with favorable parameters and have it recognized by the master contract), the entire governance system can be bypassed.

### Attack Scenario / Path Variants

**Path A: Unrestricted elections_master Deployment**
Path key: `governance_factory_bypass | master.make_action | elections_master | arbitrary_execution`
Entry surface: `master.make_action()`
Contracts touched: `Attacker-deployed elections_master → master`
1. `make_action()` validates sender by recalculating expected address from parameters
2. But doesn't check if the contract was deployed through legitimate `create_elections()` flow
3. Attacker deploys `elections_master` with `success_amount = 1`
4. Attacker casts one vote → quorum reached → calls `make_action()`
5. **Impact**: Complete governance takeover — arbitrary actions including contract upgrades (Quantstamp finding)

### Vulnerable Pattern Examples

**Example 12: Governance Takeover via Unverified Factory** [HIGH]
```
// ❌ VULNERABLE: make_action() validates address but not deployment origin
// Source: reports/dao_governance_findings/governance-takeover-via-unrestricted-elections_master-deployment.md
// Attacker deploys elections_master with success_amount = 1
// Casts one vote → quorum met → calls make_action()
// master validates recalculated address (matches) but not deployment flow
// Attacker executes arbitrary governance actions
```

---

## Impact Analysis

### Technical Impact
- **Governance takeover**: Flash loan voting, vote inflation, factory bypass enable full control (Common — 10/34 findings)
- **Treasury theft**: Arbitrary proposal execution, timelock bypass lead to fund extraction (Common — 6/34 findings)
- **Governance DoS**: Proposal cancellation abuse, safe bricking, delegation griefing block all operations (Moderate — 5/34 findings)
- **Incorrect outcomes**: Quorum rounding to 0, ties passing, quadratic tally errors produce wrong results (Moderate — 5/34 findings)
- **Silent accounting errors**: Checkpoint memory bugs, delegation desync cause gradual power drift (Moderate — 4/34 findings)

### Business Impact
- **Financial**: Complete treasury drain via timelock bypass or arbitrary execution
- **Protocol stability**: Governance deadlock blocks protocol upgrades and parameter changes
- **Trust**: Governance manipulation undermines decentralization claims

### Affected Scenarios
- All Governor-based protocols (OZ Governor, Compound Governor, custom implementations)
- ve-token governance systems with delegation
- Multisig wallets with module-based access control (Gnosis Safe + Hats)
- Cross-chain governance (L1→L2 Governor bridges)
- Grant distribution systems with quadratic voting
- NFT-based voting (Party Protocol, Nouns, etc.)

---

## Secure Implementation

**Fix 1: Snapshot-Based Voting Power**
```solidity
// ✅ SECURE: Use historical snapshot, not current balance
function castVote(uint256 proposalId, uint8 support) public {
    uint256 weight = getVotes(msg.sender, proposalSnapshot(proposalId));
    // ← Uses getPastVotes at proposal creation block — immune to flash loans
}
```

**Fix 2: Timelock Self-Governance**
```solidity
// ✅ SECURE: Only timelock can change its own parameters
function setDelay(uint256 newDelay) public {
    require(msg.sender == address(this), "Timelock: caller must be timelock");
    delay = newDelay;
}
function setGovernor(address newGovernor) public {
    require(msg.sender == address(this), "Timelock: caller must be timelock");
    governor = newGovernor;
}
```

**Fix 3: Freeze Quorum at Proposal Creation**
```solidity
// ✅ SECURE: Quorum locked at proposal creation — cannot be manipulated mid-vote
function propose(...) public returns (uint256) {
    uint256 proposalId = hashProposal(...);
    _proposals[proposalId].quorumVotes = quorum();  // frozen here
    // ← Token withdrawals during voting don't affect this quorum
}
```

---

## Detection Patterns

### Contract / Call Graph Signals
```
- castVote/vote using getVotes(current) instead of getPastVotes(snapshot)
- Timelock.setDelay() or setGovernor() callable by governor (not by address(this))
- Governor.cancel() not calling Timelock.cancel()
- _writeCheckpoint using `memory` instead of `storage` reference
- GovernorVotesQuorumFraction parameter ≠ intended percentage
- No delegation lockup during active proposals
- quorum() returning 0 at low supply with no minimum floor
- ArbitraryCallsProposal allowing calls to minting authorities
- execute() accepting Defeated or Expired proposal states
```

### High-Signal Grep Seeds
```
- propose
- castVote
- execute
- queue
- cancel
- delegate
- quorum
- quorumVotes
- quorumThresholdBps
- GovernorVotesQuorumFraction
- _writeCheckpoint
- getVotes
- getPastVotes
- proposalSnapshot
- timelock
- setDelay
- setGovernor
- scheduleBatch
- fastTrackProposalExecution
- ArbitraryCallsProposal
- enabledModuleCount
- countMemberVotes
- endorseProposal
- initializeDistributionRecord
- delegatedTokenIds
- countValidSignatures
```

### Audit Checklist
- [ ] Verify voting uses historical snapshot (getPastVotes) not current balance
- [ ] Verify quorum frozen at proposal creation, with minimum floor
- [ ] Verify timelock parameters only modifiable through the timelock itself
- [ ] Verify cancel() propagates to both Governor state and Timelock state
- [ ] Verify _writeCheckpoint uses storage reference for same-block updates
- [ ] Verify delegation/withdrawal locked during active voting periods
- [ ] Verify execute() only accepts Succeeded proposals
- [ ] Verify cancel() restricted after voting succeeds
- [ ] Verify governance factory validates deployment origin not just address
- [ ] Verify Safe module counts stay consistent across module additions
- [ ] Verify quadratic voting tallies square individual votes before summing

---

## Real-World Examples

### Known Exploits & Audit Findings
- **MakerDAO** — Flash loan used to affect governance voting outcome (2020)
- **Vader Protocol** — Flash loans can affect DAO.sol voting — Code4rena (2021)
- **Malt Finance** — Timelock bypassed via setGovernor() + setDelay(0) — Code4rena (2021)
- **Solady/Coinbase** — cancel(bytes32(0)) clears timelock delay storage — Spearbit (2024)
- **RAAC** — Canceled proposals still executable via TimelockController — Codehawks (2025)
- **Golom** — _writeCheckpoint memory vs storage bug — Code4rena (2022)
- **IQ AI** — GovernorVotesQuorumFraction(4) means 4% not 25% — Code4rena (2025)
- **Tokensoft** — initializeDistributionRecord() infinite vote mint — Sherlock (2023)
- **PartyDAO** — 51% majority hijacks NFTs via ArbitraryCallsProposal — Code4rena (2022/2023)
- **FrankenDAO** — Delegation abused to lower quorum — Sherlock (2022)
- **Alchemix** — Delegation griefing fills delegate array — Immunefi (2024)
- **Ajna** — Quadratic voting tally not squared — Sherlock (2023)
- **Hats Protocol** — Safe module addition bricks safe / phony signatures — Sherlock (2023)
- **XDAO** — Governance takeover via unverified elections_master — Quantstamp (2025)
- **Blackhole** — Expired/defeated proposals executable + quorum deadlock — Code4rena (2025)

---

## Prevention Guidelines

### Development Best Practices
1. Always use `getPastVotes(proposalSnapshot)` — never current balance for voting power
2. Freeze quorum at proposal creation with a minimum floor (e.g., at least 1)
3. Timelock parameter changes (delay, governor) must go through the timelock itself
4. Propagate proposal cancellation to both Governor and Timelock state
5. Use `storage` references in checkpoint write functions for same-block updates
6. Lock tokens/delegation during active proposal voting periods
7. Restrict `execute()` to only `Succeeded` state
8. Restrict `cancel()` from operating on `Succeeded` or `Queued` proposals
9. Validate governance contract deployment origin, not just reconstructed address
10. Set minimum quorum floor that cannot be gamed at low supply

### Testing Requirements
- Unit tests for: Flash loan voting attempt (should fail with snapshot), quorum at low supply, timelock delay modification
- Integration tests for: Full propose→vote→queue→execute lifecycle, cancel propagation to timelock
- Fuzz tests for: Random delegation→withdraw→re-delegate sequences verifying total power invariant
- Invariant tests for: `totalVotingPower == sum(allVotes)`, `quorum >= MINIMUM_QUORUM`, `timelock.delay >= MIN_DELAY`

---

## Keywords for Search

`governance`, `governor`, `timelock`, `proposal`, `castVote`, `quorum`, `quorumVotes`, `voting power`, `delegation`, `delegate`, `checkpoint`, `snapshot`, `getPastVotes`, `getVotes`, `flash loan voting`, `vote manipulation`, `proposal cancellation`, `execute proposal`, `queue proposal`, `GovernorVotesQuorumFraction`, `proposalThreshold`, `ArbitraryCallsProposal`, `multisig`, `gnosis safe`, `module`, `signer gate`, `quadratic voting`, `timelock bypass`, `governor takeover`, `treasury theft`, `vote escrow`, `NFT governance`, `voting while vesting`, `initializeDistributionRecord`, `endorseProposal`, `_writeCheckpoint`, `delegatedTokenIds`

---

## Related Vulnerabilities

- [DB/general/vetoken-governance/VETOKEN_VOTING_ESCROW_VULNERABILITIES.md](../vetoken-governance/VETOKEN_VOTING_ESCROW_VULNERABILITIES.md) — VeToken-specific voting and escrow vulnerabilities
- [DB/cosmos/app-chain/governance/governance-voting-vulnerabilities.md](../../cosmos/app-chain/governance/governance-voting-vulnerabilities.md) — Cosmos-specific governance issues
- [DB/general/access-control/access-control-vulnerabilities.md](../access-control/access-control-vulnerabilities.md) — Access control failures relevant to governance admin functions
