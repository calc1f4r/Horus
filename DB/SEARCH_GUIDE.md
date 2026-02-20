# Vulnerability Database Search Guide

> **Audience**: AI agents performing variant analysis, security audits, and vulnerability research.  
> **Goal**: Get precise, targeted results from the vulnerability database with minimal context window usage.

---

## Architecture Overview

The database uses a **4-tier search architecture** that progressively narrows from broad categories to exact line ranges:

```
Tier 1:   DB/index.json                          (Router — ~350 lines, ~12KB)
   ↓      Identifies which manifests/huntcards to load
Tier 1.5: DB/manifests/huntcards/*-huntcards.json  (Hunt Cards — compressed detection rules)
   ↓      ALL 451 patterns fit in ~55K tokens. Grep-based bulk scanning.
Tier 2:   DB/manifests/<name>.json                 (Manifest — 30-130KB each)
   ↓      Full pattern metadata with line ranges, keywords, root causes
Tier 3:   DB/**/*.md                               (Vulnerability files — read only relevant lines)
```

### Tier 1.5: Hunt Cards (New)

Hunt cards are **compressed detection rules** — one card per vulnerability pattern, each ~5 lines. They solve the context window problem: instead of loading 200KB+ manifests to decide which patterns are relevant, an agent loads all hunt cards (~55K tokens) and greps the target codebase to prune irrelevant patterns.

Each hunt card:
```json
{
  "id": "general-defi-1-empty-market-exchange-rate-inflation-000",
  "title": "Empty Market Exchange Rate Inflation",
  "severity": "CRITICAL",
  "grep": "redeemUnderlying|totalSupply|transfer",
  "detect": "When a CompoundV2-fork cToken market has extremely low totalSupply...",
  "cat": ["defi"],
  "neverPrune": true,
  "ref": "DB/general/vault-inflation-attack/defihacklabs-vault-inflation-patterns.md",
  "lines": [66, 174]
}
```

**Key fields:**
- `grep` — pipe-delimited regex for `grep -rn` or `rg` against target code
- `detect` — one-line rule describing what makes code vulnerable
- `check` — 1-5 ordered verification steps to execute directly against grep hit locations (no .md read needed)
- `antipattern` — one-line code shape indicating vulnerability (quick positive match)
- `securePattern` — one-line code shape indicating safe code (quick false-positive elimination)
- `cat` — category tags for grouping (e.g., `defi`, `oracle`, `amm`, `bridge`)
- `neverPrune` — if `true`, card survives grep-prune even with zero hits (CRITICAL patterns)
- `ref` + `lines` — read full entry only for confirmed true/likely positives: `read_file(card.ref, startLine=card.lines[0], endLine=card.lines[1])`

**Files:**
- `DB/manifests/huntcards/all-huntcards.json` — ALL 451 cards in one file
- `DB/manifests/huntcards/<manifest>-huntcards.json` — per-manifest cards

### Why This Matters

| Approach | Context Cost | Precision |
|----------|-------------|----------|
| Old: Read index.json + full files | 5,000-15,000 lines | Low (noise dilutes findings) |
| Manifests: Router → Manifest → Targeted read | 200-500 lines | High (exact pattern + line range) |
| Hunt cards: Router → Hunt cards → Grep → Targeted read | 50-200 lines | Very High (only actual hits) |

| Scenario | Without Hunt Cards | With Hunt Cards |
|----------|-------------------|----------------|
| vault_yield audit (4 manifests) | ~384KB manifest JSON + 27K lines vuln content | ~20K tokens hunt cards → grep → read only hits |

---

## Search Workflows

### Workflow A: Protocol-Type Search (Most Common)

**When**: You know the protocol type (lending, DEX, vault, etc.)

```
1. Read DB/index.json → protocolContext.mappings.<protocol_type>
2. Get manifest list + focusPatterns
3. Load each manifest → search patterns matching focusPatterns
4. Read only lineStart-lineEnd of matching patterns
```

