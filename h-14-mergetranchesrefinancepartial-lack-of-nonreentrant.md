---
# Core Classification
protocol: Gondi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35216
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-gondi
source_link: https://code4rena.com/reports/2024-04-gondi
github_link: https://github.com/code-423n4/2024-04-gondi-findings/issues/27

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

protocol_categories:
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - bin2chen
---

## Vulnerability Title

[H-14] `mergeTranches()`/`refinancePartial()` lack of `nonReentrant`

### Overview


This bug report discusses an issue with the `mergeTranches()` method in a smart contract. This method does not have protection against reentrancy attacks, which could allow attackers to manipulate the `_loans[]` storage and potentially steal funds. The report provides an example of how this vulnerability could be exploited. The recommended mitigation is to add a `nonReentrant` modifier to the affected methods. This issue has been confirmed and mitigated by the developers.

### Original Finding Content


In `mergeTranches()`, the method's code implementation is as follows:

```solidity
 function mergeTranches(uint256 _loanId, Loan memory _loan, uint256 _minTranche, uint256 _maxTranche)
        external
        returns (uint256, Loan memory)
    {
        _baseLoanChecks(_loanId, _loan);
        uint256 loanId = _getAndSetNewLoanId();
        Loan memory loanMergedTranches = _mergeTranches(loanId, _loan, _minTranche, _maxTranche);
        _loans[loanId] = loanMergedTranches.hash();
        delete _loans[_loanId];

        emit TranchesMerged(loanMergedTranches, _minTranche, _maxTranche);

        return (loanId, loanMergedTranches);
    }
```

As shown above, this method lacks reentrancy protection, which could allow reentrancy attacks to manipulate the `_loans[]`.

Example: Suppose `_loans[1] = {NFT = 1}`
1. Alice calls `refinanceFromLoanExecutionData(_loans\[1],LoanExecutionData)`.
    - `LoanExecutionData.ExecutionData.OfferExecution.LoanOffer.OfferValidator\[0].validator` `=  CustomContract  => for callback`.
2. `refinanceFromLoanExecutionData()` -> `_processOffersFromExecutionData()` -> `_validateOfferExecution()` -> `_checkValidators()` -> `IOfferValidator(CustomContract).validateOffer()`.
3. In `IOfferValidator(CustomContract).validateOffer()`, call `MultiSourceLoan.mergeTranches(_loans[1])` -> pass without `nonReentrant`.
    - `_loans\[3] = newLoan.hash()`
4. Return to `refinanceFromLoanExecutionData()`, will execute:
    - `_loans\[2] = newOtherLoan.hash()`.

There will be `_loans[2]` and `_loans[3]`, both containing `NFT=1`.
Note: Both Loans 's lender are all himself:
1. The user can `repayLoan(_loans[2])` and get the NFT back.
2. Use the NFT to borrow other people's funds, e.g. to generate `_loans[100]`.
3. `repayLoan(_loans[3])`, get NFT back.

### Recommended Mitigation

Add `nonReentrant`:

```diff
 function mergeTranches(uint256 _loanId, Loan memory _loan, uint256 _minTranche, uint256 _maxTranche)
        external
+       nonReentrant
        returns (uint256, Loan memory)
    {
        _baseLoanChecks(_loanId, _loan);
        uint256 loanId = _getAndSetNewLoanId();

    function refinancePartial(RenegotiationOffer calldata _renegotiationOffer, Loan memory _loan)
        external
+       nonReentrant
        returns (uint256, Loan memory)
    {
```

### Assessed type

Context

**[0xend (Gondi) confirmed](https://github.com/code-423n4/2024-04-gondi-findings/issues/27#event-12545516857)**

**[Gondi mitigated](https://github.com/code-423n4/2024-05-gondi-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**
> Added `nonReentrant`.

**Status:** Mitigation confirmed. Full details in reports from [oakcobalt](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/92), [minhquanym](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/62) and [bin2chen](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/15).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gondi |
| Report Date | N/A |
| Finders | bin2chen |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-gondi
- **GitHub**: https://github.com/code-423n4/2024-04-gondi-findings/issues/27
- **Contest**: https://code4rena.com/reports/2024-04-gondi

### Keywords for Search

`vulnerability`

