---
# Core Classification
protocol: Dynamo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55646
audit_firm: 0x52
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2023-10-07-Dynamo.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - @IAm0x52
---

## Vulnerability Title

[H-03] Malicious user can disable compound integration via share manipulation

### Overview


The bug report discusses a potential issue with the Compound V2 share ratio, where it can be lowered instead of always increasing. This can be manipulated to block the Compound V2 adapter in the FundsAllocator contract, allowing users to sabotage others and cause loss of yield. The report recommends a change to only block the adapter if there is a reasonable loss, and a fix has been implemented to allow for a larger nominal loss before disabling it.

### Original Finding Content

**Details**

It's a common assumption that Compound V2 share ratio can only ever increase but with careful manipulation it can actually be lowered. The full explanation is a bit long but you can find it [here](https://github.com/code-423n4/2023-01-reserve-findings/issues/310) in one of my public reports.

[FundsAllocator.vy#L67-L71](https://github.com/DynamoFinance/vault/blob/c331ffefadec7406829fc9f2e7f4ee7631bef6b3/contracts/FundsAllocator.vy#L67-L71)

          if pool.current < pool.last_value:
              # We've lost value in this adapter! Don't give it more money!
              blocked_adapters[blocked_pos] = pool.adapter
              blocked_pos += 1
              pool.delta = 0 # This will result in no tx being generated.

This quirk of Compound V2 can be used to trigger the check in FundsAllocator to block the Compound V2 adapter. This is useful if the user wants to push their own proposal allowing them to sabotage other users and cause loss of yield to the vault.

**Lines of Code**

[FundsAllocator.vy#L67-L71](https://github.com/DynamoFinance/vault/blob/c331ffefadec7406829fc9f2e7f4ee7631bef6b3/contracts/FundsAllocator.vy#L67-L71)

**Recommendation**

Instead of using an absolute check, instead only block the adapter if there is reasonable loss.

**Remediation**

Fixed [here](https://github.com/DynamoFinance/vault/commit/e3092bf4908e5f1d049e18fc52d310c9d8ce29ae) by allowing larger nominal (but still very small) loss before disabling it

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | 0x52 |
| Protocol | Dynamo |
| Report Date | N/A |
| Finders | @IAm0x52 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/0x52/2023-10-07-Dynamo.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

