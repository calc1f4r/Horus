---
# Core Classification
protocol: cosmos-sdk
chain: everychain
category: chain_halt
vulnerability_type: denial_of_service

# Attack Vector Details
attack_type: chain_halt
affected_component: abci_consensus

# Technical Primitives
primitives:
  - BeginBlock
  - EndBlocker
  - FinalizeBlock
  - ProcessProposal
  - PrepareProposal
  - linear_iteration

# Impact Classification
severity: critical
impact: chain_halt
exploitability: 0.8
financial_impact: critical

# Context Tags
tags:
  - cosmos_sdk
  - cometbft
  - chain_halt
  - dos
  - non_determinism
  - BeginBlock
  - EndBlocker
  - division_by_zero
  - negative_amount
  
language: go
version: all

# Pattern Identity (Required)
root_cause_family: denial_of_service
pattern_key: denial_of_service | abci_consensus | denial_of_service

# Interaction Scope (Required for multi-contract or multi-path issues)
interaction_scope: single_contract

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - BeginBlock
  - EndBlocker
  - FinalizeBlock
  - PrepareProposal
  - ProcessProposal
  - linear_iteration
---

## References & Source Reports

| Report | Path | Severity | Signal |
|--------|------|----------|--------|
| Groups module malicious proposal chain halt | `reports/cosmos_cometbft_findings/h-18-asa-2025-003-groups-module-can-halt-chain-when-handling-a-malicious-proposa.md` | HIGH | Division-by-zero or invalid group state in consensus path |
| BeginBlock rewards plan iteration halt | `reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md` | HIGH | Permissionless state growth consumed by BeginBlock |
| MsgRemoveDelegates arbitrary halt | `reports/cosmos_cometbft_findings/h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md` | HIGH | User message creates later consensus panic |
| FinalizeBlock non-determinism | `reports/cosmos_cometbft_findings/potential-non-determinism-issue-in-finalizeblock.md` | HIGH | Validator-dependent result in consensus execution |
| CometBFT block sync DoS | `reports/cosmos_cometbft_findings/dos-in-cometbft-block-sync-githubcomcometbftcometbftblocksync.md` | MEDIUM | Peer-controlled resource exhaustion |

## Vulnerability Title

**Chain Halt and DoS Attack Vectors in Cosmos SDK Appchains**

### Overview

Cosmos SDK appchains are susceptible to various chain halt and denial of service attacks due to unmetered linear iteration in BeginBlock/EndBlocker, division by zero in governance modules, negative amount validation failures causing panics, and non-determinism in consensus-critical code. These vulnerabilities allow attackers to halt the chain with relatively low cost, breaking security guarantees for all validators and users.



#### Agent Quick View

- Root cause statement: "This vulnerability exists because of denial_of_service"
- Pattern key: `denial_of_service | abci_consensus | denial_of_service`
- Interaction scope: `single_contract`
- Primary affected component(s): `abci_consensus`
- High-signal code keywords: `BeginBlock`, `EndBlocker`, `FinalizeBlock`, `PrepareProposal`, `ProcessProposal`, `linear_iteration`
- Typical sink / impact: `chain_halt`
- Validation strength: `moderate`

#### Contract / Boundary Map

- Entry surface(s): See pattern-specific attack scenarios below
- Contract hop(s): `N/A`
- Trust boundary crossed: `internal`
- Shared state or sync assumption: `state consistency across operations`

#### Valid Bug Signals

- Signal 1: `BeginBlock`, `EndBlocker`, `FinalizeBlock`, `PrepareProposal`, or `ProcessProposal` iterates over permissionlessly growable state.
- Signal 2: A normal user message can store malformed state that later panics in consensus code, even if the original transaction succeeds.
- Signal 3: Consensus-critical code depends on map iteration order, wall-clock time, local node state, peer input, floating point, or nondeterministic sorting.
- Signal 4: Arithmetic in consensus paths can divide by zero, create negative coins, overflow counters, or call SDK constructors that panic on attacker-controlled values.

#### False Positive Guards

- Not this bug when: The loop is over validator-set, module-constant, governance-bounded, or paginated state with enforced caps.
- Safe if: Malformed user input is rejected at message handling time and consensus paths treat stored state as already validated without panic-prone recomputation.
- Requires attacker control of: proposal contents, delegation/group/reward-plan state, mempool ordering, peer block-sync input, or any state read by ABCI lifecycle hooks.

### Root Cause

1. **Unmetered linear iteration**: BeginBlock/EndBlocker iterate over unbounded collections without gas limits
2. **Division by zero**: Missing validation allows crafted proposals to cause arithmetic panics
3. **Negative amount panics**: Integer types without non-negative validation cause sdk.NewCoin to panic
4. **Non-determinism**: Different validator nodes computing different results, breaking consensus
5. **Unbounded block sync**: Malicious peers can overwhelm syncing nodes during block sync

### Impact Analysis

#### Technical Impact
- Complete chain halt (no new blocks produced)
- Consensus failure from non-determinism
- Validator nodes crash or hang
- Block sync disruption for new nodes
- All AVS security guarantees broken

#### Business Impact
- Network completely unavailable
- Emergency governance required to patch
- Validator slashing during downtime
- User funds inaccessible
- Massive reputation damage

### Audit Checklist[text](../../../DeFiHackLabs)
- BeginBlock/EndBlocker have bounded iteration
- All user-supplied amounts validated as positive
- Division operations check for zero divisor
- Map iterations converted to sorted deterministic order
- No system time or random in consensus code
- Plan/proposal creation has scaling fees

### Real-World Examples

| Protocol | Audit Firm | Severity | Issue |
|----------|------------|----------|-------|
| MilkyWay | Cantina | HIGH | Linear iteration over rewards plans |
| Allora | Sherlock | HIGH | Negative amount causes chain halt |
| SEDA/Cosmos | Sherlock | HIGH | Groups module division by zero (ASA-2025-003) |
| Various | OtterSec | HIGH | Non-determinism in FinalizeBlock |
| CometBFT | Security Audit | MEDIUM | Block sync DoS |

### Keywords

chain_halt, BeginBlock, EndBlocker, FinalizeBlock, linear_iteration, unbounded_loop, sdk.NewCoin, division_by_zero, negative_amount, non_determinism, consensus_failure, map_iteration, time.Now, panic, DoS, ASA-2025-003, groups_module

### Detection Patterns

#### Code Patterns to Look For
```
- `for _, x := range keeper.GetAll...` inside BeginBlocker, EndBlocker, FinalizeBlock, PrepareProposal, or ProcessProposal
- `sdk.NewCoin`, `Quo`, `QuoInt`, `Int64`, division, or percentage math in consensus paths without zero/negative validation
- map iteration or unsorted key traversal used to build proposals, votes, commitments, or state roots
- message handlers that append unbounded plans/delegates/groups consumed globally each block
- panics, `Must*` helpers, or unchecked errors reachable from ABCI lifecycle hooks
```

#### Audit Checklist
- [ ] Verify all state-changing functions have appropriate access controls
- [ ] Check for CEI pattern compliance on external calls
- [ ] Validate arithmetic operations for overflow/underflow/precision loss
- [ ] Confirm oracle data freshness and sanity checks

### Keywords for Search

> These keywords enhance vector search retrieval:

`BeginBlock`, `EndBlocker`, `FinalizeBlock`, `PrepareProposal`, `ProcessProposal`, `chain_halt`, `cometbft`, `cosmos_sdk`, `denial_of_service`, `division_by_zero`, `dos`, `linear_iteration`, `negative_amount`, `non_determinism`
