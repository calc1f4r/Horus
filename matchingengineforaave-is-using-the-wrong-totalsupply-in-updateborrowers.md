---
# Core Classification
protocol: Morpho
chain: everychain
category: logic
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6920
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 4

# Context Tags
tags:
  - wrong_math
  - business_logic

protocol_categories:
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - hack3r-0m
  - Jay Jonah
  - Christoph Michel
  - Emanuele Ricci
---

## Vulnerability Title

MatchingEngineForAave is using the wrong totalSupply in updateBorrowers

### Overview


This bug report is about a critical risk issue that was found in the MatchingEngineForAave.sol code. The issue is that the _poolTokenAddress is referencing the AToken, when it should be referencing the DebtToken. If this is not corrected, the user would be rewarded for a wrong amount. To solve the issue, the correct token address should be used to query the scaledTotalSupply. The recommendation was implemented in the PR #554 and the bug has been fixed.

### Original Finding Content

## Security Risk Assessment

## Severity
**Critical Risk**

## Context
`MatchingEngineForAave.sol#L376-L385`

## Description
The `_poolTokenAddress` is referencing `AToken`, so the `totalStaked` would be the total supply of the `AToken`. In this case, the `totalStaked` should reference the total supply of the `DebtToken`; otherwise, the user would be rewarded for a wrong amount of reward.

## Recommendation
Use the correct token address to query `scaledTotalSupply` as follows:

```solidity
address variableDebtTokenAddress = lendingPool
    .getReserveData(IAToken(_poolTokenAddress).UNDERLYING_ASSET_ADDRESS())
    .variableDebtTokenAddress;

uint256 totalStaked = IScaledBalanceToken(variableDebtTokenAddress).scaledTotalSupply();
```

## Spearbit
Fixed; recommendation was implemented in the PR #554.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | hack3r-0m, Jay Jonah, Christoph Michel, Emanuele Ricci |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Morpho-Spearbit-Security-Review.pdf

### Keywords for Search

`Wrong Math, Business Logic`

