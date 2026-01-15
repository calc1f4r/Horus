---
# Core Classification
protocol: EVM Smart Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52019
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/apro/evm-smart-contracts
source_link: https://www.halborn.com/audits/apro/evm-smart-contracts
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Halborn
---

## Vulnerability Title

Lack of L2 Sequencer Status Monitoring in Deployment

### Overview

See description below for full details.

### Original Finding Content

##### Description

The audited system, a fork of Chainlink, is designed for deployment across multiple EVM-compatible chains, including Layer 2 (L2) solutions and sidechains. These chains include Scroll, Linea, ZKLink Nova, BSC, and others that are not L2s or L2s. A critical omission has been identified in the implementation: the absence of L2 sequencer feeds contracts on these chains for Apro Contract.

L2 solutions and some sidechains utilize sequencers to batch and process transactions. The operational status of these sequencers is crucial for the integrity and fairness of the oracle service. Without sequencer status monitoring, the system lacks the capability to detect and respond to sequencer downtime or unavailability.

Chainlink's standard implementation includes sequencer feeds to provide real-time status updates of L2 sequencers. These feeds allow oracle consumers to determine whether the L2 network is fully operational and accessible to all users.

The oracle may continue to report prices without accounting for the inaccessibility of the L2 network to most users, potentially leading to mispriced assets or unfair liquidations.

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:M/D:N/Y:N/R:P/S:U (2.5)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:M/D:N/Y:N/R:P/S:U)

##### Recommendation

To address this issue, one of the following measures is recommended:

1. Implement L2 Sequencer Feeds: Deploy sequencer status feed contracts on all supported L2 and sidechain networks, following Chainlink's established patterns.
2. Integrate Sequencer Status Checks: Modify the oracle contracts to incorporate checks against the sequencer status feeds before providing price data.

  

Remediation Plan
----------------

**PENDING:** The **APRO team** will solve the issue by deploying a L2 Sequencer Feed on Scroll Rollup

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | EVM Smart Contracts |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/apro/evm-smart-contracts
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/apro/evm-smart-contracts

### Keywords for Search

`vulnerability`

