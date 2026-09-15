---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25288
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-illuminate
source_link: https://code4rena.com/reports/2022-06-illuminate
github_link: https://github.com/code-423n4/2022-06-illuminate-findings/issues/139

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
  - dexes
  - cdp
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-04] Checking yieldBearingToken against u instead of backingToken

### Overview


A bug in the lend function for tempus was reported by datapunk. The bug is that the function checks `if (ITempus(principal).yieldBearingToken() != IERC20Metadata(u))`, while it should check `ITEMPUS(principal).backingToken()` instead. Sourabhmarathe (Illuminate) confirmed the bug, but disagreed with its severity. Kenzo (warden) commented that it should be classified as a medium severity bug, as user funds are not at risk. Gzeoneth (judge) decreased the severity to Medium. The recommended solution to the bug is to check `ITEMPUS(principal).backingToken()` instead.

### Original Finding Content

_Submitted by datapunk_

The lend function for tempus will fail with the right market.

### Proof of Concept

Checks `if (ITempus(principal).yieldBearingToken() != IERC20Metadata(u))`, while it should check `ITempus(principal).backingToken()`

### Recommendation

Do this instead:

        if (ITempus(principal).backingToken() != IERC20Metadata(u))

**[sourabhmarathe (Illuminate) confirmed, but disagreed with severity](https://github.com/code-423n4/2022-06-illuminate-findings/issues/139)**

**[kenzo (warden) commented](https://github.com/code-423n4/2022-06-illuminate-findings/issues/139#issuecomment-1168837586):**
 > I think should probably be medium severity as user funds not at risk.

**[gzeoneth (judge) decreased severity to Medium](https://github.com/code-423n4/2022-06-illuminate-findings/issues/139)**

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-illuminate
- **GitHub**: https://github.com/code-423n4/2022-06-illuminate-findings/issues/139
- **Contest**: https://code4rena.com/reports/2022-06-illuminate

### Keywords for Search

`vulnerability`

