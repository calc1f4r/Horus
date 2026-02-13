# Vulnerability Database - Codebase Structure

## Purpose

This repository serves as a comprehensive vulnerability pattern database for smart contract security audits. It aggregates findings from multiple audit firms into structured, searchable entries optimized for LLM-based code analysis and pattern matching.

---

## Directory Structure

```
vuln-database/
├── DB/                          # Main vulnerability database
│   ├── index.json              # ⭐ Master index - START HERE
│   ├── oracle/                  # Oracle-related vulnerabilities
│   │   ├── pyth/               # Pyth Network specific issues
│   │   │   └── PYTH_ORACLE_VULNERABILITIES.md
│   │   ├── chainlink/          # Chainlink specific issues
│   │   └── twap/               # TWAP oracle issues
│   ├── amm/                    # Economic attack patterns
│   ├── yeild/                  # Business logic vulnerabilities
│   └── [category]/             # Other vulnerability categories
├── reports/                    # Raw audit reports (source data)
│   ├── pyth_findings/          # 198 raw Pyth vulnerability reports
│   ├── chainlink_findings/     # Raw Chainlink audit reports
│   └── [topic]_findings/       # Other raw findings
├── Variant-analysis/           # Variant analysis methodology & tools
│   ├── Methodology.md          # Variant analysis guide
│   ├── Skills.md               # Required skills documentation
│   ├── Tasker.md               # Task management
│   └── resources/              # Analysis tools (CodeQL, Semgrep)
├── TEMPLATE.md                  # Canonical entry structure
├── Example.md                   # Reference example entry
├── Agents.md                    # Agent guidance document
├── CodebaseStructure.md         # This file - repository layout guide
├── solodit_fetcher.py          # Vulnerability fetching tool
└── Readme.md                    # Usage instructions
```

---

## Key Files

### DB/index.json ⭐ START HERE
**Path:** `./DB/index.json`  
**Purpose:** Lean router (~330 lines) that points agents to the right manifest files. **Agents should always read this file first** to find relevant vulnerability patterns.

**Contains:**
- `protocolContext`: Maps protocol types (lending, DEX, vault, etc.) to relevant manifest names and focus patterns
- `manifests`: Lists all 11 manifest files with descriptions and pattern counts
- `auditChecklist`: Quick security checks by category
- `keywordIndex`: Points to `DB/manifests/keywords.json` for keyword lookup

**3-Tier Search Architecture:**
```
Tier 1: DB/index.json              ← Lean router (~330 lines). Start here.
   ↓
Tier 2: DB/manifests/<name>.json   ← Pattern-level indexes with line ranges (11 manifests)
   ↓
Tier 3: DB/**/*.md                 ← Vulnerability content. Read ONLY targeted line ranges.
```

**Usage by Agents:**
```
// Find manifests for a protocol type
DB/index.json → protocolContext.mappings.lending_protocol
  → manifests: ["oracle", "general-defi", "tokens", "general-security"]

// Find patterns by keyword
DB/manifests/keywords.json → "getPriceUnsafe" → ["oracle"]
→ Load DB/manifests/oracle.json → find pattern → read targeted line ranges

// Browse patterns by severity
Load DB/manifests/general-defi.json → filter severity: ["HIGH", "CRITICAL"]
→ Read targeted line ranges from MD files
```

For the full search guide, see `DB/SEARCH_GUIDE.md`.

### TEMPLATE.md
**Path:** `./TEMPLATE.md`  
**Purpose:** Defines the canonical structure for all vulnerability entries. Every new entry MUST follow this template to ensure consistent vectorization and searchability.

### solodit_fetcher.py
**Path:** `./solodit_fetcher.py`  
**Purpose:** Python script to fetch vulnerabilities from Solodit/Cyfrin database.

**Workflow:**
1. Query Solodit API for vulnerabilities matching a keyword (e.g., "pyth", "chainlink")
2. Download individual finding reports to a local directory
3. Use an LLM agent to analyze patterns across all findings
4. Aggregate common patterns into a structured database entry following TEMPLATE.md

**Usage:**
```bash
python solodit_fetcher.py --keyword "pyth" --output "./reports/pyth_findings/"
```

### Agents.md
**Path:** `./Agents.md`  
**Purpose:** Provides guidance for AI agents working with this repository, including conventions, invariants, and best practices.

---

## Raw Findings Folders

### Structure
The `reports/` directory at root level contains raw audit report folders, while `DB/` contains categorized vulnerability entries:

```
vuln-database/
├── reports/                    # Raw audit reports from various sources
│   ├── pyth_findings/          # 198 raw Pyth vulnerability reports
│   │   ├── m-01-missing-staleness-check-in-pythoracle-can-lead-to-forced-liquidations-and-th.md
│   │   ├── m-03-confidence-interval-of-pyth-price-is-not-validated.md
│   │   └── [190+ more reports].md
│   └── chainlink_findings/     # 564 raw Chainlink audit reports
│       └── [individual reports].md
└── DB/
    └── oracle/                 # Aggregated vulnerability patterns
        ├── pyth/
        │   └── PYTH_ORACLE_VULNERABILITIES.md
        └── chainlink/
            ├── CHAINLINK_PRICE_FEED_VULNERABILITIES.md
            ├── CHAINLINK_VRF_VULNERABILITIES.md
            ├── CHAINLINK_CCIP_VULNERABILITIES.md
            └── CHAINLINK_AUTOMATION_VULNERABILITIES.md
```

### Purpose
These folders serve as the **source data** for vulnerability pattern aggregation:

- **Raw reports** contain individual findings from specific audits (Sherlock, Pashov, OtterSec, Halborn, etc.)
- Each report includes the original audit firm's analysis, code snippets, and severity assessment
- Agents reference these files when creating or expanding aggregated vulnerability entries

