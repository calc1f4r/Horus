---
# Core Classification
protocol: Morpho Bundler v3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44974
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review-December-2024.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Rvierdiiev
  - Om Parikh
  - Eric Wang
  - MiloTruck
---

## Vulnerability Title

GeneralAdapter1.morphoRepay() incorrectly fetches the borrowShares of initiator instead of onBe-

### Overview


The bug report is about a medium risk bug found in a code called GeneralAdapter1. The bug occurs when a specific function, morphoRepay(), is called with a certain value for shares. This causes an incorrect amount of shares to be repaid when the function is called with different addresses for onBehalf and initiator. The recommendation is to modify the code to fix this issue, which has already been done in a recent update.

### Original Finding Content

## Half

**Severity:** Medium Risk  
**Context:** GeneralAdapter1.sol#L309-L312, GeneralAdapter1.sol#L316  

**Description:**  
When `GeneralAdapter1.morphoRepay()` is called with `shares == type(uint256).max`, `MorphoLib.borrowShares()` is called to set shares to the amount of borrowShares held by the initiator:

```solidity
if (shares == type(uint256).max) {
    shares = MorphoLib.borrowShares(MORPHO, marketParams.id(), initiator());
    require(shares != 0, ErrorsLib.ZeroAmount());
}
```

However, later on in the function, `MORPHO.repay()` is called to repay assets for `onBehalf` and not `initiator`:

```solidity
(uint256 repaidAssets, uint256 repaidShares) = MORPHO.repay(marketParams, assets, shares, onBehalf, data);
```

As such, passing the initiator address to `MorphoLib.borrowShares()` as shown above is incorrect, since the borrowShares of `onBehalf` should be fetched instead. This causes an incorrect amount of shares to be repaid whenever `GeneralAdapter1.morphoRepay()` is called while `onBehalf` and `initiator` happen to be different addresses.  

**Recommendation:**  
Modify the third parameter passed to `MorphoLib.borrowShares` to be `onBehalf`:

```diff
- shares = MorphoLib.borrowShares(MORPHO, marketParams.id(), initiator());
+ shares = MorphoLib.borrowShares(MORPHO, marketParams.id(), onBehalf);
```

**Morpho:** Fixed in commit `6e6ef769`.  
**Spearbit:** Verified, the recommended fix was implemented.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho Bundler v3 |
| Report Date | N/A |
| Finders | Rvierdiiev, Om Parikh, Eric Wang, MiloTruck |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

