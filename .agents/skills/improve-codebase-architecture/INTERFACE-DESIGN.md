# Interface Design Workflow

Use this only after the user chooses a deepening candidate and asks to explore concrete interfaces.

The method is "design it twice": the first interface shape is rarely the best one. Produce multiple designs with deliberately different tradeoffs, then compare them using the shared architecture language.

## Step 1: Frame the problem space

Before spawning design agents or writing proposals, explain:

- The current friction and files involved
- The domain concepts from `CONTEXT.md` or inferred project language
- Constraints the interface must satisfy
- Dependencies and their categories from [DEEPENING.md](DEEPENING.md)
- What must sit behind the seam
- Which tests should survive the refactor

Include a small illustrative code sketch only if it clarifies constraints. Mark it as illustrative, not the proposed design.

## Step 2: Generate different interface designs

When parallel agents are available, ask at least three agents for different designs. Give each agent the file paths, coupling details, domain vocabulary, dependency category, and expected behavior behind the seam.

Use distinct design briefs:

1. Minimal interface: aim for 1 to 3 entry points with maximum leverage per entry point.
2. Flexible interface: support more extension points and uncommon cases.
3. Common-path interface: make the dominant caller workflow trivial.
4. Ports-and-adapters interface: use when remote owned or true external dependencies shape the seam.

Each design must include:

- Interface: types, methods, params, invariants, ordering, and error modes
- Usage example
- Implementation hidden behind the seam
- Dependency and adapter strategy
- Tradeoffs: where leverage is high and where it is thin

## Step 3: Compare and recommend

Present each design separately, then compare them in prose:

- Depth: how much behavior sits behind the interface
- Leverage: what callers gain per concept learned
- Locality: where changes and bugs concentrate
- Seam placement: whether the seam is in the right place
- Test surface: whether tests can use the same interface as callers
- Migration cost: how disruptive adoption would be

Finish with an opinionated recommendation. If a hybrid is strongest, state exactly which parts to combine.
