---
# Core Classification
protocol: f(x) v2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61789
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fx-v2-audit
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

Flashloan Functionality is Blocked

### Overview


This bug report is about a function called `flashLoan` in the `FlashLoans` contract. The function has a condition that checks if the amount being returned is less than the amount borrowed plus a fee. However, the way the `returnedAmount` is calculated does not take into account the full amount borrowed, causing the condition to always be true and resulting in the flash loan failing. This issue has been resolved in a recent update to the contract.

### Original Finding Content

The [`flashLoan` function](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/FlashLoans.sol#L67-L97) of the `FlashLoans` contract uses the [`returnedAmount < amount + fee`](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/FlashLoans.sol#L87) condition to validate repayment. However, `returnedAmount` is [computed](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/FlashLoans.sol#L86) as the post-callback balance minus the pre-loan balance, which only represents the extra tokens sent to cover fees. As a result, `returnedAmount < amount + fee` is always `true`, causing every flash loan to revert unless the borrower somehow returns the entire principal, plus fee, as the fee.

Consider changing the condition to `returnedAmount < fee` so that the function correctly enforces repayment of the fee.

***Update:** Resolved in [pull request #17](https://github.com/AladdinDAO/fx-protocol-contracts/pull/17). This pull request fixes the issue by calculating `prevBalance` after the token transfer to the receiver. Additionally, compliance to [EIP-3156](https://eips.ethereum.org/EIPS/eip-3156) standard will be achieved once M-01 is resolved.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | f(x) v2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/fx-v2-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

