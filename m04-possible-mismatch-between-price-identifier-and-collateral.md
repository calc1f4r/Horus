---
# Core Classification
protocol: UMA Audit – Phase 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11429
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-audit-phase-2/
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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M04] Possible mismatch between price identifier and collateral

### Overview


A bug was reported in the `ExpiringMultiPartyCreator` contract of the UMA protocol. This contract allows the deployer to choose the price identifier and collateral token. If these are chosen to be inconsistent with each other, the price returned by the oracle may not match the expected token price, which could lead to unexpected behavior. To prevent this, the UMA team proposed maintaining an approved mapping between collateral tokens and price identifiers. However, the team clarified that there are use cases of the UMA contracts where the price identifier may not match the collateral token, allowing users to create exotic and complex risk exposures.

### Original Finding Content

The `ExpiringMultiPartyCreator` contract allows the deployer to [choose the price identifier and collateral token](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/ExpiringMultiPartyCreator.sol#L24-L25). If these are chosen to be inconsistent with each other, the price returned by the oracle will not match the expected token price, which could confuse users and lead to unexpected behavior. Consider maintaining an approved mapping between collateral tokens and price identifiers to enforce consistency between these values.


**Update**: *Not an issue. There are use cases of the UMA contracts where the price identifier may not match the collateral token. In the words of the UMA team:*



> 
>  While many products will have matching price quote currencies and collateral tokens, we want to allow creating exotic / complex risk exposures if users prefer.
> 
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UMA Audit – Phase 2 |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uma-audit-phase-2/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