### Naming Convention
Files follow the pattern: `[severity]-[issue-number]-[description].md`
- Examples: `m-01-missing-staleness-check...`, `h-02-price-manipulation...`
- Severity prefixes: `m-` (Medium), `h-` (High), `l-` (Low), `c-` (Critical)

### Usage by Agents
1. **Reading context:** Agents can read individual reports for detailed analysis
2. **Pattern extraction:** Multiple reports with similar issues indicate a vulnerability pattern
3. **Reference linking:** Aggregated entries link back to source reports for deeper investigation

---

## Variant Analysis Methodology

### What is Variant Analysis?

Variant analysis is the process of identifying recurring vulnerability patterns across multiple codebases and audit reports. Instead of treating each finding as isolated, we aggregate similar issues into comprehensive pattern databases.

### How This Repository Supports Variant Analysis

#### 1. Pattern Aggregation
**Process:**
- Fetch 100+ individual findings for a specific topic (e.g., "Pyth oracle")
- Identify common root causes across different protocols
- Group similar issues into vulnerability categories
- Document the pattern with multiple real-world examples

**Example:** The Pyth Oracle database identified 10 distinct vulnerability patterns from 198 individual findings:
- Staleness vulnerabilities (appeared in 15+ protocols)
- Confidence interval issues (appeared in 8+ protocols)
- Exponent handling bugs (appeared in 12+ protocols)
- etc.

#### 2. Cross-Protocol Pattern Recognition
**Benefits:**
- A vulnerability found in Protocol A can predict similar issues in Protocol B
- Auditors can search for variants of known patterns in new codebases
- Each pattern entry includes detection rules for automated scanning

#### 3. Severity Calibration
**Approach:**
- Preserve original severity ratings from audit firms
- Show severity variations across different contexts
- Help auditors assess impact based on protocol-specific factors

**Example:** Staleness checks rated as MEDIUM in lending protocols but HIGH in liquidation systems

#### 4. LLM-Optimized Structure
**Features:**
- **Keywords section:** Enables semantic search across patterns
- **Detection patterns:** Code-level search queries for pattern matching
- **Vulnerable vs Secure examples:** Side-by-side comparison for learning
- **Inline references:** Direct links to source reports for variant discovery

### Workflow for Variant Analysis

```
1. Fetch Findings
   ↓ (solodit_fetcher.py)
2. Store Raw Reports (reports/[topic]_findings/)
   ↓
3. Analyze Patterns (Agent reads all reports)
   ↓
4. Group Similar Issues (Pattern recognition)
   ↓
5. Create Aggregated Entry (Following TEMPLATE.md)
   ↓
6. Link References (Source reports + inline citations)
   ↓
7. Enable Variant Search (Keywords + Detection patterns)
```

### Using the Database for Variant Analysis

**For Auditors:**
1. Search keywords related to your target codebase (e.g., "oracle", "staleness")
2. Read aggregated patterns to understand all known variants
3. Apply detection patterns to find similar issues in your target
4. Reference source reports if you find a potential variant

**For Researchers:**
1. Identify a new vulnerability in a protocol
2. Search existing patterns to see if it's a known variant
3. If new: create a pattern entry following TEMPLATE.md
4. If variant: expand existing entry with new example

**For AI Agents:**
1. Use semantic search on keywords for relevant patterns
2. Match code snippets against vulnerable examples
3. Read referenced source reports for deeper understanding
4. Apply secure implementation patterns as fixes

---

## Database Entry Structure

Each vulnerability entry in `DB/` follows this hierarchy:

```
DB/
└── [category]/              # e.g., oracle, economic, logic
    └── [subcategory]/       # e.g., pyth, chainlink, twap
        └── [ENTRY].md       # Vulnerability pattern document
```

### Entry Contents

Every `.md` entry contains:
- **YAML Frontmatter:** Metadata for indexing (title, tags, severity, etc.)
- **Overview:** High-level description of the vulnerability class
- **Vulnerability Description:** Root cause and attack scenarios
- **Vulnerable Pattern Examples:** Real code snippets with severity tags
- **Secure Implementation:** Fixed code patterns
- **Detection Patterns:** Code patterns to search for during audits
- **Keywords:** Search terms for vector retrieval

---

## How Agents Should Use This Database

### For Variant Analysis
1. **Identify the vulnerability class** - Determine the category (oracle, economic, logic, etc.)
2. **Search aggregated patterns** - Read the relevant pattern database (e.g., PYTH_ORACLE_VULNERABILITIES.md)
3. **Find similar code patterns** - Match against vulnerable examples in the entry
4. **Read source reports** - Use inline references to read original audit findings
5. **Assess context** - Determine if the variant applies to your target codebase

### For Pattern Matching
1. Search by keywords in the vulnerability entries
2. Match code patterns against vulnerable examples
3. Reference source audit reports for deeper context

### For Creating New Entries
1. Use `solodit_fetcher.py` to gather raw findings
2. Analyze patterns across multiple audit reports
3. Structure the entry following `TEMPLATE.md`
4. Include inline references to source reports

### For Expanding Entries
1. Read existing entry to understand current coverage
2. Fetch new findings using `solodit_fetcher.py`
3. Add new patterns while preserving existing structure
4. Update reference tables with new sources

---

## Related Documentation

| Document | Path | Description |
|----------|------|-------------|
| **Index** | [DB/index.json](./DB/index.json) | ⭐ Master index - agents start here |
| Template | [TEMPLATE.md](./TEMPLATE.md) | Entry structure specification |
| Example | [Example.md](./Example.md) | Reference implementation |
| Agent Guide | [Agents.md](./Agents.md) | AI agent instructions |
| Usage Guide | [Readme.md](./Readme.md) | General usage instructions |
