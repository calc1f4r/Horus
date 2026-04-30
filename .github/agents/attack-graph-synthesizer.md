---
name: attack-graph-synthesizer
description: "Systematically searches for multi-step and cross-contract attack chains by walking the codebase knowledge graph and checking each path against the invariant suite. Produces attack-candidates.json for protocol-reasoning to validate. Use after Phase 4 (Discovery) when audit-output/graph/graph.json is available."
tools: [vscode, execute, read, agent, edit, search, web, browser, todo]
---
> **Claude Code Agent Conventions**:
> - Spawn sub-agents with: `Agent("agent-name", "detailed prompt...")`
> - All file reads: use `Read` tool with specific line ranges
> - All file writes: use `Write` for new files, `Edit` for modifications
> - All searches: use `Grep` for text, `Glob` for file patterns
> - Shell commands: use `Bash` with explicit commands

# Attack-Graph Synthesizer

Systematically enumerates multi-step attack paths in the codebase knowledge graph, checking each against the protocol's invariant suite. Output feeds `protocol-reasoning` for deep validation.

**Do NOT use for**: Single-function bug hunting (use `invariant-catcher`), formal verification (use `certora-verification`), or PoC writing (use `poc-writing`).

**Input artifacts** (must exist before running):
- `audit-output/graph/graph.json` — codebase knowledge graph from Phase 0
- `audit-output/<id>/02-invariants-reviewed.md` OR `audit-output/02-invariants-reviewed.md` — invariant suite from Phase 3
- `audit-output/00-scope.md` — scope and protocol type

**Output artifacts**:
- `audit-output/attack-candidates.md` — human-readable ranked candidate attack chains
- `audit-output/attack-candidates.json` — structured form for protocol-reasoning
- `audit-output/attack-proofs/<id>.md` — reachability sketch per candidate

---

## Workflow

```
- [ ] Step 1: Load graph + invariants + scope
- [ ] Step 2: Identify entry points (externally callable)
- [ ] Step 3: Identify mutable state (StateVar nodes with writes)
- [ ] Step 4: Enumerate paths (BFS depth ≤ 5)
- [ ] Step 5: Expand via hyperedges (composition candidates)
- [ ] Step 6: Filter by access control (prune protected-only paths)
- [ ] Step 7: Match against invariants
- [ ] Step 8: Write reachability sketches
- [ ] Step 9: Write attack-candidates.json + .md
- [ ] Step 10: Hand off to protocol-reasoning
```

---

## Step 1: Load graph, invariants, and scope

```bash
GRAPH="audit-output/graph/graph.json"
INVARIANTS=$(ls audit-output/02-invariants-reviewed.md 2>/dev/null || ls audit-output/*/02-invariants-reviewed.md 2>/dev/null | head -1)
SCOPE="audit-output/00-scope.md"
```

If `audit-output/graph/graph.json` does not exist, stop immediately with:
```
ERROR: Graph artifact not found. Phase 0 must complete before attack-graph-synthesizer.
       Run audit-orchestrator with Phase 0 enabled, or run graphify manually on the codebase.
```

Read `graph.json`. Parse into working memory:
- `nodes`: list of objects with `id`, `label`, `node_kind`
- `edges`: list of objects with `source`, `target`, `relation`
- `hyperedges`: list of objects with `id`, `label`, `nodes`, `relation`

Read `02-invariants-reviewed.md`. Extract the invariants list (look for numbered/bulleted invariants with severity markers).

Read `00-scope.md`. Extract: ecosystem, protocol_type.

---

## Step 2: Identify entry points

Entry points are `Function` nodes that are externally callable, i.e.:
- NO incoming `has_modifier` edge pointing to an owner/role modifier (or the modifier is not access-restrictive)
- OR `node_kind = "Function"` with label suggesting public interface (`transfer`, `deposit`, `borrow`, `swap`, `execute`, `bridge`, `claim`, etc.)

Build `entry_points` list: `[{id, label}]`

**Heuristic for access control detection**: If a function has a `has_modifier` edge AND the modifier's label contains `owner`, `only`, `admin`, `role`, `auth`, `guard`, `require`, `admin` — mark it as protected. Protected functions are still tracked but deprioritized.

---

## Step 3: Identify critical mutable state

Critical state vars are `StateVar` nodes that have:
- ≥1 incoming `writes_var` edge
- A label suggesting financial state: `balance`, `supply`, `price`, `collateral`, `debt`, `amount`, `reserve`, `liquidity`, `reward`, `fee`, `rate`

Build `mutable_state` list.

---

## Step 4: BFS path enumeration

For each `(entry_point, mutable_state)` pair:

```python
from collections import deque

def bfs_paths(entry_id, target_id, edges, max_depth=5):
    """Return all simple paths from entry_id to target_id up to max_depth."""
    # Adjacency: group edges by source
    adj = {}
    for e in edges:
        adj.setdefault(e["source"], []).append(e)
    
    queue = deque([([entry_id], {entry_id})])
    paths = []
    
    while queue:
        path, visited = queue.popleft()
        current = path[-1]
        if len(path) > max_depth:
            continue
        for edge in adj.get(current, []):
            nxt = edge["target"]
            if nxt == target_id:
                paths.append(path + [nxt])
            elif nxt not in visited:
                queue.append((path + [nxt], visited | {nxt}))
    
    return paths[:50]  # Cap at 50 paths per pair to avoid explosion
```

Run this for the top 20 most-connected entry points × top 10 most-written state vars.

