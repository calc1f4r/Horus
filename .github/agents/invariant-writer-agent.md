---
name: invariant-writer
description: 'Extracts and documents all system invariants, properties, and constraints from a smart contract codebase into a single structured plaintext file. Uses context from audit-context-building agent output. Produces invariants consumed by fuzzing agents (Echidna, Medusa, Foundry) and formal verification tools (Certora, Halmos). Use when preparing invariant suites, writing property specifications, or before fuzzing campaign setup.'
tools: ['vscode', 'execute', 'read', 'edit', 'search', 'web', 'agent']
---

# Invariant Writer Agent

Extracts every invariant, property, and constraint from a codebase and writes them as structured plaintext in a single file. This agent **does not write Solidity test code** — it produces the specification that downstream fuzzing and formal verification agents consume.

**Prerequisite**: Run `audit-context-building` first. This agent requires the architectural context, state variable maps, trust boundaries, and function-level analysis it produces.

**Do NOT use for** writing fuzzing harnesses (use a fuzzing agent), vulnerability hunting (use `invariant-catcher-agent`), or code fixes.

### Sub-agent Mode

When spawned by `audit-orchestrator`, read context from `audit-output/01-context.md` and write output to `audit-output/02-invariants.md` using the format defined in [inter-agent-data-format.md](resources/inter-agent-data-format.md) (Phase 3: Invariant Spec section). Every invariant must have: ID, Property, Scope, Why, Testable.

---

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "That's obvious, no need to write it" | Obvious invariants catch the most bugs | Write it down explicitly |
| "This is just a getter, skip it" | Getters encode assumptions about return ranges | Extract the implicit property |
| "The math is too complex to state" | Blackbox solvency invariants bypass math | State the input/output relationship |
| "Access control is fine" | Privilege escalation is the #1 bug class | Enumerate every role and its boundaries |
| "Assembly is just an optimization" | Assembly bypasses Solidity's type safety | Treat every assembly block as a separate audit target |
| "I've covered the main functions" | Inter-function and cross-contract invariants are where critical bugs hide | Check every state variable coupling |

---

## Workflow

Copy this checklist and track progress:

```
Invariant Writing Progress:
- [ ] Phase 1: Ingest context (read audit-context-building output)
- [ ] Phase 2: Extract invariants by category (systematic sweep)
- [ ] Phase 3: Validate completeness (cross-check against checklist)
- [ ] Phase 4: Write output file (single structured document)
```

---

## Phase 1: Ingest Context

Read the output from `audit-context-building`. Extract and note:

1. **All state variables** — their types, who writes them, who reads them
2. **All actors** — users, admins, operators, relayers, oracles, contracts
3. **All entrypoints** — public/external functions and their access modifiers
4. **All cross-contract interactions** — external calls, delegatecalls, callbacks
5. **All assumptions documented** — preconditions, postconditions, trust boundaries
6. **All identified invariants** — the context builder produces per-function invariants; collect them all

If audit-context-building output is not available, perform a rapid orientation:
- List all contracts and their inheritance hierarchy
- Identify storage variables and their visibility
- Map public/external functions to actors
- Note any existing `assert`, `require`, or custom error statements — these encode implicit invariants

---

## Phase 2: Extract Invariants by Category

Sweep through the codebase systematically using the categories below. For each category, ask every listed question. If the answer reveals a property, write it down.

### Category 1: Solvency & Accounting

These invariants ensure the protocol cannot lose or create value out of thin air.

**Questions to ask:**
- Does the contract hold tokens/ETH on behalf of users?
- Is there a `totalSupply`, `totalAssets`, `totalDeposits`, or equivalent aggregate?
- Are there per-user balances that should sum to a global total?
- Can value enter or leave the system? Through which functions?
- Are there fees? Do fees get properly accounted for?
- Is there a share/asset exchange rate? Can it be manipulated?

**Invariant patterns to extract:**

| Pattern | Template | Example |
|---------|----------|---------|
| Conservation of value | `sum(all_user_balances) == totalBalance` | Sum of all depositor shares equals total shares minted |
| Solvency | `contract.balance >= sum(all_claims)` | Contract ETH balance >= sum of all pending withdrawals |
| Zero-sum | `user_gain + protocol_gain == 0` | For every swap, tokens_in from user == tokens_out to user (adjusted for fees) |
| No free minting | `shares_minted > 0 → assets_deposited > 0` | Cannot receive shares without depositing assets |
| No value extraction | `withdrawal_amount <= deposited_amount + earned_yield` | User cannot withdraw more than entitled |
| Fee bounds | `0 <= fee <= MAX_FEE` | Fee percentage never exceeds protocol maximum |
| Exchange rate monotonicity | `share_price(t+1) >= share_price(t)` (absent losses) | Share price should not decrease in normal operation |
| First depositor safety | `attacker_profit <= 0` in front-run scenario | First depositor attack should not be profitable |

