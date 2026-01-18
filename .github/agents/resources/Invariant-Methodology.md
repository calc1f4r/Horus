# The Philosophy of Generic but Precise Variant Analysis

This document covers the strategic thinking behind effective variant analysis.

---

## 🔍 Start Here: Using DB/index.json

**The vulnerability database index (`DB/index.json`) is your primary entry point** for pattern discovery. Always consult it first before exploring individual files.

### Quick Reference

```bash
# View the index structure
cat DB/index.json | jq 'keys'
# → ["meta", "categories", "searchIndex", "protocolContext", "auditChecklist"]
```

### Index Sections

| Section | Purpose | How to Use |
|---------|---------|------------|
| `searchIndex.mappings` | Keyword → file lookups | Search by function names, attack patterns, concepts |
| `protocolContext.mappings` | Protocol-type recommendations | Get priority files for lending, DEX, vault, etc. |
| `categories` | Hierarchical taxonomy with keywords | Browse by category for comprehensive coverage |
| `auditChecklist` | Quick check items per type | Rapid validation during audits |

### Example Lookups

```json
// Find files for "reentrancy"
searchIndex.mappings["reentrancy"]
→ ["DB/general/reentrancy/reentrancy.md", "DB/unique/amm/constantproduct/SENTIMENT_CURVE_READONLY_REENTRANCY.md", ...]

// Get priority files for vault audits
protocolContext.mappings.vault_yield.priority_files
→ ["DB/tokens/erc4626/ERC4626_VAULT_VULNERABILITIES.md", "DB/general/vault-inflation-attack/vault-inflation-attack.md", ...]

// Get keywords for Chainlink vulnerabilities
categories.oracle.subcategories.chainlink.keywords
→ ["latestRoundData", "stale price", "sequencer", "heartbeat", "minAnswer", "maxAnswer", ...]
```

---

## Database-Driven Pattern Discovery

### The Vulnerability Database

The vulnerability database (`DB/`) is your primary source of truth for known vulnerability patterns. Before hunting, always consult the database.

### Understanding YAML Frontmatter

Every vulnerability file contains YAML metadata that guides your search:

```yaml
---
# Core Classification
protocol: generic
chain: everychain
category: yield                    # Main category for folder mapping
vulnerability_type: inflation_attack

# Attack Vector Details
attack_type: economic_exploit|logical_error
affected_component: vault|staking|rewards

# Technical Primitives - THESE TELL YOU WHAT TO SEARCH FOR
primitives:
  - share_price          # Search: share calculation functions
  - exchange_rate        # Search: rate conversion logic
  - total_supply         # Search: totalSupply() in divisions
  - reward_accrual       # Search: reward update mechanisms

# Context Tags - THESE HELP FIND RELATED PATTERNS
tags:
  - defi
  - vault
  - erc4626
  - inflation
  - staking
---
```

### Using Primitives for Code Search

Each primitive maps to specific code patterns:

| Primitive | What to Search | Example Patterns |
|-----------|----------------|------------------|
| `share_price` | Share/asset ratio calculations | `assets * totalSupply / totalAssets` |
| `exchange_rate` | Rate conversions | `balanceOf(address(this)) / totalShares` |
| `total_supply` | Supply-based divisions | `totalSupply() / totalAssets()` |
| `reward_accrual` | Reward distribution logic | `rewardPerToken`, `lastUpdated` |
| `access_control` | Permission checks | `onlyOwner`, `require(msg.sender ==` |
| `reentrancy` | External calls before state changes | `.call{}`, `.transfer(` before state |
| `flash_loan` | Single-block operations | deposit + withdraw same block |
| `veto` | Veto/guardian mechanisms | `vetoProposal`, `guardian` |
| `51_percent_attack` | Majority control | voting power, proposal execution |

### Tag-Based Pattern Discovery

Tags help you find related vulnerabilities across the database:

```bash
# Find all files with matching tags
rg -l "tags:.*vault" DB/
rg -l "tags:.*governance" DB/

# Find files with multiple related tags
rg -l "tags:.*\b(vault|erc4626)\b" DB/
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

Every finding must reference its source pattern in the DB:

```markdown
### Finding 1: First Depositor Attack Variant

**DB Reference**: [First Depositor Attack](DB/general/yield-strategy-vulnerabilities.md#1-first-depositor--inflation-attack)
**Matched Primitive**: `share_price`, `total_supply`
**Matched Tags**: `vault`, `erc4626`
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

### Step 0: Consult DB/index.json (START HERE)
- Use `searchIndex.mappings` for keyword lookups
- Use `protocolContext.mappings` for protocol-type recommendations
- Use `auditChecklist` for quick validation items

### Step 1: Parse User Request → Index Lookup
- "access control" → `searchIndex["access control"]` or `protocolContext.governance_dao`
- "vault inflation" → `searchIndex["inflation attack"]` + `searchIndex["first depositor"]`
- "oracle manipulation" → `searchIndex["oracle"]` + specific provider keywords
- "reentrancy" → `searchIndex["reentrancy"]`

### Step 2: Read Priority DB Files
- Get files from index lookup results
- Extract YAML frontmatter (primitives, tags, affected_component)
- Note vulnerable code patterns and detection regex

### Step 3: Build Pattern Library
- Convert DB patterns to ripgrep/Semgrep patterns
- Use `categories.*.subcategories.*.keywords` for search terms
- Record abstraction levels for each pattern

### Step 4: Hunt in Codebase
- Run patterns against target code
- Document matches with confidence levels
- Link findings to DB references (file path from index)

### Step 5: Generate Reports
- Create `invariants-caught/{category}-findings/` folder
- Write report.md with all findings
- Include patterns-used.md for reproducibility
- Reference index paths for traceability

---

## Summary: The Expert Mindset

1. **Start with index.json**: Always consult `DB/index.json` first for pattern discovery
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
12. **Use protocol context**: Match protocol type to get relevant vulnerability patterns
13. **Output to invariants-caught/**: All findings are documented for reproducibility