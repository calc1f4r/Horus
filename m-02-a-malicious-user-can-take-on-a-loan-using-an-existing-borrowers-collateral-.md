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
solodit_id: 35221
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-gondi
source_link: https://code4rena.com/reports/2024-04-gondi
github_link: https://github.com/code-423n4/2024-04-gondi-findings/issues/76

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
  - nft_lending

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - oakcobalt
---

## Vulnerability Title

[M-02] A malicious user can take on a loan using an existing borrower's collateral in `refinanceFromLoanExecutionData()`

### Overview


The bug report is about a vulnerability in the code for `MultiSourceLoan.sol`. The function `refinanceFromLoanExecutionData()` does not check if the borrower of the loan matches the borrower in the loan execution data, which can be exploited. This allows a malicious borrower to use another borrower's collateral for their own loan. There are two vulnerabilities: 1. The function `_validateExecutionData` does not check for matching borrowers and can be bypassed by someone who is not the borrower. 2. The function `refinanceFromLoanExecutionData()` does not check if the new loan execution data has the same nft tokenId as the existing loan. This allows a malicious borrower to transfer the loan to themselves and lock the collateral of the original borrower. This can also happen in a front-running scenario. The recommended mitigation step is to add checks to ensure the borrower in the loan execution data matches the borrower in the loan. The bug has been confirmed and mitigated by the Gondi team. 

### Original Finding Content


In `MultiSourceLoan.sol`, `refinanceFromLoanExecutionData()` doesn't check whether `_loan.borrower == _loanExecutionData.borrower`, which is open rooms for exploits.

BorrowerB (malicious) can sign a `_loanExecutionData` offer and initiate a `refinanceFromLoanExecutionData()` call with Borrower A's loan. Borrower B will use Borrower A's collateral for his loan.

There are (2) vulnerabilities here:
1. `_validateExecutionData` will not check whether `_loan.borrower == _executionData.borrower`. In addition, it will directly [bypass the check](https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/loans/MultiSourceLoan.sol#L792) on `executionData`'s borrower signature as long as `msg.sender!=_loan.borrower`.

2. `refinanceFromLoanExecutionData()` doesn't check whether the new loanExecutiondata (`_loanExecutionData`) has the [same nft tokenId](https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/loans/MultiSourceLoan.sol#L334)(`executionData.tokenId`) as the [existing loan](https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/loans/MultiSourceLoan.sol#L308)(`_loan.nftCollateralTokenId`).

As a result, if `_loanExecutionData.borrower` (Borrower B) initiates `refinanceFromLoanExecutionData()` call, the following would happen:
- `msg.sender != _loan.borrower` (Borrwer A), this bypass `_validateExecutionData`'s signature check. Also, it will not revert because no checks on [address _borrower](https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/loans/MultiSourceLoan.sol#L319)(`loan.borrower==_loanExecutionData.borrower;`.

- There is no check on `_loanExecutionData.tokenId`. As long as `_loan` and `_loanExecutionData` has [the same `principalAddress` and the same `nftCollateralAddress`](https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/loans/MultiSourceLoan.sol#L322), `_processOffersFromExecutionData()` will succeed in [transferring principal loans to Borrower B](https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/loans/MultiSourceLoan.sol#L1025).

- As long as the `_loan.borrower` (Borrower A) has the funds for [repayment](https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/loans/MultiSourceLoan.sol#L946). (Note: Borrower A might have approved `MultiSourceLoan.sol` for asset transfer if they are ready for repayments.), the tx will succeed and Borrower A's collateral will continually be locked for Borrower B's new loan.

The above steps can also happen in a front-running scenario, where Borrower B sees that Borrower A approves `MultiSourceLoan.sol` for loan repayments and front-run Borrower A's repayment with a new loan.

### Recommended Mitigation Steps

In `_validateExecutionData`, consider adding checks to ensure `address _borrower` `== _executionData.borrower`.

**[0xend (Gondi) confirmed](https://github.com/code-423n4/2024-04-gondi-findings/issues/76#event-12543103939)**

*Note: For full discussion, see [here](https://github.com/code-423n4/2024-04-gondi-findings/issues/76).*

**[Gondi mitigated](https://github.com/code-423n4/2024-05-gondi-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**
> Checking signature from the existing borrower.

**Status:** Mitigation confirmed. Full details in reports from [oakcobalt](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/97), [minhquanym](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/67) and [bin2chen](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/20).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Gondi |
| Report Date | N/A |
| Finders | oakcobalt |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-gondi
- **GitHub**: https://github.com/code-423n4/2024-04-gondi-findings/issues/76
- **Contest**: https://code4rena.com/reports/2024-04-gondi

### Keywords for Search

`vulnerability`

