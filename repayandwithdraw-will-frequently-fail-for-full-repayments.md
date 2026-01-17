---
# Core Classification
protocol: Ion Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32701
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/ion-protocol-audit
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

repayAndWithdraw Will Frequently Fail for Full Repayments

### Overview


The `repayWithdraw` function in the `IonHandlerBase` contract has a bug where the amount to repay is specified in WETH units, causing inaccuracies when converting to `normalizedDebt` units. This can result in the function failing when trying to repay a full borrow. The issue may be due to rounding errors or the transaction being mined at a different time than expected. If the computed `normalizedDebtToRepay` is too high or too low, the call may revert. This can happen if the `normalizedDebtToRepay` is higher than the vault's `normalizedDebt` or if the vault is "dusty". To fix this, the `repayAndWithdraw` function could be refactored to include a "max repayment" option or a separate function could be created specifically for full repayments. This would require changes to the transfer of WETH and an accurate rate to compute the amount of WETH needed. The bug has been resolved in a recent pull request.

### Original Finding Content

Within the [`repayWithdraw` function](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/IonHandlerBase.sol#L131) of the `IonHandlerBase` contract, the amount to repay is specified in units of WETH. As a result of inaccuracies in [converting this to `normalizedDebt` units](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/IonHandlerBase.sol#L144-L148), when attempting to repay an account's full borrow, this function is likely to fail. Inaccuracies may arise from rounding incorrectly, or from the transaction being mined at a different time than the user anticipates and [interest accrual](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/IonHandlerBase.sol#L146) being unexpected.


If a user attempts to pay off their entire borrow and the [computed `normalizedDebtToRepay`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/IonHandlerBase.sol#L148) is too high or too low, the call may revert. In case `normalizedDebtToRepay` is higher than a vault's `normalizedDebt`, the [addition of the negated `normalizedDebtToRepay` will revert](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L663) since the value [should be less than `0`](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L1131). In case that `normalizedDebtToRepay` is too low, the [vault is likely to be dusty, causing a revert](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/IonPool.sol#L707-L708).


Consider refactoring the `repayAndWithdraw` function to include a "max repayment" logical branch. Consider using the value `repayAmount == uint.max` to indicate a full repayment, for example. Note that this will require changes to the [transfer of WETH](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/IonHandlerBase.sol#L132) since the amount of WETH will need to be computed on-the-fly, and will require [an accurate rate](https://github.com/Ion-Protocol/ion-protocol/blob/98e282514ac5827196b49f688938e1e44709505a/src/flash/handlers/base/IonHandlerBase.sol#L145) to do so. Alternatively, consider making a separate function for full repayment, and informing users, at multiple places, of the risk of failure when using the regular `repayAndWithdraw` function for full or near-full repayments.


***Update:** Resolved in [pull request #22](https://github.com/Ion-Protocol/ion-protocol/pull/22).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Ion Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/ion-protocol-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

