---
# Core Classification
protocol: Mode Earnm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29277
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
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
finders_count: 2
finders:
  - Dacian
  - 0kage
---

## Vulnerability Title

Centralisation risks as the reward code generator and the Chainlink node operator is the same entity

### Overview

See description below for full details.

### Original Finding Content

**Description:** The current system architecture for managing reward codes in MODE is centralized, with both code generation and Chainlink node operations controlled by the MODE team. The endpoint tracking and managing these codes is not public. Using Chainlink Any API under this setup adds limited value, as it's managed by a single node operator – the MODE team itself. This centralization undermines the potential benefits of a decentralized oracle network.

**Impact:** This setup leads to unnecessary complications and expenses, including LINK fees, without offering the decentralization benefits typically associated with Chainlink's infrastructure.

**Recommended Mitigation:** Two potential alternatives could be considered to address this issue:

1. **Engage an External Node Operator:** Delegate the reward code verification tasks to an external node operator. This approach would involve creating a function to call `Chainlink:setChainlinkOracle`, allowing future updates to the oracle. Making the endpoint public in the future would empower MODE to appoint new operators as needed.

2. **Simplify with In-House Tracking:** If the node operator remains the same as the code generation entity, consider simplifying the process. Maintain an on-chain mapping linking codes and addresses to their respective box amounts. Update this mapping each time `apiAddress` triggers `MysteryBox::associateOneTimeCodeToAddress` with the permissible box amount. This streamlined approach would bypass the need for Chainlink oracles and external adapters, reducing LINK fees and complexity while maintaining the current level of centralisation.

We acknowledge that the chosen design was driven by the intent to facilitate the minting of mystery boxes in a single transaction, given the gas limitations associated with VRF (Verifiable Random Function) operations. MODE team's approach was reasonable under these constraints.

**Mode:**
Acknowledged.

\clearpage

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Mode Earnm |
| Report Date | N/A |
| Finders | Dacian, 0kage |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