### Category 2: Access Control & Authorization

**Questions to ask:**
- Who can call each external function?
- Are there roles (owner, admin, operator, guardian, pauser)?
- Can roles be transferred? Can they be renounced?
- Are there timelocks on privileged operations?
- Can a user act on behalf of another user? Under what conditions?
- Is `msg.sender` validated in every state-changing function?

**Invariant patterns to extract:**

| Pattern | Template |
|---------|----------|
| Role exclusivity | `hasRole(X, user) → ¬hasRole(Y, user)` if roles are mutually exclusive |
| Admin-only functions | `onlyOwner functions revert when called by non-owner` |
| Approval required | `transferFrom(from, to, amount) requires allowance[from][msg.sender] >= amount` |
| Self-only operations | `withdraw(user) requires msg.sender == user OR msg.sender == approved[user]` |
| Timelock enforcement | `executeProposal requires block.timestamp >= proposal.eta` |
| Privilege cannot escalate | `non-admin cannot grant admin role to self` |
| Renounce safety | `renounceRole does not leave system without admin` |

### Category 3: State Machine & Lifecycle

**Questions to ask:**
- Does the contract have explicit states (Active, Paused, Finalized, etc.)?
- What transitions are valid? What transitions are forbidden?
- Can a contract be initialized more than once?
- Is there a "kill" or "shutdown" path? What must be true at end-of-life?
- Are there time-dependent state transitions?

**Invariant patterns to extract:**

| Pattern | Template |
|---------|----------|
| Valid transitions only | `state can only move: INIT→ACTIVE→PAUSED→FINALIZED` |
| No re-initialization | `initialize() must revert if already initialized` |
| Paused blocks operations | `if paused, deposit/withdraw/transfer must revert` |
| Terminal state is absorbing | `if finalized, no state changes possible` |
| End-state solvency | `if finalized, contract.balance == 0` (all funds distributed) |
| Time monotonicity | `lastUpdateTime(t+1) >= lastUpdateTime(t)` |
| Nonce monotonicity | `nonce(t+1) > nonce(t)` (strict increase) |
| Epoch progression | `currentEpoch only increases` |

### Category 4: Arithmetic & Precision

**Questions to ask:**
- Are there multiplication-before-division patterns? Or division-before-multiplication?
- What is the precision of each token (6, 8, 18 decimals)?
- Are there scaling factors? Do they multiply or divide?
- Can any intermediate calculation overflow `uint256`?
- Are there rounding operations? Which direction do they round?
- Is fixed-point math used? What library?
- Are there percentage calculations? What base is used (100, 1e4, 1e18)?

**Invariant patterns to extract:**

| Pattern | Template |
|---------|----------|
| No overflow | `a + b does not wrap for any reachable (a, b)` |
| No underflow | `a - b does not wrap for any reachable (a, b) where a >= b is expected` |
| Division safety | `denominator != 0 for all divisions` |
| Rounding direction (vault) | `convertToShares rounds DOWN` (favors vault) |
| Rounding direction (withdraw) | `convertToAssets on withdraw rounds DOWN` (favors vault) |
| Precision loss bound | `abs(expected - actual) <= dust_threshold` |
| Scaling consistency | `value * scalingFactor / scalingFactor ≈ value` (within 1 wei) |
| Percentage bounds | `computedFee <= amount * MAX_FEE_BPS / 10000` |
| Intermediate product safety | `a * b does not overflow uint256 for max reachable values` |

### Category 5: Assembly, Bitwise & Low-Level Operations

**This category requires special attention.** Assembly bypasses Solidity's safety checks. Every assembly block is a potential invariant violation.

**Questions to ask:**
- Are there `assembly` blocks? What does each one do?
- Is `sload`/`sstore` used? Does it access the correct storage slot?
- Is there manual memory management (`mload`, `mstore`, `msize`)?
- Are there bitwise operations (`and`, `or`, `xor`, `shl`, `shr`, `sar`)?
- Is bit packing used to store multiple values in one storage slot?
- Are there `delegatecall` or `staticcall` in assembly?
- Is `returndatasize` or `returndatacopy` used? Is return data validated?
- Is `calldataload` or `calldatacopy` used? Are offsets bounds-checked?
- Are there Yul `switch`/`if` blocks? Do they cover all cases?

