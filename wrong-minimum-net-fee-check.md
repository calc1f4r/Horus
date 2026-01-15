---
# Core Classification
protocol: CLOBER
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7257
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
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
  - validation

protocol_categories:
  - dexes
  - bridge
  - yield
  - cross_chain
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - Desmond Ho
  - Grmpyninja
  - Christoph Michel
  - Throttle
  - Taek Lee
---

## Vulnerability Title

Wrong minimum net fee check

### Overview


A bug was identified in the MarketFactory.sol code at lines 79 and 111. The issue was that a minimum net fee was introduced that all markets should comply by, but the protocol fees were being calculated incorrectly. This resulted in fee pairs that should be accepted being rejected, and fee pairs that should be rejected being accepted. This allowed market creators to avoid collecting protocol fees.

To fix this bug, a takerFee + makerFee >= minNetFee check was implemented, and the condition was inverted for the use of custom errors. This was fixed in Pull Requests 307, 308, and 311. The bug has now been fixed.

### Original Finding Content

## Severity: High Risk

## Context
- MarketFactory.sol#L79
- MarketFactory.sol#L111

## Description
A minimum net fee was introduced that all markets should comply by such that the protocol earns fees. The protocol fees are computed as `takerFee + makerFee`, but the market factory computes the wrong check. Fee pairs that should be accepted are currently not accepted, and, even worse, fee pairs that should be rejected are currently accepted. Market creators can avoid collecting protocol fees this way.

## Recommendation
Implement a `takerFee + makerFee >= minNetFee` check instead:
```solidity
require(int256(uint256(takerFee)) + makerFee >= minNetFee, Errors.INVALID_FEE);
```

## Clober
Fixed in PR 307, PR 308, and PR 311.

## Spearbit
Fixed. Condition has been inverted for the use of custom errors.
```solidity
if (marketHost != owner && int256(uint256(takerFee)) + makerFee < int256(uint256(minNetFee))) {
    revert Errors.CloberError(Errors.INVALID_FEE);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | CLOBER |
| Report Date | N/A |
| Finders | Desmond Ho, Grmpyninja, Christoph Michel, Throttle, Taek Lee |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Clober-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation`

