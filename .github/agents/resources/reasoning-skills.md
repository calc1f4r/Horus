# Reasoning Skills for Vulnerability Discovery

> **Purpose**: Core reasoning framework for the `protocol-reasoning-agent`. Defines the assumption layers, state reachability analysis, domain-specific reasoning guides, cross-function patterns, iteration protocol, and confidence calibration.
> **Consumer**: `protocol-reasoning-agent` and its spawned domain sub-agents.

---

## Core Philosophy

This framework operates on **deep reasoning from root causes**, NOT pattern matching. The vulnerability database provides reasoning seeds — root cause descriptions that explain *why* a vulnerability class exists — which the agent uses to reason about whether the target code can reach vulnerable states.

The key distinction:

| Approach | Pattern Matching (invariant-catcher) | Reasoning (this agent) |
|----------|--------------------------------------|------------------------|
| Method | Keyword scan → template match → report | Decompose → reason about state reachability → prove/disprove |
| Strength | Fast, systematic, high recall | Deep, novel, handles emergent interactions |
| Weakness | Misses novel vulns, high false positives | Slower, requires careful domain modeling |
| DB Usage | Keywords + code patterns | Root causes + assumption layers |
| Output | Pattern-matched findings | Reasoning chains with reachability proofs |

---

## Assumption Layers

Every smart contract function operates under implicit assumptions. Vulnerabilities arise when assumptions are violated. Analyze each function through these 5 layers:

### Layer 1: Input Assumptions

What does the function assume about its inputs?

```
For each parameter:
  1. What range of values is expected?
  2. Is that range enforced by a require/assert/revert?
  3. What happens if the MINIMUM value is passed? (0, empty array, address(0))
  4. What happens if the MAXIMUM value is passed? (type(uint256).max, 2^255-1)
  5. What happens if a malicious contract address is passed?
  6. For arrays/bytes: what happens with length 0? Length 1? Length == limit?
```

**Reasoning template**: "Function `f(x)` assumes `x > 0` but there is no require check. If `x == 0`, then [trace execution path]. This leads to [division by zero / underflow / unexpected state]."

### Layer 2: State Assumptions

What does the function assume about the contract's current state?

```
For each state variable read:
  1. What value range is assumed?
  2. Can another function change this variable between the time it's read and used?
  3. Is the assumed relationship between state variables actually maintained?
  4. Can state be manipulated in the same transaction before this function runs?
  5. What if the state was initialized but never updated (stale)?
```

**Reasoning template**: "Function `f()` reads `totalSupply` assuming it equals `sum(balances)`. But `_mint()` updates `totalSupply` before updating `balances[recipient]`. In a reentrancy scenario, [trace the inconsistent state window]."

### Layer 3: Ordering Assumptions

What does the function assume about the order of operations?

```
For each multi-step process:
  1. Is there an assumed call order? (e.g., approve before transferFrom)
  2. Can the steps be called out of order?
  3. Can the steps be called by different actors?
  4. Can the steps be front-run or sandwiched?
  5. What if a step is repeated? (idempotency)
  6. What if a step is skipped? 
```

**Reasoning template**: "The protocol assumes `deposit → borrow → repay → withdraw` ordering. But nothing prevents `borrow` without prior `deposit` if the collateral check reads from a manipulable source. Specifically, [trace the ordering violation]."

### Layer 4: Economic Assumptions

What economic conditions does the function assume?

```
For price-dependent logic:
  1. What happens if the price doubles/halves in one block?
  2. Can flash loans amplify the attacker's position?
  3. Can liquidity changes affect the outcome?
  4. What happens at boundary conditions (price = 0, price = max)?
  5. Are fees/slippage/MEV considered?
  
For token logistics:
  1. What happens with fee-on-transfer tokens?
  2. What happens with rebasing tokens?
  3. What happens with tokens that have different decimals?
  4. What happens with tokens that return false instead of reverting?
```

**Reasoning template**: "The liquidation bonus assumes a stable price during the liquidation transaction. But an attacker can use a flash loan to temporarily crash the oracle price, trigger liquidation at a discount, then restore the price. Profit = [concrete calculation]."

### Layer 5: Environmental Assumptions

What does the function assume about the execution environment?

```
For EVM contracts:
  1. What if msg.sender is a contract (not EOA)?
  2. What if called via delegatecall?
  3. What if the chain has different block times or gas limits?
  4. What if block.timestamp is manipulated (within miner's range)?
  5. What if an upgrade changes the storage layout?

For Cosmos modules:
  1. What if the message comes from another module (not a user)?
  2. What if BeginBlocker/EndBlocker order changes?
  3. What if IBC timeout fires after state has changed?

For Solana programs:
  1. What if account ownership is wrong?
  2. What if the PDA derivation uses attacker-controlled seeds?
  3. What if CPI calls have unexpected side effects?
```

---

## State Reachability Analysis

