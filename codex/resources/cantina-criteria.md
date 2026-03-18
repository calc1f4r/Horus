<!-- AUTO-GENERATED from `.claude/resources/cantina-criteria.md`; source_sha256=7935b602150c387cbb200775780a2431c65c55e92ad9e8065570c4b70d75a514 -->

> Codex/GPT compatibility layer.
> Source of truth: `.claude/resources/cantina-criteria.md`.
> This mirrored resource preserves the original content with `.claude/...` links rewritten to `codex/...` where needed.

# Cantina Judging Criteria

## Severity Matrix

Severity = Impact × Likelihood

| Likelihood \ Impact | High | Medium | Low |
|-------------------|------|--------|-----|
| **High** | HIGH | HIGH | MEDIUM |
| **Medium** | HIGH | MEDIUM | LOW |
| **Low** | MEDIUM | LOW | INFORMATIONAL |

**Note:** Matrix is a guideline requiring context, not absolute rule.

## Impact Levels

- **HIGH**: Loss of user funds OR breaks core functionality
- **MEDIUM**: Temporary DoS OR minor fund loss OR breaks non-core functionality
- **LOW**: No assets at risk (state handling issues, logic errors)

## Likelihood Levels

- **HIGH**: Any user can trigger without constraints OR outsized returns
- **MEDIUM**: Significant constraints (capital requirement, planning, other users' actions)
- **LOW**: Unusual scenarios, admin actions, many constraints, self-harm, external upgradability (if in scope)

## Severity Caps

### Capped at LOW
- Minimal loss (rounding errors/fee discrepancies, even if infinite repeatability)
- Weird ERC20 token issues
- View function errors not used in protocol

### Capped at INFORMATIONAL
- Admin errors (wrong parameters) - Note: Wrong implementation uses normal matrix
- Malicious admin (unless in scope)
- User errors without impact on others
- Design philosophy issues
- Missing basic validation
- Second-order effects (from fixes)

### INVALID
- Speculation on future code/integrations (unless relates to current code)
- Known issues in LightChaser
- Public fixes (duplicates after fix released)

## PoC Requirements

**PoC NOT required when:**
- Researcher has reputation ≥ 80
- Cantina Dedicated researcher
- Missing function issues
- LOW/INFORMATIONAL severity

**Valid PoC must:**
- Compile
- Demonstrate the impact

## Key Rules

- **Protocol README = source of truth** (not other docs)
- **Context required**: Issues must provide clarity for judge evaluation
- **Submission quality matters**: Fill template properly or risk invalidation

## Duplication Criteria (All Required)

1. Clear root cause identification
2. Medium+ severity impact
3. Valid attack path (PoC or detailed walkthrough)
4. Fixing root cause resolves vulnerability

**Downgrade/invalidation if:**
- Root cause unclear
- Insufficient impact analysis
- Invalid attack path or PoC doesn't work
- Withdrawn findings