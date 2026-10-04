---
# Core Classification
protocol: snowbridge
chain: polkadot
category: bridge
vulnerability_type: fund_accounting_bypass
root_cause_family: missing_access_control

# Pattern Identity
pattern_key: unguarded-privileged-extrinsic | bridge Gateway/Agent accounting | permissionless registration or refund call | sovereign/relayer fund drain

# Interaction Scope
interaction_scope: multi_contract
involved_contracts:
  - Gateway.sol
  - BeefyClient.sol
  - Agent contracts (AssetHub agents)
  - inbound/outbound queues
path_keys:
  - unguarded-privileged-extrinsic | create_agent | permissionless spam -> ordered-channel DoS | relayer-fund drain
  - unguarded-privileged-extrinsic | registerToken | uncovered AssetHub deposit | sovereign-fund drain
  - unguarded-privileged-extrinsic | transferNativeFromAgent | unrestricted caller | Agent asset exfiltration
  - unguarded-privileged-extrinsic | BeefyClient submit | replicated prevRandao tickets | randomness redraw

# Attack Vector Details
attack_type: access_control_bypass
affected_component: bridge fund custody and message submission (Gateway, BeefyClient, agents)

# Technical Primitives
primitives:
  - create_agent
  - registerToken
  - transferNativeFromAgent
  - submit
  - BeefyClient
  - prevRandao
  - ordered_channel
  - inbound_queue
  - agent_fund_accounting
  - multi_asset_deposits

# Grep / Hunt-Card Seeds
code_keywords:
  - create_agent
  - registerToken
  - transferNativeFromAgent
  - submit
  - BeefyClient
  - prevRandao
  - Gateway
  - inboundQueue

severity: critical
impact: fund_loss
language: rust
tags:
  - substrate
  - bridge
  - snowbridge
  - access_control
  - ethereum
  - beefy
---

## References & Source Reports

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [sb1] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | CRITICAL | Oak Security | #1 relayer-fund drain via permissionless `create_agent` spam (ordered-channel DoS) |
| [sb2] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | CRITICAL | Oak Security | #2 sovereign-fund drain via `registerToken` (uncovered 10 DOT AssetHub deposit, `Gateway.sol:418-424`) |
| [sb3] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | CRITICAL | Oak Security | #3 `submit` always returns Ok → stuck Agent funds |
| [sb6] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | MAJOR | Oak Security | #6 unrestricted `transferNativeFromAgent` (`Gateway.sol:400-412`) |
| [sb7] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | MAJOR | Oak Security | #7 BeefyClient prevRandao redraw via replicated tickets (`BeefyClient.sol:231-290`) |
| [sb8] | reports/substrate-l1_findings/snowbridge-oak-v1-1.md | MAJOR | Oak Security | #8 corrupted messages skipped |
| [sbx] | reports/substrate-l1_findings/snowbridge-oak-ext-v1-1.md | MAJOR | Oak Security | Snowbridge extension audit v1.1 (follow-up findings on Gateway/queues) |

## Unguarded Gateway Extrinsics Drain Relayer and Sovereign Bridge Funds

**Snowbridge's Ethereum-side Gateway exposes fund-custody operations (`create_agent`, `registerToken`, `transferNativeFromAgent`, `submit`) with missing or wrong access control and unrefunded deposits, enabling direct relayer/sovereign fund drains, stuck agent funds, and randomness redraws** - representative of bridges where accounting-critical registration/refund calls are permissionless or mis-gated.

### Overview