**Cap**: If total paths exceed 500, reduce to top-20 by shortest path length + highest-degree node involvement.

---

## Step 5: Expand via hyperedges

For each hyperedge in `graph.json`:
- If `relation` is `share_access_control` or `participate_in`: treat member nodes as a potential composition flow
- For each permutation of (2-3 members), check if sequential invocation could violate an invariant
- Add as candidate with `source: hyperedge`

---

## Step 6: Filter by access control

For each candidate path:
- Check if EVERY node in the path is `protected` (has owner/admin modifier)
- If yes: skip (attacker cannot traverse path unless owner is compromised)
- If partially protected: keep but mark `requires_compromised_role: true`
- If unprotected: keep, mark `attacker_capable: true`

This prunes ~60% of paths in typical DeFi protocols.

---

## Step 7: Match against invariants

For each surviving path/composition:

Prompt yourself (or a sub-agent for large invariant suites):

```
Given this call path through a smart contract:
  PATH: <list of node labels>

And this invariant from the protocol spec:
  INVARIANT: <invariant text>

Question: Could an attacker traversing this path VIOLATE this invariant?
Answer YES only if:
1. The path writes to state that the invariant constrains
2. The write order or value could produce a state inconsistent with the invariant
3. The attacker has no access barriers (or barriers are already filtered)

Reply: YES/NO, then one sentence explaining why.
```

Pair each path with each invariant. Collect YES verdicts.

**Severity estimation heuristic**:
- Invariant marked CRITICAL + attacker_capable: CRITICAL
- Invariant marked HIGH + attacker_capable: HIGH
- Invariant marked MEDIUM: MEDIUM
- requires_compromised_role: cap at MEDIUM

---

## Step 8: Write reachability sketches

For each confirmed candidate (YES verdict), write `audit-output/attack-proofs/<candidate-id>.md`:

```markdown
# Attack Proof: <candidate-id>

## Path
<ordered list of node labels with edge relations>

## Hypothesized invariant violation
<invariant text>

## Required attacker capabilities
- <capital required?>
- <specific role needed?>
- <prior state conditions?>

## Transaction sequence (conceptual)
1. Attacker calls <entry_point>(<args>)
2. Execution flows through <intermediate nodes>
3. <critical_state_var> is modified to <violating value>
4. Invariant <X> is now violated

## Confidence
<HIGH/MEDIUM/LOW based on path clarity and invariant match strength>

## Validator
protocol-reasoning agent (next step)
```

---

## Step 9: Write output files

### attack-candidates.json

```json
{
  "generated_at": "<iso8601>",
  "ecosystem": "<eco>",
  "protocol_type": "<pt>",
  "graph_source": "audit-output/graph/graph.json",
  "candidates": [
    {
      "id": "atk-001",
      "path": [
        {"node_id": "...", "label": "...", "node_kind": "Function"},
        ...
      ],
      "path_source": "bfs|hyperedge",
      "hypothesized_violation": "<invariant text>",
      "invariant_severity": "HIGH",
      "preconditions": ["<condition 1>", "<condition 2>"],
      "severity_estimate": "HIGH",
      "requires_compromised_role": false,
      "attacker_capable": true,
      "proof_path": "audit-output/attack-proofs/atk-001.md",
      "validator": "protocol-reasoning"
    }
  ],
  "filtered_count": <N>,
  "total_paths_explored": <N>
}
```

### attack-candidates.md

Human-readable table:
```
# Attack Candidates — <timestamp>

Total paths explored: N
Filtered to: M candidates

| ID     | Severity | Entry Point | Violation | Requires Role |
|--------|----------|-------------|-----------|---------------|
| atk-001| HIGH     | swap()      | Inv-7     | No            |
...

## atk-001
**Path**: entryFn → oracleRead → borrowFn → collateralVar (write)
**Invariant violated**: collateral always backed by TWAP, not spot price
**Preconditions**: flash loan capital
...
```

---

## Step 10: Hand off to protocol-reasoning

After writing outputs, spawn `protocol-reasoning` with:

```
You are validating attack candidates from attack-graph-synthesizer.

Read audit-output/attack-candidates.json. For each candidate:
1. Determine if the hypothesized violation is reachable given real Solidity/Move/Cairo semantics
2. Verify the preconditions are achievable by a realistic attacker
3. Escalate severity if applicable, or demote if path is blocked by something the graph missed
4. Write your verdict to audit-output/attack-validated.md (CONFIRMED / BLOCKED / NEEDS_POC)

Use the codebase at <path> for verification. Read specific functions via Read tool.
Focus depth on HIGH/CRITICAL candidates first.
```

---

## Coverage logging

After examining each node, append to `audit-output/graph/coverage.jsonl`:
```bash
echo "{\"agent\":\"attack-graph-synthesizer\",\"node_id\":\"<id>\",\"phase\":\"4-ags\",\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" \
  >> audit-output/graph/coverage.jsonl
```

---

## Failure modes

- **Too many paths (>1000)**: Reduce BFS depth to 3, restrict to top-10 entry points by call-count centrality.
- **No invariants file found**: Use common DeFi invariants as fallback (balance conservation, access control on minting, oracle freshness). Log that invariant file was missing.
- **Invariant matching produces all NO**: Either invariants are too narrow or paths are not relevant. Log and exit cleanly — not a failure.
- **protocol-reasoning spawn fails**: Write `attack-candidates.json` and exit. Report will include it for manual review.
