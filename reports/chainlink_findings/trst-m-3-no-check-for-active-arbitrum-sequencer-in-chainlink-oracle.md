---
# Core Classification
protocol: Stella
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19055
audit_firm: Trust Security
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
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
  - lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Trust Security
---

## Vulnerability Title

TRST-M-3 No check for active Arbitrum Sequencer in Chainlink Oracle

### Overview


This bug report is regarding an issue where the Chainlink oracle may return an invalid or stale price if the Arbitrum sequencer were to go offline. To prevent this from happening, the team recommended checking the sequencer uptime before consuming any price data. The team addressed this issue and the mitigation review was successful. The Chainlink docs provide more details on L2 Sequencer Uptime Feeds.

### Original Finding Content

**Description:**
If the Arbitrum sequencer were to go offline the Chainlink oracle may return an invalid/stale 
price. It should always be checked before consuming any data from Chainlink. 

The Chainlink docs(https://docs.chain.link/data-feeds/l2-sequencer-feeds) on L2 Sequencer Uptime Feeds specify more details.

**Recommended Mitigation:**
Check sequencer uptime before consuming any price data.

**Team response:**
Fixed.

**Mitigation Review:**
The team addressed this issue by checking sequencer uptime before consuming any price 
data.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Trust Security |
| Protocol | Stella |
| Report Date | N/A |
| Finders | Trust Security |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Trust Security/2023-05-29-Stella.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