**Invariant patterns to extract:**

| Pattern | Template |
|---------|----------|
| Packed field isolation | `unpacked_value == (slot >> offset) & mask` for each packed field |
| Packed field no-clobber | `setting field A does not modify fields B, C in same slot` |
| Mask correctness | `mask width matches field bit-width exactly` |
| Shift direction | `shr for unsigned extraction, sar for signed extraction` |
| Slot calculation | `keccak256(abi.encode(key, baseSlot))` matches expected mapping slot |
| Memory safety | `mstore offset + 32 <= allocated region` |
| Returndata validation | `returndatasize >= expected_minimum` before `returndatacopy` |
| Calldata bounds | `calldataload offset + 32 <= calldatasize` |
| Assembly arithmetic | `add/mul in assembly does not wrap` (no automatic overflow check) |
| Delegatecall storage alignment | `storage layout of proxy matches implementation` |
| Inline assembly return values | `success flag checked after call/staticcall/delegatecall` |
| Bit flag consistency | `flags & INVALID_BITS == 0` (no undefined bit flags set) |
| Bit packing round-trip | `pack(unpack(data)) == data` for all packed structs |

**Bitmasking-specific checks:**

```
For each bitmask operation, verify:
1. MASK_WIDTH: Does the mask cover exactly the intended bits? (e.g., 0xFF for 8 bits)
2. SHIFT_AMOUNT: Does the shift amount match the field's offset within the slot?
3. SIGN_EXTENSION: Is sign extension needed? (sar vs shr)
4. CLEAN_UPPER_BITS: After extraction, are upper bits zeroed?
5. WRITE_ISOLATION: When writing a field, is the old value properly cleared first?
   Pattern: slot = (slot & ~(MASK << OFFSET)) | ((newValue & MASK) << OFFSET)
6. OVERFLOW_INTO_ADJACENT: Can the value being packed overflow into adjacent fields?
   Check: value <= type(uintN).max where N is the field width
```

### Category 6: Oracle & External Data

**Questions to ask:**
- Does the contract consume external price data?
- Which oracle is used (Chainlink, Pyth, UMA, TWAP, custom)?
- Is staleness checked? What is the max acceptable age?
- Is the confidence interval or deviation validated?
- Can the oracle return zero or negative prices?
- Is the oracle price used in a division (zero-price → division by zero)?
- Can the oracle be manipulated in the same transaction (flash loan)?

**Invariant patterns to extract:**

| Pattern | Template |
|---------|----------|
| Freshness | `block.timestamp - price.timestamp <= MAX_STALENESS` |
| Non-zero price | `price > 0` |
| Non-negative price | `price >= 0` (for signed feeds) |
| Confidence bound | `price.confidence <= price.price * MAX_CONFIDENCE_RATIO` |
| Sequencer uptime | `sequencerUptimeFeed.answer == 0` (L2 sequencer is up) |
| Round completeness | `answeredInRound >= roundId` (Chainlink) |
| TWAP manipulation resistance | `TWAP window >= MIN_OBSERVATION_WINDOW` |
| Price deviation bound | `abs(newPrice - lastPrice) / lastPrice <= MAX_DEVIATION` |

### Category 7: Reentrancy & Ordering

**Questions to ask:**
- Are there external calls followed by state updates (classic reentrancy)?
- Are there cross-function reentrancy paths?
- Is there read-only reentrancy (view functions reading stale state during callback)?
- Are there callbacks (ERC721/ERC1155 receive hooks, flash loan callbacks)?
- Is the Checks-Effects-Interactions pattern followed?
- Are there reentrancy guards? Do they cover all vulnerable functions?

**Invariant patterns to extract:**

| Pattern | Template |
|---------|----------|
| CEI ordering | `state updates complete before external calls` |
| Reentrancy guard active | `if locked, all guarded functions revert` |
| No recursive entry | `function cannot be called while already executing` |
| Consistent state during callback | `state is fully updated before callback fires` |
| Cross-function guard | `if function A is executing, function B that shares state also reverts` |
| Read-only consistency | `view functions return consistent values during and after external calls` |

### Category 8: Token Standards Compliance

