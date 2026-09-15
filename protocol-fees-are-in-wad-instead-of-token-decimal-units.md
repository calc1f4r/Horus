---
# Core Classification
protocol: Primitive
chain: everychain
category: uncategorized
vulnerability_type: decimals

# Attack Vector Details
attack_type: decimals
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18737
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Primitive-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Primitive-Spearbit-Security-Review.pdf
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
  - decimals

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - M4rio.eth
  - Christoph Michel
  - Kurt Barry
  - Sabnock
---

## Vulnerability Title

Protocol fees are in WAD instead of token decimal units

### Overview


This bug report is about a high risk issue found in the Portfolio.sol#L489 code. When swapping, the deltaInput is in WAD (not token decimals) units. This means that the protocolFee will also be in WAD as a percentage of deltaInput. This WAD amount is then credited to the REGISTRY. The privileged registry can claim these fees using a withdrawal (draw) and the WAD units are not scaled back to token decimal units, resulting in withdrawing more fees than they should have received if the token has less than 18 decimals. This will reduce the global reserve by the increased fee amount and break the accounting and functionality of all pools using the token.

The recommendation is to use WAD units everywhere and only convert from/to token decimal units at the "token boundary", directly at the point of interaction with the token contract through a transfer/transferFrom/balanceOf call. The issue was resolved in PR 335 and fixed.

### Original Finding Content

## High Risk Report

## Severity
**High Risk**

## Context
`Portfolio.sol#L489`

## Description
When swapping, `deltaInput` is in WAD (not token decimals) units. Therefore, the `protocolFee` will also be in WAD as a percentage of `deltaInput`. This WAD amount is then credited to the REGISTRY:

```solidity
iteration.feeAmount = (deltaInput * _state.fee) / PERCENTAGE;
if (_protocolFee != 0) {
    uint256 protocolFeeAmount = iteration.feeAmount / _protocolFee;
    iteration.feeAmount -= protocolFeeAmount;
    _applyCredit(REGISTRY, _state.tokenInput, protocolFeeAmount);
}
```

The privileged registry can claim these fees using a withdrawal (draw) and the WAD units are not scaled back to token decimal units, resulting in withdrawing more fees than they should have received if the token has less than 18 decimals. This will reduce the global reserve by the increased fee amount and break the accounting and functionality of all pools using the token.

## Recommendation
Generally, some quantities are in WAD units and some in token decimals throughout the protocol. We recommend using WAD units everywhere and only converting from/to token decimal units at the "token boundary", directly at the point of interaction with the token contract through a `transfer` / `transferFrom` / `balanceOf` call.

## Primitive
Resolved in PR 335.

## Spearbit
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Primitive |
| Report Date | N/A |
| Finders | M4rio.eth, Christoph Michel, Kurt Barry, Sabnock |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Primitive-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Primitive-Spearbit-Security-Review.pdf

### Keywords for Search

`Decimals`

