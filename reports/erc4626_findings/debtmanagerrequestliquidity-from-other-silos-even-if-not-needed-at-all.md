---
# Core Classification
protocol: Sturdy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54509
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/7dae5fff-ba32-4207-9843-c607f15464a3
source_link: https://cdn.cantina.xyz/reports/cantina_sturdy_sep2023.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - lending
  - bridge
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - Manuel
  - HickupHH3
---

## Vulnerability Title

DebtManager.requestLiquidity from other silos even if not needed at all 

### Overview


This bug report is about a function in the DebtManager.sol code called `requestLiquidity`. This function allows users to request money from other lending protocols to complete a borrowing operation. The problem is that the code currently requests too much money from these protocols, resulting in a loss of interest. To fix this, the code should only request money from the protocols if it is needed, and the code should be rearranged to make sure this happens correctly. This issue has already been addressed in a recent update to the code.

### Original Finding Content

## Context: DebtManager.sol#L218

## Description
The `requestLiquidity` function allows users to request liquidity from other silos to fulfill a borrowAsset operation. A silo could be any other lending protocol that implements the ERC4626 standard.

The aggregator, a `YearnVaultV3`, is responsible for managing these silos. It maintains a balance of uninvested funds, termed `totalIdle`, which does not earn interest.

```solidity
if (requiredAmount > totalIdle) {
    unchecked {
        requiredAmount -= totalIdle;
    }
}
```

First, the `totalIdle` should be used to fulfill the liquidity request. If more liquidity is needed, it should be requested from the silos. After the `if` statement, the loop iterates over the silos to fulfill the remaining `requiredAmount`.

However, in the case that `requiredAmount <= totalIdle`, the `requiredAmount` could be fulfilled directly from the `totalIdle`. No additional silo requests are needed. 

Otherwise, too many funds are withdrawn from the silos and will remain in `totalIdle`, resulting in a loss of interest. This case is currently not considered. The full `requiredAmount` will be requested from silos in case `requiredAmount <= totalIdle`.

## Recommendation
Only request liquidity from silos if `requiredAmount > totalIdle`. The loop iteration over the silos should happen inside the `if` statement:

```solidity
if (requiredAmount > totalIdle) {
    unchecked {
        requiredAmount -= totalIdle;
    }
    for (uint256 i; i < lenderCount; ++i) {
        // ...
    }
}
```

## Sturdy
Addressed in ChainSecurity commit `e1c04047`.

## Cantina
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Sturdy |
| Report Date | N/A |
| Finders | Manuel, HickupHH3 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_sturdy_sep2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/7dae5fff-ba32-4207-9843-c607f15464a3

### Keywords for Search

`vulnerability`