Oak Security's 2024 Snowbridge audits found three Criticals: #1 permissionless `create_agent` spam exhausts relayer funds through ordered-channel DoS; #2 `registerToken` lets anyone trigger an uncovered 10 DOT AssetHub deposit, draining sovereign funds; #3 `submit` always returning Ok strands Agent funds. Majors: #6 unrestricted `transferNativeFromAgent` (`Gateway.sol:400-412`), #7 BeefyClient prevRandao redraw via replicated tickets (`BeefyClient.sol:231-290`), #8 corrupted messages silently skipped.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because Gateway functions that move or commit bridge funds either lack origin checks, fail to refund/charge deposits correctly, or swallow errors, so any caller can convert bridge liveness/custody operations into fund loss."
- Pattern key: `unguarded-privileged-extrinsic | bridge Gateway/Agent accounting | permissionless registration or refund call | sovereign/relayer fund drain`
- Interaction scope: `multi_contract`
- Primary affected component(s): `Gateway.sol (registration/refund paths), BeefyClient.sol (commit/randomness), agents, message queues`
- Contracts / modules involved: `Gateway.sol, BeefyClient.sol, AssetHub agents, inbound/outbound queues`
- Path keys: `create_agent spam`, `registerToken uncovered deposit`, `transferNativeFromAgent unrestricted`, `prevRandao redraw`
- High-signal code keywords: `create_agent, registerToken, transferNativeFromAgent, submit, BeefyClient, prevRandao`
- Typical sink / impact: `relayer fund drain / sovereign fund drain / stuck agent funds / randomness manipulation`
- Validation strength: `strong` (professional audit, multiple Criticals confirmed by auditor)

#### Contract / Boundary Map

- Entry surface(s): `create_agent()`, `registerToken()` (`Gateway.sol:418-424`), `transferNativeFromAgent()` (`Gateway.sol:400-412`), `submit()` on BeefyClient (`BeefyClient.sol:231-290`)
- Contract hop(s): `Gateway -> Agent (AssetHub)`, `Gateway -> inbound queue -> BeefyClient`, `submit -> prevRandao ticket pool`
- Trust boundary crossed: `Ethereum <-> Polkadot bridge boundary; relayer/governance vs public caller boundary`
- Shared state or sync assumption: `agent balances must cover queued operations; Beefy commitments must be unique per block/randomness draw`

#### Valid Bug Signals

- Signal 1: A registration function (`create_agent`, `registerToken`) callable by any address whose downstream cost (agent creation on AssetHub, 10 DOT deposit) is paid from communal relayer/sovereign funds rather than the caller ([sb1], [sb2]).
- Signal 2: A custody-transfer function (`transferNativeFromAgent`) with no caller restriction moving native funds out of an Agent ([sb6], `Gateway.sol:400-412`).
- Signal 3: A submission path that returns Ok even on failure, so failed messages strand the Agent funds they carried ([sb3]).
- Signal 4: Randomness/commit tickets keyed on values an attacker can replicate (prevRandao), allowing redraws ([sb7], `BeefyClient.sol:231-290`).

#### False Positive Guards

- Not this bug when: registration is gated by governance/owner origin AND the deposit is charged to and refundable by the caller.
- Safe if: agent creation is rate-limited, deposit-gated, and the ordered channel cannot be spammed below the relayer's funding.
- Requires attacker control of: any Ethereum address (permissionless calls) — no special role needed for #1/#2/#3.
- Note severity context: these are 2024 audit findings; verify fix status in the deployed Gateway revision before reporting as live.

### Vulnerability Description

#### Root Cause

The Gateway treats several fund-committing operations as if they were protected when they are public. `create_agent` is permissionless, and each spam call forces agent-creation work whose cost lands on relayers via the ordered channel ([sb1]). `registerToken` triggers a fixed 10 DOT deposit on AssetHub that is not covered by the caller — repeated calls drain sovereign funds ([sb2], `Gateway.sol:418-424`). `submit` cannot fail (always Ok), so agents keep funds for messages that never processed ([sb3]). `transferNativeFromAgent` has no caller gate ([sb6], `Gateway.sol:400-412`). BeefyClient accepts replicated prevRandao tickets, letting an attacker re-roll randomness selections ([sb7], `BeefyClient.sol:231-290`), and corrupted messages are skipped rather than reverted ([sb8]).