For every potential vulnerability, you MUST prove that the vulnerable state is reachable. This is the core of reasoning-based analysis.

### The Reachability Proof Structure

```
CLAIM: State S_vulnerable is reachable from state S_init.

PROOF:
  Step 1: Start from S_init (contract deployment / known good state)
  Step 2: Actor A calls function f1(args) → state transitions to S_1
     WHY: f1 is externally callable, args are controllable, no access restriction
  Step 3: [In the same transaction OR next block] Actor B calls f2(args) → S_2
     WHY: f2 is externally callable, S_1 enables the call
  ...
  Step N: State is now S_vulnerable
     VERIFICATION: S_vulnerable violates invariant INV-X because [specific reason]
     IMPACT: This enables [concrete exploit] with [quantified damage]
```

### Recursive Depth for Complex Chains

For call chains longer than 3 steps, spawn a sub-agent to trace the full path:

```
COMPLEX CHAIN DETECTED:
  f1() → f2() → f3() → callback → f4() → f5()

SPAWN SUB-AGENT:
  "Trace the complete execution path from f1() to f5() in <path>.
   For each step, verify:
   1. Is the transition externally triggerable?
   2. Does the intermediate state enable the next step?
   3. Are there any reverts/guards that block the path?
   Report: either a complete proof OR the exact step that blocks the path."
```

### Disproving Reachability

If you CANNOT prove reachability, the finding is INVALID. Document why:

```
DISPROOF:
  The vulnerable state S_vulnerable requires totalBorrowed > totalDeposits.
  But:
  - borrow() has require(totalBorrowed + amount <= totalDeposits * LTV_RATIO)
  - No other function modifies totalBorrowed
  - The LTV_RATIO is immutable and < 100%
  THEREFORE: S_vulnerable is unreachable. Finding excluded.
```

---

## Domain-Specific Reasoning Guides

### DeFi / Financial Logic

Root cause seeds to reason about:
- **Invariant violation**: "Can any sequence of transactions break `assets >= liabilities`?"
- **Price manipulation**: "Can the price input be influenced by the caller in the same transaction?"
- **Flash loan amplification**: "Does any function's behavior scale with the caller's balance? Can that balance be temporarily inflated?"
- **Rounding exploitation**: "Do repeated operations accumulate rounding errors in one direction? Can an attacker control the direction?"
- **First depositor**: "What happens when totalSupply == 0 and the first deposit is tiny?"
- **Donation attack**: "Can sending tokens directly (not via deposit) break the share price calculation?"

### Access Control / Permissions

Root cause seeds:
- **Privilege escalation**: "Can a non-privileged actor reach a state that grants them privileges?"
- **Missing authorization**: "Which functions modify critical state but don't check msg.sender?"
- **Role confusion**: "Are there multiple admin roles? Can one role's actions undermine another?"
- **Initialization race**: "Can `initialize()` be called by anyone before the intended admin?"
- **Delegatecall context**: "Does any delegatecall preserve the caller's context unexpectedly?"

### Cross-Contract Interactions

Root cause seeds:
- **Reentrancy**: "Does any function make an external call before updating state? Trace the callback surface."
- **Return value**: "Are return values from external calls checked? What if they return false?"
- **Contract existence**: "What if the target address has no code? Does the call succeed silently?"
- **Composability**: "What if this protocol is composed with a malicious wrapper contract?"

### Oracle / Price Feeds

Root cause seeds:
- **Staleness**: "How old can the price data be before it's used? Is there a maximum age check?"
- **Manipulation**: "Can the oracle's price source be influenced in the same transaction? (TWAP window, spot price)"
- **Decimal mismatch**: "Do all price feeds use the same decimal precision? What happens on multiplication?"
- **Circuit breakers**: "What happens if the oracle returns 0 or an extreme value?"

### Bridge / Cross-Chain

Root cause seeds:
- **Message replay**: "Can a cross-chain message be delivered twice? Is there a nonce/hash check?"
- **Finality**: "What if the source chain reorganizes after the message is delivered?"
- **Trust boundary**: "Who can call the message receiver? Is it restricted to the bridge endpoint?"
- **Encoding mismatch**: "Do the source and destination encode/decode the payload identically?"

---

## Cross-Function Interaction Patterns

These patterns are where reasoning-based analysis excels over pattern matching.

### Pattern: State Window Exploitation

```
DETECT:
  Function A writes state variable X
  Function B reads state variable X
  Between A's write and B's read, there is an external call (to user code)

REASON:
  "During the external call, the attacker can call function B which reads X
   in its new state, but Y hasn't been updated yet. This creates an
   inconsistent view where X reflects the new state but Y reflects the old."
```

### Pattern: Cross-Function Invariant Breaking

