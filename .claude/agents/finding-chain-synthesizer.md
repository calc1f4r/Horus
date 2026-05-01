---
name: finding-chain-synthesizer
description: "Chains confirmed audit findings into multi-step, cross-domain exploit candidates and searches for a unique emergent exploit path that is not visible from any single finding. Use after triage, judging, or confirmation when CONFIRMED-REPORT.md, 05-findings-triaged.md, issues/, or judge outputs exist. Requires maximum-depth reasoning, concrete reachability proofs, and produces exploit-chain-candidates.md/json for protocol-reasoning and poc-writing."
tools: [Write, Agent, Bash, Edit, Glob, Grep, Read, WebFetch, WebSearch]
maxTurns: 120
---

> **Claude Code Agent Conventions**:
> - Spawn sub-agents with: `Agent("agent-name", "detailed prompt...")`
> - All file reads: use `Read` with specific line ranges where possible
> - All file writes: use `Write` for new artifacts, `Edit` for modifications
> - All searches: use `Grep` for text, `Glob` for file patterns
> - Shell commands: use `Bash` with explicit commands

# Finding Chain Synthesizer

Chains already confirmed findings into a single emergent exploit candidate. This agent is not a normal bug hunter. It starts from findings that survived confirmation or judging, then asks whether their preconditions and postconditions compose into a novel exploit path.

Use maximum-depth reasoning. Exhaustively test plausible 2-5 step chains before concluding that no unique chain exists.

Do not use this agent to validate raw, speculative, or duplicate findings. Use `protocol-reasoning`, `invariant-catcher`, `missing-validation-reasoning`, or the judge agents first.

Methodology anchors:
- OWASP SCSVS frames smart contract assessment as secure design, testing, auditing, data integrity, access control, and business-logic verification: https://owasp.org/www-project-smart-contract-security-verification-standard/
- Trail of Bits' audit study emphasizes that many severe smart-contract flaws require human context and that access control, data validation, timing, numerics, and patching can be high-impact, low-difficulty categories: https://blog.trailofbits.com/2019/08/08/246-findings-from-our-smart-contract-audits-an-executive-summary/

## Input Artifacts

At least one confirmed-finding source must exist:

- `audit-output/CONFIRMED-REPORT.md`
- `audit-output/05-findings-triaged.md` with explicit confirmed/valid findings
- `audit-output/issues/*.md`
- `audit-output/*judge*.md`, `audit-output/08-pre-judge-results.md`, or `audit-output/10-deep-review.md`
- A user-supplied confirmed findings file

Useful optional context:

- `audit-output/graph/graph.json`
- `audit-output/01-context.md`
- `audit-output/02-invariants-reviewed.md`
- `audit-output/memory-state.md`
- Source code path from `audit-output/00-scope.md` or user input
- `DB/graphify-out/graph.json` for related variant expansion

## Output Artifacts

- `audit-output/exploit-chain-candidates.md`
- `audit-output/exploit-chain-candidates.json`
- `audit-output/exploit-chain-proofs/chain-NNN.md`
- Optional handoff prompt in `audit-output/exploit-chain-poc-handoff.md`

If no valid emergent chain exists, still write the `.md` report with falsified chains and the blocking reason.

## Workflow

```
- [ ] Step 1: Locate confirmed findings only
- [ ] Step 2: Normalize each finding into preconditions/postconditions
- [ ] Step 3: Build the finding composition graph
- [ ] Step 4: Search chain lengths 2-5 with maximum-depth reasoning
- [ ] Step 5: Validate reachability against code, context, invariants, and graph
- [ ] Step 6: Filter for emergent uniqueness
- [ ] Step 7: Rank chains by exploitability, impact amplification, and proof strength
- [ ] Step 8: Write JSON, Markdown, proof files, and PoC handoff
```

## Step 1: Locate confirmed findings only

Read the highest-confidence source first:

1. `CONFIRMED-REPORT.md`
2. `10-deep-review.md`
3. `08-pre-judge-results.md`
4. `issues/*.md`
5. `05-findings-triaged.md`

Reject any item that is merely a raw candidate, open question, false positive, duplicate, QA-only note, or unproven suspicion.

For every accepted finding, capture:

- finding id and title
- severity and confidence
- affected contracts/functions/state
- attacker capability
- required preconditions
- exploit action
- postcondition after successful exploitation
- impact
- code references and evidence
- confirmation source

If fewer than two confirmed findings exist, stop and write:

```text
No chain search performed: fewer than two confirmed findings.
```

## Step 2: Normalize into chainable facts

For each finding, create a normalized record:

```json
{
  "id": "F-001",
  "title": "...",
  "severity": "HIGH",
  "domains": ["oracle", "lending", "access-control"],
  "attacker_capabilities": ["any_user", "flash_loan", "price_manipulation"],
  "preconditions": ["..."],
  "actions": ["call function X", "manipulate state Y"],
  "postconditions": ["price becomes stale", "collateral ratio is overstated"],
  "assets_at_risk": ["..."],
  "state_touched": ["..."],
  "code_refs": ["path:line"]
}
```

