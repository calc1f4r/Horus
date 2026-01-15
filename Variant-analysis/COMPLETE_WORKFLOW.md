# Complete Variant Analysis Workflow for Report-Based Database Entry Creation

This document provides a step-by-step workflow for agents tasked with creating vulnerability database entries from audit reports.

## Overview

**Input:** Topic name (e.g., "pyth_oracle", "chainlink_oracle", "reentrancy")
**Output:** Comprehensive vulnerability database entry file following TEMPLATE.md format
**Source Data:** Multiple audit reports from `DB/reports/<topic>/`

## Complete Workflow

### Stage 1: Report Acquisition (15 minutes)

#### 1.1 Fetch Reports Using solodit_fetcher.py

```bash
# Navigate to database root
cd /home/calc1f4r/vuln-database

# Run fetcher script (NO quality filters!)
python solodit_fetcher.py --topic "topic_name" --output "DB/reports/topic_name/"
```

**Critical Rules:**
- ✅ Fetch ALL reports without filtering
- ✅ Create topic-specific subdirectory
- ✅ Verify download completion

#### 1.2 Inventory Reports

```bash
# List all fetched reports
ls -lh DB/reports/topic_name/

# Count total reports
ls DB/reports/topic_name/ | wc -l
```

**Expected Output:** 10-50+ individual report markdown files

---

### Stage 2: Initial Categorization (30 minutes)

#### 2.1 Quick Scan

Read ONLY the titles and first paragraph of each report to identify major categories.

**Create categorization document:**

```markdown
# Topic: [topic_name] - Initial Categorization

## Reports Summary
- Total Reports: [N]
- Date Range: [earliest] to [latest]
- Audit Firms: [list unique firms]

## Preliminary Categories

### Category 1: [Name]
- Report count: [N]
- Files:
  - file1.md
  - file2.md
  - ...

### Category 2: [Name]
- Report count: [N]
- Files:
  - file3.md
  - file4.md
  - ...
```

#### 2.2 Severity Distribution

Create quick severity overview:

| Severity | Count | Percentage |
|----------|-------|------------|
| CRITICAL | 2 | 5% |
| HIGH | 8 | 20% |
| MEDIUM | 22 | 55% |
| LOW | 8 | 20% |

---

### Stage 3: Deep Report Analysis (2-3 hours)

#### 3.1 Read Reports Systematically

For EACH report in your top category (minimum 10 reports):

**Create report analysis template:**

```markdown
## Report Analysis: [filename]

### Metadata
- **Protocol:** [name]
- **Auditor:** [firm]
- **Date:** [date]
- **Severity:** [rating]
- **Category:** [your categorization]

### Vulnerability Details

#### Root Cause
[Fundamental reason WHY vulnerability exists]

#### Attack Vector
[HOW an attacker would exploit it]

#### Vulnerable Code Pattern
```[language]
// Actual code from report
```

#### Impact
- **Technical:** [state corruption, calculation errors, etc.]
- **Financial:** [fund loss potential]
- **User:** [affected users/scenarios]

#### Fix Applied
```[language]
// Fixed code if available
```

### Pattern Classification
- **Exact Pattern:** [specific code structure]
- **General Pattern:** [abstracted pattern]
- **Variant Type:** [how it differs from others]

### Cross-Reference Notes
- Similar to: [other reports with same pattern]
- Differs from: [related but different patterns]
- Severity agreement: [yes/no with other reports]
```

#### 3.2 Cross-Report Pattern Matrix

After analyzing 10+ reports, create matrix:

| Report | Pattern Type | Severity | Unique Aspects | Protocol Type |
|--------|-------------|----------|----------------|---------------|
| mach-finance.md | No staleness check | MEDIUM | Liquidation context | Lending |
| astrolab.md | No staleness check | MEDIUM | Exchange rate calc | Vault |
| oku-protocol.md | Inverted logic | MEDIUM | Broke entire system | DEX |
| ... | ... | ... | ... | ... |

---

### Stage 4: Pattern Synthesis (1-2 hours)

#### 4.1 Identify Pattern Hierarchy

Organize patterns from specific to general:

