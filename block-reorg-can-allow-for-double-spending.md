---
# Core Classification
protocol: Aurorafastbridge
chain: everychain
category: uncategorized
vulnerability_type: chain_reorganization_attack

# Attack Vector Details
attack_type: chain_reorganization_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21063
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.20
financial_impact: high

# Scoring
quality_score: 1
rarity_score: 4

# Context Tags
tags:
  - chain_reorganization_attack

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - AuditOne
---

## Vulnerability Title

Block Reorg Can Allow For Double Spending

### Overview


Block reorg is a situation where a competing chain replaces the main blockchain. This can occur when multiple miners find valid blocks at the same time, and the network has to decide which block to include in the blockchain. In order to reduce the risk of block reorgs, the Fast Bridge project may need to take additional precautions, such as waiting for multiple confirmations before processing token transfers or implementing a fallback mechanism in case of a block reorg.

### Original Finding Content

**Description**: 

Block reorg, also known as blockchain reorganization, is a situation where a competing chain replaces the main blockchain. This can happen when multiple miners find valid blocks at the same time, and the network has to decide which block to include in the blockchain. In some cases, the network may choose to include a block that is not in the main blockchain, resulting in a reorganization of the chain.

**Recommendations:**

To mitigate the risk of block reorgs, the Fast Bridge project may need to implement additional measures, such as waiting for multiple confirmations before proceeding with token transfers or implementing a fallback mechanism in case of a block reorg.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 1/5 |
| Rarity Score | 4/5 |
| Audit Firm | AuditOne |
| Protocol | Aurorafastbridge |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`Chain Reorganization Attack`

