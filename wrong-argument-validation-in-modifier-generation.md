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
solodit_id: 32782
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

Wrong Argument Validation in Modifier Generation

### Overview


The `generate` function in the `modifier_definition` macro is causing issues when checking modifier arguments. The code incorrectly tries to match the first argument again when checking that the second argument is not `self`. This could result in flawed methods being accepted as valid modifiers. Additionally, the error message implies that the argument must be passed by value and implement the `Clone` trait, but it only checks that the argument is not a reference. The bug has been partially resolved in a pull request, but the error message still needs to be corrected to accurately reflect the code's behavior.

### Original Finding Content

In the [`generate`](https://github.com/Brushfam/openbrush-contracts/blob/553347354de6d0ead6a335ba4c197bdd01fb2d12/lang/codegen/src/modifier_definition.rs#L34) function of the `modifier_definition` macro, modifier arguments are matched against certain expected types. When checking that the [second argument is not `self`](https://github.com/Brushfam/openbrush-contracts/blob/553347354de6d0ead6a335ba4c197bdd01fb2d12/lang/codegen/src/modifier_definition.rs#L178), the `if let` block erroneously tries to match against the [first](https://github.com/Brushfam/openbrush-contracts/blob/553347354de6d0ead6a335ba4c197bdd01fb2d12/lang/codegen/src/modifier_definition.rs#L175C47-L175C53) argument again. This may allow flawed methods to be accepted as valid modifiers.


Additionally, when matching on [additional arguments](https://github.com/Brushfam/openbrush-contracts/blob/553347354de6d0ead6a335ba4c197bdd01fb2d12/lang/codegen/src/modifier_definition.rs#L182), the error message implies a necessary check that the argument is passed by value and implements the `Clone` trait. However, the check only ensures that the argument is not a reference.


Consider correcting the argument validation in the `generate` function to correspond to the intended behavior.


***Update:** Partially resolved in [pull request #144](https://github.com/Brushfam/openbrush-contracts/pull/144/files) at commit [b48968d](https://github.com/Brushfam/openbrush-contracts/pull/144/commits/b48968d62acf23e4c7c8dea2fc9d505d6bb0b7d2). The client did not take any action on the inaccurate error message. They expressed that checking if `Clone` trait is implemented, it is not realistic to do in Rust. Nonetheless, they should modify the error message to more accurately reflect what the code is actually checking.*

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

