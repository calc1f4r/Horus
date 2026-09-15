---
# Core Classification
protocol: DeFi Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33557
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DeFi%20Money/Core/README.md#2-hooks-may-break-some-invariants
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Hooks may break some invariants

### Overview


The bug report is about a potential issue in the MainController code, specifically in lines 718, 768, 823, and 861. The report states that if the hooks in the MainController can return any adjustments, it may break the following rule: "redeemed + total_debt should always be greater than or equal to minted". This means that if a new loan is created and the hook adjusts the debt amount to a smaller value, it could result in the total debt being increased by a smaller amount than the minted value, which would violate the rule. The report recommends implementing safe boundaries for the hooks to prevent this issue.

### Original Finding Content

##### Description
- https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/MainController.vy#L718
- https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/MainController.vy#L768
- https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/MainController.vy#L823
- https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/MainController.vy#L861

If we suppose that hooks in the MainController can return arbitrary adjustments, the following invariants will break:
* `redeemed + total_debt >= minted`.

For example, in the initial state when `redeemed = total_debt = minted = 0`, if we create a new loan via `create_loan(debt_amount)` and the hook adjusts `debt_amount_final` to a smaller value, then `total_debt` will be increased by a smaller value than `minted` and the following will be true:
```
redeemed + total_debt < minted
```

##### Recommendation
We recommend checking safe boundaries for hooks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DeFi Money |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DeFi%20Money/Core/README.md#2-hooks-may-break-some-invariants
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

