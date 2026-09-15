---
# Core Classification
protocol: Teller Lender Groups Update Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44223
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/472
source_link: none
github_link: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/71

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
finders_count: 1
finders:
  - hash
---

## Vulnerability Title

M-8: EMI calculation is flawed

### Overview


This bug report discusses an issue with the calculation of EMI (Equated Monthly Installment) repayment amounts in the Teller Finance system. The report identifies a flaw in the code that leads to lowered payments being made. The root cause of the issue is explained and a suggested solution is provided. The impact of this bug is incorrect payment amounts being calculated for EMI repayments. The report also mentions that there is currently no response to the issue from the team. The suggested mitigation for this bug is to not use the "min" function and instead use a different formula for calculating the amount due.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/71 

## Found by 
hash
### Summary

Taking min when calculating EMI repayment amount is flawed

### Root Cause

The amount due in case of EMI repayment is calculated as:
https://github.com/sherlock-audit/2024-11-teller-finance-update/blob/0c8535728f97d37a4052d2a25909d28db886a422/teller-protocol-v2-audit-2024/packages/contracts/contracts/libraries/V2Calculations.sol#L124-L138
```solidity
        } else {
            // Default to PaymentType.EMI
            // Max payable amount in a cycle
            // NOTE: the last cycle could have less than the calculated payment amount


            //the amount owed for the cycle should never exceed the current payment cycle amount  so we use min here 
            uint256 owedAmountForCycle = Math.min(  ((_bid.terms.paymentCycleAmount  * owedTime)  ) /
                    _paymentCycleDuration , _bid.terms.paymentCycleAmount+interest_ ) ;


            uint256 owedAmount = isLastPaymentCycle
                ? owedPrincipal_ + interest_
                : owedAmountForCycle  ;


            duePrincipal_ = Math.min(owedAmount - interest_, owedPrincipal_);
        }
```

This is incorrect and leads to lowered payments since `_bid.terms.paymentCycleAmount+interest_` will be taken instead of the ratio wise amount

Eg:
Principal (P) = 100
Annual Rate (r) = 12% = 0.12
Number of Monthly Payments (n) = 12
monthly EMI = 8.84

But if the repayment occurs after 2 months, this formula calculates the amount due as 8.84 + 2 == 10.84 instead of 8.84 * 2 

### Internal pre-conditions

_No response_

### External pre-conditions

_No response_

### Attack Path

_No response_

### Impact

Incorrectly lowered payments in case of EMI repayments 

### PoC

_No response_

### Mitigation

Dont take the min. Instead use 
```solidity
 ((_bid.terms.paymentCycleAmount  * owedTime)  ) /
                    _paymentCycleDuration
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Teller Lender Groups Update Audit |
| Report Date | N/A |
| Finders | hash |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-11-teller-finance-update-judging/issues/71
- **Contest**: https://app.sherlock.xyz/audits/contests/472

### Keywords for Search

`vulnerability`

