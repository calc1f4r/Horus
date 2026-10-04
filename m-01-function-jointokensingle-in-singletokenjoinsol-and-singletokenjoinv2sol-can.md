---
# Core Classification
protocol: Amun
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6523
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-amun-contest
source_link: https://code4rena.com/reports/2021-12-amun
github_link: https://github.com/code-423n4/2021-12-amun-findings/issues/81

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 7
finders:
  - pmerkleplant
  - certora
  - pauliax
  - robee
  - WatchPug
---

## Vulnerability Title

[M-01] Function joinTokenSingle in SingleTokenJoin.sol and SingleTokenJoinV2.sol can be made to fail

### Overview


A vulnerability has been identified in the function `joinTokenSingle` in `SingleTokenJoin.sol` and `SingleTokenJoinV2.sol` which allows users to perform a griefing attack. This attack causes any user transaction to fail with the message “FAILED_OUTPUT_AMOUNT”. The issue arises from the fact that the `JoinTokenStruct` argument for `joinTokenSingle` includes a field `outputAmount` to indicate the amount of tokens the user should receive after joining a basket, but this amount is compared to the contract's balance of the token and reverts if the amount is unequal. If an attacker sends some amount of a basket's token to the contract, every call to this function will fail as long as the output token equals the attacker's token send. The recommended mitigation steps for this vulnerability are to refactor the `require` statement to expect at least the `outputAmount` of tokens, i.e. `require(outputAmount >= _joinTokenStruct.outputAmount)`.

### Original Finding Content

## Handle

pmerkleplant


## Vulnerability details

## Impact

There's a griefing attack vulnerability in the function `joinTokenSingle` in 
`SingleTokenJoin.sol` as well as `SingleTokenJoinV2.sol` which makes any user
transaction fail with "FAILED_OUTPUT_AMOUNT".

### Proof of Concept

The `JoinTokenStruct` argument for `joinTokenSingle` includes a field `outputAmount`
to indicate the amount of tokens the user should receive after joining a basket
(see line [135](https://github.com/code-423n4/2021-12-amun/blob/main/contracts/basket/contracts/singleJoinExit/SingleTokenJoin.sol#L135) and [130](https://github.com/code-423n4/2021-12-amun/blob/main/contracts/basket/contracts/singleJoinExit/SingleTokenJoinV2.sol#L130)).

However, this amount is compared to the contract's balance of the token and
reverts if the amount is unequal.

If an attacker sends some amount of a basket's token to the contract, every call
to this function will fail as long as the output token equals the attacker's token send.

## Recommended Mitigation Steps

Refactor the `require` statement to expect at least the `outputAmount` of tokens,
i.e. `require(outputAmount >= _joinTokenStruct.outputAmount)`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Amun |
| Report Date | N/A |
| Finders | pmerkleplant, certora, pauliax, robee, WatchPug, hyh, p4st13r4 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-amun
- **GitHub**: https://github.com/code-423n4/2021-12-amun-findings/issues/81
- **Contest**: https://code4rena.com/contests/2021-12-amun-contest

### Keywords for Search

`vulnerability`