#### Attack Scenario / Path Variants

**Path A: Relayer-fund drain via create_agent spam**
Path key: `unguarded-privileged-extrinsic | create_agent | permissionless spam -> ordered-channel DoS | relayer-fund drain`
Entry surface: `create_agent()`
Contracts touched: `Gateway -> ordered channel -> AssetHub agent creation`
Boundary crossed: Ethereum-to-Polkadot message channel
1. Attacker calls `create_agent` in a loop for garbage token addresses.
2. Each call enqueues agent-creation messages into the ordered channel; relayers must deliver (and pay for) them all.
3. Channel congestion/DoS exhausts relayer funds; legitimate bridging stalls.

**Path B: Sovereign-fund drain via registerToken**
Path key: `unguarded-privileged-extrinsic | registerToken | uncovered AssetHub deposit | sovereign-fund drain`
Entry surface: `registerToken()` (`Gateway.sol:418-424`)
Contracts touched: `Gateway -> AssetHub sovereign account`
1. Attacker calls `registerToken` for arbitrary tokens.
2. Each registration consumes an uncovered fixed 10 DOT deposit from sovereign funds on AssetHub.
3. Repeated calls bleed sovereign treasury until exhausted.

**Path C: Agent fund exfiltration / stuck funds**
Path key: `unguarded-privileged-extrinsic | transferNativeFromAgent / submit | unrestricted or never-failing call | Agent asset loss or lock`
Entry surface: `transferNativeFromAgent()` (`Gateway.sol:400-412`), `submit()`
1. Attacker invokes `transferNativeFromAgent` without any allowed-caller check and moves native assets out of the Agent.
2. Separately, messages submitted via `submit` that fail downstream still return Ok — the Agent's escrowed funds for those messages are never returned.
3. Combined: direct exfiltration + permanent lock of agent balances.

**Path D: BeefyClient randomness redraw**
Path key: `unguarded-privileged-extrinsic | BeefyClient submit | replicated prevRandao tickets | randomness redraw`
Entry surface: `submit()` (`BeefyClient.sol:231-290`)
1. Attacker replicates prevRandao-based tickets across commitments.
2. The client's uniqueness/randomness assumptions break; selections can be re-rolled.
3. Downstream randomness-dependent bridge logic is biased.

#### Vulnerable Pattern Examples

**Example 1: Unrestricted transferNativeFromAgent (from [sb6])** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: Gateway.sol:400-412 — no caller gate on custody transfer
function transferNativeFromAgent(uint256 amount, address to, address refund) external {
    // MISSING: require(msg.sender == authorizedExecutor || governance);
    IAgent(agent).transferNative(amount, to, refund); // anyone drains Agent native balance
}
```

**Example 2: registerToken with uncovered sovereign deposit (from [sb2])** [Approx Vulnerability : CRITICAL]
```solidity
// ❌ VULNERABLE: Gateway.sol:418-424 — public registration, communal deposit
function registerToken(address token) external {
    // no msg.sender fee covering the 10 DOT AssetHub creation deposit
    outbound.send(RegisterToken{token: token}); // sovereign account eats 10 DOT per call
}
```

**Example 3: submit always succeeds (from [sb3])** [Approx Vulnerability : CRITICAL]
```solidity
// ❌ VULNERABLE: failure path returns Ok — agent funds never refunded
function submit(Message[] calldata msgs) external returns (bool) {
    for (uint i; i < msgs.length; ++i) {
        _dispatch(msgs[i]); // errors swallowed / deferred
    }
    return true; // always Ok → failed messages strand the funds their Agent escrowed
}
```

**Example 4: Replicated prevRandao tickets (from [sb7])** [Approx Vulnerability : HIGH]
```solidity
// ❌ VULNERABLE: BeefyClient.sol:231-290 — ticket uniqueness not enforced on prevRandao
function submit(bytes32 commitment) external {
    uint256 ticket = block.prevrandao; // attacker replicates tickets across blocks/commits
    tickets.push(ticket);              // no per-commitment uniqueness check → redraw
}
```

### Impact Analysis

#### Technical Impact

- Three distinct fund-loss sinks: relayer funds (spam-forced delivery costs), sovereign funds (uncovered deposits), agent escrow (exfiltration + stranded funds).
- Ordered-channel DoS degrades the entire bridge's liveness ([sb1]); corrupted-message skipping silently breaks delivery guarantees ([sb8]).
- Randomness redraw undermines any BeefyClient selection logic ([sb7]).

#### Business Impact

- Critical-rated: direct drains of communal bridge funds by any Ethereum address; for a sovereign bridge between Polkadot and Ethereum this is worst-case custody failure.

#### Affected Scenarios

- Any bridge whose registration/creation calls consume communal funds without caller-paid deposits.
- Custody-transfer functions lacking executor/governance gating.
- Commit/submission APIs that cannot fail (always-Ok) over escrowed funds.

### Secure Implementation

**Fix 1: Gate custody and registration calls; make callers pay**
```solidity
// ✅ SECURE: access control + caller-covered deposits (per Oak recommendations)
function registerToken(address token) external {
    uint256 fee = agentCreationCost();          // e.g. 10 DOT equivalent
    IERC20(DOT).transferFrom(msg.sender, address(this), fee); // caller pays
    outbound.send(RegisterToken{token: token});
}

