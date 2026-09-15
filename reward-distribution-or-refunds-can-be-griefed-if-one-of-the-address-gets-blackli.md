---
# Core Classification
protocol: Xyro
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45677
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-29-Xyro.md
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
  - Zokyo
---

## Vulnerability Title

Reward Distribution Or Refunds Can Be Griefed If One Of The Address Gets Blacklisted

### Overview


This bug report is about a medium severity issue that has been resolved. The issue is related to a game where a token called USDC is used. This token has a feature called blacklisting addresses, which means certain addresses can be blocked from using the token. The bug occurs when one of the winners of the game gets blacklisted before the rewards are distributed. This causes the entire game to fail and prevents a new game from starting. The recommendation to fix this issue is to use a pull method instead of a push method for distributing rewards and refunds to players.

### Original Finding Content

**Severity** - Medium

**Status** - Resolved

**Description**

Assuming the approved token is USDC which has a concept of blacklisting addresses , there can be a scenario where if let’s say 10 people participated and one of the 3 winners (Bullseye example) gets blacklisted before the finalization/distribution of rewards then the whole function reverts. This would lead to the game never getting finished since the game won’t be finalized or closed and a new game can not be started unless the previous game ends.

**Recommendation**:

Use a pull method to distribute rewards/refunds instead of pushing them to the players.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Xyro |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-29-Xyro.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

