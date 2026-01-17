---
# Core Classification
protocol: Ludex Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52928
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/82ea7f9c-0383-45e9-9630-5863839fa2c5
source_link: https://cdn.cantina.xyz/reports/cantina_riskiit_february2025.pdf
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
finders_count: 2
finders:
  - Cryptara
  - r0bert
---

## Vulnerability Title

Incorrect Liquidity Check in requestToken Could Lead to Insolvency 

### Overview


The contract's requestToken function has a bug that may lead to situations where user payouts cannot be fulfilled. This is because the function does not properly account for the entropyFee, which is used as the value for the callback. As a result, the protocol may allow bets that exceed the actual available balance, causing the contract to become insolvent. This could also result in unintended reverts or discrepancies in fund distribution. To fix this, the liquidity check should be adjusted to exclude entropyFee from the solvency calculation. Ludex Labs has already fixed this issue and Cantina Managed has also confirmed that the fix is acceptable.

### Original Finding Content

## Contract Review

## Context
(No context files were provided by the reviewer)

## Description
The contract's `requestToken` function currently checks liquidity using the condition `totalOnLine + betAmount * _multiplier`, but it does not properly account for the `entropyFee`, which is used as the value for the callback. This creates a misleading assessment of available liquidity since `entropyFee` will be spent in the next transaction and should not be considered part of the contract’s solvency. As a result, the protocol might allow bets that exceed the actual available balance, leading to situations where user payouts cannot be fulfilled. If this happens, the contract may become insolvent, breaking the invariant that the contract balance should always be equal to or greater than `totalOnLine`. In edge cases, this could result in unintended reverts or discrepancies in fund distribution, disrupting the protocol’s integrity.

## Recommendation
The liquidity check should be adjusted to exclude `entropyFee` from the solvency calculation to ensure that the contract always retains enough funds to cover outstanding liabilities. The correct comparison should be:

```
totalOnLine + betAmount * _multiplier > address(this).balance - entropyFee
```

This adjustment will prevent situations where available liquidity is overestimated and keep the protocol solvent.

## Audits
- **Ludex Labs:** Fixed in commit `d37d6ab2`.
- **Cantina Managed:** Fix ok. For ETH bets, the current code explicitly subtracts `entropyFee` in the liquidity check.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Ludex Labs |
| Report Date | N/A |
| Finders | Cryptara, r0bert |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_riskiit_february2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/82ea7f9c-0383-45e9-9630-5863839fa2c5

### Keywords for Search

`vulnerability`