**Example**: Auditing a lending protocol
```
→ index.json: protocolContext.mappings.lending_protocol
  → manifests: ["oracle", "general-defi", "tokens", "general-security"]
  → focusPatterns: ["staleness", "price manipulation", "liquidation", ...]

→ Load DB/manifests/oracle.json
  → Search patterns for "staleness" → find pattern at L183-245 in PYTH_ORACLE file
  → read_file(PYTH_ORACLE, startLine=183, endLine=245)  ← exact vulnerability content
```

### Workflow B: Keyword Search

**When**: You have a specific function name, concept, or code pattern

```
1. Load DB/manifests/keywords.json
2. Find keyword → get manifest name(s)
3. Load manifest → search patterns by codeKeywords
4. Read matching line ranges
```

**Example**: Looking for `getPriceUnsafe` vulnerabilities
```
→ keywords.json: "getpriceunsafe" → ["oracle"]
→ Load DB/manifests/oracle.json
→ Search patterns where codeKeywords contains "getPriceUnsafe"
→ Found in PYTH_ORACLE L183-245, severity: MEDIUM
→ read_file(DB/oracle/pyth/PYTH_ORACLE_VULNERABILITIES.md, 183, 245)
```

### Workflow C: Category Browse

**When**: Exploring a broad vulnerability class

```
1. Read DB/index.json → manifests section
2. Choose relevant manifest by description
3. Load manifest → browse all patterns with titles + severity
4. Read patterns of interest
```

### Workflow D: Severity-Focused Search

**When**: Looking for high-severity patterns only

```
1. Load relevant manifest
2. Filter patterns where severity includes "HIGH" or "CRITICAL"
3. Read matching line ranges
```

### Workflow E: Bulk Hunt (Audit Mode — Recommended)

**When**: Running a full audit and need to check ALL relevant patterns against target code

```
1. Read DB/index.json → protocolContext.mappings.<protocol_type>
2. Get manifest list
3. Load hunt cards for those manifests:
   - Option A: Load per-manifest cards: DB/manifests/huntcards/<name>-huntcards.json
   - Option B: Load ALL cards: DB/manifests/huntcards/all-huntcards.json (~100K tokens)
4. For each card, grep target codebase for card.grep pattern:
   grep -rn "card.grep" <target_path> --include="*.sol"
5. Cards with `neverPrune: true` always survive (CRITICAL safety net)
6. Prune cards with zero grep hits (removes ~60-80% of patterns)
7. PARTITION surviving cards into shards of 50-80 cards (grouped by cat tag)
   - Separate neverPrune cards → duplicate to every shard
   - Target: each shard fits comfortably in one agent's context
8. SPAWN one sub-agent per shard (parallel):
   - Each agent gets: its shard cards + neverPrune cards + full target code + invariants
   - Each agent runs Pass 1 (micro-directives) + Pass 2 (evidence lookup)
   - Each agent writes to audit-output/03-findings-shard-<id>.md
9. MERGE all shard findings → deduplicate by root cause → 03-findings-raw.md
```

**Example**: Auditing an ERC4626 vault
```
→ index.json: vault_yield → manifests: ["tokens", "general-defi", "oracle", "unique"]
→ Load hunt cards for those 4 manifests (241 cards)
→ Grep target code for each card's grep pattern
→ Card "First Depositor / Inflation Attack" grep "totalSupply|convertToShares|totalAssets" → HIT in Vault.sol:45
→ Execute card.check steps against Vault.sol:45 → card.antipattern matches! (no .md read yet)
→ PASS 2: read_file("DB/tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md", 151, 393) ← full evidence
→ Compare against Vault.sol:45 → True positive!
```

### Workflow F: Micro-Directive Execution (Recommended for Full Audits)

**When**: Hunt cards have been grep-pruned and you want to verify surviving patterns efficiently

```
1. After grep-pruning, you have 80-120 surviving cards
2. For each surviving card with `check` steps:
   a. Read TARGET CODE at grep hit locations
   b. Execute each card.check step against the target code
   c. Quick-match with card.antipattern (vulnerable code shape)
   d. Quick-reject with card.securePattern (safe code shape)
   e. Classify: true positive / likely positive / false positive
3. ONLY for true/likely positives: read full .md entry via card.ref + card.lines
4. This cuts .md reads from ~100 to ~10-20 (80-90% reduction)
```