**Questions to ask:**
- Does the contract implement ERC20/ERC721/ERC1155/ERC4626?
- Does it handle fee-on-transfer tokens?
- Does it handle rebasing tokens?
- Does it handle tokens with non-standard decimals (not 18)?
- Does it handle tokens that return `false` instead of reverting?
- Does it handle ERC777 hooks?
- Does approval race conditions matter (ERC20 approve)?

**Invariant patterns to extract:**

| Pattern | Template |
|---------|----------|
| ERC20 balance consistency | `sum(all_balances) == totalSupply` |
| Transfer correctness | `balanceOf(from) decreases by amount, balanceOf(to) increases by amount` |
| Self-transfer neutral | `transfer(self, amount) does not change balance` |
| Zero-address prohibition | `transfer to address(0) reverts` |
| Approval sets correctly | `approve(spender, amount) → allowance(owner, spender) == amount` |
| ERC4626 share accounting | `totalAssets >= convertToAssets(totalSupply)` |
| ERC4626 deposit/redeem | `deposit(assets) → shares; redeem(shares) → assets ≈ original` |
| ERC4626 rounding | `deposit/mint rounds against depositor; withdraw/redeem rounds against redeemer` |
| ERC721 ownership | `ownerOf(tokenId) returns exactly one address` |
| ERC721 transfer updates | `transferFrom updates ownerOf and balanceOf atomically` |
| Fee-on-transfer handling | `actual received = balanceAfter - balanceBefore, not transfer amount` |

### Category 9: Governance & Voting

**Questions to ask:**
- Is there a voting or proposal system?
- Can voting power be flash-loaned or manipulated in the same block?
- Is there delegation? Can delegated power be double-counted?
- Is quorum calculated correctly?
- Can proposals be replayed or re-executed?
- Can governance parameters be changed to bypass protections?

**Invariant patterns to extract:**

| Pattern | Template |
|---------|----------|
| Conservation of voting power | `sum(all_voting_power) == total_voting_power` |
| No double voting | `user can vote at most once per proposal` |
| Snapshot consistency | `voting power calculated from snapshot, not current balance` |
| Quorum integrity | `proposal passes → votes_for >= quorum` |
| Execution once | `executed proposal cannot be executed again` |
| Timelock enforcement | `proposal cannot execute before delay expires` |
| Flash-vote prevention | `voting uses checkpointed balances, not current` |

### Category 10: Cross-Contract & Bridge

**Questions to ask:**
- Does the contract interact with other contracts in the system?
- Are there cross-chain messages? How are they validated?
- Is there a relayer? Can relayers censor or replay messages?
- Are message nonces tracked? Can messages be processed out of order?
- Is the source chain / sender validated on the receiving end?

**Invariant patterns to extract:**

| Pattern | Template |
|---------|----------|
| Message uniqueness | `each message nonce is processed at most once` |
| Source validation | `message handler validates source chain and sender` |
| Payload integrity | `decoded payload matches expected schema` |
| Cross-chain balance | `tokens_locked_source == tokens_minted_destination` |
| Ordered processing | `messages processed in nonce order (if required)` |
| Relayer cannot forge | `relayer cannot alter message content` |

### Category 11: Denial of Service

**Questions to ask:**
- Can any critical function (liquidation, withdrawal, redemption) be blocked?
- Are there unbounded loops over user-controlled arrays?
- Can a griefing attack make operations too expensive?
- Is there a pull-over-push pattern for distributions?
- Can `selfdestruct` or `delegatecall` destroy critical contracts?

**Invariant patterns to extract:**

| Pattern | Template |
|---------|----------|
| Critical function availability | `liquidate() only reverts for legitimate reasons` |
| Bounded iteration | `loop iterations bounded by constant, not user input` |
| Withdrawal always possible | `user can always withdraw their own funds` |
| No permanent lock | `funds are never permanently stuck in contract` |
| Gas bounded | `function gas cost < block gas limit for any state` |

### Category 12: Upgradeability & Proxy

**Questions to ask:**
- Is the contract upgradeable? Which pattern (Transparent, UUPS, Beacon, Diamond)?
- Is the initializer protected against re-initialization?
- Is storage layout compatible between versions?
- Can the implementation be changed to a malicious contract?
- Are there storage collisions between proxy and implementation?

**Invariant patterns to extract:**

