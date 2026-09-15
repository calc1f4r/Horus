---
# Core Classification
protocol: Brava Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53566
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Protocol Fees Can Block Withdrawals

### Overview


Bug report: It is possible for a withdrawal to fail due to a miscalculation of shares in the `AcrossWithdraw` function. This happens when accrued fees are deducted before the withdrawal amount is calculated, causing the withdrawal to be processed for more shares than the account holds. This can occur with large withdrawals and is likely to happen when users withdraw all their assets. The issue has been rated as medium impact and can be resolved by adjusting the accounting flow to record share balances after fees are processed. The issue has been fixed by updating the `AcrossSupply.sol` function to account for protocol fees.

### Original Finding Content

## Description

It is possible for the payment of accrued fees to cause withdrawals on the same vault to fail. When processing withdrawals in `AcrossWithdraw`, the withdrawal amount is set using `sharesBefore`, which is recorded prior to the removal of accrued fees. This means that a withdrawal can be processed for a quantity of shares that the account no longer holds, which would then cause the withdrawal call to revert.

This will happen with proportionally large withdrawals and, as such, is highly likely to occur as users will usually opt to remove all assets when withdrawing. Note, this issue has the same accounting cause as BRAV-06, but it has been recorded as a separate finding due to different impact and likelihood of occurring.

This finding has been rated a medium impact as only one supported protocol is affected (Across), and the issue could be resolved by temporarily setting protocol fees to zero.

## Recommendations

Alter the accounting flow such that the share balance is recorded after fees have been processed, but before the withdrawal action occurs.

## Resolution

The withdrawal amount in `AcrossSupply.sol` has been adjusted to take into account any protocol fees paid during the function call.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Brava Labs |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf

### Keywords for Search

`vulnerability`