function transferNativeFromAgent(uint256 amount, address to, address refund) external {
    require(hasRole(EXECUTOR_ROLE, msg.sender), "unauthorized"); // origin gate
    IAgent(agent).transferNative(amount, to, refund);
}
```

**Fix 2: Fail loudly and enforce ticket uniqueness**
```solidity
// ✅ SECURE: propagate failures; bind randomness tickets to commitments
function submit(Message[] calldata msgs) external returns (bool) {
    for (uint i; i < msgs.length; ++i) {
        _dispatch(msgs[i]); // reverts bubble up; agent funds refunded on revert
    }
    return true;
}

function submitCommitment(bytes32 commitment) external {
    uint256 ticket = uint256(keccak256(abi.encode(block.prevrandao, commitment))); // unique per commitment
    require(!usedTickets[ticket], "ticket replay");
    usedTickets[ticket] = true;
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- create_agent
- registerToken
- transferNativeFromAgent
- submit
- BeefyClient
- prevRandao
- inboundQueue
```

#### Code Patterns to Look For
```
- Pattern 1: public/external registration functions whose downstream cost is paid by communal accounts (sovereign/relayer)
- Pattern 2: custody-transfer functions without role checks (transferNative*, withdraw*, refund*)
- Pattern 3: dispatch loops that swallow per-message errors over escrowed funds
- Pattern 4: randomness derived solely from block.prevrandao without commitment binding
```

#### Audit Checklist
- [ ] Who pays for agent/token registration on the destination chain — caller or communal funds?
- [ ] Can any address move funds out of an Agent or the Gateway?
- [ ] Can submission paths return success while messages failed (funds stranded)?
- [ ] Are Beefy/prevRandao tickets unique and bound to a single commitment?

### Keywords for Search

`Snowbridge`, `Gateway`, `create_agent`, `registerToken`, `transferNativeFromAgent`, `BeefyClient`, `prevRandao`, `relayer fund drain`, `sovereign fund drain`, `ordered channel DoS`, `agent escrow`, `stuck bridge funds`, `bridge accounting`, `Ethereum Polkadot bridge`, `message queue corruption`, `Oak Security`

### Related Vulnerabilities

- DB/substrate/bridges/grandpa-light-client-validation.md (consensus light-client validation)
- DB/substrate/pallets/origin-authorization-bypass.md (ungated privileged extrinsics in pallets)
- DB/substrate/lifecycle/runtime-upgrade-storage-migration.md (Snowbridge Gateway upgrade token loss)