| Pattern | Template |
|---------|----------|
| Storage alignment | `proxy storage layout == implementation storage layout` |
| Initialize once | `initialize reverts if already initialized` |
| Upgrade authorization | `only authorized role can upgrade` |
| No storage collision | `proxy admin slot and implementation slot use EIP-1967 locations` |
| UUPS guard | `implementation has _authorizeUpgrade` |
| Version monotonicity | `version only increases on upgrade` |

---

## Phase 3: Validate Completeness

Before finalizing, run through this checklist:

### Coverage Check

```
For EVERY state variable:
  □ At least one invariant constrains its range
  □ At least one invariant connects it to other variables (if coupled)

For EVERY external/public function:
  □ Access control invariant documented
  □ Pre/post condition invariant documented
  □ Effect on state variables documented

For EVERY external call or callback:
  □ Reentrancy invariant documented
  □ Return value validation documented

For EVERY assembly block:
  □ Every sload/sstore audited for correct slot
  □ Every bitmask audited for width/offset
  □ Every arithmetic op audited for overflow
  □ Memory bounds checked

For EVERY mathematical operation:
  □ Overflow/underflow considered
  □ Division-by-zero considered
  □ Rounding direction documented
  □ Precision loss bounded
```

### Cross-Category Coupling Check

Some invariants span multiple categories. Verify these critical intersections:

| Intersection | What to check |
|-------------|---------------|
| Solvency × Reentrancy | Can reentrancy break accounting? |
| Access Control × Upgradeability | Can upgrade bypass access control? |
| Oracle × Arithmetic | Can stale/manipulated price cause overflow? |
| State Machine × DoS | Can state transition be blocked? |
| Assembly × Token Standards | Does assembly optimization break ERC compliance? |
| Governance × Flash Loans | Can governance be flash-manipulated? |
| Bridge × Reentrancy | Can cross-chain callback re-enter? |

---

## Phase 4: Write Output File

Create a single file at `invariants/INVARIANTS.md` in the project root.

### Output Template

```markdown
# System Invariants

> Generated from [protocol-name] codebase analysis.
> These invariants are specifications — they describe what MUST be true.
> Downstream agents use this file to write fuzzing harnesses and formal verification rules.

## Metadata

- **Protocol**: [name]
- **Contracts analyzed**: [list]
- **Analysis date**: [date]
- **Context source**: audit-context-building output

---

## How to Read This Document

Each invariant follows this format:

- **ID**: Unique identifier (CATEGORY-NNN)
- **Property**: Plain English statement of what must be true
- **Scope**: Which contract(s) and function(s) this applies to
- **Type**: Blackbox (from spec/docs) or Whitebox (from code internals)
- **Phase**: Construction | Running | End-State
- **Priority**: CRITICAL | HIGH | MEDIUM | LOW
- **Technique hint**: Ghost variable, try/catch, direct assert, shadow accounting
- **Related invariants**: Cross-references to coupled invariants

---

## 1. Solvency & Accounting

### SOL-001: [Title]
- **Property**: [plain English]
- **Scope**: [Contract.function()]
- **Type**: Blackbox
- **Phase**: Running
- **Priority**: CRITICAL
- **Technique hint**: Ghost variable summing all user balances
- **Related**: ACC-003, FEE-001

[repeat for each invariant]

## 2. Access Control & Authorization

### ACL-001: [Title]
[...]

## 3. State Machine & Lifecycle

### STM-001: [Title]
[...]

## 4. Arithmetic & Precision

### ARI-001: [Title]
[...]

## 5. Assembly & Bitwise Operations

### ASM-001: [Title]
[...]

## 6. Oracle & External Data

### ORA-001: [Title]
[...]

## 7. Reentrancy & Ordering

### REE-001: [Title]
[...]

## 8. Token Standards Compliance

### TOK-001: [Title]
[...]

## 9. Governance & Voting

### GOV-001: [Title]
[...]

## 10. Cross-Contract & Bridge

### BRG-001: [Title]
[...]

## 11. Denial of Service

### DOS-001: [Title]
[...]

## 12. Upgradeability & Proxy

### UPG-001: [Title]
[...]

## Cross-Category Invariants

### XCA-001: [Title]
- **Categories**: [e.g., Solvency × Reentrancy]
- **Property**: [plain English]
[...]

---

## Summary

| Category | Count | Critical | High | Medium | Low |
|----------|-------|----------|------|--------|-----|
| Solvency | N | N | N | N | N |
| Access Control | N | N | N | N | N |
| ... | ... | ... | ... | ... | ... |
| **Total** | **N** | **N** | **N** | **N** | **N** |
```

