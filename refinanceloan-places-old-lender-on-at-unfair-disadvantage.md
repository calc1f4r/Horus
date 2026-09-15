---
# Core Classification
protocol: Arcade.xyz
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40690
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/b2f35a21-b116-4ed6-95e6-37405749a716
source_link: https://cdn.cantina.xyz/reports/cantina_competition_arcade_mar2024.pdf
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
finders_count: 2
finders:
  - Nyksx
  - kodyvim
---

## Vulnerability Title

Refinanceloan() places old lender on at unfair disadvantage 

### Overview


This bug report discusses an issue with the refinanceLoan() function in the ReﬁnanceController.sol file. This function allows for loans to be refinanced after approximately 2 days, but it does not require the approval of the original lender. This can put the original lender at a disadvantage if the collateral for the loan is worth more than the balance and interest. The recommendation is to consider not refinancing loans without the old lender's approval to avoid potential risks.

### Original Finding Content

## RefinanceController.sol#L130

**Description:** A loan can be refinanced approximately 2 days after its creation. However, due to the permissionless nature of `refinanceLoan()`, this could place the old lender at an unfair disadvantage.

## Code Snippet
```solidity
function refinanceLoan(
    uint256 loanId,
    LoanLibrary.LoanTerms calldata newTerms
) external override returns (uint256 newLoanId) {
    LoanLibrary.LoanData memory data = loanCore.getLoan(loanId);
    // validate refinance
    _validateRefinance(data, newTerms);
    address borrower = IERC721(loanCore.borrowerNote()).ownerOf(loanId);
    newLoanId = _refinance(
        loanId,
        newTerms,
        borrower,
        msg.sender
    );
}
```

When lenders set the terms for loans, they believe that the price of the NFT collateral would cover or match the principal of their loan term and possible earned interest. But the issue is that `refinanceLoan()` rolls over a loan without the agreement or acknowledgment of the old lender.

For instance, if a borrower defaults on their loan, the old lender can claim the collateral. If anyone notices that the collateral is worth more than the balance and interest, they could front-run to refinance the loan and ultimately claim the corresponding collateral.

## Recommendation
Consider not refinancing loans without the old lender's approval.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Arcade.xyz |
| Report Date | N/A |
| Finders | Nyksx, kodyvim |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_arcade_mar2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/b2f35a21-b116-4ed6-95e6-37405749a716

### Keywords for Search

`vulnerability`

