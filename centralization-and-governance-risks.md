---
# Core Classification
protocol: Potluck
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47526
audit_firm: OtterSec
contest_link: https://potluckprotocol.com/
source_link: https://potluckprotocol.com/
github_link: https://github.com/PotLock/core

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
  - James Wang
  - Robert Chen
---

## Vulnerability Title

Centralization And Governance Risks

### Overview

See description below for full details.

### Original Finding Content

## Potential Risks and Issues

Several potential risks and issues were identified related to centralization and mismanagement:

1. **Payout Calculations**: Payout calculations occur offline, and admins maintain full discretion over the process. Compromised admin accounts could misuse this authority to steal matching donations.
   
2. **Lack of Sanity Checks**: There is no sanity check on `pot` or `pot_factory` parameters, allowing for mismanagement of round start/end times, fee percentages, and other critical parameters.
   
3. **Configuration Changes**: Configurations may be changed after the donations start, challenging users who verify the pot contracts state they are interacting with.

## Remediation

1. **On-Chain Logic Implementation**: Implement on-chain logic for payout calculations or add additional checks to ensure transparency and prevent unauthorized actions. Utilizing a multi-signature scheme or incorporating decentralized governance mechanisms may enhance security and reduce the risk of mismanagement.

2. **Validation Checks**: Add validation checks for pot parameters during initialization or configuration updates. This may help prevent unintended errors or manipulations that break pots. Set critical parameters within reasonable and secure bounds.

3. **Restrictions on Configuration Changes**: Add restrictions on configuration changes once the donation round has started. This helps maintain transparency and ensures that users can trust the state of the contract during their interactions.

## Patch

1. **Complexity of Pairwise Calculation**: Due to the complexity of pairwise calculation, it is impractical to do calculations on-chain. Instead, a payout result challenge/resolve feature is implemented to increase transparency into payout calculations in `24e1be1`, `35fe826`, `fe4a1c9`, `de2d116`, and `5bfcf12`.

2. **Resolved Issues**: Resolved in `9a867efa` and `2b8db30`.

3. **Logging Updates**: Resolved in `79d53dfb` by logging updates to allow frontend to display and inform users of parameter changes throughout the lifetime of the pot.

© 2024 Otter Audits LLC. All Rights Reserved. 10/18

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Potluck |
| Report Date | N/A |
| Finders | James Wang, Robert Chen |

### Source Links

- **Source**: https://potluckprotocol.com/
- **GitHub**: https://github.com/PotLock/core
- **Contest**: https://potluckprotocol.com/

### Keywords for Search

`vulnerability`

