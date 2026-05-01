# Horus — Gemini CLI Instructions

This repository is **Horus**, a curated vulnerability database for smart contract security audits, natively optimized for AI-agent-driven bulk scanning, pattern matching, and comprehensive 11-phase audits across EVM, Solana, Cosmos, Sui Move, and ZK Rollup ecosystems.

As the Gemini CLI agent, you act as the orchestrator and executer. This guide defines how you must navigate the architecture, fetch context, and execute workflows.

---

## 1. Core Architecture: 4-Tier Search

The database relies on a strict **tiered architecture** to preserve token limits. **CRITICAL:** Never read entire vulnerability files (.md) directly when searching. Always traverse the tiers to find specific `start_line` and `end_line` bounds.

- **Tier 1: Router (`DB/index.json`)**
  - **Start here** for any audit or lookup. Maps protocol types (e.g., `lending_protocol`, `solana_program`) to the relevant manifests to load.
- **Tier 1.5: Hunt Cards (`DB/manifests/huntcards/all-huntcards.json`)**
  - Contains compressed detection cards with `grep` regex patterns and one-line descriptions.
  - *Workflow:* Use `grep_search` with a card's pattern against target code. Only investigate further upon a hit.
- **Tier 2: Manifests (`DB/manifests/*.json`)**
  - Full pattern-level indexes. Contains precise `lineStart` and `lineEnd` values for the actual markdown files.
- **Tier 3: Vulnerability Content (`DB/**/*.md`)**
  - Use `read_file` with the `start_line` and `end_line` discovered in Tier 2 to read *only* the specific vulnerability pattern you need.

---

## 2. Navigating Context & Raw Findings (`reports/`)

The repository contains over 22,200 raw audit findings. To prevent context flooding, these are isolated into separate Git branches. **Do not attempt to read the entire `reports/` directory.**

When you need to read raw reports for reference or to build new DB entries, fetch them dynamically:

**Fetch a single file (Preferred):**
```bash
mkdir -p reports/<CATEGORY>
gh api "repos/calc1f4r/Horus/contents/reports/<CATEGORY>/<FILE>?ref=hunt-cards" \
  --jq '.content' | base64 -d > reports/<CATEGORY>/<FILE>
```

**Clone a specific category branch:**
```bash
gh repo clone calc1f4r/Horus reports/<CATEGORY> \
  -- --branch reports/<BRANCH> --single-branch --depth 1
```
*(Refer to `docs/codebase-structure.md` for the exact mapping of `CATEGORY` to `BRANCH`)*

---

## 3. Emulating the Agent System & Skills

Horus contains 38 specialized audit workflows and tools. When running an audit phase or performing targeted discovery, you must leverage Gemini's skill system and sub-agents:

1. **Activate Skills:** Use the `activate_skill` tool to dynamically load expert procedural guidance. For example, if asked to run an audit phase or generate formal verification, call `activate_skill` with the appropriate name (e.g., `invariant-writer`, `protocol-reasoning`, `audit-orchestrator`). These skills are mapped from the repository's `.agents/skills/` directory.
2. **Sub-Agents:** 
   - When faced with highly complex architectural questions or initial reconnaissance that requires reading many files, delegate to the `codebase_investigator` sub-agent.
   - For repetitive batch tasks (like formatting multiple entries) or high-volume output commands, delegate to the `generalist` sub-agent to keep your main context lean.
3. **Reference Materials:** Rely on shared knowledge bases in `.claude/resources/` (e.g., `vulnerability-taxonomy.md`) when you need foundational protocol intuition.

---

## 4. Modifying Database Entries

When adding or updating vulnerabilities in `DB/`:

1. **Structure:** You MUST exactly follow the layout in `TEMPLATE.md`. Ensure all YAML frontmatter fields, `root_cause_family`, `pattern_key`, `code_keywords`, and concrete code examples are present.
2. **File Naming:** Files should be named descriptively, such as `CATEGORY_VULNERABILITIES.md`.
3. **Migration:** If you edit a legacy entry, you must migrate it fully to the `TEMPLATE.md` structure. Do not preserve the old layout.
4. **Mandatory Post-Action:** After ANY change to `.md` files in `DB/`, you must regenerate the system's manifests and hunt cards:
   ```bash
   source .venv/bin/activate
   python3 scripts/generate_manifests.py
   python3 scripts/build_db_graph.py
   python3 scripts/db_quality_check.py
   ```

---

## 5. Python Scripts & Automation

All utility scripts are in `scripts/`. Always use `python3` and activate the virtual environment (`source .venv/bin/activate`) before running.

If `.venv` is missing or broken, recreate it with:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

- **`scripts/generate_manifests.py`**: Crucial. Rebuilds the search index. Run after any DB edit.
- **`scripts/build_db_graph.py`**: Rebuilds `DB/graphify-out/` from manifests and hunt cards. Run after DB or hunt-card relationship changes.
- **`scripts/solodit_fetcher.py`**: Use to fetch raw audit reports into the `reports/` structure.
- **`scripts/db_quality_check.py`**: Validates the structural integrity and line ranges of DB entries. Run this to verify your DB edits.
- **`scripts/validate_retrieval_pipeline.py`**: Runs compile checks, unit tests, DB quality checks, graph smoke tests, sync checks, and audit graph finalization.
- **`scripts/validate_codex_runtime.py`**: Validates generated Codex runtime files and generated skill links.
- **`scripts/generate_entries.py`**: Assists in generating DB entries from fetched reports.

---

## 6. Execution Mindset

- **Parallel Search:** Exploit Gemini's ability to run parallel tool calls. When executing bulk hunt cards, issue multiple `grep_search` calls concurrently. If you need to read multiple vulnerability entries, fire multiple `read_file` calls (with targeted `start_line` and `end_line`) in a single turn.
- **Combine Tools:** To save conversational turns, combine your searches. For instance, you can run a `grep_search` to find a pattern's file and simultaneously invoke a `read_file` on `DB/index.json` or `manifests.json` if you also need to route the next step.
- **Surgical Precision:** Your most important goal in this codebase is to minimize the amount of data you ingest. Rely on indexes (`DB/index.json` and `keywords.json`) and specific line reads to maintain speed and high intelligence.
