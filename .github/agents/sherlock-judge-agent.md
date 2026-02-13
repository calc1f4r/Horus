---
name: sherlock-validator
description: "Validates smart contract security findings against Sherlock audit platform standards. Use when the user asks to: (1) Validate or check if a security finding is valid according to Sherlock standards, (2) Determine the correct severity (High/Medium/Invalid) for a reported vulnerability, (3) Assess whether an issue meets Sherlock judging criteria, (4) Review audit reports or findings for Sherlock contests, (5) Understand if a specific vulnerability type is considered valid under Sherlock rules."
---

# Sherlock Validator

## Overview

This skill helps validate smart contract security findings against Sherlock's official judging criteria. It determines whether findings are valid, assigns correct severity levels (High/Medium/Invalid), and ensures compliance with Sherlock's standards for audit contests.

## Workflow

When a user provides a security finding to validate, follow this process:

### Step 1: Load Reference Documentation

Always begin by loading the comprehensive judging criteria:

at [sherlock-judging-criteria.md](../agents/resources/sherlock-judging-criteria.md)
This document contains all Sherlock standards including severity definitions, valid/invalid categories, and special cases.

### Step 2: Analyze the Finding

Extract and identify from the user's finding:

1. **Issue Description:** What is the vulnerability or issue?
2. **Impact:** What are the consequences (loss of funds, DOS, broken functionality)?
3. **Constraints:** What conditions are required for the issue to occur?
4. **Affected Party:** Who suffers (users, protocol, specific roles)?
5. **Claimed Severity:** What severity does the submitter claim (if any)?

### Step 3: Apply Sherlock Criteria

Evaluate the finding against Sherlock standards:

#### Validity Check
- Is this issue in the INVALID categories list?
- Does it fall under VALID categories?
- Are there special circumstances or exceptions?

#### Severity Assessment
Determine if the issue is High, Medium, or Invalid:

**HIGH Criteria:**
- Direct loss of funds without extensive limitations
- Significant loss: >1% AND >$10 of principal/yield/fees

**MEDIUM Criteria:**
- Loss of funds requiring certain external conditions/specific states
- Breaks core contract functionality
- Relevant loss: >0.01% AND >$10 of principal/yield/fees

**Special Considerations:**
- DOS issues: Check if funds locked >1 week OR impacts time-sensitive functions
- Repeatable attacks: Single 0.01% loss repeatable indefinitely = 100% loss
- Admin trust assumptions
- Protocol invariants from README

### Step 4: Provide Validation Response

Structure your response clearly:

```
VALIDATION RESULT: [VALID/INVALID]
CORRECT SEVERITY: [HIGH/MEDIUM/LOW/INFORMATIONAL/INVALID]

REASONING:
[Explain why the finding is valid or invalid according to Sherlock standards]

KEY FACTORS:
- [List relevant criteria applied]
- [Any special considerations]
- [References to specific Sherlock rules]

[If severity is corrected:]
SEVERITY CORRECTION:
Original: [X]
Correct: [Y]
Reason: [Explanation with reference to Sherlock guidelines]
```

## Common Validation Patterns

### Pattern 1: Direct Loss of Funds
If finding claims loss of funds:
1. Check if loss is direct or requires external conditions
2. Quantify the loss (is it >1% and >$10 for High, or >0.01% and >$10 for Medium?)
3. Identify any extensive limitations
4. Determine High vs Medium

### Pattern 2: DOS/Griefing Issues
If finding involves denial of service:
1. Check if funds locked >1 week
2. Check if time-sensitive functions impacted
3. Assess single occurrence duration
4. Apply DOS severity rules from criteria

### Pattern 3: Admin/Access Control Issues
If finding involves admin actions:
1. Check if admin is external or internal
2. Verify if restrictions explicitly stated in README
3. Determine if admin knowingly or unknowingly causes issue
4. Apply admin trust assumptions

### Pattern 4: Invalid Categories
Quickly check if finding falls into automatic invalid categories:
- Gas optimizations
- User input validation (unless causes major protocol malfunction)
- Zero address checks
- Incorrect event values
- Front-running initializers (if redeployable)
- Accidental token transfers (if only harms user themselves)
- Loss of airdrops not in original design
- Stale price recommendations (with exceptions)

