---
# Core Classification
protocol: Connext NXTP — Noncustodial Xchain Transfer Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13338
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/07/connext-nxtp-noncustodial-xchain-transfer-protocol/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - services
  - synthetics

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Martin Ortner
  -  Heiko Fisch

  -  David Oz Kashi
---

## Vulnerability Title

Sdk.finishTransfer - missing validation

### Overview

See description below for full details.

### Original Finding Content

#### Description


`Sdk.finishTransfer` should validate that the router that locks liquidity in the receiving chain, should be the same router the user had committed to in the sending chain.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Connext NXTP — Noncustodial Xchain Transfer Protocol |
| Report Date | N/A |
| Finders | Martin Ortner,  Heiko Fisch
,  David Oz Kashi |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/07/connext-nxtp-noncustodial-xchain-transfer-protocol/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

