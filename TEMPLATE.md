# Vulnerability Template

> **Purpose**: This template is optimized for vector database indexing, low-context agent retrieval, and hunt-card generation. Follow this structure precisely so entries stay compact, grep-able, and semantically rich.

## Design Goals

- Front-load the first `~120-150` lines with source references, root cause, triage guidance, and grep seeds.
- Separate materially different exploit paths instead of collapsing them into one generic attack story.
- Include explicit false-positive guards so agents can reject weak matches earlier.
- Keep optional deep-dive material near the bottom so agents can stop reading once they have enough evidence.

---

## Template Structure

```markdown
---
# Core Classification (Required)
protocol: <protocol_name>              # e.g., "uniswap", "aave", "compound", "generic"
chain: <blockchain>                    # e.g., "ethereum", "bsc", "arbitrum", "everychain"
category: <vulnerability_category>     # e.g., "oracle", "reentrancy", "access_control", "arithmetic"
vulnerability_type: <specific_type>    # e.g., "stale_price", "price_manipulation", "frontrunning"

# Pattern Identity (Required)
root_cause_family: <root_cause_family> # e.g., "missing_validation", "rounding_error", "callback_reentrancy"
pattern_key: <missing_control> | <component> | <trigger> | <sink>

# Attack Vector Details (Required)
attack_type: <attack_classification>   # e.g., "data_manipulation", "economic_exploit", "logical_error"
affected_component: <component>        # e.g., "price_feed", "validation_logic", "state_transition"

# Oracle-Specific Fields (if category: oracle)
oracle_provider: <provider>            # e.g., "chainlink", "pyth", "uniswap_twap", "custom"
oracle_attack_vector: <vector>         # e.g., "staleness", "manipulation", "sandwich", "variance"

# Technical Primitives (Required - list all applicable)
primitives:
  - <primitive_1>                      # e.g., "confidence_interval", "timestamp", "price_feed"
  - <primitive_2>                      # e.g., "aggregation", "validation", "staleness_check"
  - <primitive_3>                      # Add all relevant technical components

# Grep / Hunt-Card Seeds (Required)
code_keywords:
  - <keyword_1>                        # grep-able identifier, function, modifier, storage var, selector, or error name
  - <keyword_2>
  - <keyword_3>
  - <keyword_4>

# Impact Classification (Required)
severity: <critical|high|medium|low>
impact: <impact_type>                  # e.g., "incorrect_pricing", "fund_loss", "dos", "manipulation"
exploitability: <0.0-1.0>             # Likelihood score: 0.0 (hard) to 1.0 (trivial)
financial_impact: <none|low|medium|high|critical>

# Context Tags (Optional but recommended)
tags:
  - <tag_1>                            # e.g., "defi", "lending", "dex"
  - <tag_2>                            # e.g., "time_dependent", "external_dependency"
  
# Version Info (Optional)
language: <solidity|rust|move|cairo>
version: <version_affected>            # e.g., ">=0.8.0", "all"
---

## References & Source Reports

> Keep this near the top. Agents should be able to find supporting reports without reading the entire entry.

| Label | Path | Severity | Auditor | Source ID / Link |
|-------|------|----------|---------|------------------|
| [tag1] | reports/<topic>_findings/file.md | HIGH | <audit_firm> | <solodit_id or link> |

## Vulnerability Title

**Clear, Descriptive Title** - Should immediately convey the issue

### Overview

Brief 1-2 sentence summary of the vulnerability that captures the essence for semantic search.

#### Agent Quick View

- Root cause statement: "This vulnerability exists because ..."
- Pattern key: `<missing_control> | <component> | <trigger> | <sink>`
- Primary affected component(s): `<component / contract / function family>`
- High-signal code keywords: `<keyword_1>, <keyword_2>, <keyword_3>, ...`
- Typical sink / impact: `<fund loss / accounting corruption / griefing / unfair liquidation / DoS>`
- Validation strength: `<strong | moderate | weak>`

#### Valid Bug Signals

- Signal 1: <what must be true for this to be a real reportable bug>
- Signal 2: <state / attacker control / missing validation that confirms exploitability>
- Signal 3: <impact-producing condition>

#### False Positive Guards

- Not this bug when: <existing mitigation, upstream guard, unreachable path, dust-only impact>
- Safe if: <correct validation or invariant is already enforced>
- Requires attacker control of: <oracle, callback, token, config, governance action, etc.>

### Vulnerability Description

Detailed explanation of the vulnerability with the following subsections:

#### Root Cause

Explain the fundamental issue that causes this vulnerability. Be specific about:
- What validation/check is missing
- What assumption is incorrect
- What edge case is not handled

#### Attack Scenario / Path Variants

Describe each materially distinct exploit path separately. Use `Path A`, `Path B`, `Path C` when the bug can be reached through different entry points, trust assumptions, or sinks.

**Path A: [Primary Exploit Path]**
1. Initial conditions/setup required
2. Actions taken by attacker
3. State changes that occur
4. Final outcome/impact

**Path B: [Alternate Exploit Path]**
1. Different setup or trigger
2. Different attacker action or dependency
3. State change / invariant break
4. Final outcome/impact

**Path C: [Edge / Cross-Function Path]**
1. Optional multi-step or cross-contract route
2. ...

#### Vulnerable Pattern Examples

Provide multiple real-world code examples showing the vulnerability:

**Example 1: [Specific Issue Name]** [Approx Vulnerability : MID| LOW | HIGH | CRITICAL]
```solidity
// ❌ VULNERABLE: [Specific reason why this is vulnerable]
function vulnerableFunction() public {
    // Vulnerable code pattern
    // Include inline comments explaining the issue
}
```

**Example 2: [Another Variant]** [Approx Vulnerability : MID| LOW | HIGH | CRITICAL]
```solidity
// ❌ VULNERABLE: [Another specific issue]
function anotherVulnerablePattern() public {
    // Different manifestation of the same vulnerability
}
```

**Example 3: [Edge Case]**   [Approx Vulnerability : MID| LOW | HIGH | CRITICAL]
```solidity
// ❌ VULNERABLE: [Edge case scenario]
function edgeCaseVulnerable() public {
    // Less obvious vulnerable pattern
}
```

### Impact Analysis

#### Technical Impact
- List specific technical consequences
- Include state corruption details
- Explain cascading effects

#### Business Impact
- Financial loss potential
- User trust implications
- Protocol stability concerns

#### Affected Scenarios
- Specific use cases where this is exploitable
- Conditions that increase severity
- Related vulnerabilities that compound the issue

### Secure Implementation

Provide multiple examples of correct implementations:

**Fix 1: [Recommended Approach]**
```solidity
// ✅ SECURE: [Explanation of why this is secure]
function secureImplementation() public {
    // Properly implemented code
    // Include inline comments explaining the security measures
}
```

**Fix 2: [Alternative Approach]**
```solidity
// ✅ SECURE: [Alternative secure pattern]
function alternativeSecureImplementation() public {
    // Another valid secure implementation
}
```

### Detection Patterns

#### High-Signal Grep Seeds
```
- keyword_1
- keyword_2
- keyword_3
- keyword_4
```

#### Code Patterns to Look For
```
- Pattern 1: [Specific code smell or anti-pattern]
- Pattern 2: [Another indicator]
- Pattern 3: [Warning sign in the codebase]
```

#### Audit Checklist
- [ ] Check 1: [Specific validation to perform]
- [ ] Check 2: [Another security check]
- [ ] Check 3: [Edge case to verify]

### Real-World Examples

#### Known Exploits
- **[Protocol Name]** - [Brief description] - [Date] - [$Amount if applicable]
  - Link: [URL to post-mortem if available]
  - Root cause: [Specific issue]

#### Related CVEs/Reports
- CVE-XXXX-XXXXX: [Description]
- Audit Report: [Reference]

### Prevention Guidelines

#### Development Best Practices
1. [Specific coding guideline]
2. [Testing requirement]
3. [Review checklist item]

#### Testing Requirements
- Unit tests for: [Specific test cases]
- Integration tests for: [Scenarios to test]
- Fuzzing targets: [Areas to fuzz]

### References

#### Technical Documentation
- [Link to relevant documentation]
- [Standard or specification reference]
- [Best practice guide]

#### Security Research
- [Relevant security paper or article]
- [Analysis or deep-dive]
- [Tool or scanner that detects this]

### Keywords for Search

> These keywords enhance vector search retrieval - include comprehensive terms:

`keyword1`, `keyword2`, `keyword3`, `related_concept1`, `related_concept2`, `common_variant1`, `common_variant2`

### Related Vulnerabilities

- [Link to related vulnerability file]
- [Another related pattern]
- [Compound vulnerability scenario]

---

## Notes for Database Usage

- **Semantic Search**: The Overview and Description sections are most important for embedding
- **Metadata Filtering**: Use frontmatter fields to filter by category, severity, etc.
- **Code Pattern Matching**: Vulnerable and secure examples help LLMs recognize similar patterns
- **Context Relevance**: Tags and keywords improve retrieval precision for specific audit contexts
```

