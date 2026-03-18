<!-- AUTO-GENERATED from `.claude/resources/domain-decomposition.md`; source_sha256=9befac5b85684925ef4eefe2b448714e50f254173333a043d7bc7fbc8e185397 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/domain-decomposition.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Domain Decomposition Strategy

> **Purpose**: Defines how the `protocol-reasoning` agent decomposes a codebase into domains, assigns sub-agents, manages iteration rounds, and handles cross-domain reasoning.
> **Consumer**: `protocol-reasoning`.

---

## What is a Domain?

A **domain** is a cohesive group of contracts/functions that manage a single aspect of the protocol's business logic. Domains share internal state and have well-defined interfaces with other domains.

Examples:
- **Lending Domain**: deposit, withdraw, borrow, repay, interest accrual
- **Oracle Domain**: price feeds, TWAP calculation, fallback logic
- **Liquidation Domain**: health factor calculation, liquidation execution, incentives
- **Governance Domain**: proposals, voting, execution, timelocks

---

## Standard Domain Templates by Protocol Type

### Lending Protocol (`lending_protocol`)

| Domain | Contracts/Functions | Key State | Interfaces With |
|--------|-------------------|-----------|-----------------|
| **Core Lending** | deposit, withdraw, borrow, repay | balances, totalSupply, totalBorrowed | Oracle, Liquidation, Token |
| **Oracle** | getPrice, updatePrice, fallback | priceFeed, lastUpdated | Core Lending, Liquidation |
| **Liquidation** | liquidate, getHealthFactor | liquidationBonus, closeFactor | Core Lending, Oracle |
| **Interest Rate** | getRate, accrueInterest | rateModel, utilization | Core Lending |
| **Token/Shares** | mint, burn, transfer, convertToShares | totalShares, totalAssets | Core Lending |
| **Governance** | setParams, pause, unpause | admin, params | All |

### DEX / AMM (`dex_amm`)

| Domain | Contracts/Functions | Key State | Interfaces With |
|--------|-------------------|-----------|-----------------|
| **Pool Core** | swap, addLiquidity, removeLiquidity | reserves, totalLiquidity | Oracle, Fee, Token |
| **Fee** | calculateFee, collectProtocolFee | feeRate, protocolFees | Pool Core |
| **Oracle/TWAP** | observe, consult | observations, cardinality | Pool Core |
| **Position Mgmt** | mint, burn, collect (for CL) | positions, ticks | Pool Core, Fee |
| **Router** | exactInput, exactOutput, multicall | N/A (stateless) | Pool Core |
| **Governance** | setFee, whitelistPool | params, allowed | All |

### Vault / Yield (`vault_yield`)

| Domain | Contracts/Functions | Key State | Interfaces With |
|--------|-------------------|-----------|-----------------|
| **Vault Core** | deposit, withdraw, redeem | totalAssets, totalShares | Strategy, Token |
| **Strategy** | harvest, invest, divest | strategyBalance, lastHarvest | Vault Core, External |
| **Share Accounting** | convertToShares, convertToAssets | exchangeRate | Vault Core |
| **Fee** | managementFee, performanceFee | feeRecipient, feeRate | Vault Core, Strategy |
| **Governance** | setStrategy, migrate, pause | admin, pendingStrategy | All |

### Bridge / Cross-Chain (`cross_chain_bridge`)

| Domain | Contracts/Functions | Key State | Interfaces With |
|--------|-------------------|-----------|-----------------|
| **Message Send** | send, encode, estimateFee | nonce, pending | Endpoint |
| **Message Receive** | receive, decode, execute | executed, trusted | Endpoint, Execution |
| **Execution** | executePayload, retry | payloadHash, state | Message Receive |
| **Endpoint/Adapter** | lzReceive, _nonblockingReceive | trustedRemote | Message Send/Receive |
| **Token Lock/Mint** | lock, mint, burn, unlock | lockedAmount, minted | Message Send/Receive |

### Cosmos App-Chain (`cosmos_appchain`)

| Domain | Contracts/Functions | Key State | Interfaces With |
|--------|-------------------|-----------|-----------------|
| **Module Core** | MsgHandlers, Queries | KVStore state | Other Modules, IBC |
| **Staking** | Delegate, Undelegate, Redelegate | validators, delegations | Module Core, Slashing |
| **IBC** | OnRecvPacket, OnTimeout, OnAck | channels, sequences | Module Core, Relayer |
| **BeginBlock/EndBlock** | BeginBlocker, EndBlocker | epochState | Module Core, Staking |
| **Governance** | MsgSubmitProposal, MsgVote | proposals, votes | All |

### Solana Program (`solana_program`)

| Domain | Contracts/Functions | Key State | Interfaces With |
|--------|-------------------|-----------|-----------------|
| **Core Instructions** | process_instruction handlers | program accounts | Token, CPI |
| **Account Validation** | account checks, PDA derivation | seeds, bumps | Core Instructions |
| **CPI (Cross-Program)** | invoke, invoke_signed | target programs | External Programs |
| **Token Operations** | transfer, mint_to, burn | token accounts, mints | Core Instructions |
| **Authority** | authority checks, multi-sig | signers, owners | All |

---

## Domain Discovery Process

When the protocol type doesn't match a standard template, discover domains dynamically:

