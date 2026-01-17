---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53482
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Hexens
---

## Vulnerability Title

[LID-23] Rebase Limiter maxTotalPooledEther optimisation

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** PositiveTokenRebaseLimier.sol:increaseEther#L139-L160

**Description:**

The calculation for `maxTotalPooledEther` in `increaseEther` depends fully on two variables that are only set during initialisation and won't change any further. The calculation can therefore be moved to initialisation as a memory variable in `TokenRebaseLimiterData`. This is because the result will always be the same in every subsequent call to `increaseEther`.
```
function increaseEther(
    TokenRebaseLimiterData memory _limiterState, uint256 _etherAmount
)
    internal
    pure
    returns (uint256 consumedEther)
{
    if (_limiterState.positiveRebaseLimit == UNLIMITED_REBASE) return _etherAmount;

    uint256 prevPooledEther = _limiterState.currentTotalPooledEther;
    _limiterState.currentTotalPooledEther += _etherAmount;

    uint256 maxTotalPooledEther = _limiterState.preTotalPooledEther +
        (_limiterState.positiveRebaseLimit * _limiterState.preTotalPooledEther) / LIMITER_PRECISION_BASE;

    _limiterState.currentTotalPooledEther
        = Math256.min(_limiterState.currentTotalPooledEther, maxTotalPooledEther);

    assert(_limiterState.currentTotalPooledEther >= prevPooledEther);

    return _limiterState.currentTotalPooledEther - prevPooledEther;
}
```

**Remediation:**  We would recommend to perform the change as described in the description in favour of gas optimisation.

**Status:**  Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

