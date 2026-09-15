---
# Core Classification
protocol: Debita Finance V3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44232
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/627
source_link: none
github_link: https://github.com/sherlock-audit/2024-10-debita-judging/issues/211

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
finders_count: 20
finders:
  - newspacexyz
  - shaflow01
  - 0xe4669da
  - dany.armstrong90
  - Maroutis
---

## Vulnerability Title

M-4: The fee calculation in extendLoan function has a error

### Overview


This bug report discusses an issue with the fee calculation in the extendLoan function of the DebitaV3Loan.sol contract. When a borrower extends their loan duration, they are required to pay additional fees. However, due to a mistake in the calculation, the user may end up paying more than necessary. This is because the function mistakenly uses the timestamp instead of the extended loan duration for the fee calculation. This bug can potentially lead to financial losses for the user. The report also includes a proposed solution to fix the issue.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-10-debita-judging/issues/211 

## Found by 
0x37, 0xPhantom2, 0xc0ffEE, 0xe4669da, ExtraCaterpillar, Falendar, KaplanLabs, Maroutis, Nave765, bbl4de, dany.armstrong90, davidjohn241018, dhank, dimulski, durov, jsmi, momentum, newspacexyz, shaflow01, ydlee
### Summary

When a borrower extends the loan duration, they are required to pay additional fees for the extended time. However, due to a calculation error, this fee may be incorrect, potentially causing the user to pay more than necessary.

### Root Cause

https://github.com/sherlock-audit/2024-11-debita-finance-v3/blob/1465ba6884c4cc44f7fc28e51f792db346ab1e33/Debita-V3-Contracts/contracts/DebitaV3Loan.sol#L602
```solidity
                // if user already paid the max fee, then we dont have to charge them again
                if (PorcentageOfFeePaid != maxFee) {
                    // calculate difference from fee paid for the initialDuration vs the extra fee they should pay because of the extras days of extending the loan.  MAXFEE shouldnt be higher than extra fee + PorcentageOfFeePaid
                    uint feeOfMaxDeadline = ((offer.maxDeadline * feePerDay) /
                        86400);
                    if (feeOfMaxDeadline > maxFee) {
                        feeOfMaxDeadline = maxFee;
                    } else if (feeOfMaxDeadline < feePerDay) {
                        feeOfMaxDeadline = feePerDay;
                    }

                    misingBorrowFee = feeOfMaxDeadline - PorcentageOfFeePaid;
                }
```

The calculation for feeOfMaxDeadline should be:

extendedLoanDuration * feePerDay,

where extendedLoanDuration represents the extended borrowing time. However, the function mistakenly uses the timestamp directly for calculations, leading to an incorrect fee computation.

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

_No response_

### Impact

The user might end up paying significantly higher fees than expected, leading to potential financial losses.

### PoC

_No response_

### Mitigation

```diff
```solidity
                // if user already paid the max fee, then we dont have to charge them again
                if (PorcentageOfFeePaid != maxFee) {
                    // calculate difference from fee paid for the initialDuration vs the extra fee they should pay because of the extras days of extending the loan.  MAXFEE shouldnt be higher than extra fee + PorcentageOfFeePaid
-                   uint feeOfMaxDeadline = ((offer.maxDeadline * feePerDay) /
+                   uint feeOfMaxDeadline = (((offer.maxDeadline - loanData.startedAt)* feePerDay) /
                        86400);
                    if (feeOfMaxDeadline > maxFee) {
                        feeOfMaxDeadline = maxFee;
                    } else if (feeOfMaxDeadline < feePerDay) {
                        feeOfMaxDeadline = feePerDay;
                    }

                    misingBorrowFee = feeOfMaxDeadline - PorcentageOfFeePaid;
                }
```
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Debita Finance V3 |
| Report Date | N/A |
| Finders | newspacexyz, shaflow01, 0xe4669da, dany.armstrong90, Maroutis, ydlee, Falendar, bbl4de, 0x37, ExtraCaterpillar, 0xPhantom2, davidjohn241018, KaplanLabs, momentum, durov, dhank, dimulski, Nave765, jsmi, 0xc0ffEE |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-10-debita-judging/issues/211
- **Contest**: https://app.sherlock.xyz/audits/contests/627

### Keywords for Search

`vulnerability`

