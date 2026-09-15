---
# Core Classification
protocol: Covalent
chain: everychain
category: uncategorized
vulnerability_type: don't_update_state

# Attack Vector Details
attack_type: don't_update_state
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 913
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-covalent-contest
source_link: https://code4rena.com/reports/2021-10-covalent
github_link: https://github.com/code-423n4/2021-10-covalent-findings/issues/57

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 4

# Context Tags
tags:
  - don't_update_state

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[H-02] unstake should update exchange rates first

### Overview


This bug report is about the `unstake` function in a software which does not immediately update the exchange rates when called. This means that when a user stakes an amount of tokens, the exchange rate is calculated using the old exchange rate. As a result, when the user unstakes, more shares are burned than required and the user loses rewards. A proof of concept was included to demonstrate the impact of this bug. The recommended mitigation step is to move the `updateGlobalExchangeRate()` and `updateValidator(v)` calls to the beginning of the function.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

The `unstake` function does not immediately update the exchange rates. It first computes the `validatorSharesRemove = tokensToShares(amount, v.exchangeRate)` **with the old exchange rate**.

Only afterwards, it updates the exchange rates (if the validator is not disabled):

```solidity
// @audit shares are computed here with old rate
uint128 validatorSharesRemove = tokensToShares(amount, v.exchangeRate);
require(validatorSharesRemove > 0, "Unstake amount is too small");

if (v.disabledEpoch == 0) {
    // @audit rates are updated here
    updateGlobalExchangeRate();
    updateValidator(v);
    // ...
}
```

## Impact
More shares for the amount are burned than required and users will lose rewards in the end.

## POC
Demonstrating that users will lose rewards:

1. Assume someone staked `1000 amount` and received `1000 shares`, and `v.exchangeRate = 1.0`. (This user is the single staker)
2. Several epochs pass, interest accrues, and `1000 tokens` accrue for the validator, `tokensGivenToValidator = 1000`. User should be entitled to 1000 in principal + 1000 in rewards = 2000 tokens.
3. But user calls `unstake(1000)`, which sets `validatorSharesRemove = tokensToShares(amount, v.exchangeRate) = 1000 / 1.0 = 1000`. **Afterwards**, the exchange rate is updated: `v.exchangeRate += tokensGivenToValidator / totalShares = 1.0 + 1.0 = 2.0`. The staker is updated with `s.shares -= validatorSharesRemove = 0` and `s.staked -= amount = 0`. And the user receives their 1000 tokens but notice how the user's shares are now at zero as well.
4. User tries to claim rewards calling `redeemAllRewards` which fails as the `rewards` are 0.

If the user had first called `redeemAllRewards` and `unstake` afterwards they'd have received their 2000 tokens.

## Recommended Mitigation Steps
The exchange rates always need to be updated first before doing anything.
Move the `updateGlobalExchangeRate()` and `updateValidator(v)` calls to the beginning of the function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 4/5 |
| Audit Firm | Code4rena |
| Protocol | Covalent |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-covalent
- **GitHub**: https://github.com/code-423n4/2021-10-covalent-findings/issues/57
- **Contest**: https://code4rena.com/contests/2021-10-covalent-contest

### Keywords for Search

`Don't update state`

