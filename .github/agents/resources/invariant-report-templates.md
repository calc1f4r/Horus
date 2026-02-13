# Invariant Catcher — Report Templates

## Contents
- Output folder structure
- Main findings report template
- Individual finding template

---

## Output Folder Structure

```
project-root/
├── invariants-caught/
│   ├── {category}-findings/
│   │   ├── report.md              # Main findings report
│   │   ├── patterns-used.md       # Patterns extracted from DB
│   │   └── findings/
│   │       ├── finding-001.md
│   │       └── finding-002.md
```

---

## Main Report Template

Use this template for `invariants-caught/{category}-findings/report.md`:

```markdown
---
generated: {timestamp}
category: {vulnerability_category}
db_sources:
  - DB/{path1}
  - DB/{path2}
total_findings: {count}
severity_breakdown:
  critical: {n}
  high: {n}
  medium: {n}
  low: {n}
---

# {Category} Vulnerability Findings

## Executive Summary

{Brief overview of findings}

## Patterns Used from Database

| Pattern | DB Source | Matches Found |
|---------|-----------|---------------|
| {Pattern Name} | `DB/{path}` | {n} |

## Findings

### Finding 1: [Title]

**Severity**: HIGH
**File**: `src/contracts/Vault.sol:L45-L52`
**Pattern Match**: {DB pattern name}

**Vulnerable Code**:
\`\`\`solidity
{code snippet}
\`\`\`

**Why Vulnerable**:
{explanation from DB pattern}

**Recommendation**:
{fix from DB}

**DB Reference**: [{Pattern Name}](DB/{path}#{anchor})

---

## Tags & Primitives Covered

**Tags searched**: {comma-separated list}
**Primitives matched**: {comma-separated list}

## Appendix: Detection Commands Used

\`\`\`bash
rg -n "pattern1"
rg -n "pattern2"
\`\`\`
```

---

## Individual Finding Template

Use for `invariants-caught/{category}-findings/findings/finding-{NNN}.md`:

```markdown
---
id: {NNN}
title: {finding title}
severity: {critical|high|medium|low}
confidence: {high|medium|low}
file: {path}:{lines}
db_pattern: {pattern name}
db_source: DB/{path}
---

# Finding {NNN}: {Title}

## Location
`{file}:{line_start}-{line_end}` in `{function_name}()`

## Vulnerable Code
\`\`\`solidity
{code snippet with surrounding context}
\`\`\`

## DB Pattern Match
**Pattern**: {name}
**Confidence**: {High/Medium/Low} — {why this confidence level}

## Why Vulnerable
{Explanation linking the code to the DB-documented vulnerability pattern}

## Impact
{Concrete impact: fund loss, DoS, access bypass, etc.}

## Recommendation
{Fix from DB pattern, adapted to this specific instance}
```