### Step 1: Contract Clustering

```
Read audit-output/01-context.md (Contract Inventory + State Variable Map)

For each pair of contracts (C_i, C_j):
  1. Do they share state variables? → Same domain
  2. Does C_i call C_j frequently? → Same or adjacent domains
  3. Do they serve the same business function? → Same domain
  4. Can they be understood independently? → Different domains
```

### Step 2: Function Grouping

```
For each contract:
  Group functions by:
  1. Which state variables they modify (writers to the same var → same group)
  2. Which external entry points they support (same user flow → same group)
  3. Which invariants they maintain (same invariant → same group)
```

### Step 3: Domain Boundary Identification

```
A domain boundary exists where:
  1. Trust level changes (untrusted input → trusted internal)
  2. Data format changes (raw bytes → structured, cross-chain encoded → decoded)
  3. Time domain changes (synchronous → asynchronous, same-block → multi-block)
  4. Actor changes (user-facing → admin-facing → keeper-facing)
```

---

## Sub-Agent Assignment Protocol

### One Sub-Agent Per Domain

Each domain gets exactly ONE sub-agent with a focused prompt:

```
DOMAIN SUB-AGENT PROMPT TEMPLATE:

You are analyzing the [DOMAIN_NAME] domain of a [PROTOCOL_TYPE] protocol.

TARGET CODEBASE: <path>
YOUR DOMAIN FILES:
  - <file1.ext> (functions: f1, f2, f3)
  - <file2.ext> (functions: f4, f5)

YOUR DOMAIN STATE:
  - <var1>: <type> (written by: f1, f3; read by: f2, f4, f5)
  - <var2>: <type> (written by: f2; read by: f1, f5)

INTERFACES WITH OTHER DOMAINS:
  - Oracle Domain: reads getPrice() — assume price can be stale or manipulated
  - Token Domain: calls transfer() — assume could be fee-on-transfer
  - [list all cross-domain calls]

REASONING SEEDS (from DB root causes):
  - <generalized root cause 1>
  - <generalized root cause 2>
  - <generalized root cause 3>

INVARIANTS TO TEST:
  - INV-X: <property> (from 02-invariants.md)
  - INV-Y: <property>

ROUND: [1|2|3|4] — [Standard|Cross-Domain|Edge Cases|Completeness]

YOUR TASK:
Apply the assumption layer analysis (Input, State, Ordering, Economic, Environmental)
from resources/reasoning-skills.md to every function in your domain.

For each potential vulnerability found:
1. State the violated assumption
2. Provide a COMPLETE reachability proof (step-by-step from init state)
3. Quantify the impact
4. Rate confidence: PROVEN / LIKELY / POSSIBLE

If you encounter a call chain > 3 steps deep, spawn a sub-agent to trace it.

Write findings using the Finding Schema from resources/inter-agent-data-format.md.
Return ALL findings as a structured list.
```

### Sub-Agent Recursion Rules

Sub-agents CAN spawn their own sub-agents, but with strict limits:

1. **Max recursion depth**: 2 (domain sub-agent → trace sub-agent → STOP)
2. **Trace sub-agents only** — recursive sub-agents may ONLY trace execution paths, not discover new domains
3. **Each trace sub-agent gets**: the specific call chain to trace + the question to answer
4. **Trace sub-agent returns**: either a PROOF (reachable) or DISPROOF (blocked at step N)

---

## Iteration Management

### 4 Mandatory Rounds

| Round | Focus | Sub-Agent Scope | Expected Output |
|-------|-------|-----------------|-----------------|
| 1 | Standard per-domain analysis | Each domain independently | Per-domain findings |
| 2 | Cross-domain interaction analysis | Domain pairs with shared state/interfaces | Cross-domain findings |
| 3 | Edge cases and boundary conditions | Each domain with extreme inputs/states | Edge case findings |
| 4 | Completeness check and adversarial review | All domains — what did we miss? | Gap findings + invariant proofs |

### Round Transitions

```
After Round N completes:
  1. Collect all findings from all domain sub-agents
  2. Deduplicate by root cause
  3. Feed Round N findings as context into Round N+1
  4. For Round 2: additionally provide cross-domain interface data
  5. For Round 3: additionally provide boundary value tables
  6. For Round 4: additionally provide invariant coverage gaps
```

### Convergence Criteria

Stop iterating (skip remaining rounds) if:
- **Round 1 produces 0 findings AND the protocol is trivially simple** (<5 functions)
- Otherwise, ALL 4 rounds are mandatory

### Cross-Domain Reasoning (Round 2 Specifics)

```
For each domain pair (D_i, D_j) that shares an interface:

  1. DATA FLOW: What data flows from D_i to D_j?
     - Can D_i send data that D_j's assumptions don't cover?
     - Is the data validated at the boundary?

  2. STATE COUPLING: Do D_i and D_j share state?
     - Can D_i modify state that breaks D_j's invariants?
     - Is the shared state updated atomically?

  3. TEMPORAL COUPLING: Do D_i and D_j have time dependencies?
     - Can D_i's operation be sandwiched with D_j's?
     - What if D_i completes but D_j hasn't started?

  4. TRUST MISMATCH: Do D_i and D_j have different trust models?
     - Can an untrusted actor in D_i influence trusted state in D_j?
```
