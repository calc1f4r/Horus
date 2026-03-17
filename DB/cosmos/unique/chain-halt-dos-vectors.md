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

## References
- [h-18-asa-2025-003-groups-module-can-halt-chain-when-handling-a-malicious-proposa.md](../../reports/cosmos_cometbft_findings/h-18-asa-2025-003-groups-module-can-halt-chain-when-handling-a-malicious-proposa.md)
- [linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md](../../reports/cosmos_cometbft_findings/linear-iteration-over-rewards-plans-in-beginblock-exposes-permissionless-chain-h.md)
- [h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md](../../reports/cosmos_cometbft_findings/h-3-adversary-can-arbitrarily-trigger-a-chain-halt-by-sending-msgremovedelegates.md)
- [potential-non-determinism-issue-in-finalizeblock.md](../../reports/cosmos_cometbft_findings/potential-non-determinism-issue-in-finalizeblock.md)
- [dos-in-cometbft-block-sync-githubcomcometbftcometbftblocksync.md](../../reports/cosmos_cometbft_findings/dos-in-cometbft-block-sync-githubcomcometbftcometbftblocksync.md)

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

- Signal 1: Unbounded loop over user-controlled array can exceed block gas limit
- Signal 2: External call failure causes entire transaction to revert
- Signal 3: Attacker can grief operations by manipulating state to cause reverts
- Signal 4: Resource exhaustion through repeated operations without rate limiting

#### False Positive Guards

- Not this bug when: Loop iterations are bounded by a reasonable constant
- Safe if: External call failures are handled gracefully (try/catch or pull pattern)
- Requires attacker control of: specific conditions per pattern

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

`BeginBlock`, `EndBlocker`, `FinalizeBlock`, `PrepareProposal`, `ProcessProposal`, `chain_halt`, `cometbft`, `cosmos_sdk`, `denial_of_service`, `division_by_zero`, `dos`, `linear_iteration`, `negative_amount`, `non_determinism`
