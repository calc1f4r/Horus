---
# Core Classification
protocol: Astera
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62278
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
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
finders_count: 3
finders:
  - Saw-mon and Natalie
  - Cergyk
  - Jonatas Martins
---

## Vulnerability Title

In updateAToken and updateVariableDebtToken of the LendingPoolConfigurator encodedCallis con-

### Overview


This bug report is about a high-risk vulnerability found in the `LendingPoolConfigurator` contract. The vulnerability is located in the `updateAToken` and `updateVariableDebtToken` functions, specifically in the construction of the `encodedCall` variable. This variable is used to update certain parameters in the proxy contracts, but it is missing the `reserveType` parameter. This results in incorrect data being set for `RESERVE_TYPE`, `name`, `symbol`, and `params` in the proxy contracts, which can cause incorrect data to be queried or updated in the lending pool. The recommendation is to add the missing `reserveType` parameter and use `abi.encodeCall` instead of `abi.encodeWithSelector` to avoid potential future mistakes. The bug has been fixed by Astera and verified by Spearbit.

### Original Finding Content

## Vulnerability Report

## Severity
**High Risk**

## Context
- `LendingPoolConfigurator.sol#L173-L183`
- `LendingPoolConfigurator.sol#L206-L215`

## Description
In `updateAToken` and `updateVariableDebtToken` of the `LendingPoolConfigurator`, `encodedCall` is constructed incorrectly:

```solidity
bytes memory encodedCall = abi.encodeWithSelector(
    /*...*/ selector,
    cachedPool,
    // ...
    input.asset,
    input.incentivesController,
    decimals, // <--- `reserveType` is missing after here
    input.name,
    input.symbol,
    input.params
);
```

As a result, `RESERVE_TYPE`, `name`, `symbol`, and `params` will be set incorrectly in the proxy contracts. This will cause all subsequent calls to query or update data for an incorrect reserve in the lending pool:

```solidity
pool.function(_underlyingAsset, RESERVE_TYPE, /*...*/ )
```

## Recommendation
Add the missing `reserveType` parameter and also ensure that instead of using `abi.encodeWithSelector`, `abi.encodeCall` is used to avoid potential future mistakes regarding typos and incorrect parameter types.

## Audit Reports
- **Astera:** Fixed in commit 8bc4648c.
- **Spearbit:** Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Astera |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, Cergyk, Jonatas Martins |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astera-Spearbit-Security-Review-December-2024.pdf

### Keywords for Search

`vulnerability`

