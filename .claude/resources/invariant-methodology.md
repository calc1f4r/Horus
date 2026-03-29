# The Philosophy of Generic but Precise Variant Analysis

This document covers the strategic thinking behind effective variant analysis.

---

## Start Here: Using the 3-Tier Manifest Architecture

**Horus uses a 3-tier architecture** for efficient, precise pattern discovery. Always start with the router.

```
Tier 1: DB/index.json              ← Lean router (~330 lines). Start here.
   ↓
Tier 2: DB/manifests/<name>.json   ← Pattern-level index with line ranges (11 manifests)
   ↓
Tier 3: DB/**/*.md                 ← Vulnerability content. Read ONLY targeted line ranges.
```

### Quick Reference

```bash
# View the router structure
cat DB/index.json | jq 'keys'
# → ["meta", "searchStrategy", "manifests", "protocolContext", "auditChecklist", "keywordIndex"]
```

### Router Sections

| Section | Purpose | How to Use |
|---------|---------|------------|
| `protocolContext.mappings` | Protocol-type → manifest names + focus patterns | Get priority manifests for lending, DEX, vault, etc. |
| `manifests` | Lists all 11 manifests with descriptions + pattern counts | Pick the right manifest to load |
| `auditChecklist` | Quick check items per type | Rapid validation during audits |
| `keywordIndex` | Points to `DB/manifests/keywords.json` | Keyword → manifest lookup |

### Example Lookups

**By Protocol Type:**
```
DB/index.json → protocolContext.mappings.lending_protocol
  → manifests: ["oracle", "general-defi", "tokens", "general-security"]
  → focusPatterns: ["staleness", "liquidation", "flash loan", ...]
→ Load DB/manifests/oracle.json → find pattern by title/severity/codeKeywords
→ Read DB/oracle/pyth/PYTH_ORACLE_VULNERABILITIES.md lines 93-248
```

**By Keyword:**
```
DB/manifests/keywords.json → "reentrancy" → ["general-infrastructure"]
→ Load DB/manifests/general-infrastructure.json → find reentrancy patterns
→ Read targeted line ranges from the MD file
```

**By Manifest Browse:**
```
Load DB/manifests/general-defi.json → 115 patterns
→ Filter by severity: ["HIGH", "CRITICAL"]
→ Read targeted line ranges for each match
```

---

## Database-Driven Pattern Discovery

### The Horus

Horus (`DB/`) is your primary source of truth for known vulnerability patterns. Before hunting, always consult the database.

### Understanding YAML Frontmatter

### Understanding Manifest Pattern Entries

Each manifest contains pattern entries with pre-extracted metadata that guides your search:

```json
{
  "id": "general-defi-inflation-001",
  "title": "First Depositor / Inflation Attack",
  "lineStart": 45,
  "lineEnd": 198,
  "lineCount": 154,
  "severity": ["HIGH", "CRITICAL"],
  "codeKeywords": ["convertToShares", "totalSupply", "totalAssets", "donate"],
  "rootCause": "Empty vault allows first depositor to manipulate share price...",
  "subsections": [
    {"title": "Vault Inflation via Donation", "lineStart": 80, "lineEnd": 130}
  ]
}
```

### Using codeKeywords for Code Search

The `codeKeywords` from manifest entries map to specific code patterns to search for:

| codeKeyword | What to Search | Example Patterns |
|-----------|----------------|------------------|
| `convertToShares` | Share/asset ratio calculations | `assets * totalSupply / totalAssets` |
| `totalSupply` | Supply-based divisions | `totalSupply() / totalAssets()` |
| `latestRoundData` | Oracle price fetching | Chainlink price feed calls |
| `getPriceUnsafe` | Pyth oracle calls | Pyth price without staleness |
| `onlyOwner` | Permission checks | Access control modifiers |
| `delegatecall` | Proxy forwarding | State corruption via delegatecall |
| `lzReceive` | LayerZero message handling | Bridge message validation |

### Keyword-Based Pattern Discovery

Use `DB/manifests/keywords.json` to find which manifests contain relevant patterns:

