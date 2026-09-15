---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37037
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
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

`getLatestData` Does Not Check If Arbitrum Sequencer Is Down In Chainlink Feeds

### Overview


This bug report discusses a vulnerability in the use of Chainlink in L2 chains like Arbitrum. This could potentially give an unfair advantage to malicious actors. It is recommended to follow the code example provided by Chainlink to avoid this issue. The bug has been resolved and is of medium severity.

### Original Finding Content

**Severity** - Medium

**Status** - Resolved

**Description**

When utilizing Chainlink in L2 chains like Arbitrum, it's important to ensure that the prices provided are not falsely perceived as fresh, even when the sequencer is down. This vulnerability could potentially be exploited by malicious actors to gain an unfair advantage.

**Recommendation**:

It is recommended to follow the code example of Chainlink: https://docs.chain.link/data-feeds/l2-sequencer-feeds#example-code

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

