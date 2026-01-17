---
# Core Classification
protocol: Term Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26296
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/term-finance/term1/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/term-finance/term1/review.pdf
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Borrowers cannot withdraw excess collateral after liquidation or default

### Overview


A bug was found in the TermRepoLocker contract, where borrowers were unable to withdraw excess collateral after they were entirely liquidated or defaulted. The issue was caused by a check in the externalUnlockCollateral() function on line 282, which would always evaluate to true and trigger a revert if the borrower’s owed balance had been fully repaid. This prevented the borrower from retrieving the excess collateral tokens. The bug was fixed with the implementation of PR 757, which allowed borrowers to withdraw leftover collateral after their repurchase obligation had been entirely repaid through liquidation or default.

### Original Finding Content

## Description

Borrowers are unable to withdraw excess collateral after they are entirely liquidated or defaulted. The excess collateral will be locked within the `TermRepoLocker` contract.

This issue stems from the check in `externalUnlockCollateral()` on line [282]:

```solidity
281 address borrower = termAuth.user;
if (termRepoServicer.getBorrowerRepurchaseObligation(borrower) == 0) {
283 revert ZeroBorrowerRepurchaseObligation(); // SigP: This will revert when loan paid in full
}
285 _unlockCollateral(borrower, collateralToken, amount);
if (isBorrowerInShortfall(borrower)) {
287 revert CollateralBelowMaintenanceRatios(borrower, collateralToken);
}
```

`termRepoServicer.getBorrowerRepurchaseObligation(borrower)` will always return `0` if the borrower’s owed balance has been fully repaid. In the case of a liquidation or a default, it is possible for this to happen without all of the collateral tokens being paid to the liquidator. The excess collateral tokens would then remain in the `TermRepoLocker` contract, marked as belonging to the borrower. If the borrower attempts to retrieve those tokens, however, the test on line [282] will evaluate to true and the revert on line [283] will be triggered.

## Recommendations

Allow borrowers to withdraw leftover collateral after their repurchase obligation has been entirely repaid through liquidation or default.

## Resolution

This finding has been addressed in PR 757.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Term Finance |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/term-finance/term1/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/term-finance/term1/review.pdf

### Keywords for Search

`vulnerability`

