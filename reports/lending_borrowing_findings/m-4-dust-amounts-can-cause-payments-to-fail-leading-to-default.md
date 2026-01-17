---
# Core Classification
protocol: Cooler
chain: everychain
category: logic
vulnerability_type: dust

# Attack Vector Details
attack_type: dust
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6285
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/36
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/218

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - dust
  - revert_by_sending_dust
  - front-running
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - IllIllI
  - HollaDieWaldfee
  - kiki\_dev
  - ak1
---

## Vulnerability Title

M-4: Dust amounts can cause payments to fail, leading to default

### Overview


This bug report is about an issue found in the code of the Cooler.sol file of the Sherlock Audit project. The issue is that when a loan is due, if a dust amount is sent, the balance underflows and the transaction reverts, leading to default. This means that an attacker can send a dust amount right before the loan is due, front-running any payments also destined for the final block before default. If the attacker's transaction goes in first, the borrower will be unable to pay back the loan before default, and will lose their remaining collateral.

The bug was found by kiki_dev, HollaDieWaldfee, IllIllI, and ak1, and was identified using manual review. The recommendation is to only collect and subtract the minimum of the current loan balance and the amount specified in the repaid variable. Hrishibhat commented that it was a good spot. The sponsor commented that it was a niche case.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/218 

## Found by 
kiki\_dev, HollaDieWaldfee, IllIllI, ak1

## Summary

Dust amounts can cause payments to fail, leading to default


## Vulnerability Detail

In order for a loan to close, the exact right number of wei of the debt token must be sent to match the remaining loan amount. If more is sent, the balance underflows, reverting the transaction.


## Impact

An attacker can send dust amounts right before a loan is due, front-running any payments also destined for the final block before default. If the attacker's transaction goes in first, the borrower will be unable to pay back the loan before default, and will lose thier remaining collateral. This may be the whole loan amount.


## Code Snippet

If the repayment amount isn't exactly the remaining loan amount, and instead is more (due to the dust payment), the subtraction marked below will underflow, reverting the payment:
```solidity
// File: src/Cooler.sol : Cooler.repay()   #1

108        function repay (uint256 loanID, uint256 repaid) external {
109            Loan storage loan = loans[loanID];
110    
111            if (block.timestamp > loan.expiry) 
112                revert Default();
113            
114            uint256 decollateralized = loan.collateral * repaid / loan.amount;
115    
116           if (repaid == loan.amount) delete loans[loanID];
117           else {
118 @>             loan.amount -= repaid;
119                loan.collateral -= decollateralized;
120            }
121    
122            debt.transferFrom(msg.sender, loan.lender, repaid);
123            collateral.transfer(owner, decollateralized);
124:       }
```
https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L108-L124


## Tool used

Manual Review


## Recommendation

Only collect and subtract the minimum of the current loan balance, and the amount specified in the `repaid` variable


## Discussion

**hrishibhat**

Sponsor comment:
> Good spot. Niche case.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Cooler |
| Report Date | N/A |
| Finders | IllIllI, HollaDieWaldfee, kiki\_dev, ak1 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/218
- **Contest**: https://app.sherlock.xyz/audits/contests/36

### Keywords for Search

`Dust, Revert By Sending Dust, Front-Running, Business Logic`