**Example**: Processing an oracle staleness card
```
→ Card: "Missing Staleness Check"
  grep hit in PriceOracle.sol:42
  check[0]: "VERIFY: updatedAt is checked against reasonable threshold"
  → Read PriceOracle.sol:35-55 → no updatedAt comparison found! FAIL
  check[1]: "Check startedAt > 0 validation exists" → FAIL
  antipattern: "No validation of updatedAt timestamp" → MATCH
  → Classified: TRUE POSITIVE
  → Now read DB/oracle/chainlink/CHAINLINK_PRICE_FEED_VULNERABILITIES.md:133-289 for evidence
```

---

## Available Manifests

| Manifest | File | Patterns | Focus |
|----------|------|----------|-------|
| `oracle` | DB/manifests/oracle.json | 39 | Chainlink, Pyth, price manipulation |
| `amm` | DB/manifests/amm.json | 65 | Concentrated liquidity, constant product AMMs |
| `bridge` | DB/manifests/bridge.json | 32 | LayerZero, Wormhole, Hyperlane, cross-chain |
| `tokens` | DB/manifests/tokens.json | 33 | ERC20, ERC4626, ERC721 |
| `cosmos` | DB/manifests/cosmos.json | 26 | Cosmos SDK, IBC, staking, precompiles |
| `solana` | DB/manifests/solana.json | 38 | Solana programs, Token-2022 |
| `general-security` | DB/manifests/general-security.json | 31 | Access control, signatures, validation |
| `general-defi` | DB/manifests/general-defi.json | 115 | Flash loans, vaults, precision, calculations |
| `general-infrastructure` | DB/manifests/general-infrastructure.json | 41 | Proxies, reentrancy, storage, bridges |
| `general-governance` | DB/manifests/general-governance.json | 56 | Governance, stablecoins, rug pulls, MEV |
| `unique` | DB/manifests/unique.json | 59 | Protocol-specific unique exploits |

---

## Pattern Entry Format

Each pattern in a manifest looks like:

```json
{
  "id": "oracle-staleness-check-001",
  "title": "1. CheckUpkeep/PerformUpkeep Mismatch",
  "lineStart": 93,
  "lineEnd": 248,
  "lineCount": 156,
  "severity": ["MEDIUM"],
  "codeKeywords": ["checkUpkeep", "performData", "performUpkeep"],
  "rootCause": "checkUpkeep returns data encoded in one format, but performUpkeep expects...",
  "subsections": [
    {
      "title": "Vulnerability Description",
      "lineStart": 102,
      "lineEnd": 115,
      "severity": ["MEDIUM"],
      "codeKeywords": ["checkUpkeep"]
    }
  ]
}
```

**Key fields for agents:**
- `lineStart` / `lineEnd` → Use with `read_file` for surgical access
- `severity` → Filter for HIGH/CRITICAL when prioritizing
- `codeKeywords` → Match against target codebase identifiers
- `rootCause` → Quick preview of the vulnerability without reading the file
- `subsections` → Drill into specific sub-patterns for even more precision

---

## Best Practices for Agents

### DO
- **Start with index.json** to route to the right manifest(s)
- **Load only relevant manifests** — don't load all 11
- **Use lineStart/lineEnd** to read only the exact section needed
- **Search by codeKeywords** to match against code identifiers you find in target
- **Check severity** to prioritize findings
- **Use protocolContext** to quickly get the right manifests for a protocol type

### DON'T
- Don't read entire vulnerability .md files (500-2400 lines) — use line ranges
- Don't load all manifests at once — pick 2-3 relevant ones
- Don't rely on filename alone — use pattern metadata for precision
- Don't skip the router — it tells you which manifests are relevant

### Context Window Efficiency

