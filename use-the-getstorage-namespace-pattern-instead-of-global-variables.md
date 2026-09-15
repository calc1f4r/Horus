---
# Core Classification
protocol: LI.FI
chain: everychain
category: uncategorized
vulnerability_type: diamond

# Attack Vector Details
attack_type: diamond
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7038
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/LIFI-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - diamond

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

Use the getStorage() /NAMESPACE pattern instead of global variables

### Overview


This bug report is about the overlapping of global variables in the contracts Swapper.sol, SwapperV2.sol and DexManagerFacet.sol. These contracts use a global variable called appStorage, which is placed on the first storage slot. This overlap can cause unpredictable results if any other contract uses a global variable that overlaps with appStorage, especially when it involves access control. To prevent this, the getStorage()/NAMESPACE pattern should be used for appStorage. The underlying functionality was refactored into a library using the getStorage() pattern with PR #43, and was verified.

### Original Finding Content

## Severity: High Risk

## Context
- `Swapper.sol#L17`
- `SwapperV2.sol#L17`
- `DexManagerFacet.sol#L21`

## Description
The facet `DexManagerFacet` and the inherited contracts `Swapper.sol` / `SwapperV2.sol` define a global variable `appStorage` on the first storage slot. These two overlap, which in this case is intentional. However, it is dangerous to use this construction in a Diamond contract as this uses `delegatecall`. If any other contract uses a global variable, it will overlap with `appStorage` with unpredictable results. This is especially important because it involves access control.

For example, if the contract `IAxelarExecutable.sol` were to be inherited in a facet, then its global variable `gateway` would overlap. Luckily, this is currently not the case.

```solidity
contract DexManagerFacet {
    ...
    LibStorage internal appStorage;
    ...
}

contract Swapper is ILiFi {
    ...
    LibStorage internal appStorage; // overlaps with DexManagerFacet which is intentional
    ...
}
```

## Recommendation
Use the `getStorage()` / `NAMESPACE` pattern for `appStorage`, as is done in other parts of the code.

LiFi: We will refactor the underlying functionality into a Library that uses the `getStorage()` pattern. Refactored with PR #43.

Spearbit: Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

`Diamond`

