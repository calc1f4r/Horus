---
# Core Classification
protocol: Zkdx
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37506
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-18-zkDX.md
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
  - Zokyo
---

## Vulnerability Title

Lack of Event Emission After Sensitive Actions

### Overview

See description below for full details.

### Original Finding Content

**Severity** : Low

**Status** : Resolved

**Description** :

The system exhibits a lack of event emissions following the execution of sensitive actions across multiple contracts, decreasing transparency and making tracking transactions difficult. Specifically:


In the vault contract, the `withdrawFees` function allows the withdrawal of accumulated fees to any address but does not emit an event upon completion.
The `VaultPriceFeed` contract interacts with the Pyth Oracle for managing price feeds of various tokens. It includes critical functions like `setValidTime`, `setFeedIds`, `setPyth`, and `setStableToken` that alter the state of the contract without emitting events after execution. 

**Recommendation** : 

It is recommended to define and emit events for all critical state-changing operations within the contracts, including successful fee withdrawals and any changes made through the `VaultPriceFeed` contract's functions. Details such as the token address, amount withdrawn, receiver's address, and the specific state changes made should be included in these events to enhance transparency and facilitate tracking.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Zkdx |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-18-zkDX.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

