---
# Core Classification
protocol: Optimism
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40805
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c185d7eb-d80b-49d4-8141-44e122c6fee4
source_link: https://cdn.cantina.xyz/reports/cantina_optimism_feb2024.pdf
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
  - cdp
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - cccz
  - Jeiwan
  - Christos Pap
---

## Vulnerability Title

address(0) checks are missing from the ERC721Bridge contract 

### Overview

See description below for full details.

### Original Finding Content

## ERC721Bridge Analysis

## Context

Location: `ERC721Bridge.sol#L73-L82`

## Description

The `__ERC721Bridge_init` function is called during the initialization of both the `L1ERC721Bridge` and `L2ERC721Bridge`. However, the `address(0)` checks that were present in the previous version are now missing from the `ERC721Bridge` contract.

```solidity
/// @notice Initializer.
/// @param _messenger Contract of the CrossDomainMessenger on this network.
/// @param _otherBridge Contract of the ERC721 bridge on the other network.
// solhint-disable-next-line func-name-mixedcase
function __ERC721Bridge_init(
    CrossDomainMessenger _messenger,
    StandardBridge _otherBridge
) internal onlyInitializing {
    messenger = _messenger;
    otherBridge = _otherBridge;
}
```

## Recommendation

Since the `address(0)` is used to initialize the `_messenger` or `_otherBridge`, `address(0xdEaD)` can be used on both the `L1ERC721Bridge` and `L2ERC721Bridge` contracts while also including the zero-address checks. Additionally, instead of initializing with zero or dead values, you can consider using the `_disableInitializers` method in the constructor.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Optimism |
| Report Date | N/A |
| Finders | cccz, Jeiwan, Christos Pap |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_optimism_feb2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c185d7eb-d80b-49d4-8141-44e122c6fee4

### Keywords for Search

`vulnerability`

