---
# Core Classification
protocol: Interplanetary Consensus (Ipc)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37365
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary Consensus (IPC).md
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

`commitCheckpoint` Returns Execution Without Rewarding The Relayer

### Overview


This bug report is about a function called `commitCheckpoint()` in the code file GatewayRouterFacet.sol. The function is supposed to reward the relayer if a certain condition is met, but due to a mistake in the code, the relayer is not being rewarded. The severity of this bug is considered medium and it has already been resolved. The recommendation is to fix the code so that the relayer can be rewarded properly.

### Original Finding Content

**Severity** - Medium

**Status** - Resolved

**Description**

Function `commitCheckpoint()` (L41 GatewayRouterFacet.sol) commits a verified checkpoint and rewards the relayer if `checkpointRelayerRewards` is set to true . But a value of 0 is sent to the function `distributeRewardsToRelayer` at L64  , this would just return execution and not reward the relayer.

**Recommendation**: 

Reward the relayer appropriately

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Interplanetary Consensus (Ipc) |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-27-InterPlanetary Consensus (IPC).md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