```
Root Cause: [Fundamental security issue]
│
├── Vulnerability Class 1: [Pattern family 1]
│   ├── Variant A: [Specific manifestation]
│   │   └── Examples: report1.md, report3.md, report5.md
│   ├── Variant B: [Different manifestation]
│   │   └── Examples: report2.md, report7.md
│   └── Variant C: [Edge case]
│       └── Examples: report9.md
│
├── Vulnerability Class 2: [Pattern family 2]
│   ├── Variant A: [Specific manifestation]
│   │   └── Examples: report4.md, report6.md
│   └── Variant B: [Different manifestation]
│       └── Examples: report8.md, report10.md
│
└── Vulnerability Class 3: [Pattern family 3]
    └── ...
```

#### 4.2 Severity Consensus

For each pattern, establish consensus:

```markdown
### Pattern: [pattern_name]

#### Severity Assessment

| Source | Severity | Reasoning |
|--------|----------|-----------|
| Sherlock (Report A) | MEDIUM | "Can lead to unfair liquidations" |
| Pashov (Report B) | MEDIUM | "Price manipulation risk" |
| Code4rena (Report C) | LOW | "Requires specific conditions" |
| Internal (Report D) | MEDIUM | "High impact, medium likelihood" |

**Consensus:** MEDIUM (3/4 auditors)
**Range:** LOW to MEDIUM
**Database Entry Severity:** MEDIUM (using consensus)
```

#### 4.3 Impact Aggregation

Compile impact statements across all reports:

```markdown
### Impact Analysis: [pattern_name]

#### Technical Impact (from reports)
- State corruption in pricing module (8/12 reports)
- Incorrect liquidation calculations (5/12 reports)
- DoS via price staleness (1/12 reports)
- Cascading errors in dependent systems (3/12 reports)

#### Business Impact (from reports)
- Direct fund loss to users (7/12 reports)
- Unfair treatment of healthy positions (4/12 reports)
- Protocol insolvency risk (2/12 reports)
- Reputation damage (mentioned in 3/12 reports)

#### Affected Scenarios (from reports)
- High volatility periods (10/12 reports)
- Low liquidity markets (5/12 reports)
- Network congestion (2/12 reports)
- Oracle downtime (4/12 reports)
```

---

### Stage 5: Database Entry Writing (2-4 hours)

#### 5.1 Initialize Entry from Template

```bash
# Copy template
cp TEMPLATE.md DB/oracle/topic_name/VULNERABILITY_NAME.md
```

#### 5.2 Fill Frontmatter

```yaml
---
# Core Classification
protocol: generic  # or specific protocol name
chain: everychain  # or specific: ethereum, arbitrum, etc.
category: oracle  # oracle, reentrancy, access_control, etc.
vulnerability_type: stale_price  # specific vulnerability type

# Attack Vector Details
attack_type: data_manipulation  # or economic_exploit, logical_error
affected_component: price_feed  # specific component

# Oracle-Specific (if applicable)
oracle_provider: pyth  # pyth, chainlink, band, etc.
oracle_attack_vector: staleness  # staleness, manipulation, etc.

# Technical Primitives
primitives:
  - timestamp_validation
  - price_freshness
  - oracle_integration
  # Add all relevant primitives

# Impact Classification
severity: medium  # Use consensus from analysis
impact: incorrect_pricing  # Primary impact type
exploitability: 0.7  # 0.0 (hard) to 1.0 (trivial)
financial_impact: high  # none, low, medium, high, critical

# Context Tags
tags:
  - defi
  - lending
  - pull_oracle
  # Add relevant tags

# Version Info
language: solidity  # solidity, rust, move, cairo
version: all  # or specific version constraints
---
```

#### 5.3 Create References Table

```markdown
## References & Source Reports

> **For Agents**: Read the full reports from the referenced file paths for detailed information.

### [Category Name] Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Protocol A - Issue Description | `DB/reports/topic/file1.md` | MEDIUM | Sherlock |
| Protocol B - Issue Description | `DB/reports/topic/file2.md` | MEDIUM | Pashov |
| Protocol C - Issue Description | `DB/reports/topic/file3.md` | HIGH | Code4rena |

### [Another Category] Vulnerabilities
| Report | Path | Severity | Audit Firm |
|--------|------|----------|------------|
| Protocol D - Issue Description | `DB/reports/topic/file4.md` | LOW | OtterSec |
...
```

**Critical:** Only reference files that ACTUALLY exist in `DB/reports/`

#### 5.4 Write Overview Section

