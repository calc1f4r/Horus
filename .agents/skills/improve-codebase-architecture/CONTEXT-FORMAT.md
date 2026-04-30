# CONTEXT.md Format

Use `CONTEXT.md` to record project-specific domain language that should guide module naming and seam placement.

## Single-context repos

Use a root `CONTEXT.md`.

```md
# <Context Name>

<One or two sentences describing what this context is and why it exists.>

## Language

**Order**:
<One-sentence definition.>
_Avoid_: Purchase, transaction

**Invoice**:
<One-sentence definition.>
_Avoid_: Bill, payment request

## Relationships

- An **Order** produces one or more **Invoices**
- An **Invoice** belongs to exactly one **Customer**

## Example dialogue

> **Dev:** "When a **Customer** places an **Order**, do we create the **Invoice** immediately?"
> **Domain expert:** "No. An **Invoice** is generated after **Fulfillment**."

## Flagged ambiguities

- "account" was used for both **Customer** and **User**. Resolved: these are distinct.
```

## Multi-context repos

Use a root `CONTEXT-MAP.md` that points to context-specific files.

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) - receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) - creates invoices and payments

## Relationships

- **Ordering -> Billing**: Ordering emits events consumed by Billing
```

## Rules

- Add only domain concepts specific to this repo.
- Do not add generic programming terms.
- Prefer one precise term and list aliases to avoid.
- Keep definitions to one sentence.
- Show important relationships and cardinality when known.
- Flag ambiguous terms explicitly with the chosen resolution.
- Create `CONTEXT.md` lazily only when a review or grilling loop resolves a load-bearing term.
