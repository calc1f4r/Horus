---
# Core Classification
protocol: predict.fun lending market
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41808
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/561
source_link: none
github_link: https://github.com/sherlock-audit/2024-09-predict-fun-judging/issues/118

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
finders_count: 9
finders:
  - tobi0x18
  - kennedy1030
  - bughuntoor
  - dany.armstrong90
  - 000000
---

## Vulnerability Title

M-3: Refinancing and auction take less fee than expected.

### Overview


The bug report is about a problem with the protocol fee calculation in the PredictDotLoan smart contract. When creating a new loan, the protocol fee is correctly applied to the amount taken from the lender. However, when using the `refinance` and `auction` functions, the protocol fee is applied to the debt instead of the amount taken. This results in the protocol earning less fees than expected. The root cause of the issue is a wrong math formula used in the code. The impact of this bug is that the protocol will make significantly less fees than expected. The suggested mitigation is to use a different formula for calculating the protocol fee. The protocol team has already fixed this issue in their code.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-09-predict-fun-judging/issues/118 

## Found by 
000000, 0xNirix, bughuntoor, dany.armstrong90, iamnmt, kennedy1030, silver\_eth, t.aksoy, tobi0x18
### Summary

When creating a new loan within `_acceptOffer`, the `protocolFee` is applied to the whole amount taken from the lender - the fulfilled amount.

```solidity
    function _transferLoanAmountAndProtocolFee(
        address from,
        address to,
        uint256 loanAmount
    ) private returns (uint256 protocolFee) {
        protocolFee = (loanAmount * protocolFeeBasisPoints) / 10_000;
        LOAN_TOKEN.safeTransferFrom(from, to, loanAmount - protocolFee);
        if (protocolFee > 0) {
            LOAN_TOKEN.safeTransferFrom(from, protocolFeeRecipient, protocolFee);
        }
    }
``` 

So if the user fulfills 1000 USDC and the protocol fee is 2%, the fee that will be taken will be 20 USDC and the user will receive 980 USDC.

However, this is not the case within `refinance` and `auction`.

```solidity
        uint256 _nextLoanId = nextLoanId;
        uint256 debt = _calculateDebt(loan.loanAmount, loan.interestRatePerSecond, callTime - loan.startTime);
        uint256 protocolFee = (debt * protocolFeeBasisPoints) / 10_000;
```

There. the protocol fee is applied on the `debt`. So if a position with a debt of 980 USDC gets auctioned, the fee that will be paid will be 19,6 USDC.  In this case, the protocol will earn 2% less fees than expected.

Whenever there's a protocol fee, `refinance` and `auction` will earn less fees proportional to the set `protocolFee`. Meaning that if the fee is 1%, these functions would earn 1% less. And if the fee is set to 2%, the loss will be 2%.

As the protocol can easily lose up to 2% of its fees, this according to Sherlock rules should be classified as High severity
> Definite loss of funds without (extensive) limitations of external conditions. The loss of the affected party must exceed 1%.


### Root Cause

Wrong math formula used

### Affected Code
https://github.com/sherlock-audit/2024-09-predict-fun/blob/main/predict-dot-loan/contracts/PredictDotLoan.sol#L585


### Impact

Protocol will make significantly less fees than expected.


### PoC

_No response_

### Mitigation

Use the following formula instead
```solidity
        uint256 protocolFee = (debt * protocolFeeBasisPoints) / (10_000 - protocolFeeBasisPoints);
```



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/PredictDotFun/predict-dot-loan/pull/50

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | predict.fun lending market |
| Report Date | N/A |
| Finders | tobi0x18, kennedy1030, bughuntoor, dany.armstrong90, 000000, 0xNirix, t.aksoy, silver\_eth, iamnmt |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-09-predict-fun-judging/issues/118
- **Contest**: https://app.sherlock.xyz/audits/contests/561

### Keywords for Search

`vulnerability`