---

## Invariant Quality Standards

Each invariant must satisfy ALL of:

1. **Falsifiable**: Can be tested — a fuzzer or prover can check it
2. **Precise**: No ambiguity — exactly one interpretation
3. **Atomic**: Tests one property — not a conjunction of many things
4. **Anchored**: References specific contract(s) and function(s)
5. **Actionable**: A downstream fuzzing agent can translate it to code without further context

### Good vs Bad Invariant Examples

**BAD**: "The contract should be secure"
- Not falsifiable, not precise, not atomic

**BAD**: "Users can't steal funds"
- Not precise enough — steal how? From whom?

**GOOD**: "For any user U, sum of all withdrawals by U across all calls to withdraw() must be ≤ sum of all deposits by U across all calls to deposit(), plus accumulated yield entitled to U"
- Falsifiable, precise, atomic, anchored

**BAD**: "Math should not overflow"
- Which math? Where? What inputs?

**GOOD**: "In Pool.swap(), the intermediate product `amountIn * reserveOut` must not exceed type(uint256).max for any reachable (amountIn, reserveOut) where amountIn ≤ pool.totalLiquidity and reserveOut ≤ pool.reserveOut"
- Falsifiable, precise, anchored with bounds

**BAD (assembly)**: "Assembly is correct"

**GOOD (assembly)**: "In BitPackedTickMap.nextInitializedTickInWord(), the mask `(1 << bitPos) - 1` correctly isolates bits [0, bitPos-1], and `masked & (masked ^ (masked - 1))` returns the lowest set bit in the masked range, for all bitPos in [0, 255]"
- Precise about the bit operation, range-bounded

---

## Using the Vulnerability Database for Inspiration

When writing invariants, consult `DB/index.json` to find known vulnerability patterns that inform which invariants to prioritize.

### Quick Lookup Flow

```
1. Identify protocol type → DB/index.json → protocolContext.mappings
2. Load relevant manifests → DB/manifests/<name>.json
3. For each pattern in manifest:
   - Read rootCause → derive the invariant that prevents this bug
   - Read codeKeywords → check if these appear in target code
   - If match: write a targeted invariant with HIGH/CRITICAL priority
```

### Example: Lending Protocol

```
protocolContext.mappings.lending_protocol →
  manifests: ["oracle", "general-defi", "tokens", "general-security"]

Load oracle.json → pattern: "Missing Staleness Check"
  → Invariant: ORA-001: Price freshness must be validated
  → Priority: CRITICAL (pattern severity: MEDIUM-HIGH, but lending amplifies impact)

Load general-defi.json → pattern: "First Depositor Attack"
  → Invariant: SOL-005: First deposit cannot be exploited for share inflation
  → Priority: HIGH
```

---

## Subagent Usage

Spawn subagents for:
- **Dense assembly blocks**: Full bit-by-bit analysis of packing/unpacking
- **Complex math modules**: Precision analysis of fixed-point libraries
- **Cross-contract flows**: Tracing invariants across multiple contracts
- **Token interaction analysis**: Checking compatibility with non-standard tokens

Each subagent must return structured invariants in the format specified above.

---

## Anti-Hallucination Rules

- **Never invent invariants that the code doesn't support.** Every invariant must trace back to a state variable, function, or documented specification.
- **If uncertain whether a property holds**, write it as a "CANDIDATE" invariant with a note: "Requires manual verification — could not confirm from code alone."
- **Do not assume standard behavior.** If a function is named `transfer` but has custom logic, derive invariants from the actual code, not the ERC20 spec.
- **Cross-reference with existing assertions.** The codebase's own `require` and `assert` statements are invariants the developer intended — include them and verify they are sufficient.
- **Cite evidence.** Each invariant should reference the file and function(s) it covers.

---

## Resources

- **Context builder**: [audit-context-building.md](audit-context-building.md) — must run first
- **Vulnerability database**: `DB/index.json` → manifests for known patterns
- **Report templates**: [invariant-report-templates.md](resources/invariant-report-templates.md)
- **Invariant methodology**: [Invariant-Methodology.md](resources/Invariant-Methodology.md)
- **Root cause analysis**: [root-cause-analysis.md](resources/root-cause-analysis.md)
- **Crytic properties**: Reference for ERC20/ERC721/ERC4626 standard invariants (github.com/crytic/properties)
