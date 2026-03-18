<!-- AUTO-GENERATED from `.claude/resources/memory-state.md`; source_sha256=5302daab0281261ceff6f8fd629de87bd7bc58ac8c25b9928b534dbbe7279e33 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/memory-state.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Memory State: Persistent Inter-Agent Memory Layer

> **Purpose**: Defines the shared memory bus that agents write to and read from throughout the audit pipeline. Inspired by Mem0's extraction→update→retrieval paradigm for persistent agent memory, adapted for multi-agent security audits.
> **Consumer**: All agents in the audit pipeline.

---

## Motivation (from Mem0 Paper)

LLMs operating as agents lose context between spawns — each sub-agent starts "cold" with only the prompt the orchestrator provides. The Mem0 architecture demonstrates that **structured, persistent memory mechanisms** dramatically improve multi-session agent coherence. The three key principles we adapt:

1. **Extraction**: After completing work, an agent distills salient insights (not raw output) into structured memory entries
2. **Update**: Memory entries are consolidated — new entries ADD knowledge, UPDATE existing entries when refined, or flag CONTRADICTIONS when two agents disagree
3. **Retrieval**: Before starting work, an agent reads the memory state to inherit accumulated knowledge from all prior agents

This transforms the pipeline from a **sequential file handoff** into a **cumulative knowledge accumulator** where late-phase agents are smarter than early-phase agents.

---

## Architecture

```
audit-output/
├── memory-state.md            ← Canonical shared memory (all agents read/write)
├── memory-state.json          ← Structured version (for programmatic queries)
├── ...existing pipeline files...
```

### Memory State vs. Existing Pipeline Bus

The existing pipeline bus (`discovery-state-round-N.md`, `pipeline-state.md`) tracks **outputs** — what was found. Memory state tracks **knowledge** — what was learned, what was surprising, what dead-ends were hit, and what patterns emerged. They are complementary:

| Aspect | Pipeline Bus | Memory State |
|--------|-------------|--------------|
| **Content** | Findings, verdicts, PoC results | Insights, hypotheses, dead-ends, patterns |
| **Granularity** | Per-phase structured outputs | Per-agent distilled summaries |
| **When written** | End of each phase | End of each agent's work (within a phase) |
| **Who reads** | Next phase in sequence | ALL subsequent agents |
| **Purpose** | Data handoff | Knowledge accumulation |

---

## Memory Entry Schema

Each agent writes a memory entry using this structure:

```markdown
### MEM-<PHASE>-<AGENT>-<ROUND> : <one-line title>
- **Agent**: <agent name>
- **Phase**: <phase number and name>
- **Timestamp**: <when written>
- **Type**: INSIGHT | HYPOTHESIS | DEAD_END | PATTERN | CONTRADICTION | QUESTION

#### Summary
<2-5 sentences distilling the most important thing this agent learned>

#### Key Insights
- <insight 1 — e.g., "The protocol uses a custom oracle wrapper that caches prices for 2 blocks">
- <insight 2 — e.g., "State variable X is never validated after admin update">
- ...

#### Hypotheses (unconfirmed, for downstream agents to verify)
- <hypothesis 1 — e.g., "The fee calculation may truncate to zero for small amounts — needs FV confirmation">
- ...

#### Dead Ends (paths explored that yielded nothing — saves others from repeating)
- <dead end 1 — e.g., "Checked reentrancy in Pool.deposit() — CEI pattern is correctly applied">
- ...

#### Open Questions (for specific downstream agents)
- <question> → best answered by: <agent name or phase>
- ...

#### Affected Code Summary
- <file:lines — key code areas this agent focused on>
```

### Memory Entry Types

| Type | When to Use | Example |
|------|------------|---------|
| **INSIGHT** | Confirmed architectural understanding or behavioral observation | "The oracle uses a TWAP with a 30-minute window, not spot price" |
| **HYPOTHESIS** | Suspected issue that needs validation by another agent | "Flash loan attack may break the share price invariant" |
| **DEAD_END** | Investigated path that turned out safe — prevents redundant work | "Checked all external calls in Vault — no reentrancy vectors" |
| **PATTERN** | Recurring code pattern observed across multiple contracts | "Team consistently uses unchecked blocks for loop counters" |
| **CONTRADICTION** | Two agents or two code paths disagree on behavior | "NatSpec says 'reverts on zero' but implementation allows zero" |
| **QUESTION** | Specific question directed at a downstream agent | "Does the invariant `totalShares > 0` hold after full withdrawal?" |

---

## Memory State File: `audit-output/memory-state.md`

