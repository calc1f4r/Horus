---
# Core Classification
protocol: Compound Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11832
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/compound-audit/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - liquidity_manager
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Misleading NatSpec Comments

### Overview


This bug report is about Ethereum Natural Specification (NatSpec). NatSpec is meant to describe code in a way that is understandable to users. In this report, there are several comments that are misleading or incorrect, and they should be updated appropriately. 

The first issue is with the `getBorrowRate` interface and implementation. The comments state that the rate is scaled by 10e18, but it is actually scaled by 1e18. The `CToken` contract comment about the maximum borrow rate per block is also incorrect, as it states 0.0005% when it should be 0.0005 (or 0.05%). 

The comment on line 7 of `Unitroller.sol` is an incomplete thought/sentence. The comment on line 41 of `ComptrollerStorage.sol` uses the word “discount” when it should use “bonus”, as a 25% discount is equivalent to a 33% bonus. The comment on line 6 of `Exponential.sol` says “fixed-decision” when it should say “fixed-precision”. Lastly, the comment on line 83 of `CToken.sol` describes `borrowIndex` as the accumulator of earned interest when it should be the accumulator of the earned interest rate. 

In conclusion, this bug report is about incorrect or misleading comments in the NatSpec code. These comments should be updated to avoid confusion or misleading users.

### Original Finding Content

Since the purpose of the Ethereum Natural Specification (NatSpec) is to describe the code to the user, misleading statements should be considered a violation of the public API that may confuse or mislead users.


The `getBorrowRate` [interface](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/InterestRateModel.sol#L19) and [implementation](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/WhitePaperInterestRateModel.sol#L113) `@return` comments state that the rate is scaled by 10e18. In fact, it is only scaled by 1e18.


The `CToken` contract [`borrowRateMaxMantissa` comment](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/CToken.sol#L38) states that the maximum borrow rate per block is 0.0005% but it is actually 0.0005 ( or 0.05% ).


The comment on [line 7 of `Unitroller.sol`](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/Unitroller.sol#L7-L8) is an incomplete thought/sentence.


The comment on [line 41 of `ComptrollerStorage.sol`](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/ComptrollerStorage.sol#L41) uses the word “discount” when it should use “bonus”, which may cause confusion for people trying to understand the code. For example, a 25% discount is equivalent to a 33% bonus. That is, “25% off” is the same as “33% more for free”.


The comment on [line 6 of `Exponential.sol`](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/Exponential.sol#L6) says “fixed-decision” when it should say “fixed-precision”.


The comment on [line 83 of `CToken.sol`](https://github.com/compound-finance/compound-protocol/blob/f385d71983ae5c5799faae9b2dfea43e5cf75262/contracts/CToken.sol#L83) describes `borrowIndex` as the accumulator of earned interest when it should be the accumulator of the earned interest rate.


Consider updating the comments appropriately.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Compound Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/compound-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

