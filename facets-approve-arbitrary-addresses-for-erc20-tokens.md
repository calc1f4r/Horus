---
# Core Classification
protocol: LI.FI
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7054
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
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
  - approve

protocol_categories:
  - dexes
  - bridge
  - services
  - cross_chain
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Jonah1005
  - DefSec
  - Gerard Persoon
---

## Vulnerability Title

Facets approve arbitrary addresses for ERC20 tokens

### Overview


This bug report is about the LiFi Diamond contract, which is used to approve an address for an ERC20 token. The user is able to provide two values, the parameter names of which change depending on the context. This allows the user to call functions in the facets and use the approved address to transfer tokens out of the contract, even though normally there shouldn't be any tokens in the LiFi Diamond contract. 

To address the bug, it is recommended that the bridge approval contract address should be stored in an immutable or a storage variable instead of taking it as a user input. This way, only pre-defined addresses can be approved and interacted with. The bug has been fixed with PR #79, PR #102 and PR #103 for LiFi, and has been verified for Spearbit.

### Original Finding Content

## Severity: Medium Risk

## Context
Across the following files and lines:
- `AcrossFacet.sol#L103`
- `AmarokFacet.sol#L145`
- `AnyswapFacet.sol#L127`
- `ArbitrumBridge-Facet.sol#L111`
- `CBridgeFacet.sol#L103`
- `GenericBridgeFacet.sol#L111`
- `GnosisBridgeFacet.sol#L119`
- `HopFacet.sol#L106`
- `HyphenFacet.sol#L101`
- `NXTPFacet.sol#L127`
- `OmniBridgeFacet.sol#L88`
- `OptimismBridge-Facet.sol#L100`
- `PolygonBridgeFacet.sol#L101`
- `StargateFacet.sol#L229`
- `WormholeFacet.sol#L94`

## Description
All the facets pointed above approve an address for an ERC20 token, where both these values are provided by the user:

```solidity
LibAsset.maxApproveERC20(IERC20(token), router, amount);
```

The parameter names change depending on the context. So for any ERC20 token that the `LifiDiamond` contract holds, the user can:
- Call any of the functions in these facets to approve another address for that token.
- Use the approved address to transfer tokens out of the `LifiDiamond` contract.

**Note:** Normally, there shouldn’t be any tokens in the `LiFi Diamond` contract, so the risk is limited. Also, see "Hardcode bridge addresses via immutable."

## Recommendation
For each bridge facet, the bridge approval contract address is already known. Store these addresses in an immutable or a storage variable instead of taking them as user input. Only approve and interact with these pre-defined addresses.

## LiFi
Fixed with PR #79, PR #102, PR #103

## Spearbit
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | LI.FI |
| Report Date | N/A |
| Finders | Jonah1005, DefSec, Gerard Persoon |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation, Approve`

