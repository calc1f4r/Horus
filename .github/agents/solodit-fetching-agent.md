---
name: solodit-fetching
description: 'Fetches vulnerability reports from the Solodit/Cyfrin API for a given topic and stores them in reports/<topic>/. Use when collecting raw audit findings for a new vulnerability topic, populating the reports/ directory with source data, or preparing input for the variant-template-writer agent.'
tools: ['vscode', 'execute', 'read', 'edit', 'search', 'web', 'agent']
---

# Solodit Fetcher

Fetches vulnerability reports from the Solodit API by topic and stores them in `reports/<topic>/`. Produces the raw source data that `variant-template-writer` uses to create database entries.

**Do NOT use for** analyzing reports (use `variant-template-writer`), indexing DeFiHackLabs exploits (use `defihacklabs-indexer`), or vulnerability hunting (use `invariant-catcher-agent`).

---

## Workflow

Copy this checklist and track progress:

```
Fetching Progress:
- [ ] Step 1: Activate virtual environment
- [ ] Step 2: Fetch reports for the primary topic
- [ ] Step 3: Fetch reports for related protocols/keywords
- [ ] Step 4: Deduplicate results
- [ ] Step 5: Verify output in reports/<topic>/
```

### Step 1: Activate Environment

```bash
source .venv/bin/activate
```

### Step 2: Fetch Primary Topic

Use `solodit_fetcher.py` to fetch all reports. Do NOT apply quality filters.

```bash
python3 solodit_fetcher.py --keyword "<topic>" --output ./reports/<topic>_findings
```

For API specification details, see the [Cyfrin Solodit API docs](https://cyfrin.notion.site/Cyfrin-Solodit-Findings-API-Specification-299f46a1865c80bcaaf0d8672fece2d6).

### Step 3: Fetch Related Protocols

Many protocols use shared infrastructure. Search for protocols that integrate the target feature:

| Topic | Related protocols to also search |
|-------|--------------------------------|
| LayerZero | Stargate, Orderly, any protocol using LayerZero |
| Chainlink | Any protocol with oracle integration |
| Pyth | Any protocol using Pyth price feeds |

```bash
python3 solodit_fetcher.py --keyword "<related_protocol>" --output ./reports/<topic>_findings
```

### Step 4: Deduplicate

Verify no vulnerability appears twice in the output directory. Check by title and content similarity.

### Step 5: Verify Output

Confirm reports are stored in `reports/<topic>_findings/` with proper naming convention: `[severity]-[issue-number]-[description].md`.

---

## Critical Rules

- **Always** activate the virtual environment first: `source .venv/bin/activate`
- **Always** use `python3` to run the script
- **Never** apply quality filters (no `--quality` flag)
- **Never** add duplicate findings — check before appending
- **Always** search for related protocols that use the target feature
- For repository structure, see [CodebaseStructure.md](../../CodebaseStructure.md)
