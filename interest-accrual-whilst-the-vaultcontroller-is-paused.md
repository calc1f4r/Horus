---
# Core Classification
protocol: Interest Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19417
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf
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
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Interest accrual whilst the VaultController is paused

### Overview


This bug report is about a problem with the VaultController contract, where users are unable to repay borrowed funds when the contract is paused, but the interest is still accruing. This can potentially force users into liquidation, as they are locked out from repaying USDi into their vault, but interest keeps accruing over time. The project team accepted the risk and no mitigations have been implemented. The recommendation is to modify the pay_interest() function so that it does not accrue any interest when the protocol is paused, and to not make an interest calculation a precursor to pausing.

### Original Finding Content

## Description

When VaultController is paused, users are unable to repay borrowed funds, but the interest is still accrued, potentially forcing users into liquidation.

VaultController is a pausable contract, and amongst its functions, which are inaccessible when paused are `repayUSDi()` and `repayAllUSDi()`, both of which bear the `whenNotPaused` modifier. However, `calculateInterest()` and `pay_interest()` are both still callable when the contract is paused, with interest accruing as a function of time (and the reserve ratio).

As a result of this, it is possible that a user could mint a vault, deposit into it, borrow USDi against it, and then accrue interest, potentially putting the vault on the edge of insolvency. Consider a situation where, just before this user is about to call `repayUSDi()`, the protocol is paused (e.g., in a situation where the reserve ratio is very low and so the interest rate is very high). In this situation, the user is locked out from repaying USDi into their vault, but interest keeps accruing over time, eventually forcing the user into insolvency. They are then liquidated as soon as the protocol is unpaused and lose their assets.

## Recommendations

Modify `pay_interest()` so that it does not accrue any interest while the protocol is paused. In doing so, it is recommended not to make an interest calculation a precursor to pausing, as any issue with interest calculation could potentially render the contract unpausable.

## Resolution

This risk was accepted by the project team. No mitigations have been implemented.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Interest Protocol |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/interest-protocol/review.pdf

### Keywords for Search

`vulnerability`

