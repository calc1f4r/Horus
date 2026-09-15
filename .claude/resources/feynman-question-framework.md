# Feynman Question Framework for Smart Contract Auditing

> "If you cannot explain WHY a line of code exists, in what order it MUST execute, and what BREAKS if it changes — you have found where bugs hide."

This framework provides systematic questions that function-analyzer sub-agents apply per-function. Questions OPEN the mind; assumptions CLOSE it. Always be questioning.

---

## Category 1: Purpose Questions — WHY is this here?

For each line or block of code:

```
Q1.1: Why does this line exist? What invariant does it protect?
      → If you cannot name the invariant, the line may be:
        (a) unnecessary, or (b) protecting something undocumented

Q1.2: What happens if I DELETE this line entirely?
      → If nothing breaks → dead code
      → If something breaks → you found what it protects
      → If something SHOULD break but doesn't → missing dependency

Q1.3: What SPECIFIC attack or edge case motivated this check?
      → If there's a guard like `require(amount > 0)`, what goes
        wrong at amount=0? Trace the zero through the entire function.

Q1.4: Is this check SUFFICIENT for what it's trying to prevent?
      → `amount > 0` doesn't prevent dust griefing
      → `caller == owner` doesn't prevent key compromise
      → A bounds check doesn't prevent off-by-one within bounds
```

---

## Category 2: Ordering Questions — WHAT IF I MOVE THIS?

For each state-changing operation:

```
Q2.1: What if this line executes BEFORE the line above it?
      → Would a different ordering allow state manipulation?
      → Validate-then-act violations: reading state, external call,
        THEN updating state → stale state during external call

Q2.2: What if this line executes AFTER the line below it?
      → Does delaying create a window of inconsistent state?
      → Can an external call/callback between these lines exploit the gap?

Q2.3: What is the FIRST line that changes state? What is the LAST line
      that reads state? Is there a gap between them?
      → State reads after state writes may see stale data
      → State writes before validation may leave dirty state on abort

Q2.4: If this function ABORTS HALFWAY, what state is left behind?
      → Side effects that persist despite abort (external calls already
        made, events emitted, cross-contract writes)?
      → Can an attacker intentionally trigger partial execution?

Q2.5: Can the ORDER in which users call this function matter?
      → Front-running: does calling first give advantage?
      → Does behavior differ based on prior state from another user's call?
```

---

## Category 3: Consistency Questions — WHY does A have it but B doesn't?

Compare functions that SHOULD be symmetric:

```
Q3.1: If functionA has an access guard and functionB doesn't, WHY?
      → Is functionB intentionally unrestricted, or did the dev forget?
      → Every function touching the same storage should have consistent
        access control unless there's an explicit reason

Q3.2: If deposit() checks X, does withdraw() also check X?
      → Pair analysis: deposit/withdraw, stake/unstake, lock/unlock,
        mint/burn, open/close, borrow/repay, add/remove,
        create/destroy, encode/decode
      → The inverse operation must validate at least as strictly

Q3.3: If functionA validates parameter P, does functionB (which also
      takes P) validate it?
      → Same parameter, different validation = one of them is wrong

Q3.4: If functionA emits an event, does functionB (doing similar work)
      also emit one?
      → Missing events = off-chain systems can't track state changes

Q3.5: If functionA uses overflow-safe arithmetic, does functionB?
      → Inconsistent overflow protection = the unprotected one may overflow
```

---

## Category 4: Assumption Questions — WHAT IS IMPLICITLY TRUSTED?

Expose hidden assumptions:

```
Q4.1: What does this function assume about THE CALLER?
      → Who can call this? Enforced or just assumed?
      → Could the caller be a different type? (EOA vs contract vs proxy)
      → What if the caller IS the system itself? (self-calls, recursion)

Q4.2: What does this function assume about EXTERNAL DATA?
      → Tokens: standard behavior? Fee-on-transfer? Rebasing? Unusual decimals?
      → Oracle data: always fresh? What if stale, zero, or manipulated?
      → User input: sanitized? Type confusion? Encoding tricks?

Q4.3: What does this function assume about CURRENT STATE?
      → "Never called when paused" — but IS it enforced?
      → "Balance always sufficient" — but who guarantees that?
      → "Map never empty" — but what if it is?
      → "Already initialized" — but what if it wasn't?

Q4.4: What does this function assume about TIME or ORDERING?
      → Block timestamp can be manipulated (~15s on Ethereum)
      → What if deadline already passed? What if time = 0?
      → What if events arrive out of order?

Q4.5: What does this function assume about PRICES or RATES?
      → Can the value be manipulated within the same transaction?
      → Is the data source fresh? What if oracle is stale or dead?
      → What if the value is 0? MAX_VALUE? Precision mismatch?

Q4.6: What about INPUT AMOUNTS or SIZES?
      → What if amount = 0? Maximum representable value? 1 (dust)?
      → What if amount exceeds available balance?
      → What if a collection is empty? Millions of entries?
```

---

## Category 5: Boundary & Edge Case Questions — WHAT BREAKS AT THE EDGES?