| Action | Context Cost | Value |
|--------|-------------|-------|
| Read full index.json (old) | ~3800 lines | Low (mostly noise) |
| Read new router | ~330 lines | High (routing decisions) |
| Load 1 manifest | 1000-4500 lines | Medium (pattern browsing) |
| Read 1 pattern (targeted) | 50-200 lines | Very High (exact content) |

**Ideal flow**: 330 lines (router) + 200 lines (manifest scan) + 150 lines (pattern read) = **680 lines** for a precise result.

---

## Exhaustive Search (Audit Mode)

When running a full audit via `audit-orchestrator`, use maximum-depth search:

### Strategy

1. **Load ALL manifests** relevant to the detected protocol type(s) — union manifests from all matched `protocolContext.mappings` entries
2. **Always include** `general-security` and `unique` as baseline manifests
3. **Keyword cross-check**: Load `DB/manifests/keywords.json`, scan target code for keyword hits, and add any newly-discovered manifests
4. **If no protocol detected**: Load all 11 manifests (fallback for unknown codebases)

### Per-Manifest Search Sequence

For each loaded manifest:

```
1. Parse all patterns → extract codeKeywords arrays
2. Build a combined regex: "keyword1|keyword2|keyword3|..."
3. Search target codebase: grep -rn "regex" <path> --include="*.sol"
4. For each hit:
   a. Record: pattern ID, target file, target line, matched keyword
   b. Score relevance: exact keyword match → HIGH, partial → MEDIUM
5. For HIGH-relevance hits:
   a. Read DB vulnerability content: read_file(DB/<path>.md, lineStart, lineEnd)
   b. Compare vulnerable pattern against target code
   c. Classify: true positive / likely positive / false positive
```

### Context Cost (Exhaustive)

| Action | Lines | Notes |
|--------|-------|-------|
| Read index.json | ~330 | One-time |
| Load keywords.json | ~500 | One-time keyword scan |
| Load 1 manifest | 1000-4500 | Per manifest |
| Read 1 matched pattern | 50-200 | Per HIGH-relevance hit |
| **Total for full audit** | ~5000-15000 | Spread across sub-agent context windows |

The orchestrator manages context budget by loading manifests one at a time, extracting keywords, then discarding the manifest before loading the next.

### Recommended: Hunt Card Approach for Exhaustive Audit

Instead of loading manifests one at a time, use hunt cards for maximum coverage with minimal context:

```
1. Load all hunt cards for resolved manifests (~100K tokens with micro-directives)
2. Batch grep: for each card, search target code for card.grep:
   grep -rn "keyword1|keyword2" <path> --include="*.sol"
3. Cards with `neverPrune: true` always survive (CRITICAL safety net)
4. Prune: discard remaining cards with zero grep hits (typically 60-80%)
5. PASS 1: Execute card.check steps against target code at grep hit locations
   - Use card.antipattern for quick positive matching
   - Use card.securePattern for quick false-positive elimination
6. PASS 2: For confirmed hits only, read full DB entries using card.ref + card.lines
7. Validate each confirmed hit against target code
```

This approach lets an agent hold ALL vulnerability detection patterns AND verification logic in context simultaneously — impossible with full manifests.

### Context Cost (Hunt Card Approach)

| Action | Tokens | Notes |
|--------|--------|-------|
| Read index.json | ~3K | One-time routing |
| Load all hunt cards (1 file) | ~100K | ALL 451 patterns with micro-directives |
| Grep target code | 0 | Run in terminal |
| Pass 1: micro-directive execution | 0 | Uses card.check against already-read target code |
| Pass 2: read matched DB entries | ~5-15K | Only for confirmed hits (~10-20 patterns) |
| **Total** | **~105-120K** | Leaves room for target codebase |

---

## Regenerating Manifests

When vulnerability files are added or updated, re-run:

```bash
python3 generate_manifests.py
```

This will:
1. Re-parse all `.md` files in `DB/`
2. Re-generate all manifests with updated patterns and line ranges
3. Re-generate all hunt cards in `DB/manifests/huntcards/`
4. Update the router `index.json`
5. Back up the previous index
