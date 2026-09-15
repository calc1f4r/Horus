---
# Core Classification
protocol: Clave
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46285
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/a9206360-7dc7-4e1e-9d5b-b52ad4561016
source_link: https://cdn.cantina.xyz/reports/cantina_clave_december2024.pdf
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
finders_count: 2
finders:
  - MiloTruck
  - Víctor Martínez
---

## Vulnerability Title

Incentives May Become Locked in the System After Switching Incentive Tokens 

### Overview


The bug report is about a function called setIncentive in a file called ClaggBaseAdapter.sol. This function allows the owner to change the incentives for a specific pool in the protocol. There are two scenarios for updating the incentives: if the previous round has ended, the entire configuration can be updated, and if the previous round is still active, additional incentives can be added. However, the bug is that the protocol only uses the elapsed time to determine if a round has ended, instead of also checking if there are any unclaimed incentives left in the vault. This means that if the current time exceeds the round's expiry and there are still unclaimed incentives, they will become locked in the IncentivesVault when the owner changes the configuration to another token. The bug can be fixed by calling a function called compound at the beginning of the setIncentive function. The bug has been fixed in a commit with the code 05dfa5fa. The fix has been verified by Cantina Managed, which means that the issue has been resolved and the setIncentive function now checks if the poolIncentive is equal to 0 before updating the incentives, ensuring that all incentives from the previous round have been distributed.

### Original Finding Content

## ClaggBaseAdapter.sol 📄

## Context
Line: 216

## Description
The `setIncentive` function allows the owner to configure and update protocol incentives for a specific pool. It offers two scenarios:
- If the previous incentive round has ended, the entire configuration can be updated.
- If the previous round is still active, additional incentives can only be added.

However, the protocol currently uses only the elapsed time as a criterion to determine if a round has ended, instead of also verifying whether there are any remaining unclaimed incentives in the vault. If the current `block.timestamp` exceeds the round's expiry and some incentives remain unprocessed, these unclaimed tokens will become locked in the `IncentivesVault` when the owner changes the configuration into another token. This issue arises because the action does not compound before updating the incentive token.

## Recommendation
Consider calling `compound` at the top of the function.

## Clave
Fixed at commit `05dfa5fa`.

## Cantina Managed
Verified, `setIncentive()` now checks `poolIncentive == 0`, which ensures that incentives from the previous round have been fully distributed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Clave |
| Report Date | N/A |
| Finders | MiloTruck, Víctor Martínez |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_clave_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/a9206360-7dc7-4e1e-9d5b-b52ad4561016

### Keywords for Search

`vulnerability`