---

## Usage Instructions

### 1. Creating a New Vulnerability Entry

1. Copy the template structure above (everything within the markdown code block)
2. Create a new file under `DB/<category-or-subfolder>/...` using the existing repository layout
3. Fill in all required fields in the frontmatter, especially `root_cause_family`, `pattern_key`, and `code_keywords`
4. Front-load the entry: the top of the file should let an agent understand the bug without reading the appendix
5. If there are multiple exploit routes, enumerate them explicitly as `Path A`, `Path B`, `Path C`
6. Include multiple code examples showing variations
7. Run `python3 generate_manifests.py` after adding or substantially changing DB content

### 1A. Migrating An Existing Vulnerability Entry

1. If a legacy `DB/**/*.md` entry already covers the pattern, migrate that file in-place instead of creating a new duplicate
2. Upgrade the frontmatter to include all current required fields, especially `root_cause_family`, `pattern_key`, and `code_keywords`
3. Add the low-context triage sections near the top: `Agent Quick View`, `Valid Bug Signals`, and `False Positive Guards`
4. Split blended exploit narratives into explicit `Path A / Path B / Path C` variants when the trigger or sink changes
5. Preserve evidence-rich legacy content, references, and code examples; reorganize rather than delete whenever possible
6. Regenerate manifests after migration so hunt cards and keyword routing reflect the new structure

