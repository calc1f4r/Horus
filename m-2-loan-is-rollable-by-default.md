---
# Core Classification
protocol: Cooler
chain: everychain
category: logic
vulnerability_type: initialization

# Attack Vector Details
attack_type: initialization
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6283
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/36
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/265

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
  - initialization
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 13
finders:
  - HollaDieWaldfee
  - simon135
  - enckrish
  - yixxas
  - Nyx
---

## Vulnerability Title

M-2: Loan is rollable by default

### Overview


This bug report is about an issue with the loan system of a project. The issue is that when clearing a new loan, the flag of ```rollable``` is set to true by default. This means a borrower can extend the loan anytime before the expiry, giving them an unfair advantage over the lenders. To prevent this, the lenders have to separately toggle the status to false. It is also possible for someone to roll their loan, especially if the capital requirements are not huge. The recommendation is to set ```rollable``` to false by default or add an extra function parameter to determine the initial value of this status. The issue was discussed and it was decided that the ```rollable``` flag should be set to false by default.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/265 

## Found by 
hansfriese, Nyx, enckrish, wagmi, yixxas, HollaDieWaldfee, HonorLt, Tricko, Zarf, libratus, simon135, usmannk, Trumpero

## Summary
Making the loan rollable by default gives an unfair early advantage to the borrowers.

## Vulnerability Detail
When clearing a new loan, the flag of ```rollable``` is set to true by default:
```solidity
    loans.push(
        Loan(req, req.amount + interest, collat, expiration, true, msg.sender)
    );
```
This means a borrower can extend the loan anytime before the expiry:
```solidity
    function roll (uint256 loanID) external {
        Loan storage loan = loans[loanID];
        Request memory req = loan.request;

        if (block.timestamp > loan.expiry) 
            revert Default();

        if (!loan.rollable)
            revert NotRollable();
```
If the lenders do not intend to allow rollable loans, they should separately toggle the status to prevent that:
```solidity
    function toggleRoll(uint256 loanID) external returns (bool) {
        ...
        loan.rollable = !loan.rollable;
        ...
    }
```

I believe it gives an unfair advantage to the borrower because they can re-roll the loan before the lender's transaction forbids this action.

## Impact
Lenders who do not want the loans to be used more than once, have to bundle their transactions. Otherwise, it is possible that someone might roll their loan, especially if the capital requirements are not huge because anyone can roll any loan.

## Code Snippet

https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L177

https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L191

https://github.com/sherlock-audit/2023-01-cooler/blob/main/src/Cooler.sol#L126-L147

## Tool used

Manual Review

## Recommendation
I believe ```rollable``` should be set to false by default or at least add an extra function parameter to determine the initial value of this status.

## Discussion

**hrishibhat**

Sponsor comment:
> Valid. Will default to false.


**sherlock-admin**

> Retracted since https://github.com/sherlock-audit/2023-01-cooler-judging/issues/215 shows that there can be circumstances where funds lose value over the life of the loan

You've deleted an escalation for this issue.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Sherlock |
| Protocol | Cooler |
| Report Date | N/A |
| Finders | HollaDieWaldfee, simon135, enckrish, yixxas, Nyx, Tricko, Trumpero, usmannk, hansfriese, wagmi, HonorLt, libratus, Zarf |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-cooler-judging/issues/265
- **Contest**: https://app.sherlock.xyz/audits/contests/36

### Keywords for Search

`Initialization, Business Logic`