```markdown
## 1. [Vulnerability Class Name]

### Overview

[2-3 sentences with rich semantic context about the vulnerability class. Include:
- What the vulnerability is fundamentally about
- Why it exists in the system/protocol
- What makes it dangerous/exploitable
- What systems/operations are affected]

> **📚 Source Reports for Deep Dive:**
> - `DB/reports/topic/report1.md` (Protocol A - Auditor)
> - `DB/reports/topic/report2.md` (Protocol B - Auditor)
> - `DB/reports/topic/report3.md` (Protocol C - Auditor)

```

**Optimization for Vector Search:**
- Use domain-specific terminology
- Include attack context
- Mention affected components
- Add related concepts and synonyms

#### 5.5 Write Vulnerability Description

```markdown
### Vulnerability Description

#### Root Cause

[Detailed explanation of WHY the vulnerability exists. Be specific about:
- What validation/check is missing or incorrect
- What assumption is wrong
- What edge case is not handled
- What security principle is violated]

#### Attack Scenario

[Step-by-step exploitation scenario:]

1. [Initial state/condition]
2. [Attacker action 1]
3. [System response/state change]
4. [Attacker action 2]
5. [Final outcome/impact]

[Include specific numbers, timeframes, and concrete examples where possible]
```

#### 5.6 Create Vulnerable Pattern Examples

**For each pattern variant:**

```markdown
**Example [N]: [Specific Pattern Description]** [SEVERITY]
> 📖 Reference: `DB/reports/topic/actual-file.md`

```solidity
// ❌ VULNERABLE: [Why this specific code is vulnerable]
// Impact: [Specific impact of this pattern]
// Context: [Where/when this appears]
function vulnerableFunction(params) {
    // Actual vulnerable code from report
    // Include enough context to understand the issue
}
```
```

**Rules:**
- Minimum 3-5 examples per vulnerability class
- Each labeled with approximate severity: [CRITICAL|HIGH|MEDIUM|LOW]
- Reference actual source report
- Include inline comments explaining the vulnerability
- Show realistic, complete code (not fragments)
- Preserve original variable names and logic from reports

#### 5.7 Write Impact Analysis

```markdown
### Impact Analysis

#### Technical Impact
- [Impact 1 with frequency]: [Description] ([X]/[Total] reports)
- [Impact 2 with frequency]: [Description] ([X]/[Total] reports)
- [Impact 3 with frequency]: [Description] ([X]/[Total] reports)

#### Business Impact
- [Business impact 1]: [Description with real examples from reports]
- [Business impact 2]: [Description with quantification where available]
- [Business impact 3]: [Reputation/trust implications]

#### Affected Scenarios
- **[Scenario 1]**: [When/where this vulnerability manifests]
- **[Scenario 2]**: [Specific use cases at risk]
- **[Scenario 3]**: [Compounding factors that increase severity]
```

#### 5.8 Create Secure Implementation Section

```markdown
### Secure Implementation

**Fix 1: [Recommended Approach]**
```solidity
// ✅ SECURE: [Explanation of why this is secure]
// Prevents: [What attack vectors this blocks]
function secureImplementation(params) {
    // Correct implementation showing proper validation
    // Include comments explaining security measures
}
```

**Fix 2: [Alternative Approach]**
```solidity
// ✅ SECURE: [Different but equally valid approach]
// Trade-offs: [Any considerations]
function alternativeSecure(params) {
    // Another correct pattern
}
```
```

**Provide minimum 2-3 different secure implementation approaches**

#### 5.9 Write Detection Patterns

```markdown
### Detection Patterns

#### Code Patterns to Look For
```
- Pattern 1: [Specific code smell] - Example: `getPriceUnsafe()` without `publishTime` check
- Pattern 2: [Anti-pattern] - Example: Comparison with `type(uint64).max` tolerance
- Pattern 3: [Warning sign] - Example: `publishTime > 0` as only validation
- Pattern 4: [Edge case indicator] - Example: Missing null/zero checks
```

#### Audit Checklist
- [ ] [Specific check 1]: Verify all `functionX()` calls include `validationY()`
- [ ] [Specific check 2]: Ensure tolerance parameters are reasonable (< [threshold])
- [ ] [Specific check 3]: Check edge case handling for [condition]
- [ ] [Specific check 4]: Validate error handling for [scenario]
- [ ] [Specific check 5]: Confirm fallback mechanism exists for [failure mode]
```

#### 5.10 Add Real-World Examples

