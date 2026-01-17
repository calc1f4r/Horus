---
# Core Classification
protocol: OpenBrush Contracts Library Security Review
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32778
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/openbrush-contracts-library-security-review
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

Incorrect max_flashloan Amount When Using FlashLender and PSP22Capped Together

### Overview


The `max_flashloan` function in the `FlashLenderImpl` code calculates the amount of tokens to be flash-minted by subtracting the current total supply from the total maximum balance of the PSP22. However, when using both the `FlashLender` and `PSP22Capped` extensions, this function does not take into account the cap. This can lead to incorrect amounts being returned and potentially causing transactions to fail. The bug has been fixed in a recent update, but it is recommended to add a function to check the cap and ensure the correct amount is returned for flash loans.

### Original Finding Content

The [`max_flashloan` function](https://github.com/Brushfam/openbrush-contracts/blob/553347354de6d0ead6a335ba4c197bdd01fb2d12/contracts/src/token/psp22/extensions/flashmint.rs#L48) in `FlashLenderImpl` calculates the total amount of tokens to be flash-minted as the total maximum balance minus the current total supply of the PSP22.


However, when using both the `FlashLender` and `PSP22Capped` extensions, the `max_flashloan` function does not take into account the cap. This means that when users call the function, an incorrect amount will be returned. If users then consider this amount as valid and attempt to perform a flash-borrow operation, the transaction can revert.


Consider adding a function that checks the cap (by calling the `_cap` function) and calling it within `max_flashloan` to obtain the correct flash loan amount.


***Update:** Resolved in [pull request #142](https://github.com/Brushfam/openbrush-contracts/pull/142) at commit [c1c1fe1](https://github.com/Brushfam/openbrush-contracts/pull/142/commits/c1c1fe1b22d28bae07eed02fb85a6b74ede39aaf).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | OpenBrush Contracts Library Security Review |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/openbrush-contracts-library-security-review
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

