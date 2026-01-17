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
solodit_id: 35219
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-gondi
source_link: https://code4rena.com/reports/2024-04-gondi
github_link: https://github.com/code-423n4/2024-04-gondi-findings/issues/13

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

[H-17] `refinanceFull`/`addNewTranche` reusing a lender's signature leads to unintended behavior

### Overview


The bug report is about a vulnerability in a code called "MultiSourceLoan". This code has two functions, "refinanceFull()" and "addNewTranche()", that use the same signature. This means that a user can use the signature of "refinanceFull()" to execute "addNewTranche()" which can result in double the borrowed amount and increase the risk of borrowing. The recommended mitigation is to add a type field in "RenegotiationOffer" to differentiate between the two functions. The bug has not been fixed yet and is still considered a risk. 

### Original Finding Content


<https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/loans/MultiSourceLoan.sol#L358> 

<https://github.com/code-423n4/2024-04-gondi/blob/b9863d73c08fcdd2337dc80a8b5e0917e18b036c/src/lib/loans/MultiSourceLoan.sol#L194>

### Vulnerability details

In `MultiSourceLoan`, `refinanceFull()` and `addNewTranche()` use the same signature.

```solidity
    function refinanceFull(
        RenegotiationOffer calldata _renegotiationOffer,
        Loan memory _loan,
        bytes calldata _renegotiationOfferSignature
    ) external nonReentrant returns (uint256, Loan memory) {
...
        if (lenderInitiated) {
            if (_isLoanLocked(_loan.startTime, _loan.startTime + _loan.duration)) {
                revert LoanLockedError();
            }
            _checkStrictlyBetter(
                _renegotiationOffer.principalAmount,
                _loan.principalAmount,
                _renegotiationOffer.duration + block.timestamp,
                _loan.duration + _loan.startTime,
                _renegotiationOffer.aprBps,
                totalAnnualInterest / _loan.principalAmount,
                _renegotiationOffer.fee
            );
        } else if (msg.sender != _loan.borrower) {
            revert InvalidCallerError();
        } else {
            /// @notice Borrowers clears interest
@>          _checkSignature(_renegotiationOffer.lender, _renegotiationOffer.hash(), _renegotiationOfferSignature);
            netNewLender -= totalAccruedInterest;
            totalAccruedInterest = 0;
        }
```

```solidity
    function addNewTranche(
        RenegotiationOffer calldata _renegotiationOffer,
        Loan memory _loan,
        bytes calldata _renegotiationOfferSignature
    ) external nonReentrant returns (uint256, Loan memory) {
...
        uint256 loanId = _renegotiationOffer.loanId;

        _baseLoanChecks(loanId, _loan);
        _baseRenegotiationChecks(_renegotiationOffer, _loan);
@>      _checkSignature(_renegotiationOffer.lender, _renegotiationOffer.hash(), _renegotiationOfferSignature);
        if (_loan.tranche.length == getMaxTranches) {
            revert TooManyTranchesError();
        }
```

So when `lender` signs `RenegotiationOffer`, it is meant to replace `tranche`, i.e. execute `refinanceFull()`. But a malicious user can use this sign and front-run execute `addNewTranche()`. 

`addNewTranche()` doesn't limit the `RenegotiationOffer` too much. The newly generated `Loan` will be approximately twice the total amount borrowed, and the risk of borrowing against the `lender` will increase dramatically.

### Impact

Maliciously using the signature of `refinanceFull()` to execute `addNewTranche()` will result in approximately double the borrowed amount, and the risk of borrowing will increase dramatically.

### Recommended Mitigation

In `RenegotiationOffer`, add a type field to differentiate between signatures.

### Assessed type

Context

**[0xend (Gondi) confirmed](https://github.com/code-423n4/2024-04-gondi-findings/issues/13#event-12543544476)**

**[Gondi mitigated](https://github.com/code-423n4/2024-05-gondi-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**
> Check `trancheIndex` to differentiate between `refiFull`/`addNewTranche`.

**Status:** Unmitigated. Full details in reports from [minhquanym](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/65), [bin2chen](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/18) and [oakcobalt](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/95), and also included in the [Mitigation Review](#mitigation-review) section below.

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
- **GitHub**: https://github.com/code-423n4/2024-04-gondi-findings/issues/13
- **Contest**: https://code4rena.com/reports/2024-04-gondi

### Keywords for Search

`vulnerability`

