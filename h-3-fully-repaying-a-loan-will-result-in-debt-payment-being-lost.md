---
# Core Classification
protocol: Cooler
chain: everychain
category: logic
vulnerability_type: configuration

# Attack Vector Details
attack_type: configuration
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6280
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/36
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/33

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
  - configuration
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - Avci
  - 0x52
  - Bahurum
  - stent
  - ElKu
---

## Vulnerability Title

H-3: Fully repaying a loan will result in debt payment being lost

### Overview


This bug report is about an issue found in the Cooler smart contract. When a loan is fully repaid, the loan storage associated with the loanID being repaid is deleted. This means that the loan.lender is now address(0) and the loan payment will be sent there instead. This will result in the debt being transferred to address(0) instead of the lender and some ERC20 tokens will revert when being sent to address(0) but a large number will simply be sent there and lost forever. The issue was found by 0x52, wagmi, serial-coder, HonorLt, stent, Avci, libratus, Bahurum, ElKu, berndartmueller and was confirmed by hrishibhat. The code snippet for the issue can be found at https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L108-L124. The recommendation given is to send collateral/debt then delete, which will ensure that the lender will receive the debt payment.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/33 

## Found by 
0x52, wagmi, serial-coder, HonorLt, stent, Avci, libratus, Bahurum, ElKu, berndartmueller

## Summary

When a `loan` is fully repaid the `loan` storage is deleted. Since `loan` is a `storage` reference to the loan, `loan.lender` will return `address(0)` after the `loan` has been deleted. This will result in the `debt` being transferred to `address(0)` instead of the lender. Some ERC20 tokens will revert when being sent to `address(0)` but a large number will simply be sent there and lost forever.

## Vulnerability Detail

    function repay (uint256 loanID, uint256 repaid) external {
        Loan storage loan = loans[loanID];

        if (block.timestamp > loan.expiry) 
            revert Default();
        
        uint256 decollateralized = loan.collateral * repaid / loan.amount;

        if (repaid == loan.amount) delete loans[loanID];
        else {
            loan.amount -= repaid;
            loan.collateral -= decollateralized;
        }

        debt.transferFrom(msg.sender, loan.lender, repaid);
        collateral.transfer(owner, decollateralized);
    }

In `Cooler#repay` the loan storage associated with the loanID being repaid is deleted. `loan` is a storage reference so when `loans[loanID]` is deleted so is `loan`. The result is that `loan.lender` is now `address(0)` and the loan payment will be sent there instead.

## Impact

Lender's funds are sent to `address(0)`

## Code Snippet

https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L108-L124

## Tool used

Manual Review

## Recommendation

Send collateral/debt then delete:

    -   if (repaid == loan.amount) delete loans[loanID];
    +   if (repaid == loan.amount) {
    +       debt.transferFrom(msg.sender, loan.lender, loan.amount);
    +       collateral.transfer(owner, loan.collateral);
    +       delete loans[loanID];
    +       return;
    +   }

## Discussion

**hrishibhat**

Sponsor comment:
> Great spot, embarassing oversight.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Cooler |
| Report Date | N/A |
| Finders | Avci, 0x52, Bahurum, stent, ElKu, berndartmueller, wagmi, serial-coder, HonorLt, libratus |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/33
- **Contest**: https://app.sherlock.xyz/audits/contests/36

### Keywords for Search

`Configuration, Business Logic`