```bash
# Look up keywords to find relevant manifests
cat DB/manifests/keywords.json | jq '.keywords.reentrancy'
# → ["general-infrastructure"]

cat DB/manifests/keywords.json | jq '.keywords.getPriceUnsafe'
# → ["oracle"]
```

---

## Output Organization: The invariants-caught/ Folder

### Structure

All findings must be documented in the `invariants-caught/` folder at the project root:

```
project-root/
├── invariants-caught/
│   ├── {category}-findings/
│   │   ├── report.md              # Main findings report
│   │   ├── patterns-used.md       # Patterns extracted from DB
│   │   └── findings/
│   │       ├── finding-001.md     # Individual finding details
│   │       └── finding-002.md
│   └── ...
```

### Report Format

Each report should include:

1. **YAML Frontmatter**: Metadata about the search
2. **Executive Summary**: High-level findings overview
3. **Patterns Used**: Which DB entries were consulted
4. **Findings List**: Each vulnerability found
5. **Detection Commands**: Reproducible search commands

### Linking to DB Sources

Every finding must reference its source pattern in the DB with line ranges:

```markdown
### Finding 1: First Depositor Attack Variant

**DB Reference**: [First Depositor Attack](DB/general/vault-inflation-attack/vault-inflation-attack.md#L45-L198)
**Manifest**: `general-defi.json` → pattern `general-defi-inflation-001`
**Matched codeKeywords**: `convertToShares`, `totalSupply`
**Severity**: HIGH
```

---

## Why Variants Exist

Vulnerabilities cluster because developers make consistent mistakes:

1. **Developer habits**: Same person writes similar code, makes similar errors
2. **Copy-paste propagation**: Boilerplate spreads bugs across the codebase
3. **API misuse patterns**: Complex APIs invite consistent misunderstandings
4. **Framework idioms**: Framework patterns create predictable vulnerability shapes
5. **Incomplete fixes**: Original bug fixed in one place, missed elsewhere

Understanding WHY variants exist helps predict WHERE to find them.

## Root Cause Analysis

Before searching, extract the essential vulnerability pattern:

### Ask These Questions

1. **What operation is dangerous?** (e.g., `eval()`, `system()`, raw SQL)
2. **What data makes it dangerous?** (e.g., user-controlled input)
3. **What's missing?** (e.g., sanitization, validation, bounds check)
4. **What context enables it?** (e.g., authentication state, error handling path)

### The Root Cause Statement

Formulate a clear statement:

> "This vulnerability exists because [UNTRUSTED DATA] reaches [DANGEROUS OPERATION] without [REQUIRED PROTECTION]."

Examples:
- "User input reaches `eval()` without sanitization"
- "Attacker-controlled size reaches `malloc()` without overflow check"
- "Untrusted path reaches `open()` without canonicalization"

This statement IS your search pattern.

## The Abstraction Ladder

Patterns exist at different abstraction levels. Start at Level 0 and climb.

### Level 0: Exact Match

Match the literal vulnerable code:

```python
# Original vulnerable code
query = "SELECT * FROM users WHERE id=" + request.args.get('id')
```

```bash
# Level 0 pattern
rg 'SELECT \* FROM users WHERE id=" \+ request\.args\.get'
```

- **Matches**: 1 (the original)
- **False positives**: 0
- **Value**: Confirms the bug exists, baseline for generalization

### Level 1: Variable Abstraction

Replace variable names with wildcards:

```yaml
# Level 1 pattern
pattern: $QUERY = "SELECT * FROM users WHERE id=" + $INPUT
```

- **Matches**: 3-5 (same query pattern, different variables)
- **False positives**: Low
- **Value**: Find copy-paste variants

### Level 2: Structural Abstraction

Generalize the structure:

```yaml
# Level 2 pattern
patterns:
  - pattern: $Q = "..." + $INPUT
  - pattern-inside: |
      def $FUNC(...):
        ...
        cursor.execute($Q)
```

- **Matches**: 10-30 (any string concat used in query)
- **False positives**: Medium
- **Value**: Find pattern variants

### Level 3: Semantic Abstraction

Abstract to the security property:

```yaml
# Level 3 pattern (taint mode)
mode: taint
pattern-sources:
  - pattern: request.args.get(...)
  - pattern: request.form.get(...)
pattern-sinks:
  - pattern: cursor.execute(...)
```