### 2. Optimizing for Vector Search

**Key Principles**:
- **Rich Context**: Write descriptive text that uses domain-specific terminology
- **Consistent Structure**: Always follow the same section order
- **Multiple Examples**: Provide variations to improve pattern matching
- **Semantic Keywords**: Include related concepts and synonyms
- **Clear Categorization**: Use precise, hierarchical categories in frontmatter
- **Low-Context Retrieval**: Put the root cause statement, valid bug signals, false-positive guards, and grep seeds near the top
- **Exploit Path Separation**: Split distinct paths instead of mixing deposit-path, withdraw-path, callback-path, and governance-path logic together
- **False-Positive Control**: Explicitly document when the pattern is *not* reportable

**Example Categories**:
```yaml
# Oracle Vulnerabilities
category: oracle
vulnerability_type: [stale_price|price_manipulation|confidence_interval|aggregation|frontrunning|variance_attack]
oracle_provider: [chainlink|pyth|uniswap_twap|band|api3|custom]

# Access Control
category: access_control
vulnerability_type: [missing_access|privilege_escalation|role_confusion|unprotected_init]

# Reentrancy
category: reentrancy
vulnerability_type: [classic_reentrancy|cross_function|read_only|cross_contract]

# Economic
category: economic
vulnerability_type: [flash_loan|sandwich|mev|arbitrage|liquidity_manipulation]
```

### 3. Folder Structure

```
Vulnerability-database/
├── TEMPLATE.md
├── DB/
│   ├── oracle/
│   ├── amm/
│   ├── bridge/
│   ├── tokens/
│   ├── general/
│   └── unique/
├── DB/index.json                  # Router
├── DB/manifests/*.json            # Pattern indexes
└── DB/manifests/huntcards/*.json  # Hunt cards
```

### 4. Using with Cursor/Vector Database

When the vulnerability database is indexed:
- **Contextual Retrieval**: Asking "show oracle vulnerabilities" will retrieve oracle category files
- **Semantic Matching**: Code patterns will match similar vulnerable code during audits
- **Multi-field Filtering**: Combine category + severity + protocol for precise results
- **Related Concepts**: Keywords and tags improve discovery of related issues
- **Fast Triage**: Agents can often stop after `References & Source Reports`, `Agent Quick View`, and `Detection Patterns`

### 5. Quality Checklist

Before committing a new vulnerability:
- [ ] All required frontmatter fields are filled
- [ ] `root_cause_family`, `pattern_key`, and `code_keywords` are present and specific
- [ ] The first ~150 lines contain enough context for a low-window agent to triage the bug
- [ ] `Valid Bug Signals` and `False Positive Guards` are explicit
- [ ] Distinct exploit routes are split into `Path A / B / C` where applicable
- [ ] At least 3 vulnerable code examples provided
- [ ] At least 2 secure implementation examples included
- [ ] Impact analysis is comprehensive
- [ ] Keywords section includes 10+ relevant terms
- [ ] Real-world examples included (if available)
- [ ] Detection patterns clearly documented
- [ ] `code_keywords` and `High-Signal Grep Seeds` are grep-able identifiers, not generic prose
- [ ] File is in the correct `DB/` category folder and manifests were regenerated if needed

### 6. Notes For Example.md

- `TEMPLATE.md` is the authoritative structure.
- `Example.md` is a style reference and may be more verbose or composite than a single-pattern entry.
- Prefer the template's compact top-of-file structure when there is any conflict.
