# Manifest Update Guide

Every new or modified vulnerability entry MUST have its manifests regenerated so the 3-tier search architecture stays current.

## Architecture Overview

The database uses a **3-tier search architecture**:

```
Tier 1: DB/index.json              ← Lean router (~330 lines). Agents start here.
   ↓
Tier 2: DB/manifests/<name>.json   ← Pattern-level indexes with line ranges (11 manifests)
   ↓
Tier 3: DB/**/*.md                 ← Vulnerability content. Read ONLY targeted line ranges.
```

Manifests are **auto-generated** from the MD files. You do NOT manually edit `DB/index.json` or `DB/manifests/*.json`.

## How to Update After Creating/Modifying an Entry

### Step 1: Create, Edit, Or Migrate the Vulnerability MD File

Place the file in the correct category folder:

| Category | Path |
|----------|------|
| Oracle | `DB/oracle/{provider}/` |
| AMM | `DB/amm/{type}/` |
| Bridge | `DB/bridge/{protocol}/` |
| Tokens | `DB/tokens/{standard}/` |
| Cosmos | `DB/cosmos/{type}/` |
| Solana | `DB/Solona-chain-specific/` |
| General | `DB/general/{vulnerability-class}/` |
| Unique | `DB/unique/{category}/` |

Follow [TEMPLATE.md](../../../TEMPLATE.md) for structure. When touching a legacy entry, migrate it using [entry-migration-guide.md](entry-migration-guide.md) instead of preserving the older layout. Treat `TEMPLATE.md` as authoritative if it conflicts with `Example.md`.

### Step 2: Regenerate Manifests

Run the manifest generator from the repository root:

```bash
python3 generate_manifests.py
```

This automatically:
- Parses all MD files in `DB/`
- Extracts H2/H3 sections with line ranges
- Generates pattern-level indexes (severity, codeKeywords, rootCause)
- Updates `DB/index.json` (lean router)
- Updates all 11 `DB/manifests/*.json` files
- Rebuilds `DB/manifests/keywords.json`

### Step 3: Verify the Update

Check that your entry appears in the correct manifest:

```bash
# Verify entry is indexed (replace with your file name)
cat DB/manifests/<category>.json | grep "YOUR_FILE_NAME"

# Verify keywords were extracted
cat DB/manifests/keywords.json | grep "your_keyword"

# Check pattern count
cat DB/index.json | grep -A2 '"<category>"'
```

## Manifest Category Mapping

| Manifest | DB Paths Covered |
|----------|-----------------|
| `oracle.json` | `DB/oracle/**` |
| `amm.json` | `DB/amm/**` |
| `bridge.json` | `DB/bridge/**` |
| `tokens.json` | `DB/tokens/**` |
| `cosmos.json` | `DB/cosmos/**` |
| `solana.json` | `DB/Solona-chain-specific/**` |
| `general-security.json` | `DB/general/access-control/`, `signature/`, `validation/`, `reentrancy/`, `randomness/` |
| `general-defi.json` | `DB/general/flash-loan*/`, `vault-inflation*/`, `precision/`, `calculation/`, `rounding*/`, etc. |
| `general-infrastructure.json` | `DB/general/proxy*/`, `storage*/`, `initialization/`, `diamond-proxy/`, `uups-proxy/`, etc. |
| `general-governance.json` | `DB/general/dao-governance*/`, `stablecoin*/`, `mev-bot/`, `malicious/`, etc. |
| `unique.json` | `DB/unique/**` |

## What the Generator Extracts Per Pattern

Each H2 section in your MD file becomes a searchable pattern with:

```json
{
  "id": "oracle-staleness-001",
  "title": "Missing Staleness Check",
  "lineStart": 93,
  "lineEnd": 248,
  "lineCount": 156,
  "severity": ["MEDIUM"],
  "codeKeywords": ["getPriceUnsafe", "publishTime"],
  "rootCause": "No freshness validation on oracle price data...",
  "subsections": [
    {"title": "Variant A: No Check At All", "lineStart": 110, "lineEnd": 145}
  ]
}
```

### Tips for Better Indexing

1. **Use clear H2 headings** — they become pattern titles
2. **Include severity tags** like `[MEDIUM]`, `[HIGH]`, `[CRITICAL]` in pattern sections
3. **Use code blocks** with function/variable names — they become `codeKeywords`
4. **Write root cause statements** near the top of each section — they become `rootCause`
5. **Use H3 subheadings** for variants — they become searchable `subsections`
6. **Populate `code_keywords` frontmatter** with grep-able identifiers — this improves manifest keywords and hunt cards
7. **Front-load low-context triage sections** (`Agent Quick View`, `Valid Bug Signals`, `False Positive Guards`) so downstream agents do not need the full file

## Update Checklist

```
Manifest Update:
- [ ] MD file created/modified in correct DB/{category}/ folder
- [ ] File follows TEMPLATE.md structure
- [ ] Legacy entries touched during this change were migrated using entry-migration-guide.md
- [ ] `root_cause_family`, `pattern_key`, and `code_keywords` are present
- [ ] `Agent Quick View`, `Valid Bug Signals`, and `False Positive Guards` are present near the top of the file
- [ ] H2 headings are descriptive vulnerability titles
- [ ] Severity tags included in pattern sections
- [ ] Code examples in fenced blocks with real function names
- [ ] Root cause statements present
- [ ] Ran `python3 generate_manifests.py`
- [ ] Verified entry appears in correct manifest
- [ ] Verified keywords extracted
```
