---
# Core Classification
protocol: flare-fassets
chain: flare
category: dos
vulnerability_type: gas_griefing_fee_theft

# Pattern Identity
root_cause_family: hardcoded_gas_allowance
pattern_key: gas_capped_nat_transfer | executeMinting executor fee payout | agent front-runs executor | fee redirected to agent collateral pool

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - Minting.sol (MintingFacet.executeMinting)
  - CollateralReservations.sol (reserveCollateral)
  - Transfers.sol (transferNAT)
path_keys:
  - gas_capped_nat_transfer | executeMinting | Minting -> Transfers.transferNAT -> executor receive() reverts
  - gas_capped_nat_transfer | agent_executeMinting_front_run | Minting -> distributeCollateralReservationFee

# Attack Vector Details
attack_type: logical_error
affected_component: executor_fee_distribution

# Technical Primitives
primitives:
  - TRANSFER_GAS_ALLOWANCE
  - call_with_gas_cap
  - executor_fee_natGWei
  - permission_check_or_disjunction
  - collateral_reservation_fee_distribution
  - front_running

# Grep / Hunt-Card Seeds
code_keywords:
  - executeMinting
  - transferNAT
  - TRANSFER_GAS_ALLOWANCE
  - executorFeeNatGWei
  - unclaimedExecutorFee
  - distributeCollateralReservationFee
  - crt.executor

# Impact Classification
severity: medium
impact: fund_loss
financial_impact: medium

# Context Tags
tags:
  - defi
  - bridge
  - gas_griefing
  - front_running
  - executor_economics
  - agent_role
  - native_transfer

# Version Info
language: solidity
version: ">=0.8.0"
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [45447] | reports/flare-l1_findings/45447-sc-medium-executor-cannot-execute-minting-while-the-agent-can-execute-the-transaction-and-stea.md | MEDIUM | immunefi | https://reports.immunefi.com/flare-fassets-or-mainnet-audit-comp/45447-sc-medium-executor-cannot-execute-minting-while-the-agent-can-execute-the-transaction-and-stea.md |

## Gas-capped executor fee payout in executeMinting lets agents steal executor fees via front-running

### Overview

In Flare FAssets `executeMinting`, the executor's NAT fee is sent via `Transfers.transferNAT`, which forwards only a hardcoded 100k gas stipend (`TRANSFER_GAS_ALLOWANCE`) to the recipient. Contract executors whose `receive()` exceeds the stipend always revert, and since the agent also satisfies the `executeMinting` permission check, the agent can front-run the executor, execute the minting itself, and sweep the "unclaimed" executor fee into its own collateral pool.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because the executor fee payout uses a fixed 100k-gas `call` while the executor may be an arbitrary contract, and unclaimed fees are donated to the agent's collateral pool — an outcome the agent itself can trigger by calling `executeMinting` first."
- Pattern key: `gas_capped_nat_transfer | executeMinting executor fee payout | agent front-runs executor | fee redirected to agent collateral pool`
- Interaction scope: `multi_contract`
- Primary affected component(s): `Minting.executeMinting fee distribution, Transfers.transferNAT`
- Contracts / modules involved: `Minting.sol, CollateralReservations.sol, Transfers.sol, AgentVault/CollateralPool`
- Path keys: `gas_capped_nat_transfer | executeMinting | Minting -> Transfers.transferNAT -> executor receive() reverts`, `gas_capped_nat_transfer | agent_executeMinting_front_run | Minting -> distributeCollateralReservationFee`
- High-signal code keywords: `executeMinting, transferNAT, TRANSFER_GAS_ALLOWANCE, executorFeeNatGWei, unclaimedExecutorFee, distributeCollateralReservationFee`
- Typical sink / impact: `executor fee theft + permanent DoS of contract executors; fee flows to agent's collateral pool`
- Validation strength: `strong` (foundry PoC in report [45447] shows revert with gas-hungry receive())

#### Contract / Boundary Map

- Entry surface(s): `MintingFacet.executeMinting(proof, crtId)` — callable by `crt.minter || crt.executor || agent owner`
- Contract hop(s): `reserveCollateral (executor + fee stored) -> executeMinting -> Transfers.transferNAT{gas: 100k}(executor) -> executor.receive()`
- Trust boundary crossed: `external call into user-supplied executor contract with capped gas; fee-claim fallback path benefits adversary (agent)`
- Shared state or sync assumption: `unclaimedExecutorFee must either reach the executor or be held, not silently reallocated to the party that can trigger the fallback`

