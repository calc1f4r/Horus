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
solodit_id: 35237
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2024-04-gondi
source_link: https://code4rena.com/reports/2024-04-gondi
github_link: https://github.com/code-423n4/2024-04-gondi-findings/issues/10

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
  - bin2chen
---

## Vulnerability Title

[M-18] `distribute()` when can't repay all lenders, may lack of notification to `LoanManager` for accounting

### Overview


The `LiquidationDistributor` is a code used for distributing funds after an auction. If the amount raised from the auction is not enough, the lenders are repaid in a certain order. However, there is a bug in the code that can cause issues with accounting if the subsequent lender is a `LoanManager`. This can lead to incorrect calculations and accumulation of interest. To fix this, the recommended solution is to always call `loanManager` even if there are no funds to be repaid. This bug has been confirmed and mitigated by the team.

### Original Finding Content


The `LiquidationDistributor` is used to distribute funds after an auction. When the auction amount is insufficient, lenders are repaid in sequence.

```solidity
    function distribute(uint256 _proceeds, IMultiSourceLoan.Loan calldata _loan) external {
...
        if (_proceeds > totalPrincipalAndPaidInterestOwed + totalPendingInterestOwed) {
            for (uint256 i = 0; i < _loan.tranche.length;) {
                IMultiSourceLoan.Tranche calldata thisTranche = _loan.tranche[i];
                _handleTrancheExcess(
                    _loan.principalAddress,
                    thisTranche,
                    msg.sender,
                    _proceeds,
                    totalPrincipalAndPaidInterestOwed + totalPendingInterestOwed
                );
                unchecked {
                    ++i;
                }
            }
        } else {
@>          for (uint256 i = 0; i < _loan.tranche.length && _proceeds > 0;) {
                IMultiSourceLoan.Tranche calldata thisTranche = _loan.tranche[i];
                _proceeds = _handleTrancheInsufficient(
                    _loan.principalAddress, thisTranche, msg.sender, _proceeds, owedPerTranche[i]
                );
                unchecked {
                    ++i;
                }
            }
        }
    }
```

The code snippet above introduces a condition `_proceeds > 0` to terminate the loop when there's no remaining balance in `_proceeds`, thereby preventing further execution of `_handleTrancheInsufficient()`.

However, this approach creates an issue. If the subsequent lender is a `LoanManager`, it won't be notified for accounting via `_handleTrancheInsufficient()` -> `_handleLoanManagerCall()` -> `LoanManager(_tranche.lender).loanLiquidation()`.

Although no funds can be repaid, accounting is still necessary to notice and prevent incorrect accounting, causing inaccuracies in `totalAssets()` and continued accumulation of interest.
This outstanding debt should be shared among current users and prevent it from persisting as bad debt.

### Impact

Failure to notify `LoanManager.loanLiquidation()` may result in accounting inaccuracies.

### Recommended Mitigation

```diff
    function distribute(uint256 _proceeds, IMultiSourceLoan.Loan calldata _loan) external {
...
        } else {
-           for (uint256 i = 0; i < _loan.tranche.length && _proceeds > 0;) {
+           for (uint256 i = 0; i < _loan.tranche.length;) {
                IMultiSourceLoan.Tranche calldata thisTranche = _loan.tranche[i];
                _proceeds = _handleTrancheInsufficient(
                    _loan.principalAddress, thisTranche, msg.sender, _proceeds, owedPerTranche[i]
                );
                unchecked {
                    ++i;
                }
            }
        }
    }
```

### Assessed type

Context

**[0xend (Gondi) confirmed](https://github.com/code-423n4/2024-04-gondi-findings/issues/10#event-12543550109)**

**[Gondi mitigated](https://github.com/code-423n4/2024-05-gondi-mitigation?tab=readme-ov-file#mitigation-of-high--medium-severity-issues):**
> Always call `loanManager` (even if 0 proceeds).

**Status:** Mitigation confirmed. Full details in reports from [oakcobalt](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/113), [minhquanym](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/83) and [bin2chen](https://github.com/code-423n4/2024-05-gondi-mitigation-findings/issues/36).

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
| Finders | bin2chen |

### Source Links

- **Source**: https://code4rena.com/reports/2024-04-gondi
- **GitHub**: https://github.com/code-423n4/2024-04-gondi-findings/issues/10
- **Contest**: https://code4rena.com/reports/2024-04-gondi

### Keywords for Search

`vulnerability`

