---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40864
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad
source_link: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
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
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Christoph Michel
---

## Vulnerability Title

Cannot use uint256.max to repay the balance of compoundv2migrationbundler 

### Overview


The bug report discusses an issue with the CompoundV2MigrationBundler contract. The contract's natspec for the compoundV2Repay function is unclear about the amount parameter, specifically what "all" refers to. This has led to confusion and errors when trying to use the function. The code also has a bug where it tries to repay the entire borrow balance instead of the bundler's balance, causing the transaction to fail. The recommendation is to always cap the amount to the bundler's balance to avoid this issue. 

### Original Finding Content

## Context: CompoundV2MigrationBundler.sol#L40

## Description
The `compoundV2Repay`'s natspec states the following for the `amount` parameter:  
*The amount of cToken to repay. Pass `type(uint256).max` to repay all (except for cETH).*

It's ambiguous what "all" refers to: the bundler's token balance or the borrow balance. We assume the bundler's balance, as that's the approach taken by the other bundlers. Passing `type(uint256).max` to repay the bundler's cToken balance does not work. Note that if `amount == type(uint256).max`, this value is not adjusted and just forwarded to the `ICToken(cToken).repayBorrowBehalf` call.

CompoundV2 will execute this code:

```solidity
/* We fetch the amount the borrower owes, with accumulated interest */
uint accountBorrowsPrev = borrowBalanceStoredInternal(borrower);

/* If repayAmount == -1, repayAmount = accountBorrows */
uint repayAmountFinal = repayAmount == type(uint).max ? accountBorrowsPrev : repayAmount;
```

This caps the amount to be repaid to the entire borrow balance, not to the bundler's balance. The call will revert as it tries to repay the entire borrow balance with the bundler's balance.

## Example
A user tries to migrate part of their position by trying to repay half of their borrow balance of 1000 assets. The first action in the bundle redeems shares from another protocol to receive the desired repay amount of roughly 500 assets, and the second action is to repay by setting `assets = type(uint256).max` to "repay the bundler's asset balance," as defined by the natspec. The batch will revert as Aave V2 will try to repay the entire borrow balance of 1000 but the bundler only has 500 assets.

## Recommendation
Consider always capping the amount to the bundler's balance. Trying to repay more will never work, and the protocol itself will already cap it to the entire borrow balance:

```solidity
if (amount != type(uint256).max) 
    amount = Math.min(amount, ERC20(underlying).balanceOf(address(this)));
```

```solidity
amount = Math.min(amount, ERC20(underlying).balanceOf(address(this)));
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_morpho_metamorpho_dec2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c8366258-22bd-4e11-a6e9-c39ce06539ad

### Keywords for Search

`vulnerability`