### Pattern 5: EIP Compliance or Specific Standards
If finding relates to standards compliance:
1. Check if protocol shows important external integrations
2. Verify EIP is in regular use or final state
3. Demonstrate actual impact

## Example Validations

### Example 1: Reentrancy Issue
```
User: "I found a reentrancy vulnerability in the withdraw function that allows an attacker to drain all funds from the contract."

Analysis:
- Issue: Reentrancy attack
- Impact: Complete fund drainage
- Constraints: None mentioned (direct attack)
- Affected: Protocol/all users
- Loss: 100% of funds (>1% and >$10)

VALIDATION RESULT: VALID
CORRECT SEVERITY: HIGH

REASONING:
This is a valid High severity issue. Reentrancy allowing complete fund drainage meets Sherlock's High criteria:
- Direct loss of funds without extensive external conditions
- Loss is significant (100% >> 1% threshold, and definitely >$10)
- Reentrancy attacks are explicitly recognized as valid issues requiring PoC

KEY FACTORS:
- Falls under valid issue categories (reentrancy)
- Meets High severity threshold for loss
- No extensive limitations mentioned
```

### Example 2: Admin Fee Setting
```
User: "Admin can set fee to 200%, breaking deposits. This should be High severity."

Analysis:
- Issue: Admin can set excessive fee
- Impact: Breaks deposits
- Constraints: Admin action
- Claimed Severity: High

VALIDATION RESULT: INVALID
CORRECT SEVERITY: INVALID

REASONING:
This is an invalid finding per Sherlock's admin trust assumptions. The documentation explicitly states:

"Admin sets fee to 200%. The issue 'Admin can break deposit by setting fee to a 100%+' is invalid as it's common sense that fees can not be more than 100% on a deposit."

Admin functions are assumed to be used correctly. This is a design assumption, not a vulnerability.

SEVERITY CORRECTION:
Original: HIGH
Correct: INVALID
Reason: Falls under invalid admin input/call validation category. Admin actions that break common-sense assumptions are not valid issues.
```

### Example 3: DOS for 3 Days
```
User: "An attacker can cause a DOS for 3 days by filling up an array. Medium severity."

Analysis:
- Issue: DOS through array filling
- Duration: 3 days
- Impact: Temporary service disruption
- Constraints: Attacker can repeat

VALIDATION RESULT: VALID (with considerations)
CORRECT SEVERITY: MEDIUM (potentially HIGH if repeatable)

REASONING:
DOS issues are evaluated on two criteria:
1. Funds locked >1 week
2. Impacts time-sensitive functions

Single occurrence of 3 days doesn't meet the >1 week threshold. However, per Sherlock guidelines: "if the single occurrence is relatively long (e.g. >2 days) and takes only 2-3 iterations to cause 7-day DOS, it may be considered valid."

KEY FACTORS:
- Single occurrence: 3 days (relatively long)
- If repeatable with 2-3 iterations → reaches 7-day threshold
- Check if any time-sensitive functions are affected
- If affects time-sensitive functions → can be Medium
- If both criteria met (7 days + time-sensitive) → can be High
```

## Tips for Accurate Validation

1. **Always load the reference criteria first** - Don't rely on memory
2. **Check for exceptions** - Many invalid categories have specific exceptions
3. **Quantify losses** - Ensure losses meet the >1%/>$10 or >0.01%/>$10 thresholds
4. **Consider repeatability** - A small repeatable loss can escalate to high severity
5. **Review hierarchy of truth** - README > code comments > defaults
6. **Don't assume likelihood** - Sherlock explicitly ignores likelihood in severity assessment
7. **Look for PoC requirements** - Complex issues may need PoC to be considered valid
8. **Check duplication criteria** - Understand if finding shares root cause with others

## When to Request More Information

If the user's finding lacks critical information, ask for:

- Specific attack path or vulnerability path
- Quantification of loss (percentage and dollar amount)
- External conditions or constraints required
- Whether the issue is repeatable
- What functions or features are affected
- Whether there's a README with protocol invariants
- Whether the deployment chain has a private mempool (for front-running issues)

## Resources

### references/
- **sherlock-judging-criteria.md** - Complete Sherlock judging standards (ALWAYS load this first)