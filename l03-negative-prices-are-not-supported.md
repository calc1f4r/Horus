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
solodit_id: 11432
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-audit-phase-2/
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

[L03] Negative prices are not supported

### Overview

See description below for full details.

### Original Finding Content

The UMA oracle [reports prices as `int` value](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/oracle/interfaces/OracleInterface.sol#L33), which may be negative. However, the `PricelessPositionManager` contract does not support negative prices and simply [replaces negative values with zero](https://github.com/UMAprotocol/protocol/blob/e6eaa48124ae3f209fb117cf05eb18292cf26d21/core/contracts/financial-templates/implementation/PricelessPositionManager.sol#L605-L608). This mismatch may lead to errors or unexpected behavior.


Consider modifying either the oracle or the financial contract so that they are compatible.


**Update:** *This is the expected behavior. In the words of the UMA team:*



> 
>  We’ve decided not to support negative prices in this version of ExpiringMultiParty because the incentives break down when a token becomes a liability rather than an asset. However, we want to leave the DVM a bit more general to allow negative prices for other use cases outside of positively-valued synthetic token contracts. We set a negative price to 0 in this contract to prevent the contract from locking up any funds in the case that an error in parameterization or at the DVM level causes a negative price to be returned. We expect that any price identifier used by the ExpiringMultiParty will always return nonnegative price values from the DVM.
> 
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
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

