---
# Core Classification
protocol: Umami
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44594
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-04-19-Umami.md
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

Unchecked Chainlink sequencer uptime

### Overview


This bug report discusses an issue with the ChainlinkWrapper contract that can cause errors on the L2 chain. The report recommends checking the uptime status of the Chainlink L2 sequences and acting accordingly. The bug has been resolved and the Chainlink wrapper has been removed. For more information, check the chainlink docs and code snippet provided.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

In contract ChainlinkWrapper there are no checks for the uptime status of the Chainlink L2 sequences. It's recommended that L2 oracles fetch the uptime for the Chainlink sequencer to ensure the data returned can be trusted. This can lead to errors on the L2 chain as the price data is not updated correctly. For a more detailed explanation, check the chainlink docs and code snippet: https://docs.chain.link/data-feeds/l2-sequencer-feeds.

**Recommendation**: 

check if the sequencer is active and act on the response accordingly

**Note**: Chainlink wrapper was removed, unused
https://github.com/UmamiDAO/V2-Vaults/commit/4419ae6e85f59ef5c3d711ec0c8f7b942620fe90

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Umami |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-04-19-Umami.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

