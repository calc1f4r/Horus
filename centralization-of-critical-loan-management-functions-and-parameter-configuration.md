---
# Core Classification
protocol: Isle Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45745
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle Finance.md
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

Centralization of Critical Loan Management Functions and Parameter Configurations

### Overview


This bug report discusses a potential issue with a loan management system that is controlled by a single admin. This centralized control could pose risks for the protocol. The report recommends implementing a multisig wallet, transitioning to a decentralized governance model, and introducing a time-lock mechanism to mitigate these risks.

### Original Finding Content

**Severity**: Low

**Status**: Acknowledged

**Description**: 

Loan management functions, such as approving loans, marking loans as impaired, reversing impairment decisions, and declaring borrower defaults, are centralized and controlled by an admin. Parameter settings like adminFee, maxCoverLiquidation, minCover, poolLimit, windowDuration, and cycleDuration are also managed by the admin. Although a multisig wallet is intended for these functions to reduce individual risks, significant centralization remains inherent in the protocol.

**Recommendation**: 

To mitigate the risks associated with centralization, consider the following recommendations:

Multisig Wallet Adoption: Implement the intended multisig wallet to add multiple layers of approval for critical functions. Ensure that the multisig contract is robust and secure.
Decentralized Governance: Gradually migrate to a decentralized governance model where the community can partake in significant decisions. Utilize governance tokens and voting mechanisms to distribute the decision-making process.
Time-lock Mechanism: Introduce a time-lock mechanism for critical administrative functions, allowing the community to review and react to changes before they are finalized.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Isle Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

