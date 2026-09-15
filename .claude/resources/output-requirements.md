# Output Requirements

When performing ultra-granular analysis, Agent MUST structure output following the Per-Function Microstructure Checklist format demonstrated in [function-micro-example-context.md](function-micro-example-context.md).

> **Core Principle**: "If you cannot explain WHY a line of code exists, in what order it MUST execute, and what BREAKS if it changes — you have found where bugs hide."

---

## Required Structure

For EACH analyzed function, output MUST include:

**1. Purpose & Intent** (mandatory)
- Clear statement of function's role in the system
- **Feynman explain step**: explain in the simplest terms possible (fewer words = better understanding)
- State the function's INTENT (what it's SUPPOSED to do) vs IMPLEMENTATION (what it ACTUALLY does)
- Flag any intent-implementation gap: `INTENT-IMPL GAP: [description]` or `No gap detected`
- Name the invariant this function protects, or flag: `NO CLEAR INVARIANT`
- Minimum 2-3 sentences

**2. Inputs & Assumptions** (mandatory)
- All parameters (explicit and implicit)
- All preconditions
- All trust assumptions
- Each input must identify: type, source, trust level
- Minimum 5 assumptions documented

**Assumption Interrogation** (mandatory — apply Feynman Q4):
- About the caller: Who can call? Enforced or assumed? What caller types?
- About external data: Token behavior, oracle freshness, input sanitization
- About current state: What state is assumed true? Enforced?
- About time/ordering: Timestamp assumptions, deadline validity
- About amounts/sizes: What if 0? Max? Dust? Beyond available?

**3. Outputs & Effects** (mandatory)
- Return values (or "void" if none)
- All state writes
- All external interactions
- All events emitted
- All postconditions
- Minimum 3 effects documented

**What's Missing Detection** (mandatory):
- State that SHOULD be updated but ISN'T
- Events that SHOULD be emitted but AREN'T
- Return values that could be silently wrong
- Missing access control, reentrancy guard, or validation

**4. Line-by-Line Feynman Interrogation** (mandatory)
For EACH logical code block, document:
- **What:** What the block does (1 sentence)
- **Why here:** Why this ordering/placement (1 sentence)
- **What breaks:** What breaks if this line is deleted? Moved up? Moved down?
- **Assumptions:** What must be true (1+ items)
- **Depends on:** What prior state/logic this relies on
- **Sufficiency:** Is this check SUFFICIENT for what it prevents? (Q1.4)
- **First Principles / 5 Whys / 5 Hows:** Apply at least ONE per block

Minimum standards:
- Analyze at minimum: ALL conditional branches, ALL external calls, ALL state modifications
- For complex blocks (>5 lines): Apply First Principles AND 5 Whys or 5 Hows
- For simple blocks (<5 lines): Minimum What + Why here + What breaks + 1 Assumption

**5. Ordering & Sequence Analysis** (mandatory for state-changing functions)
- **Execution sequence**: Step 1 → Step 2 → ... → Step N
- **First state change / Last state read / Gap analysis**
- **Abort analysis**: What state persists if function aborts at each step?
- **Front-running exposure**: Can call ordering give an advantage?

**6. Mirror & Consistency Analysis** (mandatory for functions with inverse operations)
- Identify inverse function (deposit↔withdraw, mint↔burn, etc.)
- Compare validation strictness, state changes, access control, event emission
- Flag asymmetries: `MIRROR ASYMMETRY: [description]`

**7. Edge Case & Boundary Analysis** (mandatory)
Document behavior for:
- First call (empty state)
- Last call (draining/exhaustion)
- Twice in rapid succession
- Zero input / Max input / Dust input
- Self-referential call (system as parameter)

**8. Cross-Function & Multi-Transaction Dependencies** (mandatory)
- Internal calls made (list all)
- External calls made (list all with: "What can callee do at THIS moment?")
- Functions that call this function
- Shared state with other functions
- Invariant couplings (how this function's invariants interact with others)
- Minimum 3 dependency relationships documented

**Multi-Transaction Reasoning**:
- Second call correctness (does second call account for state changes from first?)
- Accumulated state divergence (rounding drift, monotonic growth, stale rewards)
- Attacker sequence exposure (after calling this, what becomes newly dangerous?)

**9. What's Missing Checklist** (mandatory)
- [ ] All state variables that should be updated — are they?
- [ ] Access control present where needed?
- [ ] Reentrancy protection needed given external calls?
- [ ] Event emission needed for off-chain tracking?
- [ ] Return value consumed by callers and correct under all paths?
- [ ] Zero/bounds validation present for all untrusted inputs?
- [ ] Slippage/deadline protection needed?
- [ ] State cleanup needed?

---

## Quality Thresholds

A complete micro-analysis MUST identify:
- Minimum 3 invariants (per function)
- Minimum 5 assumptions (across all sections, from assumption interrogation)
- Minimum 3 risk considerations (especially for external interactions)
- At least 1 application of First Principles
- At least 3 applications of 5 Whys or 5 Hows (combined)
- At least 1 ordering/sequence analysis per state-changing function
- At least 1 edge case analysis per function
- At least 1 mirror/consistency check for functions with inverses
- Every function has a Feynman explain step
- Intent vs Implementation gap explicitly stated
- What's Missing checklist completed

---

## Format Consistency

- Use markdown headers: `**Section Name:**` for major sections
- Use bullet points (`-`) for lists
- Use code blocks (` ```solidity `) for code snippets
- Reference line numbers: `L45`, `lines 98-102`
- Separate blocks with `---` horizontal rules for readability
- Flag gaps: `INTENT-IMPL GAP:`, `MIRROR ASYMMETRY:`, `NO CLEAR INVARIANT`, `MISSING:`