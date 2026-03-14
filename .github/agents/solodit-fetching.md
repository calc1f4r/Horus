---
name: solodit-fetching
description: 'Fetches vulnerability reports from the Solodit/Cyfrin API for a given topic and stores them in reports/<topic>_findings/. Preserve the raw source metadata needed for downstream fine-grained report indexing. Use when collecting raw audit findings for a new vulnerability topic, populating the reports/ directory with source data, or preparing input for the variant-template-writer agent.'
tools: ['vscode', 'execute', 'read', 'edit', 'search', 'web', 'agent','todo']
---

# Solodit Fetcher

Fetches vulnerability reports from the Solodit API by topic and stores them in `reports/<topic>_findings/`. Produces the raw source data that `variant-template-writer` uses to create database entries.

**Do NOT use for** analyzing reports (use `variant-template-writer`), indexing DeFiHackLabs exploits (use `defihacklabs-indexer`), or vulnerability hunting (use `invariant-catcher`).

---

## Workflow

Copy this checklist and track progress:

```
Fetching Progress:
- [ ] Step 1: Activate virtual environment
- [ ] Step 2: Fetch reports for the primary topic
- [ ] Step 3: Fetch reports for related protocols/keywords
- [ ] Step 4: Preserve provenance and resolve filename collisions
- [ ] Step 5: Deduplicate by source identifiers first, then content
- [ ] Step 6: Verify raw output in reports/<topic>_findings/
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

### Step 4: Preserve Provenance

Ensure every fetched file preserves the metadata needed for downstream indexing:

- `source`, `solodit_id`, `source_link`, `contest_link`, `github_link`
- `protocol`, `audit_firm`, `severity`
- original title and finding content

Do **not** hand-normalize weak fields like `category` or `vulnerability_type` to force them to match the folder topic. Folder placement is an acquisition hint, not a final classification.

If multiple findings would land on the same filename, keep both raw reports by renaming the later file rather than overwriting provenance.

### Step 5: Deduplicate

Verify no vulnerability appears twice in the output directory.

1. Check hard duplicates first: same `solodit_id`, same source URL, same GitHub issue, or same contest finding number
2. Check soft duplicates second: normalized title + protocol + strongly overlapping body content
3. If duplicate status is unclear, keep both raw files and let `variant-template-writer` resolve them during indexing

### Step 6: Verify Output

Confirm reports are stored in `reports/<topic>_findings/`.

- Prefer the naming convention `[severity]-[issue-number]-[description].md` when the source provides that information
- Do not treat the filename as authoritative classification data
- Confirm the output preserves the metadata required by the [report indexing framework](resources/report-indexing.md)

---

## Critical Rules

- **Always** activate the virtual environment first: `source .venv/bin/activate`
- **Always** use `python3` to run the script
- **Never** apply quality filters (no `--quality` flag)
- **Never** hand-edit `category` or `vulnerability_type` to force-fit the topic
- **Never** drop source IDs or URLs, even when other metadata is weak
- **Never** add duplicate findings when the source identity is clear
- **Always** search for related protocols that use the target feature
- **If duplicate status is unclear, keep both raw files and resolve it later during report indexing**
- For repository structure, see [CodebaseStructure.md](../../CodebaseStructure.md)
