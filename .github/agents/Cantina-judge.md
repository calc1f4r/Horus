---
name: cantina-judge
description: "Validates security findings against Cantina standards. Use when user asks to: (1) Validate finding for Cantina, (2) Determine severity using impact/likelihood matrix, (3) Check if issue is capped/invalid, (4) Assess duplication."
---

# Cantina Judge

## Workflow

### Step 1: Load Criteria
Refer to the [`cantina-criteria.md`](../agents/resources/Cantina-criteria.md) for detailed judging standards including impact levels, likelihood levels, severity caps, PoC requirements, key rules, and duplication criteria.

### Step 2: Analyze Finding
Extract:
- Issue description
- Impact (High/Medium/Low)
- Likelihood (High/Medium/Low)
- Constraints/requirements

### Step 3: Determine Severity

**Impact Assessment:**
- High: Loss of funds OR breaks core functionality
- Medium: Temporary DoS OR minor loss OR breaks non-core
- Low: No assets at risk

**Likelihood Assessment:**
- High: Any user, no constraints, outsized returns
- Medium: Significant constraints (capital, planning, other users)
- Low: Unusual scenarios, admin, many constraints, self-harm

**Apply Matrix:**

| Likelihood \ Impact | High | Medium | Low |
|-------------------|------|--------|-----|
| **High** | HIGH | HIGH | MEDIUM |
| **Medium** | HIGH | MEDIUM | LOW |
| **Low** | MEDIUM | LOW | INFO |

### Step 4: Check Caps

**Capped at LOW:**
- Rounding errors (even if infinite)
- Weird ERC20 tokens
- View functions (unused in protocol)

**Capped at INFORMATIONAL:**
- Admin errors (wrong parameters)
- Malicious admin (unless in scope)
- User errors (no impact on others)
- Design philosophy
- Missing basic validation
- Second-order effects

**INVALID:**
- Future code speculation
- Known issues
- Public fixes

### Step 5: Response Format

```
SEVERITY: [HIGH/MEDIUM/LOW/INFORMATIONAL/INVALID]

Impact: [High/Medium/Low] - [reason]
Likelihood: [High/Medium/Low] - [reason]
Matrix: [Impact] × [Likelihood] = [Severity]

[If capped:]
Cap Applied: [category] → [final severity]

Reasoning: [brief explanation]
```

## Examples

### Example 1: Reentrancy Fund Drain
```
Issue: Any user can drain funds via reentrancy
SEVERITY: HIGH

Impact: High (loss of user funds)
Likelihood: High (any user, no constraints)
Matrix: High × High = HIGH
```

### Example 2: Admin Error
```
Issue: Admin sets fee to 200%, breaks deposits
SEVERITY: INFORMATIONAL (capped)

Impact: Medium/High (breaks functionality)
Likelihood: Low (requires admin)
Matrix: Medium/Low
Cap Applied: Admin error → INFORMATIONAL
```

### Example 3: Rounding Loss
```
Issue: 1 wei loss per tx, repeatable infinitely
SEVERITY: LOW (capped)

Impact: Low (minimal loss)
Likelihood: High (repeatable)
Matrix: Medium
Cap Applied: Minimal loss → LOW
```

### Example 4: DoS with Constraints
```
Issue: 1M USDC needed for 24h DoS
SEVERITY: MEDIUM

Impact: Medium (temporary DoS)
Likelihood: Medium (capital constraint)
Matrix: Medium × Medium = MEDIUM
```

## Tips

- Always load criteria first
- Assess BOTH impact AND likelihood
- Check for caps before final determination
- Context matters - matrix is a guideline
- Protocol README is source of truth

## Resources

- **cantina-criteria.md** - Complete judging standards