```markdown
# Audit Memory State

> Cumulative knowledge from all agents across all phases. Read this BEFORE starting your work.
> Last updated: <timestamp> by <agent name>

## Table of Contents
- [Phase 1: Reconnaissance](#phase-1)
- [Phase 2: Context Building](#phase-2)
- [Phase 3: Invariant Extraction](#phase-3)
- [Phase 4: Discovery Round N](#phase-4-round-n)
- [Phase 5+: Triage & Verification](#phase-5)

---

## Phase 1: Reconnaissance
### MEM-1-ORCHESTRATOR: Protocol classification and scope
...

## Phase 2: Context Building
### MEM-2-CONTEXT-BUILDER: Architectural overview
...
### MEM-2-FUNC-ANALYZER-Pool: Pool contract analysis
...
### MEM-2-SYSTEM-SYNTHESIZER: Cross-contract synthesis
...

## Phase 3: Invariant Extraction
### MEM-3A-INVARIANT-WRITER: Invariant extraction
...
### MEM-3B-INVARIANT-REVIEWER: Invariant hardening
...

## Phase 4: Discovery Round 1
### MEM-4A-R1-INVARIANT-CATCHER-SHARD-1: DB pattern hunting
...
### MEM-4B-R1-PROTOCOL-REASONING: Reasoning-based discovery
...
### MEM-4C-R1-PERSONA-ORCHESTRATOR: Multi-persona audit
...
### MEM-4D-R1-VALIDATION-REASONING: Validation gap scan
...

(repeat for each round)

## Phase 5+: Triage & Verification
### MEM-5-ORCHESTRATOR: Triage insights
...
```

---

## Memory State JSON: `audit-output/memory-state.json`

For programmatic queries, a parallel JSON representation:

```json
{
  "version": 1,
  "lastUpdated": "<timestamp>",
  "entries": [
    {
      "id": "MEM-2-CONTEXT-BUILDER",
      "agent": "audit-context-building",
      "phase": 2,
      "round": null,
      "type": "INSIGHT",
      "title": "Architectural overview",
      "summary": "Protocol is a lending pool with custom oracle wrapper...",
      "insights": ["insight1", "insight2"],
      "hypotheses": ["hypothesis1"],
      "deadEnds": ["deadEnd1"],
      "questions": [{"question": "...", "targetAgent": "invariant-writer"}],
      "affectedCode": ["src/Pool.sol:1-450", "src/Oracle.sol:1-200"]
    }
  ]
}
```

---

## Agent Integration Rules

### Rule 1: Every Agent MUST Write a Memory Entry

After completing their primary work (writing findings, context, invariants, etc.), every agent MUST append a memory entry to `audit-output/memory-state.md`. This is NOT optional — even if the agent found nothing, the DEAD_END entries prevent downstream agents from revisiting the same paths.

### Rule 2: Every Agent MUST Read Memory State Before Starting

Before beginning their primary workflow, every agent spawned after Phase 1 MUST read `audit-output/memory-state.md` (or the relevant sections). This is how accumulated knowledge flows forward.

**Reading strategy by phase**:
| Agent Phase | What to Read from Memory State |
|-------------|--------------------------------|
| Phase 2 (context builder) | Phase 1 entries — detection insights, protocol classification reasoning |
| Phase 3A (invariant writer) | Phase 1-2 entries — architecture insights, fragility clusters, code patterns |
| Phase 3B (invariant reviewer) | Phase 1-3A entries — writer's extraction challenges, hypothesis about bounds |
| Phase 4A (invariant catcher) | Phase 1-3 entries — all architectural knowledge + invariant insights |
| Phase 4B (protocol reasoning) | Phase 1-3 entries + Phase 4A entries (if sequential) |
| Phase 4C (multi-persona) | Phase 1-3 entries — architecture + invariant knowledge for all personas |
| Phase 4D (validation reasoning) | Phase 1-3 entries — focus on PATTERN and DEAD_END entries |
| Phase 5 (triage) | ALL entries — use hypotheses/contradictions to guide falsification |
| Phase 6 (PoC writing) | Phase 1-5 entries — dead-ends inform what NOT to PoC |
| Phase 8-10 (judging) | ALL entries — contradictions and hypotheses inform judge scrutiny |

### Rule 3: Memory Entries are Append-Only Within a Phase

Agents MUST NOT modify or delete other agents' memory entries. They MAY reference and respond to them:
- "Regarding MEM-3A-INVARIANT-WRITER hypothesis about fee truncation: CONFIRMED — I found truncation to zero for amounts < 1e6"
- "Contradicting MEM-2-CONTEXT-BUILDER: Pool.withdraw() is NOT access-controlled — any user can call it"

### Rule 4: The Orchestrator Consolidates Between Phases

After each phase completes, the orchestrator:
1. Reads all new memory entries from that phase
2. Checks for CONTRADICTIONS — if two agents contradict each other, adds a `CONTRADICTION` entry with both sides
3. Promotes high-value HYPOTHESES — if a hypothesis was independently raised by 2+ agents, marks it as `HIGH_PRIORITY`
4. Summarizes DEAD_ENDS — aggregates dead-end paths to keep the file scannable

---

## Integration with Existing Cross-Pollination

Memory state **enhances** the existing cross-pollination bus (`discovery-state-round-N.md`), not replaces it:

