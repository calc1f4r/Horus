---
# Core Classification
protocol: Credifi
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58548
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Credifi-Security-Review.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 2

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[M-01] Unchecked ERC20 Transfer in Loan Repayment

### Overview


The report describes a bug in a contract that allows for missing or undelivered funds when using Non-Compliant Tokens. This is due to the contract performing an ERC20 token transfer without verifying its success. The affected code is located in a specific file and the recommendation is to use a different function to prevent this issue. The team has responded that the bug has been fixed.

### Original Finding Content


## Severity

Medium Risk

## Description

The contract performs an ERC20 token `transferFrom()` without verifying its success. While most major tokens revert on failure, some non-ERC20 standard tokens technically allow them to return false instead of reverting.

This introduces a risk where Non-Compliant Tokens may fail silently, while the protocol assumes success, potentially leading to missing or undelivered funds.

## Location of Affected Code

File: [src/CredifiERC20Adaptor.sol#L620](https://github.com/credifi/contracts-audit/blob/ba976bad4afaf2dc068ca9dcd78b38052d3686e3/src/CredifiERC20Adaptor.sol#L620)

```solidity
function _performLoanRepayment( address user, IndividualLoan storage loan, uint256 repayAmount, address payer, bool requireFullRepayment ) internal returns (uint256 actualRepayAmount, uint256 remainingDebt, bool fullyRepaid) {
   // code

   // Transfer repay tokens from payer to this contract
   borrowToken.transferFrom(payer, address(this), actualRepayAmount);
   // code
}
```

## Recommendation

Consider using `safeTransferFrom()` instead of `transferFrom()`:

```solidity
// Use OpenZeppelin's SafeERC20
using SafeERC20 for IERC20;

// Replace transfer with:
borrowToken.safeTransferFrom(payer, address(this), actualRepayAmount);
```

## Team Response

Fixed.



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 2/5 |
| Audit Firm | Shieldify |
| Protocol | Credifi |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Credifi-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

