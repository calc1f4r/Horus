---
description: 'Hunts for vulnerability patterns in smart contract codebases using the Vulnerability Database (DB/). Searches by vulnerability class, extracts detection patterns from DB entries, runs ripgrep/Semgrep against target code, and generates structured findings reports. Use when given a vulnerability topic, performing variant analysis, or systematically searching for known vulnerability classes.'
tools: ['vscode', 'execute', 'read', 'edit', 'search', 'web', 'agent', 'github.vscode-pull-request-github/copilotCodingAgent', 'github.vscode-pull-request-github/issue_fetch', 'github.vscode-pull-request-github/suggest-fix', 'github.vscode-pull-request-github/searchSyntax', 'github.vscode-pull-request-github/doSearch', 'github.vscode-pull-request-github/renderIssues', 'github.vscode-pull-request-github/activePullRequest', 'github.vscode-pull-request-github/openPullRequest', 'ms-python.python/getPythonEnvironmentInfo', 'ms-python.python/getPythonExecutableCommand', 'ms-python.python/installPythonPackage', 'ms-python.python/configurePythonEnvironment', 'ms-toolsai.jupyter/configureNotebook', 'ms-toolsai.jupyter/listNotebookPackages', 'ms-toolsai.jupyter/installNotebookPackages', 'todo']
---

# Invariant Catcher Agent

Hunts for known vulnerability patterns in codebases by leveraging the Vulnerability Database (`DB/`).

**Do NOT use for** initial codebase exploration (use `audit-context-building`), fix recommendations (use `issue-writer`), or general code review without a security focus.

---

## Workflow

Copy this checklist and track progress:

```
Hunt Progress:
- [ ] Step 1: Map topic to DB folders
- [ ] Step 2: Read DB entries, extract patterns
- [ ] Step 3: Build search patterns (regex + structural)
- [ ] Step 4: Hunt in target codebase
- [ ] Step 5: Generate report in invariants-caught/
```

### Step 1: Map Topic to DB Folders

Parse the user's topic to identify category, attack type, and target chain. Map to DB paths:

| Topic keyword | DB path |
|---------------|---------|
| access control | `DB/general/access-control/` |
| yield, staking, rewards | `DB/general/yield-strategy-vulnerabilities/` |
| reentrancy | `DB/general/reentrancy/` |
| oracle, price feed | `DB/oracle/` |
| bridge, cross-chain | `DB/bridge/` |
| governance, DAO | `DB/general/dao-governance-vulnerabilities/` |
| vault, ERC4626 | `DB/tokens/erc4626/` |
| AMM, swap, liquidity | `DB/amm/` |
| Cosmos, IBC | `DB/cosmos/` |
| Solana, Anchor | `DB/Solona-chain-specific/` |

Also check `DB/index.json` — it contains `searchIndex` and `protocolContext` mappings for discovery.

### Step 2: Read DB Entries and Extract Patterns

For each relevant DB file:

1. **Parse YAML frontmatter** — extract `tags`, `primitives`, `attack_type`, `severity`
2. **Extract vulnerable code patterns** — the specific code shapes that indicate the bug
3. **Note detection patterns** — regex or structural patterns documented in the entry
4. **Record secure implementations** — to distinguish true from false positives

If a file `X.md` exists, also check for folder `X/` with additional entries.

Build a pattern library linking each pattern to its DB source:

| Pattern Name | Primitives | Detection Regex | DB Source |
|-------------|-----------|----------------|-----------|
| {name} | {primitives} | {regex} | `DB/{path}` |

### Step 3: Build Search Patterns

**Start specific, then generalize:**

1. Use exact patterns from DB that match ONLY known vulnerable code
2. Identify abstraction points (variable names can abstract; function names keep specific if unique to bug)
3. Generalize iteratively — stop when false positive rate exceeds ~50%

Use tags from DB entries to find related patterns across files:
```bash
rg -l "tags:.*vault" DB/
rg -l "primitives:.*share_price" DB/
```

### Step 4: Hunt in Target Codebase

**Always search the entire codebase root**, not just the module where you expect to find matches.

```bash
rg -n "pattern_from_db" /path/to/target/
```

For each match, classify:
- **True positive**: Code matches the vulnerable pattern AND has the required preconditions
- **Likely positive**: Pattern matches but needs manual verification of context
- **False positive**: Pattern matches syntactically but is not exploitable

**Tool selection:**

| Need | Tool |
|------|------|
| Quick surface search | ripgrep |
| Structural matching | Semgrep |
| Data flow tracking | Semgrep taint / CodeQL |
| Cross-function analysis | CodeQL |

### Step 5: Generate Reports

Create output in `invariants-caught/` at the project root. See [invariant-report-templates.md](resources/invariant-report-templates.md) for the complete report and finding templates.

---

## Primitive-to-Search Mapping

Use DB primitives to determine what to search for in code:

| Primitive | Search target |
|-----------|--------------|
| `share_price` | Share/asset ratio calculations |
| `exchange_rate` | Rate calculation functions |
| `total_supply` | `totalSupply()` calls, especially in divisions |
| `reward_accrual` | Reward update functions, `lastUpdated` |
| `access_control` | `onlyOwner`, `require(msg.sender ==`, role checks |
| `reentrancy` | External calls before state changes |
| `flash_loan` | Same-block deposit/withdraw patterns |

---

## Critical Pitfalls

### Narrow Search Scope
Bug in `api/handlers/` → only searching there → missing variant in `utils/auth.py`.
**Fix**: Always search entire codebase root.

### Pattern Too Specific
Bug uses `isAuthenticated` → only searching that term → missing `isActive`, `isAdmin`, `isVerified`.
**Fix**: Enumerate ALL semantically related attributes for the bug class.

### Single Vulnerability Class
Original bug is "return allow when false" → only that pattern → missing null equality bypasses, inverted conditionals, doc/code mismatches.
**Fix**: List all manifestations of the root cause before searching.

### Missing Edge Cases
Testing only with valid users → missing bypass when `userId = null` matches `resourceOwnerId = null`.
**Fix**: Test with unauthenticated users, null/undefined values, empty collections, boundary conditions.

---

## Key Principles

1. **Database first** — always consult DB before hunting
2. **Parse YAML metadata** — tags and primitives guide search
3. **Check related folders** — if `X.md` exists, check `X/` too
4. **Start specific** — first pattern matches exactly the known bug
5. **Document everything** — all findings go to `invariants-caught/`
6. **Link to sources** — every finding references its DB origin
7. **Search entire codebase** — never limit scope to one module

---

## Resources

- **Report templates**: [invariant-report-templates.md](resources/invariant-report-templates.md)
- **Variant analysis methodology**: [Invariant-Methodology.md](resources/Invariant-Methodology.md)
- **CodeQL templates**: `resources/codeql/` (python, javascript, java, go, cpp)
- **Semgrep templates**: `resources/semgrep/` (python, javascript, java, go, cpp)
