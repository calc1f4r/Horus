# DB-Powered Hunting Workflow

Single source of truth for hunt card operations. Used by `audit-orchestrator` (Phase 4) and `invariant-catcher` (shard mode + standalone).

## Contents
- [Hunt Card Format](#hunt-card-format)
- [Step 1: Grep-Prune](#step-1-grep-prune)
- [Step 2: Partition into Shards](#step-2-partition-into-shards)
- [Step 3: Micro-Directive Execution](#step-3-micro-directive-execution)
- [Step 4: Merge Shard Findings](#step-4-merge-shard-findings)
- [Finding Schema](#finding-schema)

---

## Hunt Card Format

Each card is a compressed detection rule (~200 tokens) with micro-directives:

```json
{
  "id": "tokens-erc4626-001",
  "title": "First Depositor / Inflation Attack",
  "severity": "CRITICAL",
  "grep": "totalSupply|convertToShares|totalAssets",
  "detect": "Share value inflatable when totalSupply approaches zero",
  "check": [
    "VERIFY: deposit function handles totalSupply == 0 case",
    "VERIFY: virtual shares/assets or dead shares used"
  ],
  "antipattern": "convertToShares returns totalSupply == 0 ? shares : ...",
  "securePattern": "Virtual offset in share calculation OR dead shares in constructor",
  "cat": ["token", "erc4626"],
  "ref": "DB/tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md",
  "lines": [151, 393],
  "neverPrune": true
}
```

| Field | Purpose |
|-------|---------|
| `grep` | Pipe-delimited keywords for initial pruning |
| `check` | Ordered verification steps — execute against target code |
| `antipattern` | Vulnerable code shape — if matched → likely positive |
| `securePattern` | Safe code shape — if matched → false positive |
| `neverPrune` | Card survives grep-prune even with zero hits |
| `ref` + `lines` | Full DB entry for evidence lookup |

---

## Step 1: Grep-Prune

Run each card's `grep` pattern against the target codebase. Cards with zero hits are pruned.

**Using the utility script** (preferred):
```bash
python3 scripts/grep_prune.py <target_path> DB/manifests/huntcards/all-huntcards.json --output audit-output/hunt-card-hits.json
```

**Manual equivalent**:
```bash
grep -rn "card.grep" <path> --include="*.sol" --include="*.rs" --include="*.go" --include="*.move" --include="*.cairo" --include="*.vy" -l
```

Rules:
- Cards with `neverPrune: true` ALWAYS survive, even with zero hits
- Typically eliminates 60-80% of cards
- Output: `audit-output/hunt-card-hits.json`

---

## Step 2: Partition into Shards

Split surviving cards into shards of 50-80, grouped by `cat` tag.

**Using the utility script** (preferred):
```bash
python3 scripts/partition_shards.py audit-output/hunt-card-hits.json --output audit-output/hunt-card-shards.json
```

**Or use pre-computed bundles** (faster, when protocol type is known):
```
DB/manifests/bundles/<protocol_type>-shards.json
```

Rules:
- `neverPrune` cards → "critical set" duplicated to EVERY shard
- Large groups (>80 cards) → split into sub-shards of ~60
- Small groups (<20 cards) → merged into combined shards
- Output: `audit-output/hunt-card-shards.json`

---

## Step 3: Micro-Directive Execution

Each shard sub-agent runs a 2-pass analysis:

### Pass 1: Quick Classification (no .md reads)

For each card in the shard at grep hit locations:
1. Read TARGET CODE at the grep hit location
2. Execute each `check` step against the target code
3. If `antipattern` matches → **likely positive** (fast path)
4. If `securePattern` matches → **false positive** (prune immediately)
5. If neither → **uncertain** (proceed to Pass 2)

### Pass 2: Evidence Lookup (only for true/likely positives)

For confirmed/uncertain matches only:
```
read_file(card.ref, startLine=card.lines[0], endLine=card.lines[1])
```
Compare the full DB entry's vulnerable pattern against target code. Classify:
- **TRUE POSITIVE**: Code matches the vulnerable pattern exactly
- **LIKELY POSITIVE**: Code partially matches, needs manual review
- **FALSE POSITIVE**: Code uses the secure pattern or doesn't apply

### Feedback Loop (quality gate)

After processing all cards:
1. **Zero HIGH/CRITICAL findings AND >50% cards processed?** → Re-check top 10 highest-severity cards (may have filtered too aggressively)
2. **>20 true positives from 50 cards?** → Too many matches. Re-apply `securePattern` filters more strictly.

---

## Step 4: Merge Shard Findings

After all shard sub-agents return, merge results.

**Using the utility script** (preferred):
```bash
python3 scripts/merge_shard_findings.py audit-output/
```

**Manual merge**:
1. Read all `audit-output/03-findings-shard-*.md`
2. Deduplicate: same code line + same root cause → keep higher confidence
3. Renumber: F-001, F-002, ...
4. Write: `audit-output/03-findings-raw.md` + `audit-output/03-merge-log.md`

---

## Finding Schema

Every finding across all phases MUST use this format:

```markdown
### F-NNN: [Title]

| Field | Value |
|-------|-------|
| **Severity** | CRITICAL / HIGH / MEDIUM / LOW |
| **Confidence** | HIGH / MEDIUM / LOW |
| **Affected Code** | `ContractName.functionName()` (file:line) |
| **Root Cause** | One-sentence description |
| **DB Reference** | `DB/category/file.md` lines X-Y |
| **Shard** | shard-N-category (if applicable) |

**Description**: [2-3 sentences explaining the vulnerability]

**Evidence**:
[Code snippet from target showing the vulnerable pattern]

**Expected Secure Pattern**:
[What the code should look like based on card.securePattern or DB entry]
```
