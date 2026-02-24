---
name: defihacklabs-indexing
description: 'Analyzes DeFiHackLabs exploit PoCs and README documentation to extract vulnerability patterns, attack vectors, and root causes. Creates TEMPLATE.md-compliant database entries with verified attack mechanics from real-world exploits. Use when indexing DeFi exploits from DeFiHackLabs, creating vulnerability entries from PoC code, or building pattern databases from historical incidents.'
tools: ['vscode', 'execute', 'read', 'edit', 'search', 'web', 'agent','todo']
---

# DeFiHackLabs Exploit Indexer

Analyzes real-world DeFi exploit PoCs from DeFiHackLabs to extract verified vulnerability patterns and create TEMPLATE.md-compliant database entries.

**Do NOT use for** analyzing audit reports (use `Variant-Template-writer`), general codebase exploration (use `audit-context-building`), or writing PoCs from scratch (use `poc-writer-agent`).

---

## Source Structure

```
DeFiHackLabs/
├── past/{year}/README.md          # Exploit metadata (date, protocol, loss, links)
├── src/test/{YYYY-MM}/*_exp.sol   # Exploit PoCs (Foundry tests)
└── script/Exploit-template*.sol   # Template reference
```

Each PoC file header contains: `@KeyInfo` (loss, attacker, contracts, tx), `@Info` (vulnerable code), `@Analysis` (post-mortems).

---

## Workflow

Copy this checklist and track progress:

```
Indexing Progress:
- [ ] Phase 1: Extract metadata from README + PoC header
- [ ] Phase 2: Deep-read PoC code — document attack steps with line refs
- [ ] Phase 3: Apply root cause analysis (5 questions + falsification)
- [ ] Phase 4: Abstract pattern (Level 0 → Level 2 minimum)
- [ ] Phase 5: Create TEMPLATE.md-compliant entry
- [ ] Phase 6: Verification gate — every claim has source evidence
- [ ] Phase 7: Regenerate manifests
```

### Phase 1: Metadata Extraction

For each exploit, extract from README and PoC header:

| Field | Source |
|-------|--------|
| Date | README title (`YYYYMMDD`) |
| Protocol | README title |
| Vulnerability type | README title |
| Loss amount | README "Lost:" line |
| Chain | PoC `createSelectFork` argument |
| Attacker / Attack contract / Vulnerable contract | PoC `@KeyInfo` header |
| Attack TX | PoC `@KeyInfo` header |
| Post-mortem links | README "Link reference" + PoC `@Analysis` |

### Phase 2: PoC Deep Analysis

Read the ENTIRE PoC file. For each function:

1. **Document attack steps as numbered sequence** with line references (L45-L50)
2. **Identify the critical exploit moment** — which line triggers the vulnerability?
3. **Trace data flow** — how does value move from victim to attacker?
4. **Note prerequisites** — flash loans, specific token holdings, timing requirements

For ultra-granular per-function microstructure analysis, follow [OUTPUT_REQUIREMENTS.md](resources/OUTPUT_REQUIREMENTS.md) and verify against [COMPLETENESS_CHECKLIST-CONTEXT.md](resources/COMPLETENESS_CHECKLIST-CONTEXT.md).

### Phase 3: Root Cause Analysis

Apply the [root cause analysis framework](resources/root-cause-analysis.md):
1. Answer all 5 critical questions with evidence from the PoC code
2. Formulate the root cause statement
3. Score confidence (HIGH/MEDIUM/LOW)
4. Run the falsification protocol — actively try to disprove the finding

### Phase 4: Pattern Abstraction

Apply the [pattern abstraction ladder](resources/pattern-abstraction-ladder.md):
- **Level 0**: Document exact exploit code with source reference
- **Level 1**: Generalize to code pattern (replace protocol-specific names)
- **Level 2**: Identify vulnerability class family
- **Level 3**: State the violated security principle

### Phase 5: Database Entry Creation

Create a TEMPLATE.md-compliant entry. See [TEMPLATE.md](../../TEMPLATE.md) for exact structure and [Example.md](../../Example.md) for a complete reference.

Map vulnerability types using the [taxonomy](resources/vulnerability-taxonomy.md).

Optimize text for vector search using the [search optimization guide](resources/vector-search-optimization.md).

### Phase 6: Verification Gate

**Every entry must pass ALL checks before finalization.**

```
Verification Gate:
- [ ] Every code example extracted from actual PoC (no synthetic code)
- [ ] Loss amount matches README exactly
- [ ] Vulnerability type describes the actual root cause (not just symptoms)
- [ ] Attack steps match PoC execution order (verified line-by-line)
- [ ] All references link to real post-mortems/analyses
- [ ] Root cause statement passes falsification protocol
- [ ] Confidence score assigned and justified
- [ ] Detection patterns derived from actual exploit code
- [ ] Secure implementation actually fixes the root cause
- [ ] No vague claims — every statement has a code reference (L45, L98-102)
```

### Phase 7: Regenerate Manifests

After creating the entry, regenerate the search manifests:

```bash
python3 generate_manifests.py
```

This auto-updates `DB/index.json` and all `DB/manifests/*.json` files. See the [manifest update guide](resources/index-update-guide.md) for verification steps.

---

## Evidence Requirements for 99.99% Confidence

### Source Traceability

Every claim in the database entry must trace to a specific source:

| Claim type | Required evidence |
|------------|------------------|
| Vulnerability exists | Exact line numbers in PoC showing the exploit |
| Loss amount | README "Lost:" line verbatim |
| Root cause | Specific missing check/validation identified in vulnerable contract |
| Attack path | Step-by-step from PoC with L-references |
| Impact | On-chain TX hash or PoC assertion proving profit |

### Cross-Validation

When multiple exploits share a pattern:
- Document each instance independently first
- Then synthesize — note agreement AND disagreement
- Flag outliers explicitly: "5/6 exploits use flash loans; 1 uses accumulated funds"

### Anti-Hallucination Rules

1. **NEVER invent exploit details** — only document what's in the PoC
2. **NEVER assume attack mechanics** — verify by reading actual code
3. **NEVER overstate severity** — use actual loss amounts, not hypotheticals
4. **NEVER create synthetic code examples** — extract from real exploits
5. **Quote, don't paraphrase** — use actual variable/function names from the PoC

If uncertain about any detail, write: "Unclear from PoC — requires on-chain TX analysis" rather than guessing.

---

## Batch Processing

When processing multiple exploits, group by vulnerability type first (e.g., all reentrancy exploits together). This reveals cross-exploit patterns. Process chronologically within each group to track attack evolution.

Prioritize by loss amount — high-impact exploits first.

---

## Output Structure

Each analyzed exploit produces:

1. **Database entry** → `DB/{category}/{subcategory}/{pattern-name}.md` (TEMPLATE.md format)
2. **Manifest regeneration** → Run `python3 generate_manifests.py` to update all manifests

---

## Critical Rules

**MUST**: Read actual PoC code. Verify loss amounts. Document all prerequisites. Use real code snippets. Apply falsification protocol. Run `python3 generate_manifests.py` after creating entries.

**NEVER**: Hallucinate exploit details. Overstate severity. Skip PoC analysis (README alone is insufficient). Create synthetic examples. Use vague descriptions. Skip index updates.

Deep understanding of one exploit is more valuable than shallow coverage of many. Accuracy is paramount — this database drives future vulnerability discovery.