#### Valid Bug Signals

- Signal 1: Fee payout uses `.call{value, gas: FIXED}` to an arbitrary contract recipient
- Signal 2: A permission check admits a party (agent) that financially benefits from the payout failing
- Signal 3: On payout failure/unclaimed, funds are redirected to that beneficiary's pool within the same call

#### False Positive Guards

- Not this bug when: executor is an EOA (receive() costs ~0; transfer succeeds) — fee theft then requires pure front-running which still nets the agent the unclaimed fee only if payout is skipped for non-callers
- Safe if: executor fee is pulled (withdrawal pattern) by the executor, or unclaimed fees are returned to the minter/burned rather than given to the agent
- Requires attacker control of: an agent identity (to front-run and capture fees) or merely a gas-heavy executor `receive()` for the DoS variant (any executor can be griefed by its own design, but the theft needs the agent)

### Vulnerability Description

#### Root Cause

1. `Transfers.transferNAT` uses `(bool success, ) = _recipient.call{value: _amount, gas: TRANSFER_GAS_ALLOWANCE}("")` — 100k gas hard cap. A contract executor whose `receive()` performs e.g. ERC20 ops (~50k–100k+ gas each) exceeds the cap and the whole `executeMinting` reverts ("transfer failed") when the executor itself calls.
2. The permission check `msg.sender == crt.minter || msg.sender == crt.executor || Agents.isOwner(agent, msg.sender)` lets the agent execute the minting. When the caller is not the executor, `unclaimedExecutorFee` stays set and is folded into `distributeCollateralReservationFee(agent, crt.reservationFeeNatWei + unclaimedExecutorFee)` — paid into the agent's collateral pool.

#### Attack Scenario / Path Variants

**Path A: Agent front-runs contract executor and captures its fee** [Approx Vulnerability : MID]
Path key: `gas_capped_nat_transfer | agent_executeMinting_front_run | Minting -> distributeCollateralReservationFee`
1. User reserves collateral naming a smart-contract executor bot and pays on the underlying chain.
2. Agent watches the mempool for the executor's `executeMinting` and front-runs it (agent passes the permission disjunction).
3. Because `msg.sender != crt.executor`, the fee payout is skipped and `unclaimedExecutorFee` is added to the agent's collateral pool via `distributeCollateralReservationFee`.
4. Executor loses its fee; agent's pool (in which the agent is a large staker) gains it. Repeatable per minting.

**Path B: Permanent DoS of contract executors via gas stipend** [Approx Vulnerability : MID]
Path key: `gas_capped_nat_transfer | executeMinting | Minting -> Transfers.transferNAT -> executor receive() reverts`
1. Contract executor's `receive()` legitimately consumes >100k gas (e.g. two ERC20 transfers + a NAT withdraw, per PoC).
2. Every `executeMinting` attempt by the executor reverts at "transfer failed".
3. Executor wastes gas per attempt; minting eventually completes via minter/agent call — with the fee again diverted to the agent pool. Executor's economics permanently broken.

#### Vulnerable Pattern Examples

**Example 1: gas-capped NAT transfer to arbitrary executor** [Approx Vulnerability : MID]
```solidity
// ❌ VULNERABLE: hardcoded 100k gas stipend for a recipient that may be an
// arbitrary contract; its receive() can easily exceed the cap
(bool success, ) = _recipient.call{value: _amount, gas: TRANSFER_GAS_ALLOWANCE}("");
```

**Example 2: fee skip when caller isn't the executor + donation to agent pool** [Approx Vulnerability : MID]
```solidity
// ❌ VULNERABLE: agent passes the permission check, so it can always force the
// "unclaimed" path and collect the executor's fee into its own pool
uint256 unclaimedExecutorFee = crt.executorFeeNatGWei * Conversion.GWEI;
if (msg.sender == crt.executor) {
    Transfers.transferNAT(crt.executor, unclaimedExecutorFee);
    unclaimedExecutorFee = 0;
}
CollateralReservations.distributeCollateralReservationFee(agent,
    crt.reservationFeeNatWei + unclaimedExecutorFee);
```

**Example 3: permissive permission disjunction enabling the front-run** [Approx Vulnerability : MID]
```solidity
// ❌ VULNERABLE (context): agent owner is an allowed caller AND the beneficiary
// of unclaimed fees — direct conflict of interest
require(msg.sender == crt.minter || msg.sender == crt.executor || Agents.isOwner(agent, msg.sender), ...);
```