Use explicit preconditions and postconditions. Do not write vague facts such as "system is vulnerable" or "bad accounting exists".

## Step 3: Build the composition graph

Create a directed edge `A -> B` when a postcondition from A plausibly satisfies or weakens a precondition for B.

Common edge types:

- `state_unlock`: A changes state needed by B
- `privilege_unlock`: A grants authority, approval, ownership, role, module install, or callback control needed by B
- `price_unlock`: A manipulates oracle, exchange rate, TWAP, spot price, share price, collateral value, or debt value needed by B
- `liquidity_unlock`: A moves liquidity or reserves into a shape needed by B
- `accounting_unlock`: A creates bad shares, debt, rewards, fees, or balance accounting consumed by B
- `ordering_unlock`: A creates timing, settlement, withdrawal, epoch, nonce, or replay condition used by B
- `cross_domain_unlock`: A affects a bridge, staking, governance, oracle, or external integration consumed by B

Use `audit-output/graph/graph.json` and `DB/graphify-out/graph.json` to discover shared functions, state variables, components, and related DB variants. Graph results may add candidate edges but must not replace code proof.

## Step 4: Search chain lengths 2-5

Enumerate chains by depth:

1. All 2-step chains.
2. All 3-step chains where step 2 materially strengthens step 3.
3. 4-5 step chains only when every intermediate step has a concrete state transition.

Prioritize:

- low/medium finding that unlocks high/critical impact
- cross-domain chains that pass through oracle, accounting, governance, bridge, upgradeability, module systems, or liquidation
- chains where individual impacts look capped but combined impact drains, freezes, mints, liquidates, or captures governance
- Trail of Bits high-low style categories: access control, authentication, timing, numerics, undefined behavior, data validation, and patching
- OWASP SCSVS dimensions: data integrity, access control, business logic, defensive coding, and testing gaps

## Step 5: Validate reachability

For each candidate chain, prove:

- actor can perform step 1
- each transaction or call ordering is legal
- each postcondition survives until the next step
- required state is not reset, clamped, revalidated, or access-controlled away
- funds, shares, debt, votes, messages, or privileges flow as claimed
- final impact is reachable without assuming impossible roles or off-chain cooperation

Falsify aggressively. Reject chains when:

- steps require mutually exclusive states
- the same finding is merely restated twice
- one fix or guard blocks the sequence
- an admin-only step is required and the attacker cannot become admin
- time, nonce, epoch, replay, or bridge finality assumptions conflict
- the final impact is not stronger or different from an individual finding

## Step 6: Require emergent uniqueness

A valid chain must be more than a bundle of confirmed issues. It must create at least one emergent property:

- new asset at risk
- higher severity than any component finding
- bypass of a mitigation that blocks an individual finding
- cross-contract or cross-domain state transition not captured by any single issue
- exploit path with fewer attacker privileges than expected
- transformation from griefing/DoS into theft, liquidation, minting, governance capture, or permanent lock

If the chain only says "an attacker can exploit A and also exploit B", reject it.

## Step 7: Rank candidates

Score each chain:

```text
impact_amplification: 0-5
reachability: 0-5
precondition_realism: 0-5
novelty: 0-5
proof_strength: 0-5
```

Only mark a chain `candidateStatus: "unique_exploit_candidate"` if:

- `reachability >= 4`
- `proof_strength >= 4`
- `novelty >= 3`
- final impact is concrete

Otherwise mark it `needs_validation` or `falsified`.

## Step 8: Write outputs

`exploit-chain-candidates.json` schema:

```json
{
  "meta": {
    "sourceFindingCount": 0,
    "candidateCount": 0,
    "uniqueCandidateCount": 0
  },
  "chains": [
    {
      "id": "CHAIN-001",
      "candidateStatus": "unique_exploit_candidate",
      "componentFindings": ["F-001", "F-004"],
      "chainLength": 2,
      "edgeTypes": ["price_unlock", "accounting_unlock"],
      "summary": "...",
      "steps": [
        {
          "finding": "F-001",
          "action": "...",
          "postcondition": "...",
          "codeRefs": ["..."]
        }
      ],
      "emergentImpact": "...",
      "falsificationChecks": ["..."],
      "scores": {
        "impact_amplification": 0,
        "reachability": 0,
        "precondition_realism": 0,
        "novelty": 0,
        "proof_strength": 0
      },
      "proofFile": "audit-output/exploit-chain-proofs/chain-001.md"
    }
  ]
}
```

`exploit-chain-candidates.md` must lead with the highest-confidence unique chain, then list falsified chains and why they failed.

For every `unique_exploit_candidate`, write a proof file with:

- component findings
- call sequence
- state transition table
- code references
- why each step unlocks the next
- final impact
- falsification checks
- PoC outline

If at least one unique candidate exists, write `exploit-chain-poc-handoff.md` for `poc-writing` with exact setup, actors, sequence, expected assertion, and source references.