| Mechanism | Scope | What Flows |
|-----------|-------|------------|
| `discovery-state-round-N.md` | Between discovery rounds (Phase 4 only) | Findings, cross-check requests, unexplored areas |
| `memory-state.md` | Across ALL phases (1-11) | Insights, hypotheses, dead-ends, patterns, contradictions |
| `pipeline-state.md` | Phase tracking | Status, outputs, verification flags |

Example of how memory state enhances cross-pollination:

**Without memory state**: In Round 2, Protocol Reasoning reads `discovery-state-round-1.md` and knows what findings exist — but not WHY the invariant-catcher checked certain functions and found nothing there.

**With memory state**: In Round 2, Protocol Reasoning reads the invariant-catcher's memory entry saying "Checked reentrancy attack paths in Vault — all use CEI pattern correctly. focus elsewhere." This is a DEAD_END entry that saves Protocol Reasoning from wasting time on the same analysis.

---

## Memory Write Templates

### For Context Building Agents (Phase 2)

```markdown
### MEM-2-<AGENT>: <title>
- **Agent**: <name>
- **Phase**: 2 — Context Building
- **Type**: INSIGHT

#### Summary
<Describe the most surprising or important architectural finding>

#### Key Insights
- <How contracts are connected — which ones share state>
- <Unusual patterns — custom math, non-standard hooks, admin backdoors>
- <External dependencies — which oracles, tokens, bridges are used>

#### Hypotheses
- <Suspected fragility points — "This math library may lose precision at scale">

#### Dead Ends
- <Code areas that are straightforward forks of battle-tested libraries>

#### Open Questions
- <Questions about protocol behavior that require documentation or invariant analysis>
```

### For Discovery Agents (Phase 4)

```markdown
### MEM-4X-R<N>-<AGENT>: <title>
- **Agent**: <name>
- **Phase**: 4 — Discovery Round <N>
- **Type**: <INSIGHT | HYPOTHESIS | DEAD_END | PATTERN>

#### Summary
<Most important discovery or non-discovery. If found nothing, say what you checked and why it's clean.>

#### Key Insights
- <Root causes found — the underlying WHY, not just the symptom>
- <Patterns in how the team writes code — consistent mistakes or consistent safety>

#### Hypotheses
- <Findings with MEDIUM confidence — need another stream or round to confirm>
- <Cross-domain interactions that MIGHT be exploitable>

#### Dead Ends
- <Vulnerability classes checked that don't apply to this codebase>
- <Code paths verified as safe — with brief justification>

#### Open Questions
- <Cross-stream requests beyond what's in discovery-state-round-N.md>
- <Questions about code behavior that require a different analytical approach>

#### Affected Code Summary
- <List of files/functions deeply analyzed — so others know what's been covered>
```

### For Verification Agents (Phase 6-7)

```markdown
### MEM-<PHASE>-<AGENT>: <title>
- **Agent**: <name>
- **Phase**: <6 or 7> — <PoC or FV>
- **Type**: <INSIGHT | DEAD_END>

#### Summary
<Which PoCs passed/failed and why. Which invariants were violated/held.>

#### Key Insights
- <Setup requirements — "Protocol requires initial liquidity of at least X for PoC to work">
- <Environmental constraints — "Fork from block N because state changed after">

#### Dead Ends
- <Attack paths that looked exploitable but failed because of guard X>
- <PoC approaches that didn't work — saves retry effort>
```

---

## Orchestrator Memory Consolidation Template

Written by the orchestrator between phases:

```markdown
### MEM-CONSOLIDATION-PHASE-<N>: Cross-agent knowledge synthesis
- **Agent**: audit-orchestrator
- **Phase**: <N> (consolidation)
- **Type**: INSIGHT

#### Contradiction Resolution
- MEM-X says A; MEM-Y says B → Resolution: <which is correct and why>

#### Promoted Hypotheses (multi-agent agreement)
- Hypothesis "<H>" raised by agents [A, B] independently → Priority: HIGH
  Target verification: Phase <N+1> agent <Z>

#### Coverage Summary
- Code areas with deep coverage (3+ agents analyzed): [list]
- Code areas with shallow coverage (1 agent): [list]  
- Code areas with ZERO coverage: [list] → Priority targets for next phase

#### Accumulated Dead Ends (do NOT re-investigate)
- <aggregated list from all agents in this phase>
```

---

## Quality Rules

1. **Conciseness**: Memory entries should be 10-30 lines, not 100+. Distill, don't dump.
2. **Specificity**: "Checked Oracle" is useless. "Checked Oracle.getLatestPrice() L42-55 — staleness verified via updatedAt check at L48" is useful.
3. **Code references**: Every insight must reference specific code (file + line).
4. **No raw findings in memory**: Findings go in the standard pipeline outputs. Memory captures the META — what you learned, not what you found.
5. **Actionability**: Every hypothesis should state what would confirm or refute it. Every question should name a target agent.
