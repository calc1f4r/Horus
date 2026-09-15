# Contributing

Thank you for contributing to Horus. This guide covers how to add entries, improve agents, and maintain quality.

## Local Python Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

## Adding Vulnerability Entries

### From Audit Reports

1. **Fetch reports** using the solodit fetcher:
   ```bash
   source .venv/bin/activate
   python3 scripts/solodit_fetcher.py --keyword "<topic>" --output ./reports/<topic>_findings
   ```

2. **Analyze patterns** across 5+ reports to identify recurring vulnerability classes.

3. **Create entry** following [TEMPLATE.md](TEMPLATE.md) in the appropriate `DB/` subfolder:
   ```
   DB/<category>/<subcategory>/<pattern-name>.md
   ```

4. **Regenerate manifests**:
   ```bash
   python3 scripts/generate_manifests.py
   python3 scripts/build_db_graph.py
   ```

5. **Verify** the new entry appears correctly in `DB/manifests/*.json`, `DB/index.json`, and the regenerated graph artifacts:
   ```bash
   python3 scripts/db_quality_check.py
   python3 scripts/validate_retrieval_pipeline.py
   ```

### From DeFiHackLabs Exploits

1. Read the exploit PoC in `DeFiHackLabs/src/test/`
2. Extract vulnerability pattern, root cause, and attack steps
3. Create a TEMPLATE.md-compliant entry with real code from the PoC
4. Regenerate manifests and graph artifacts

## Entry Quality Checklist

Before submitting:

- [ ] All required YAML frontmatter fields filled
- [ ] At least 3 vulnerable code examples from real reports
- [ ] At least 2 secure implementation examples
- [ ] Impact analysis with frequency data
- [ ] 10+ search keywords
- [ ] Detection patterns documented
- [ ] All file path references verified to exist
- [ ] No hallucinated protocol names or findings
- [ ] Severity ratings match source reports exactly
- [ ] Root cause describes the fundamental issue, not symptoms

## File Naming Conventions

- **DB entries**: `CATEGORY_VULNERABILITIES.md` (e.g., `PYTH_ORACLE_VULNERABILITIES.md`)
- **Reports**: `[severity]-[issue-number]-[description].md` (e.g., `m-01-missing-staleness-check.md`)
- **Agent files**: lowercase with hyphens, matching the `name:` field (e.g., `poc-writing.md`)

## Improving Agents

The canonical agent and skill sources live in `.claude/`. The `.github/agents/`,
`.agents/skills/`, and `.codex/` surfaces are generated mirrors. When modifying
agent behavior:

1. Edit the source files under `.claude/agents/`, `.claude/skills/`, `.claude/resources/`, or `.claude/rules/`.
2. Keep skill bodies focused and move detailed reference material into shared resources.
3. Regenerate generated surfaces:
   ```bash
   python3 scripts/sync_codex_compat.py
   python3 scripts/sync_codex_compat.py --sync-github-agents
   ```
4. Verify runtime and mirror integrity:
   ```bash
   python3 scripts/sync_codex_compat.py --check
   python3 scripts/validate_codex_runtime.py
   ```
5. Test with real tasks before submitting.

## Code Style

- Use forward slashes in all file paths
- Consistent terminology throughout (pick one term, use it everywhere)
- No time-sensitive information
- Evidence-backed claims with source references

## Reporting Issues

Open an issue for:
- Incorrect vulnerability patterns
- Missing detection rules
- Outdated references
- Agent behavior problems
