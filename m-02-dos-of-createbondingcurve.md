---
# Core Classification
protocol: PumpScience_2024-12-24
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45300
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/PumpScience-security-review_2024-12-24.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.00
financial_impact: medium

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - derivatives

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] DOS of CreateBondingCurve

### Overview


The report states that there is a bug in the `CreateBondingCurve` instruction that requires passing a `bonding_curve_token_account`. This account uses `associated_token::mint` and `associated_token::authority`, which means it can be created in advance. However, if it already exists, the function will fail. This can be exploited by an attacker who can create a `TokenAccount` and prevent users from creating a Bonding Curve. The recommendation is to change the `init` to `init_if_needed` to prevent this issue.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `CreateBondingCurve` instruction requires passing `bonding_curve_token_account`:

```rust
    #[account(
        init,
        payer = creator,
        associated_token::mint = mint,
        associated_token::authority = bonding_curve,
    )]
    bonding_curve_token_account: Box<Account<'info, TokenAccount>>,
```

`bonding_curve_token_account` uses `associated_token::mint` and `associated_token::authority`, so the `TokenAccount` can be created in advance.
If this already exists, creating the function will fail because init is used.

An attacker can extract the calculated `bonding_curve` address and create a `TokenAccount` to prevent users from creating a Bonding Curve.

## Recommendations

````diff
    #[account(
-        init,
+        init_if_needed,
        payer = creator,
        associated_token::mint = mint,
        associated_token::authority = bonding_curve,
    )]
    bonding_curve_token_account: Box<Account<'info, TokenAccount>>,```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | PumpScience_2024-12-24 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/PumpScience-security-review_2024-12-24.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