```markdown
### Real-World Examples

#### Known Exploits & Findings
- **[Protocol Name]** - [Brief description] - [Date if available]
  - Severity: [Actual severity from audit]
  - Auditor: [Audit firm]
  - Reference: `DB/reports/topic/file.md`
  - Root cause: [Specific technical issue]
  - Impact: [$Amount if disclosed] or [qualitative impact]

[Repeat for 3-5 major examples]

#### Related CVEs/Reports
- [Industry report or CVE if applicable]
- [Research paper or analysis]
```

#### 5.11 Create Keyword Section

```markdown
### Keywords for Search

> These keywords enhance vector search retrieval - comprehensive list of related terms:

**Core Terms:** `primary_keyword`, `vulnerability_type`, `function_name`, `api_call`

**Attack Vectors:** `attack_method_1`, `exploitation_technique`, `bypass_method`

**Impacts:** `fund_loss`, `price_manipulation`, `dos`, `state_corruption`

**Related APIs:** `related_function_1`, `similar_api_2`, `alternative_method_3`

**Affected Systems:** `protocol_type_1`, `defi_primitive`, `smart_contract_type`

**Code Patterns:** `anti_pattern_1`, `missing_validation_type`, `logic_error_class`

**Synonyms:** `alternative_term_1`, `related_concept`, `similar_vulnerability`

**Protocols:** `example_protocol_1`, `affected_project_2` (from actual reports)
```

**Aim for 20-30+ total keywords across categories**

#### 5.12 Link Related Vulnerabilities

```markdown
### Related Vulnerabilities

**Compounds With:**
- [[Link to related vuln file]](../path/to/file.md) - [Why they compound]
- [[Another related vuln]](../path/to/file.md) - [Interaction description]

**Enables:**
- [[Downstream vulnerability]](../path/to/file.md) - [How this enables that]

**Part of Family:**
- [[Parent category]](../path/to/file.md) - [Hierarchical relationship]
- [[Sibling vulnerability]](../path/to/file.md) - [Related pattern]
```

---

### Stage 6: Quality Assurance (30-60 minutes)

#### 6.1 Reference Verification Checklist

- [ ] All file paths in references table are actual files
- [ ] Verify each path: `ls DB/reports/topic/referenced-file.md`
- [ ] No hallucinated report names or protocols
- [ ] All severity ratings match source reports
- [ ] All audit firm names are correct

#### 6.2 Content Quality Checklist

- [ ] Minimum 5-10 reports analyzed per vulnerability class
- [ ] At least 3-5 vulnerable pattern examples
- [ ] At least 2-3 secure implementation examples  
- [ ] Severity is consensus-based, not overstated
- [ ] Impact analysis has technical + business + scenario coverage
- [ ] Detection patterns are specific and actionable
- [ ] Keywords comprehensive (20+ terms)
- [ ] All code examples have inline explanations
- [ ] Overview section has rich semantic context

#### 6.3 Accuracy Verification

- [ ] No severity inflation (use LOWEST when reports disagree)
- [ ] No synthetic examples unmarked as such
- [ ] Cross-checked pattern frequency claims
- [ ] Verified all protocol names mentioned exist in reports
- [ ] Confirmed all $ amounts match source reports
- [ ] No speculation about impacts not in reports

#### 6.4 Search Optimization Check

- [ ] Overview uses domain-specific terminology
- [ ] Descriptions include attack scenarios
- [ ] Keywords cover synonyms and related concepts
- [ ] Code examples labeled with `❌ VULNERABLE` / `✅ SECURE`
- [ ] Severity tags present: `[CRITICAL|HIGH|MEDIUM|LOW]`
- [ ] Reference markers: `> 📖 Reference:` formatted correctly

---

### Stage 7: Finalization (15 minutes)

#### 7.1 Create Tracking Document

```markdown
## Variant Analysis Completion Report: [topic_name]

### Statistics
- **Total Reports Analyzed:** [N]
- **Vulnerability Classes Identified:** [N]
- **Database Entries Created:** [N]
- **Analysis Duration:** [hours]
- **Completion Date:** [date]

### Coverage Matrix

| Vulnerability Class | Reports | Entries | Status |
|---------------------|---------|---------|--------|
| [Class 1] | 12 | 1 | ✅ Complete |
| [Class 2] | 8 | 1 | ✅ Complete |
| [Class 3] | 5 | 1 | 🔄 Partial |

### Quality Metrics

- Average reports per entry: [N]
- Average examples per entry: [N]
- Reference accuracy: 100% ✅
- Severity validation: 100% ✅
- Hallucination incidents: 0 ✅

### Files Created

- `DB/oracle/topic_name/vulnerability_1.md`
- `DB/oracle/topic_name/vulnerability_2.md`
- ...

### Notes & Observations

[Any patterns observed, recommendations for future analysis, etc.]
```

