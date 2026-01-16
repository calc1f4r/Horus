---
# Core Classification
protocol: Shido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37655
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Shido.md
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

DoS in CometBFT Block Sync (github.com/cometbft/cometbft/blocksync)

### Overview


This bug report is about a potential issue in the Shido blockchain that could be caused by a malicious peer. The problem is that this peer could send a block with a very high LastCommit round, which could lead to excessive memory usage and crashes. This could disrupt the normal functioning of the blockchain and prevent it from connecting to the network. The likelihood of this happening is low to moderate, as it would require a malicious peer with knowledge of the block sync mechanism. To fix this issue, it is recommended to upgrade to the latest version of github.com/cometbft/cometbft. 

### Original Finding Content

**Severity:** Medium

**Status:** Acknowledged

**Description:** 

A malicious peer can cause a DoS by sending a block with a very high LastCommit round, leading to excessive memory usage and potential crashes.

**Impact:** 

This vulnerability can disrupt the normal operation of the Shido blockchain by preventing it from syncing with the network.

**Likelihood:** 

Low to moderate, as it requires a malicious peer with knowledge of the block sync mechanism.

**Recommendation:** Upgrade github.com/cometbft/cometbft to the latest version to mitigate this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Shido |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-06-30-Shido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

