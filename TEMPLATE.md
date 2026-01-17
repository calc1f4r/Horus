# Vulnerability Template

> **Purpose**: This template is optimized for vector database indexing and LLM-powered semantic search in Cursor. Follow this structure precisely to ensure effective pattern matching and retrieval.

---

## Template Structure

```markdown
---
# Core Classification (Required)
protocol: <protocol_name>              # e.g., "uniswap", "aave", "compound", "generic"
chain: <blockchain>                    # e.g., "ethereum", "bsc", "arbitrum", "everychain"
category: <vulnerability_category>     # e.g., "oracle", "reentrancy", "access_control", "arithmetic"
vulnerability_type: <specific_type>    # e.g., "stale_price", "price_manipulation", "frontrunning"

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

## Reference 
- [tag1] : location of the report for agent to give a through read for more accurate finding.
## Vulnerability Title

**Clear, Descriptive Title** - Should immediately convey the issue

### Overview

Brief 1-2 sentence summary of the vulnerability that captures the essence for semantic search.

### Vulnerability Description

Detailed explanation of the vulnerability with the following subsections:

#### Root Cause

Explain the fundamental issue that causes this vulnerability. Be specific about:
- What validation/check is missing
- What assumption is incorrect
- What edge case is not handled

#### Attack Scenario

Step-by-step explanation of how an attacker would exploit this:
1. Initial conditions/setup required
2. Actions taken by attacker
3. State changes that occur
4. Final outcome/impact

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
2. Create a new file: `oracle/vuln-<short-name>.md` (or appropriate category folder)
3. Fill in all required fields in the frontmatter
4. Write comprehensive descriptions with rich semantic context
5. Include multiple code examples showing variations

### 2. Optimizing for Vector Search

**Key Principles**:
- **Rich Context**: Write descriptive text that uses domain-specific terminology
- **Consistent Structure**: Always follow the same section order
- **Multiple Examples**: Provide variations to improve pattern matching
- **Semantic Keywords**: Include related concepts and synonyms
- **Clear Categorization**: Use precise, hierarchical categories in frontmatter

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
vuln-database/
├── TEMPLATE.md                    # This file
├── oracle/                        # Oracle-related vulnerabilities
│   ├── pyth-stale-price.md
│   ├── chainlink-no-validation.md
│   └── twap-manipulation.md
├── reentrancy/                    # Reentrancy vulnerabilities
├── access-control/                # Access control issues
├── arithmetic/                    # Math and overflow issues
├── economic/                      # Economic exploits
└── logic/                         # Business logic flaws
```

### 4. Using with Cursor/Vector Database

When the vulnerability database is indexed:
- **Contextual Retrieval**: Asking "show oracle vulnerabilities" will retrieve oracle category files
- **Semantic Matching**: Code patterns will match similar vulnerable code during audits
- **Multi-field Filtering**: Combine category + severity + protocol for precise results
- **Related Concepts**: Keywords and tags improve discovery of related issues

### 5. Quality Checklist

Before committing a new vulnerability:
- [ ] All required frontmatter fields are filled
- [ ] At least 3 vulnerable code examples provided
- [ ] At least 2 secure implementation examples included
- [ ] Impact analysis is comprehensive
- [ ] Keywords section includes 10+ relevant terms
- [ ] Real-world examples included (if available)
- [ ] Detection patterns clearly documented
- [ ] File is in correct category folder