```
Q5.1: What happens on the FIRST call? (Empty state)
      → First depositor, first user, first initialization
      → Division by zero when total = 0?
      → Share/ratio inflation when pool is empty?

Q5.2: What happens on the LAST call? (Draining/exhaustion)
      → Last withdraw that empties everything
      → Remaining dust that can never be extracted?
      → Does rounding trap value permanently?

Q5.3: What if called TWICE in rapid succession?
      → Re-initialization, double-spending, double-counting
      → Does second call see state from first?

Q5.4: What if TWO DIFFERENT functions are called in same context?
      → Borrow in funcA, manipulate in funcB, repay in funcA
      → Cross-function interaction breaking invariants?

Q5.5: What if called with THE SYSTEM ITSELF as a parameter?
      → Self-referential: transfer to self, compare with self
      → Circular references or recursive structures?
```

---

## Category 6: Return Value & Error Path Questions

```
Q6.1: What does this function return? Who consumes the return value?
      → If caller ignores return value, what's lost?
      → If return value is wrong, what downstream logic breaks?

Q6.2: What happens on the ERROR/ABORT path?
      → Side effects before the error?
      → Can error message leak sensitive information?
      → Can an attacker cause targeted errors (griefing/DoS)?

Q6.3: What if an EXTERNAL CALL fails silently?
      → Low-level call returning false without checking
      → Error swallowed by try-catch or ignored return value

Q6.4: Is there a code path where NO return and NO error happens?
      → Functions falling through without explicit return
      → Default/zero values used when they shouldn't be
      → Missing match/switch arms
```

---

## Category 7: Multi-Transaction & Sequence Analysis

### Part A: Within Single Transaction

```
Q7.1: If external call happens BEFORE state update, what if swapped?
      → If swap causes revert → original ordering may be exploitable
      → If swap works → original ordering is safe OR swap reveals
        the intended safe ordering was never enforced

Q7.2: For EVERY external call: what can the CALLEE do at THIS exact moment?
      → What state is committed vs pending at point of external call?
      → Can callee re-enter with stale state?
      → Can callee call a DIFFERENT function that reads not-yet-updated state?

Q7.3: What is the MINIMAL state that MUST be updated before each external call?
      → List every state variable the callee could read or depend on
      → Any updated AFTER the call → potential ordering vulnerability
```

### Part B: Across Multiple Transactions

```
Q7.4: If user calls with value X, then again with value Y — correct second time?
      → Does second call account for state changes from first call?
      → deposit(100), deposit(50): correct when totalSupply != 0?

Q7.5: Can accumulated state from MULTIPLE calls create a condition
      a SINGLE call can never reach?
      → Rounding errors compounding: each call loses 1 wei precision
      → Monotonically growing state hitting ceiling or overflow
      → Reward staleness: infrequent updates → incorrect accumulation

Q7.6: Can an attacker craft a SEQUENCE of transactions to reach
      a state no single "normal" path would produce?
      → Deposit-borrow-withdraw-liquidate → bad debt
      → Stake-unstake-restake → compound rounding errors
      → Create-transfer-destroy → orphan child state
      → For each function: "After calling THIS, what functions become
        newly available or newly dangerous?"
```

---

## Creativity Triggering Questions (from Dravee)

Apply these as a final sweep after systematic analysis:

```
STATE MANIPULATION:
- Can you change someone else's state? (doing something for someone)
- Can you influence someone else's state? (manipulating something used by someone)
- Are all state variables updated as they should be?
- Are state variables updated at all when they should be?
- Are state variables updated when they SHOULDN'T be?

INPUT ABUSE:
- Can a malicious contract be supplied to the system?
- Can I supply mismatched inputs? (TokenId not belonging to User)
- Can I supply unexpected inputs? (past timestamp, zero amount)
- Can something silently pass instead of reverting?

VALUE & REWARDS:
- Can someone be prevented from transferring funds to the contract?
- Can rewards be blocked/reduced/delayed/inflated/claimed too early/claimed for someone else?
- Can funds get stolen/locked/stuck?

FLOW MANIPULATION:
- Can the action be done several times? (claiming twice)
- What about edge cases in inputs? (min, max, zero)
- What about corner cases in the flow? (claim before stake, close before open)
- Is something MISSING in a function/contract that SHOULD be there?
- Does the action even work correctly? Does it work at all?

SENTENCE TEMPLATES (replace keywords):
- "ACTION will revert if CONDITION" → what reverts unexpectedly?
- "ACTION will silently not work" → what fails silently?
- "ACTION will still work even if CONDITION" → what succeeds when it shouldn't?
- "If ACTION is not done before ACTION2, then USER/ASSET/STATE is negatively impacted"
- "ACTION leaving excess funds in the contract" → stuck value?
```

---

## Application Priority

Not every question applies to every line. Use judgment:

| Code Type | Heavy On | Light On |
|-----------|----------|----------|
| State-changing lines | Q2 (ordering), Q4 (assumptions) | Q1, Q6 |
| Validation/guard lines | Q1 (purpose), Q3 (consistency) | Q2, Q7 |
| External calls | Q4 (assumptions), Q7 (sequencing), Q6 (returns) | Q1 |
| Math operations | Q5 (boundaries), Q4.6 (amounts) | Q3 |
| Access control | Q3 (consistency), Q4.1 (caller) | Q5 |
| Event emissions | Q3.4 (consistency) | Everything else |
