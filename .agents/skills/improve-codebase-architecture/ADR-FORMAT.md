# ADR Format

Use ADRs to record architecture decisions that future reviews should respect.

ADRs live in `docs/adr/` and use sequential filenames:

```text
0001-short-slug.md
0002-short-slug.md
```

Create `docs/adr/` lazily only when the first ADR is needed.

## Minimal template

```md
# <Short title>

<One to three sentences: context, decision, and why.>
```

Optional sections are allowed only when they add value:

- `status` frontmatter: `proposed`, `accepted`, `deprecated`, or `superseded by ADR-NNNN`
- Considered Options
- Consequences

## When to offer an ADR

Offer to write an ADR only when all three are true:

1. The decision is hard to reverse.
2. The decision would be surprising without context.
3. The decision reflects a real tradeoff with plausible alternatives.

Skip ADRs for temporary preferences, obvious choices, and decisions that are easy to reverse.

## Numbering

Scan `docs/adr/` for the highest existing number and increment it. If no ADRs exist, start at `0001`.