### Impact Analysis

#### Technical Impact
- Executor fee state (`crt.executorFeeNatGWei`) silently reallocated to agent collateral pool on non-executor execution
- Contract executors permanently unable to execute mintings (revert at gas-capped transfer)
- Mempool-visible race between executor and agent for every minting execution

#### Business Impact
- Executor fee theft at scale (per-minting, repeatable, MEV-friendly front-run)
- Report classified: permanent freezing/loss of executor fees; unfair economic advantage to agents
- Discourages third-party executor bots, centralizing execution

#### Affected Scenarios
- FAssets mintings where users delegate execution to contract executor bots (the common pattern per [45904])
- Any executor with non-trivial `receive()` logic
- Compounds with 45904: failed executor txs extend the unproven-payment window agents can exploit for forced defaults

### Secure Implementation

**Fix 1: pull-based executor fee + remove agent windfall**
```solidity
// ✅ SECURE: executor fee becomes withdrawable by the executor (pull pattern),
// never donated to the agent; agent execution no longer captures the fee
if (msg.sender == crt.executor) {
    Transfers.transferNAT(crt.executor, unclaimedExecutorFee);  // keep push for EOAs/simple contracts
} else {
    executorFeeClaims[crt.executor] += unclaimedExecutorFee;    // accrue, no gas-capped call needed
    unclaimedExecutorFee = 0;
}
CollateralReservations.distributeCollateralReservationFee(agent, crt.reservationFeeNatWei);
// separately: allow executor to spend up to remaining tx gas (no fixed stipend)
// when it is the msg.sender calling executeMinting
```

### Detection Patterns

#### Contract / Call Graph Signals
```
- `.call{value: X, gas: CONSTANT}` to user-controlled addresses
- Fee/remainder branches that route value to a party who is also an allowed caller of the function
- Permission disjunctions mixing beneficiary roles (minter || executor || agent)
```

#### High-Signal Grep Seeds
```
- executeMinting
- transferNAT
- TRANSFER_GAS_ALLOWANCE
- unclaimedExecutorFee
- executorFeeNatGWei
- distributeCollateralReservationFee
```

#### Code Patterns to Look For
```
- Pattern 1: hardcoded gas stipends on NAT/ETH pushes to arbitrary contracts
- Pattern 2: "unclaimed" fee reallocation to a privileged caller's own pool
- Pattern 3: executor fee claimed only when msg.sender == executor (race-sensitive push)
```

#### Audit Checklist
- [ ] Check every `call{gas: N}` recipient class — can it be an arbitrary contract?
- [ ] For each fee, trace where it lands on every allowed caller path (minter/executor/agent)
- [ ] Verify no allowed caller profits from another caller's failure

### Real-World Examples

#### Known Exploits
- **Flare FAssets (audit finding, not exploited on mainnet)** - Immunefi Audit Comp May 2025 - Report #45447
  - Link: https://reports.immunefi.com/flare-fassets-or-mainnet-audit-comp/45447-sc-medium-executor-cannot-execute-minting-while-the-agent-can-execute-the-transaction-and-stea.md
  - Root cause: 100k gas cap on executor fee push + unclaimed fee donated to agent's collateral pool

### Prevention Guidelines

#### Development Best Practices
1. Prefer pull (withdrawal) patterns for fees to arbitrary contracts
2. Never route unclaimed fees to a party that can itself trigger the unclaimed path
3. When the recipient is the tx sender, forward all available gas rather than a fixed stipend

#### Testing Requirements
- Unit tests: gas-heavy `receive()` executor — executeMinting must not permanently brick
- Integration tests: agent front-run of executor tx — executor must still receive its fee
- Fuzzing: executor receive() gas consumption vs. stipend; fee routing across all three caller roles

### Keywords for Search

`flare`, `fassets`, `executeminting`, `transfernat`, `transfer_gas_allowance`, `executorfee`, `unclaimedexecutorfee`, `gas_griefing`, `gas_stipend`, `front_running`, `agent_fee_theft`, `collateralpool`, `distributecollateralreservationfee`, `pull_over_push`, `native_transfer_failure`, `mev`

### Related Vulnerabilities

- DB/unique/l1-misc/flare/fassets-minting-payment-default-forged-attestation.md (failed executor txs widen the window for forged defaults)
- DB/unique/l1-misc/flare/fassets-collateral-pool-unverified-reward-claim.md (same agent-vs-pool value-extraction cluster)
