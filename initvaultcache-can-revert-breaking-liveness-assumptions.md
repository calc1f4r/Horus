---
# Core Classification
protocol: Euler Labs - EVK
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35951
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-EVK-April-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-EVK-April-2024.pdf
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
finders_count: 5
finders:
  - Christos Pap
  - M4rio.eth
  - Christoph Michel
  - David Chaparro
  - Emanuele Ricci
---

## Vulnerability Title

initVaultCache can revert breaking liveness assumptions

### Overview


This bug report discusses a medium risk issue in the Cache.sol code, specifically lines 80-88 and 91-92. The problem is that while some parts of the code handle overflows properly, other parts still have the potential to cause a revert. This means that certain functions, such as withdraw, redeem, or liquidate, may not be able to be executed. The report suggests making changes to the code and updating the white paper to address this issue. The problem has been fixed in a recent pull request, and the white paper has been updated to include information about interest overflows.

### Original Finding Content

## Severity: Medium Risk

## Context
- `Cache.sol#L80-L88`
- `Cache.sol#L91-L92`

## Description
While some parts of the `initVaultCache` gracefully handle overflows, other parts can still revert:

```solidity
// multiplication can overflow
uint256 newTotalBorrows =
vaultCache.totalBorrows.toUint() * newInterestAccumulator /
vaultCache.interestAccumulator; 

// if newTotalBorrows didn't overflow, this shouldn't overflow either because it was divided by
interestAccumulator > interestFee. (unless we use FullMath to compute newTotalBorrows)

uint256 feeAssets = (newTotalBorrows - vaultCache.totalBorrows.toUint()) * interestFee.toUint16() /
(1e4 << INTERNAL_DEBT_PRECISION_SHIFT);
```

The guarantee described in the Whitepaper is broken: In the event that a vault encounters an overflow (either in `rpow` or its accumulator) the accumulator will stop growing, meaning that no further interest will be earned/charged. However, debts can still be repaid and funds withdrawn.

## Recommendation
The `initVaultCache` function should not lock up as it would break liveness for important functions like withdraw, redeem, or liquidate that should always be possible to execute.

## Euler
Fixed in PR 184.

## Spearbit
The PR mitigates the finding. Spearbit suggests the following changes to be applied:
1. Write an inline comment that explains the reasoning behind the logic calculating `newInterestAccumulator` and `newTotalBorrows`. It would help a lot both Euler's new developers and external security researchers that will look at the code to understand the codebase or find issues during bug bounties.
2. Update the EVK white paper, introducing a chapter about liveliness or expanding the existing one about "Interest Overflows".

## Euler Response
Acknowledged. The white paper was updated to better cover this and similar effects. The Interest Overflows section should be an obvious source of information for anyone interested in this code.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Euler Labs - EVK |
| Report Date | N/A |
| Finders | Christos Pap, M4rio.eth, Christoph Michel, David Chaparro, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-EVK-April-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Euler-Spearbit-Security-Review-EVK-April-2024.pdf

### Keywords for Search

`vulnerability`

