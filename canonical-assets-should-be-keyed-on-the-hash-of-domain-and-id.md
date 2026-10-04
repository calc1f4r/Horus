---
# Core Classification
protocol: Connext
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7238
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - validation

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0xLeastwood
  - Jonah1005
---

## Vulnerability Title

Canonical assets should be keyed on the hash of domain and id

### Overview


This bug report addresses an issue with the TokenRegistry component of the LibConnextStorage, AssetLogic, AssetFacet, and TokenRegistry systems. The owner of TokenRegistry has the power to register new tokens in the system, and they are registered using the hash of their domain and id. However, it is an issue if TokenRegistry registers two canonical assets with the same id, as this could lead to unintended transfers or reverts.

The recommendation is to consider using the keccak256 hash of the canonical asset’s domain and id for mapping keys. This has been solved in PR 1588, and verified by Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
- `LibConnextStorage.sol`#L184
- `AssetLogic.sol`#L36
- `AssetFacet.sol`#L143
- `TokenRegistry.sol`#L112-L113
- `TokenRegistry.sol`#L334

## Description
A canonical asset is a tuple of a (domain, id) pair. TokenRegistry’s owner has the power to register new tokens in the system (See `TokenRegistry.ensureLocalToken()` and `TokenRegistry.enrollCustom()`). A canonical asset is registered using the hash of its domain and id (See `TokenRegistry._setCanonicalToRepresentation()`). Connext uses only the id of a canonical asset to uniquely identify. Here are a few references:
- `swapStorages`
- `canonicalToAdopted`

It is an issue if TokenRegistry registers two canonical assets with the same id. If this id fetches the incorrect canonical asset, an unintended one might be transferred to the destination chain, or the transfers may revert.

## Recommendation
Consider using the keccak256 hash of the canonical asset’s domain and id for mapping keys.

## Connext
Solved in PR 1588.

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Connext |
| Report Date | N/A |
| Finders | 0xLeastwood, Jonah1005 |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Connext-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation`