#### 7.2 Submit for Review

Create checklist for reviewer:

```markdown
## Review Checklist for [entry_name]

### Structural Completeness
- [ ] Frontmatter filled correctly
- [ ] References table present with working links
- [ ] All major sections present (Overview, Description, Impact, etc.)
- [ ] Minimum example counts met

### Content Quality  
- [ ] Root cause clearly explained
- [ ] Attack scenarios realistic and detailed
- [ ] Severity justified and consensus-based
- [ ] Impact analysis comprehensive

### Accuracy
- [ ] All references verified
- [ ] No hallucinated protocols or findings
- [ ] Severity matches source reports
- [ ] Code examples from actual reports

### Search Optimization
- [ ] Rich semantic context in overview
- [ ] Comprehensive keyword coverage
- [ ] Proper labeling and formatting
- [ ] Cross-links to related vulnerabilities
```

---

## Quick Reference: Critical Rules

### MUST DO ✅

1. Analyze **minimum 5-10 reports** before creating entry
2. Include **actual references** to files in `DB/reports/`
3. Label **each code example** with severity: `[CRITICAL|HIGH|MEDIUM|LOW]`
4. Provide **multiple pattern variants** (not just one)
5. Write **rich semantic descriptions** for vector search
6. Include **both vulnerable AND secure** implementations
7. **Cross-validate severity** across multiple sources
8. Use **consensus severity** (prefer LOWEST when disagreement)

### NEVER DO ❌

1. **Overstate severity** beyond what reports document
2. **Hallucinate references** to non-existent reports
3. **Create synthetic examples** without labeling as illustrative
4. **Single-source entries** from only 1-2 reports
5. **Vague descriptions** without technical details
6. **Incomplete code** fragments without context
7. **Skip impact analysis** sections
8. **Apply quality filters** when fetching reports

---

## Estimated Time Budget

| Stage | Time | Cumulative |
|-------|------|------------|
| 1. Report Acquisition | 15 min | 15 min |
| 2. Initial Categorization | 30 min | 45 min |
| 3. Deep Report Analysis | 2-3 hours | 3-4 hours |
| 4. Pattern Synthesis | 1-2 hours | 4-6 hours |
| 5. Database Entry Writing | 2-4 hours | 6-10 hours |
| 6. Quality Assurance | 30-60 min | 7-11 hours |
| 7. Finalization | 15 min | 7-11 hours |

**Total per major vulnerability class:** 7-11 hours

**For topics with multiple classes:** Multiply by number of distinct classes

---

## Success Criteria

A high-quality database entry:

- ✅ Based on **10+ real audit reports**
- ✅ Contains **5+ vulnerable pattern examples** with references
- ✅ Includes **2+ secure implementations**
- ✅ Has **comprehensive impact analysis** (technical, business, scenarios)
- ✅ Provides **actionable detection patterns** and audit checklist
- ✅ Contains **20+ keywords** for semantic search
- ✅ **All references verified** and point to actual files
- ✅ **Severity consensus-based** and justified
- ✅ **No hallucinations** - every claim traceable to source
- ✅ **Search-optimized** with rich semantic context

---

## Troubleshooting

### Issue: Not enough reports for a pattern

**Solution:** 
- Broaden search to include related patterns
- Check if pattern should be subsection of larger class
- Document as "limited evidence" pattern

### Issue: Conflicting severity ratings

**Solution:**
- Create severity consensus table
- Use LOWEST severity for database entry
- Document range in description

### Issue: Unclear root cause

**Solution:**
- Re-read reports focusing on "why" not "what"
- Look for commonality across multiple reports
- Consult technical documentation for the component

### Issue: Too many pattern variants

**Solution:**
- Create hierarchical organization
- Group related variants under common parent
- Consider splitting into multiple database entries

---

## Next Steps After Completion

1. **Cross-link**: Update related vulnerability entries with links to new entry
2. **Index**: Ensure vector database includes new entry
3. **Validate**: Have another agent review using quality checklist
4. **Iterate**: Apply lessons learned to next vulnerability class analysis