- **Matches**: 50-100+ (any user input to any query)
- **False positives**: High (many will have proper parameterization)
- **Value**: Comprehensive coverage, requires triage

### Choosing Your Level

| Goal | Recommended Level |
|------|-------------------|
| Verify a specific fix | Level 0 |
| Find copy-paste bugs | Level 1 |
| Audit a component | Level 2 |
| Full security assessment | Level 3 |

## The Generalization Process

### Rule: One Change at a Time

Never generalize multiple elements simultaneously:

```
BAD:  exact code -> fully abstract pattern
GOOD: exact code -> abstract var1 -> abstract var2 -> abstract operation
```

Each step:
1. Make ONE change
2. Run the pattern
3. Review ALL new matches
4. Decide: acceptable FP rate?
5. Continue or revert

### Decision Points

At each generalization step, ask:

**Should I abstract this variable name?**
- YES if: Different names could have same bug
- NO if: The name indicates a specific semantic meaning you want to preserve

**Should I abstract this literal value?**
- YES if: Any value would trigger the bug
- NO if: Only specific values (like `2` in a shift operation) are dangerous

**Should I use `...` wildcards?**
- YES if: Argument position doesn't matter
- NO if: Only specific argument positions are sinks

**Should I add taint tracking?**
- YES if: Need to verify data actually flows from source to sink
- NO if: Presence of pattern is sufficient evidence

## False Positive Management

### Acceptable FP Rates by Context

| Context | Acceptable FP Rate |
|---------|-------------------|
| Automated CI blocking | <5% |
| Developer warning | <20% |
| Security audit triage | <50% |
| Research/exploration | <80% |

### Common FP Sources and Filters

**Dead code**: Add reachability constraints
```yaml
pattern-not-inside: |
  if False:
    ...
```

**Test code**: Exclude test directories
```bash
rg "pattern" --glob '!**/test*' --glob '!**/*_test.*'
```

**Already sanitized**: Add sanitizer patterns
```yaml
pattern-not: dangerous_func(sanitize($X))
```

**Literal values**: Exclude non-user-controlled data
```yaml
pattern-not: dangerous_func("...")  # Literal string
```

## Multi-Repository Campaign

For large-scale hunts: **Recon** (ripgrep to find hotspots) → **Deep Analysis** (Semgrep/CodeQL on hotspots) → **Refinement** (reduce FPs) → **Automation** (CI-ready rules).

## Tracking Your Hunt

Maintain a tracking document:

```markdown
## Variant Analysis: [Original Bug ID]

### Root Cause
[Statement of the vulnerability pattern]

### Patterns Tried
| Pattern | Level | Matches | True Pos | False Pos | Notes |
|---------|-------|---------|----------|-----------|-------|
| exact   | 0     | 1       | 1        | 0         | Baseline |
| ...     | ...   | ...     | ...      | ...       | ...   |

### Confirmed Variants
| Location | Severity | Status | Notes |
|----------|----------|--------|-------|
| file:line| High     | Fixed  | ...   |

### False Positive Patterns
- Pattern X: Always FP because [reason]
- Pattern Y: FP in [context] but TP in [context]
```

## Anti-Patterns to Avoid

### Starting Too Generic

**Wrong**: Jump straight to semantic analysis
**Right**: Start with exact match, generalize incrementally

### Generalizing Everything

**Wrong**: Abstract all elements at once
**Right**: Abstract one element, verify, repeat

### Ignoring False Positives

**Wrong**: "I'll triage later"
**Right**: Analyze FPs immediately, they guide pattern refinement

### Tool Loyalty

**Wrong**: "I only use CodeQL"
**Right**: Use ripgrep for recon, Semgrep for iteration, CodeQL for precision

### Pattern Hoarding

**Wrong**: Keep all patterns regardless of FP rate
**Right**: Delete patterns that don't provide value

## Expanding Vulnerability Classes

A single root cause can manifest in multiple ways. Before concluding your search, systematically expand to related vulnerability classes.

### The Expansion Checklist

For each root cause, ask:

1. **What other attributes/functions have similar semantics?**
   - If bug involves `isAuthenticated`, also check: `isActive`, `isAdmin`, `isVerified`, `isLoggedIn`
   - If bug involves `userId`, also check: `ownerId`, `creatorId`, `authorId`

