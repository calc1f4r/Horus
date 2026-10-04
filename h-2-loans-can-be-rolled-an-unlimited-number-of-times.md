---
# Core Classification
protocol: Cooler
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6279
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/36
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/215

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
  - business_logic
  - configuration

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 20
finders:
  - HollaDieWaldfee
  - 0x52
  - yixxas
  - ali\_shehab
  - oxcm
---

## Vulnerability Title

H-2: Loans can be rolled an unlimited number of times

### Overview


This bug report was found by a group of contributors on GitHub and is related to the "Cooler" project. The issue is that the lender is unable to limit the number of times a loan can be rolled. This means that the lender cannot decide if the loan has been rolled too many times already. If the lender has given an interest-free loan, they may be forced to wait until the end of the universe if the borrower chooses to roll an excessive number of times. If the borrower is using a quickly-depreciating collateral, the lender may be at a loss if the term is rolled multiple times and the borrower defaults thereafter. The initial value of `loan.rollable` is always `true`, so unless the lender calls `toggleRoll()` in the same transaction that they call `clear()`, a determined attacker will be able to roll as many times as they wish. The recommended solution is to have a variable controlling the number of rolls the lender is allowing, and or only allow a roll if the current `block.timestamp` is within one `req.duration` of the current `loan.expiry`. The issue has been resolved as a result of the change for #265.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/215 

## Found by 
0x52, enckrish, IllIllI, cducrest-brainbot, banditx0x, simon135, Allarious, Trumpero, Breeje, neumo, Atarpara, yixxas, libratus, usmannk, ali\_shehab, oxcm, thekmj, HollaDieWaldfee, HonorLt, bin2chen

## Summary

Loans can be rolled an unlimited number of times, without letting the lender decide if has been done too many times already


## Vulnerability Detail

The lender is expected to be able to toggle whether a loan can be rolled or not, but once it's enabled, there is no way to prevent the borrower from rolling an unlimited number of times in the same transaction or in quick succession.


## Impact

If the lender is giving an interest-free loan and assumes that allowing a roll will only extend the term by one, they'll potentially be forced to wait until the end of the universe if the borrower chooses to roll an excessive number of times.

If the borrower is using a quickly-depreciating collateral, the lender may be happy to allow one a one-term extension, but will lose money if the term is rolled multiple times and the borrower defaults thereafter.

The initial value of `loan.rollable` is always `true`, so unless the lender calls `toggleRoll()` in the same transaction that they call `clear()`, a determined attacker will be able to roll as many times as they wish.


## Code Snippet

As long as the borrower is willing to pay the interest up front, they can call `roll()` any number of times, extending the duration of the total loan to however long they wish:
```solidity
// File: src/Cooler.sol : Cooler.roll()   #1

129        function roll (uint256 loanID) external {
130            Loan storage loan = loans[loanID];
131            Request memory req = loan.request;
132    
133            if (block.timestamp > loan.expiry) 
134                revert Default();
135    
136            if (!loan.rollable)
137                revert NotRollable();
138    
139            uint256 newCollateral = collateralFor(loan.amount, req.loanToCollateral) - loan.collateral;
140            uint256 newDebt = interestFor(loan.amount, req.interest, req.duration);
141    
142            loan.amount += newDebt;
143            loan.expiry += req.duration;
144            loan.collateral += newCollateral;
145            
146            collateral.transferFrom(msg.sender, address(this), newCollateral);
147:       }
```
https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L129-L147

[`toggleRoll()`](https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L185-L193) can't be used to stop rolls if they're all done in a single transaction.


## Tool used

Manual Review


## Recommendation

Have a variable controlling the number of rolls the lender is allowing, and or only allow a roll if the current `block.timestamp` is within one `req.duration` of the current `loan.expiry`


## Discussion

**hrishibhat**

Sponsor comment:
> Will resolve as result of change for #265

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Cooler |
| Report Date | N/A |
| Finders | HollaDieWaldfee, 0x52, yixxas, ali\_shehab, oxcm, cducrest-brainbot, bitx0x, Trumpero, usmannk, Breeje, Allarious, IllIllI, simon135, Atarpara, enckrish, neumo, bin2chen, thekmj, HonorLt, libratus |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/215
- **Contest**: https://app.sherlock.xyz/audits/contests/36

### Keywords for Search

`Business Logic, Configuration`