```
DETECT:
  Invariant: X + Y == Z (maintained across all individual functions)
  Function A: updates X and Z atomically
  Function B: updates Y and Z atomically

REASON:
  "If A and B execute concurrently (or A calls B via callback),
   Z is updated twice independently. After both complete:
   X_new + Y_new != Z (because Z = Z_init + delta_A + delta_B,
   but it should be Z_init + delta_A OR Z_init + delta_B, not both)"
```

### Pattern: Implicit Dependency Chain

```
DETECT:
  Function C depends on the output of function B
  Function B depends on the output of function A
  A → B → C forms a chain, but the caller can skip B

REASON:
  "The protocol assumes the call sequence A → B → C. But C is externally
   callable and only checks its direct inputs (from B's output). If the
   caller provides crafted inputs directly to C, bypassing B's validation,
   then [trace what C does with invalid intermediate state]."
```

---

## Iteration Protocol

The reasoning agent performs 4 mandatory rounds, each with a different focus:

### Round 1: Standard Analysis (Per Domain)

Focus: Apply assumption layers to each function within its domain.

```
For each function in the domain:
  1. Enumerate all 5 assumption layers
  2. For each assumption, ask: "Can this be violated?"
  3. If yes, trace the violation to a concrete impact
  4. Produce findings with reachability proofs
```

### Round 2: Cross-Domain Analysis

Focus: Analyze interactions BETWEEN domains identified in Round 1.

```
For each pair of domains (D_i, D_j):
  1. What state does D_i export that D_j consumes?
  2. Can D_i put that state into a range that D_j doesn't expect?
  3. What happens if D_i's operation is sandwiched with D_j's?
  4. Are there shared state variables that both domains modify?
```

### Round 3: Edge Cases & Extremes

Focus: Boundary conditions, initialization, migration, and upgrade scenarios.

```
Test every function with:
  - All state variables at their minimum values (0, empty)
  - All state variables at their maximum values (type max)
  - First-time use (no prior state)
  - Post-migration state (variables partially initialized)
  - Maximum number of iterations (loop bounds)
  - Concurrent access from multiple actors
```

### Round 4: Completeness & Adversarial Review

Focus: What did we miss? Actively search for gaps.

```
For each invariant from 02-invariants.md:
  1. Is there a finding that could break this invariant?
  2. If not, explicitly prove why the invariant holds
  3. For any invariant that has NO finding AND NO proof, investigate deeper

For each CRITICAL/HIGH from Rounds 1-3:
  1. Are there RELATED vulnerabilities we missed?
  2. Can the same root cause manifest in a different function?
  3. What if the fix for this finding introduces a new issue?
```

---

## Confidence Calibration

### Finding Confidence Levels

| Level | Criteria | Action |
|-------|----------|--------|
| **PROVEN** | Complete reachability proof with concrete values | Include as HIGH confidence |
| **LIKELY** | Reachability proof with 1 uncertain step | Include as MEDIUM confidence, note the uncertainty |
| **POSSIBLE** | Reasoning suggests vulnerability but reachability unproven | Include as LOW confidence, mark for manual review |
| **SPECULATIVE** | Theoretical concern without concrete path | EXCLUDE from findings — add to "Areas for Manual Review" |

### Calibration Rules

1. **Never inflate confidence** — if you can't prove reachability, say so
2. **PROVEN requires concrete values** — "if amount is 0" is not enough; show the exact call sequence
3. **Economic findings require profit calculation** — attacker must net positive after gas + flash loan fees
4. **Cross-domain findings default to LIKELY** unless the full chain is traced
5. **Round 4 findings default to POSSIBLE** unless explicitly strengthened

### Root Cause Deduplication

Two findings share a root cause if fixing one prevents the other. Use these questions:

1. Is the same code line responsible for both?
2. Would the same `require()` statement prevent both?
3. Do they require the same precondition to exploit?

If YES to all 3 → merge into one finding (pick the higher severity, note both impacts).

---

## DB Root Cause Integration

When reading vulnerability patterns from the database, extract the **root cause** and use it as a reasoning seed — NOT as a template to match against.

### Extraction Process

```
1. Read the DB pattern's rootCause field from the manifest
2. Generalize it: "No freshness validation on oracle data" 
   → "Data consumed without freshness/validity check"
3. Apply the generalized seed to the target codebase:
   "Where does this codebase consume external data without validation?"
4. For each match, reason through the 5 assumption layers
5. Produce findings that may look NOTHING like the original DB pattern
```

### Example Transformation

```
DB Root Cause: "Missing staleness check on Chainlink latestRoundData()"
Generalized Seed: "External data consumed without temporal validation"

Applied to target code (which uses a custom oracle, not Chainlink):
  → "The protocol reads customOracle.getPrice() which returns a cached value.
     The cache is updated by an external keeper. There is no check on when
     the cache was last updated. If the keeper fails for 24 hours, the protocol
     uses a 24-hour-old price for liquidation calculations."

This finding would NEVER match the Chainlink keyword pattern, but the reasoning
from the DB root cause seed discovered it.
```
