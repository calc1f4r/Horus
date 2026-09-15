---
# Core Classification
protocol: Cvi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37063
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-30-CVI.md
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

Missing Checks For Whether Arbitrum Sequencer Is Active

### Overview


A medium severity bug has been resolved in the protocol. The bug occurred when the protocol was deployed to L2, causing potential issues with price oracles. ChainLink recommends that users check if the L2 sequencer is active, as if it goes down, oracles may have incorrect prices. To avoid this, it is recommended to use the sequencer oracle within the protocol. Failure to do so may result in stale prices for USDC and affect the liquidation process.

### Original Finding Content

**Severity**: Medium

**Status**: Resolved

**Description**

The protocol intends to deploy to L2. ChainLink recommends that users using price oracles, check whether the Arbitrum sequencer is active
https://docs.chain.link/data-feeds#l2-sequencer-uptime-feeds
If the sequencer goes down, oracles may have stale prices, since L2-submitted transactions (i.e. by the aggregating oracles) will not be processed.

**Recommendation**: 

Use sequencer oracle inside the protocol, or else it might give stale prices for USDC and affect the liquidation process where we demand a certain peg from the returned amount.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Cvi |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-30-CVI.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

