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
solodit_id: 61791
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/fx-v2-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Flashloan Functionality Does Not Follow ERC-3156 Standard

### Overview


The report discusses a bug in the ERC-3156 specification for flash loans. The specification states that after a callback, the `flashLoan` function should take the loan amount and fee token from the receiver. However, the current implementation expects the caller to return the tokens, which prevents the contract from working with other compliant contracts. The specification also states that the `flashFee` function should return the fee charged for the loan, but it is currently not clear what should happen if the token is not supported. The team behind the f(x) Protocol has acknowledged the issue and plans to fix it in a future update.

### Original Finding Content

[ERC-3156](https://eips.ethereum.org/EIPS/eip-3156) specifies:

> After the callback, the `flashLoan` function MUST take the amount + fee token from the receiver, or revert if this is not successful.

Instead of taking the token, [`flashLoan`](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/FlashLoans.sol#L86) expects the caller to have returned the tokens. This will stop the contract from integrating with any compliant `IERC3156FlashBorrower` contracts as they will not return the tokens to the contract here.

[ERC-3156](https://eips.ethereum.org/EIPS/eip-3156) further specifies:

> The `flashFee` function MUST return the fee charged for a loan of amount token. If the token is not supported `flashFee` MUST revert.

The use of the word "supported" is ambiguous here, in that it does not specify that a maximum loan amount of zero means that a token is "unsupported." However, the ERC does conflate returning zero in `maxFlashLoan` to mean that a token is unsupported. Therefore, in situations where `maxFlashLoan` will return zero, `flashFee` must revert. Currently, the function simply [calculates a fraction of the amount given](https://github.com/AladdinDAO/fx-protocol-contracts/blob/56a47eab8d10334e479df83a2b13a8b68ce390e9/contracts/core/FlashLoans.sol#L59), regardless of the token.

Consider fixing the `flashLoan` and `flashFee` functions to be compliant with ERC-3156 as described above.

***Update:** Acknowledged, resolution planned. The f(x) Protocol team stated:*

> *We acknowledge the issue and plan to address it in a future update.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

