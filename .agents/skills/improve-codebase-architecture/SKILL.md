---
name: "improve-codebase-architecture"
description: "Find deepening opportunities in a codebase. Use when the user wants architectural review, refactoring candidates, tighter module seams, better test surfaces, lower coupling, or a codebase that is easier for humans and agents to navigate. Reads domain language from CONTEXT.md or CONTEXT-MAP.md and respects docs/adr/ decisions."
---
Use the [improve-codebase-architecture subagent](../../../.codex/agents/improve-codebase-architecture.toml) when you want delegated execution.
That subagent is configured for live web search and may delegate to narrower repo subagents when the workflow splits cleanly.

Input: `[target-path-or-topic]`.

Run an architecture-deepening review for `<arguments>`.

This skill is adapted from Matt Pocock's `improve-codebase-architecture` workflow:
https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture

## Core vocabulary

Use this vocabulary consistently in recommendations:

| Term | Meaning |
|------|---------|
| **Module** | Anything with an interface and implementation: function, class, package, layer, or vertical slice. |
| **Interface** | Everything callers must know: types, invariants, ordering constraints, error modes, config, and performance behavior. |
| **Implementation** | The code hidden behind a module's interface. |
| **Depth** | Leverage at the interface. A deep module provides a lot of behavior behind a small interface. |
| **Seam** | The place where an interface lives and behavior can be changed without editing callers. |
| **Adapter** | A concrete thing satisfying an interface at a seam. |
| **Leverage** | What callers get from depth: more capability per concept they must learn. |
| **Locality** | What maintainers get from depth: change, bugs, and knowledge concentrated in one place. |

For full definitions, read [LANGUAGE.md](LANGUAGE.md).

## Workflow

1. **Read project context first**
   - Prefer `CONTEXT-MAP.md` if present, then the relevant `CONTEXT.md`.
   - Read `docs/adr/*.md` for decisions in the target area.
   - If no context file exists, proceed with inferred domain language and create `CONTEXT.md` only when the review resolves a real domain term.

2. **Explore architecture friction**
   - Use fast local discovery first: `rg --files`, targeted `rg`, and focused file reads.
   - Use explorer subagents when the target splits into independent modules or flows.
   - Track where understanding one domain concept requires bouncing across many shallow modules.
   - Apply the deletion test: if deleting a module removes complexity, it was pass-through; if complexity reappears across callers, it was earning its keep.

3. **Present deepening candidates**
   - Present numbered candidates before proposing concrete interfaces.
   - For each candidate include: files, problem, solution, benefits, test impact, and any ADR conflict.
   - Use project domain vocabulary plus this skill's architecture vocabulary.
   - Ask which candidate the user wants to explore.

4. **Grill the selected candidate**
   - Walk constraints, dependencies, seam placement, adapter needs, and tests that should survive.
   - Classify dependencies with [DEEPENING.md](DEEPENING.md).
   - Update `CONTEXT.md` when the conversation clarifies load-bearing domain language. Use [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md).
   - Offer an ADR only for decisions that are hard to reverse, surprising without context, and caused by a real tradeoff. Use [ADR-FORMAT.md](ADR-FORMAT.md).

5. **Design interfaces when requested**
   - If the user wants concrete interface options, follow [INTERFACE-DESIGN.md](INTERFACE-DESIGN.md).
   - Generate at least three meaningfully different interface designs when parallel agents are available.
   - Compare designs by depth, locality, seam placement, dependency strategy, and test surface.

## Output shape

For initial reviews, produce:

```md
# Architecture Deepening Candidates

## Candidate 1: <domain-name> module

Files:
- <path>

Problem:
<why the current interface or seam causes friction>

Solution:
<plain English refactor direction, not detailed interface yet>

Benefits:
- Leverage: <what callers get>
- Locality: <what maintainers get>
- Tests: <how the test surface improves>

ADR conflict:
<none, or explicit ADR reference and why reopening may be justified>
```

Do not implement a refactor during the initial review unless the user explicitly asks for implementation.

## Related references

- [LANGUAGE.md](LANGUAGE.md) - required terms and rejected framings
- [DEEPENING.md](DEEPENING.md) - dependency categories and testing strategy
- [INTERFACE-DESIGN.md](INTERFACE-DESIGN.md) - design-it-twice workflow
- [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md) - domain language file format
- [ADR-FORMAT.md](ADR-FORMAT.md) - lightweight decision record format
