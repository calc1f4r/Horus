---
# Core Classification
protocol: Backed Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1859
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-04-backed-protocol-contest
source_link: https://code4rena.com/reports/2022-04-backed
github_link: https://github.com/code-423n4/2022-04-backed-findings/issues/80

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

protocol_categories:
  - dexes
  - bridge
  - cdp
  - services
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WatchPug
  - CertoraInc  hickuphh3
---

## Vulnerability Title

[M-04] `requiredImprovementRate` can not work as expected when `previousInterestRate` less than 10 due to precision loss

### Overview


This bug report concerns a vulnerability in the NFTLoanFacilitator.sol contract code. The vulnerability allows someone to buy out a loan with the same terms as the previous lender, even though they should be providing at least 10% better terms. This is because of precision loss when the previous interest rate is less than 10 and the required improvement rate is 100. 

The proof of concept for this bug is as follows. Alice creates a loan with a maximum per annum interest rate of 10, and receives a loan ID of 1. Bob then lends money for this loan with an interest rate of 9. Charlie then lends money for the same loan, with the same terms as Bob, but buys out the loan with the same terms. This should not be possible, as Charlie should be providing at least 10% better terms.

The recommendation for this bug is to consider using the Math.sol contract from OpenZeppelin, and to change the check to the following code: 

```solidity
(previousInterestRate != 0 // do not allow rate improvement if rate already 0
        && previousInterestRate - Math.ceilDiv(previousInterestRate * requiredImprovementRate, SCALAR) >= interestRate)
```

This bug report concerns a vulnerability in the NFTLoanFacilitator.sol contract code which allows someone to buy out a loan with the same terms as the previous lender, even though they should be providing at least 10% better terms. This is because of precision loss when the previous interest rate is less than 10 and the required improvement rate is 100. The recommendation for this bug is to consider using the Math.sol contract from OpenZeppelin, and to change the check to the given code.

### Original Finding Content

_Submitted by WatchPug, also found by CertoraInc and hickuphh3_

[NFTLoanFacilitator.sol#L167-L179](https://github.com/code-423n4/2022-04-backed/blob/e8015d7c4b295af131f017e646ba1b99c8f608f0/contracts/NFTLoanFacilitator.sol#L167-L179)

```solidity
{
    uint256 previousInterestRate = loan.perAnumInterestRate;
    uint256 previousDurationSeconds = loan.durationSeconds;

    require(interestRate <= previousInterestRate, 'NFTLoanFacilitator: rate too high');
    require(durationSeconds >= previousDurationSeconds, 'NFTLoanFacilitator: duration too low');

    require((previousLoanAmount * requiredImprovementRate / SCALAR) <= amountIncrease
    || previousDurationSeconds + (previousDurationSeconds * requiredImprovementRate / SCALAR) <= durationSeconds 
    || (previousInterestRate != 0 // do not allow rate improvement if rate already 0
        && previousInterestRate - (previousInterestRate * requiredImprovementRate / SCALAR) >= interestRate), 
    "NFTLoanFacilitator: proposed terms must be better than existing terms");
}
```

The `requiredImprovementRate` represents the percentage of improvement required of at least one of the terms when buying out from a previous lender.

However, when `previousInterestRate` is less than `10` and `requiredImprovementRate` is `100`, due to precision loss, the new `interestRate` is allowed to be the same as the previous one.

Making such an expected constraint absent.

### Proof of Concept

1.  Alice `createLoan()` with `maxPerAnumInterest` = 10, received `loanId` = 1
2.  Bob `lend()` with `interestRate` = 9  for `loanId` = 1
3.  Charlie `lend()` with `interestRate` = 9 (and all the same other terms with Bob) and buys out `loanId` = 1

Charlie is expected to provide at least 10% better terms, but actually bought out Bob with the same terms.

### Recommended Mitigation Steps

Consider using: [OpenZeppelin/Math.sol#L39-L42](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.5.0/contracts/utils/math/Math.sol#L39-L42)<br>

And change the check to:

```solidity
(previousInterestRate != 0 // do not allow rate improvement if rate already 0
        && previousInterestRate - Math.ceilDiv(previousInterestRate * requiredImprovementRate, SCALAR) >= interestRate)
```

**[wilsoncusack (Backed Protocol) confirmed and resolved](https://github.com/code-423n4/2022-04-backed-findings/issues/80#issuecomment-1094305756)**

**[gzeon (judge) commented](https://github.com/code-423n4/2022-04-backed-findings/issues/80#issuecomment-1100093154):**
 > Sponsor confirmed with fix.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Backed Protocol |
| Report Date | N/A |
| Finders | WatchPug, CertoraInc  hickuphh3 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-04-backed
- **GitHub**: https://github.com/code-423n4/2022-04-backed-findings/issues/80
- **Contest**: https://code4rena.com/contests/2022-04-backed-protocol-contest

### Keywords for Search

`vulnerability`

