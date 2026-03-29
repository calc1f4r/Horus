# Completeness Checklist

Before concluding micro-analysis of a function, verify:

---

## Structural Completeness
- [ ] Purpose & Intent section: 2+ sentences, Feynman explain step, intent vs implementation stated
- [ ] Intent-Implementation gap: explicitly flagged (`INTENT-IMPL GAP:`) or `No gap detected`
- [ ] Invariant: named invariant protected, or `NO CLEAR INVARIANT` flagged
- [ ] Inputs & Assumptions section: All parameters + implicit inputs documented
- [ ] Assumption Interrogation: Caller, external data, current state, time, amounts all questioned
- [ ] Outputs & Effects section: All returns, state writes, external calls, events
- [ ] What's Missing Detection: State, events, return values, guards all checked for absence
- [ ] Line-by-Line Feynman Interrogation: Every logical block analyzed (WHY/ORDER/BREAKS)
- [ ] Ordering & Sequence Analysis: Execution sequence, first state change, abort analysis
- [ ] Mirror & Consistency Analysis: Inverse function identified and compared (if applicable)
- [ ] Edge Case & Boundary Analysis: First/last/twice/zero/max scenarios documented
- [ ] Cross-Function & Multi-Transaction Dependencies: All calls, shared state, sequence reasoning
- [ ] What's Missing Checklist: All items checked

---

## Content Depth
- [ ] Identified at least 3 invariants (what must always hold)
- [ ] Documented at least 5 assumptions (from assumption interrogation)
- [ ] Applied First Principles at least once
- [ ] Applied 5 Whys or 5 Hows at least 3 times total
- [ ] Risk analysis for all external interactions (reentrancy, malicious contracts, etc.)
- [ ] At least 1 ordering/sequence analysis for state-changing functions
- [ ] At least 1 edge case boundary documented
- [ ] Mirror consistency check completed (for functions with inverses)
- [ ] Multi-transaction reasoning documented (second call correctness, sequence exposure)

---

## Feynman Quality Gates
- [ ] Can explain what the function does in 1-2 simple sentences (Feynman explain step)
- [ ] For every line: can explain WHY it exists (Q1.1)
- [ ] For every state change: can explain what ORDER it must execute in (Q2)
- [ ] For every state change: can explain what BREAKS if it changes (Q1.2)
- [ ] For every check: can explain if it's SUFFICIENT (Q1.4)
- [ ] All hidden assumptions surfaced (Q4 categories)
- [ ] Edge cases systematically explored (Q5)

---

## Continuity & Integration
- [ ] Cross-reference with related functions (if internal calls exist, analyze callees)
- [ ] Propagated assumptions from callers (if this function is called by others)
- [ ] Identified invariant couplings (how this function's invariants relate to global system)
- [ ] Tracked data flow across function boundaries (if applicable)
- [ ] Multi-transaction state: second call correctness documented
- [ ] Sequence exposure: what becomes dangerous after calling this function

---

## Anti-Hallucination Verification
- [ ] All claims reference specific line numbers (L45, L98-102, etc.)
- [ ] No vague statements ("probably", "might", "seems to") - replaced with "unclear; need to check X"
- [ ] Contradictions resolved (if earlier analysis conflicts with current findings, explicitly updated)
- [ ] Evidence-based: Every invariant/assumption tied to actual code
- [ ] Never accepted code at face value — questioned every developer decision

---

## Completeness Signal

Analysis is complete when:
1. All checklist items above are satisfied
2. No remaining "TODO: analyze X" or "unclear Y" items
3. Full call chain analyzed (for internal calls, jumped into and analyzed)
4. All identified risks have mitigation analysis or acknowledged as unresolved
5. Feynman explain step passes (can explain simply)
6. Intent vs implementation explicitly compared
7. What's Missing checklist has no unchecked items