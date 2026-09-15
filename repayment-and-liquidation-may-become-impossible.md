---
# Core Classification
protocol: Archi Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60915
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
source_link: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
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
finders_count: 4
finders:
  - Mustafa Hasan
  - Zeeshan Meghji
  - Ibrahim Abouzied
  - Hytham Farah
---

## Vulnerability Title

Repayment and Liquidation May Become Impossible

### Overview


The bug report discusses an issue in the `credit/CreditCaller.sol` file where if a loan is not liquidated in time, price fluctuations can make it impossible to repay and liquidate the loan due to underflows. This means that the protocol could operate at a loss and the farmer could hold onto their loan indefinitely. The recommendation is to update the `_repayClaim()` and `liquidate()` functions to minimize losses instead of reverting the function in case of under-collateralization.

### Original Finding Content

**Update**
The team has fixed the issue by adding the appropriate conditionals to avoid underflow if there is insufficient collateral to repay the loan.

**File(s) affected:**`credit/CreditCaller.sol`

**Description:** If a loan is not liquidated in time, price fluctuations could make repayment and liquidation impossible due to underflows:

```
// in _repayClaim(). It will underflow if the sum of usedMintedAmount for all tokens > totalMintedAmount
totalMintedAmount = totalMintedAmount.sub(usedMintedAmount);
```

```
// in liquidate(). It will underflow if borrowedMinted > mintedAmount.
uint256 health = mintedAmount.sub(borrowedMinted).mul(LIQUIDATE_DENOMINATOR).div(mintedAmount);
```

In these scenarios, the protocol would be operating at a loss and the farmer would hold out their loan indefinitely.

**Recommendation:** Update `_repayClaim()` and `liquidate()` so that should a loan become under-collateralized, the protocol attempts to minimize losses rather than revert the function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Archi Finance |
| Report Date | N/A |
| Finders | Mustafa Hasan, Zeeshan Meghji, Ibrahim Abouzied, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/archi-finance/abb48b19-672a-4390-bf11-59c485978d61/index.html

### Keywords for Search

`vulnerability`

