# Contributing

Thank you for contributing to the Vulnerability Database. This guide covers how to add entries, improve agents, and maintain quality.

## Adding Vulnerability Entries

### From Audit Reports

1. **Fetch reports** using the solodit fetcher:
   ```bash
   source .venv/bin/activate
   python3 solodit_fetcher.py --keyword "<topic>" --output ./reports/<topic>_findings
   ```

2. **Analyze patterns** across 5+ reports to identify recurring vulnerability classes.

3. **Create entry** following [TEMPLATE.md](TEMPLATE.md) in the appropriate `DB/` subfolder:
   ```
   DB/<category>/<subcategory>/<pattern-name>.md
   ```

4. **Regenerate manifests**:
   ```bash
   python3 generate_manifests.py
   ```

5. **Verify** the new entry appears correctly in `DB/manifests/*.json` and `DB/index.json`.

### From DeFiHackLabs Exploits

1. Read the exploit PoC in `DeFiHackLabs/src/test/`
2. Extract vulnerability pattern, root cause, and attack steps
3. Create a TEMPLATE.md-compliant entry with real code from the PoC
4. Regenerate manifests

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
- **Agent files**: lowercase with hyphens (e.g., `poc-writer-agent.md`)

## Improving Agents

Agent skill files live in `.github/agents/`. When modifying:

1. Keep the SKILL.md body under 500 lines
2. Use third-person descriptions
3. Include a workflow checklist with trackable steps
4. Reference detailed content in separate files under `resources/`
5. Test with real tasks before submitting

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