2. **What other boolean logic errors could occur?**
   - Inverted conditions (`if not x` vs `if x`)
   - Wrong default return value (`return true` vs `return false`)
   - Short-circuit evaluation errors

3. **What edge cases exist for the data types involved?**
   - Null/None/undefined comparisons
   - Empty string vs null
   - Zero vs null
   - Empty array/collection

4. **What documentation mismatches could exist?**
   - Function does opposite of docstring
   - Parameter meaning inverted
   - Return value semantics reversed

### Semantic Analysis

Some bugs can only be found by comparing code behavior to documented intent:

**Pattern:** Function name or docstring suggests one behavior, code does another

```python
# Docstring says "Returns True if access should be DENIED"
# But code returns True when user HAS permission (should be allowed)
def check_restricted_permission(user, perm):
    """Returns True if access should be DENIED."""
    if user.has_perm(perm):
        return True  # BUG: This grants access to users with permission
    return False
```

**Detection strategy:**
1. Search for functions with "deny", "restrict", "block", "forbid" in names
2. Manually verify return value semantics match the name/docs
3. Create rules that flag suspicious patterns for manual review

### Null Equality Bypasses

A common class of authorization bypass:

```python
# If anonymous_user.id is None and guest_order.owner_id is None
# Then None == None evaluates to True, bypassing the check
if order.owner_id == current_user.id:
    return True  # Allows access
```

**Detection strategy:**
1. Find all owner/permission checks using equality comparisons
2. Trace what values the compared fields can have
3. Check if both sides can be null simultaneously

---

## DB-to-Code Workflow Summary

### Step 0: Consult DB/index.json → Load Manifests (START HERE)
- Read `DB/index.json` (~330 lines) for protocol context and manifest listing
- Use `protocolContext.mappings` to identify relevant manifests for the protocol type
- Use `DB/manifests/keywords.json` for keyword → manifest lookups
- Use `auditChecklist` for quick validation items

### Step 1: Parse User Request → Manifest Lookup
- "access control" → `keywords.json["access_control"]` → `general-security` manifest
- "vault inflation" → `keywords.json["convertToShares"]` → `general-defi` manifest
- "oracle manipulation" → `protocolContext.lending_protocol` → `oracle` manifest
- "reentrancy" → `keywords.json["reentrancy"]` → `general-infrastructure` manifest

### Step 2: Read Targeted DB Patterns
- Load relevant manifest(s) from `DB/manifests/<name>.json`
- Find patterns by title, severity, or codeKeywords
- Read ONLY the targeted line ranges (lineStart → lineEnd) from the MD files
- Note vulnerable code patterns and detection regex from the targeted sections

### Step 3: Build Pattern Library
- Convert DB patterns to ripgrep/Semgrep patterns
- Use `codeKeywords` from manifest entries as search terms
- Record abstraction levels for each pattern

### Step 4: Hunt in Codebase
- Run patterns against target code
- Document matches with confidence levels
- Link findings to DB references (manifest ID + file path + line range)

### Step 5: Generate Reports
- Create `invariants-caught/{category}-findings/` folder
- Write report.md with all findings
- Include patterns-used.md for reproducibility
- Reference manifest IDs and line ranges for traceability

---

## Summary: The Expert Mindset

1. **Start with index.json → manifests**: Always consult the 3-tier architecture first
2. **Understand before searching**: Root cause analysis is non-negotiable
3. **Start specific**: Your first pattern should match exactly one thing
4. **Climb the ladder**: Generalize one step at a time
5. **Measure as you go**: Track matches and FP rates at each step
6. **Know when to stop**: High FP rate means you've gone too far
7. **Iterate ruthlessly**: Refine patterns based on what you learn
8. **Document everything**: Your tracking doc is as valuable as your patterns
9. **Expand vulnerability classes**: One root cause has many manifestations
10. **Check semantics**: Verify code matches documentation intent
11. **Test edge cases**: Null values and boundary conditions reveal hidden bugs
12. **Use protocol context**: Match protocol type to get relevant manifests
13. **Output to invariants-caught/**: All findings are documented for reproducibility
