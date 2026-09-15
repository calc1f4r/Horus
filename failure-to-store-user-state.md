---
# Core Classification
protocol: Kamino Lend Integration
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46939
audit_firm: OtterSec
contest_link: https://www.exponent.finance/
source_link: https://www.exponent.finance/
github_link: https://github.com/exponent-finance/exponent-core

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
finders_count: 3
finders:
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Failure to Store User State

### Overview


The report highlights a bug in the kamino_lend_standard instruction, specifically in the init_sy function. This bug allows for potential exploitation by transferring ownership of an obligation_farm to the Kamino lending authority, which can then be used to interact with the farm using a different user_state. This is due to the fact that the obligation_farm is not stored in the SyMeta structure. This poses a security risk as it allows for incorrect verification of the user's state when interacting with deposit and withdraw instructions, potentially leading to unauthorized access to rewards and assets. The recommended solution is to store the obligation_farm in SyMeta to ensure that every interaction with the system verifies the correct farm state and prevents unauthorized access. This bug has been resolved in PR#610.

### Original Finding Content

## Kamino Lending Security Issue

In the `init_sy` instruction in `kamino_lend_standard`, the `obligation_farm`, which represents the user’s state in Kamino Farms for earning rewards, is utilized to verify the `user_state` in deposit and withdraw instructions. However, it is not stored in the `SyMeta` structure. 

As a result, this oversight allows for a potential exploit where an attacker may transfer ownership of an `obligation_farm` to the Kamino lending (`klend`) authority, thus enabling the attacker to utilize a different `user_state` to interact with the farm. Without storing the `obligation_farm` in `SyMeta`, there is no direct reference to verify that the correct user state is used while interacting with the deposit and withdraw instructions. These instructions rely on correctly verifying the user’s state to ensure that the correct user is interacting with the system and that they may claim or modify rewards or assets tied to their state.

## Remediation

Store the `obligation_farm` in `SyMeta` to ensure that every interaction with the system verifies the correct farm state, such that only the legitimate owner may modify or interact with the farm state.

## Patch

Resolved in PR#610.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Kamino Lend Integration |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://www.exponent.finance/
- **GitHub**: https://github.com/exponent-finance/exponent-core
- **Contest**: https://www.exponent.finance/

### Keywords for Search

`vulnerability`

