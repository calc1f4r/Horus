---
# Core Classification
protocol: Sudoswap LSSVM2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18294
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
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
finders_count: 5
finders:
  - Gerard Persoon
  - Shodan
  - Rajeev
  - Lucas Goiriz
  - David Chaparro
---

## Vulnerability Title

Pair may receive less ETH trade fees than expected under certain conditions

### Overview


This bug report is about a medium risk issue in the LSSVMPairETH.sol code. The issue is that depending on the values of protocol fee and royalties, if _feeRecipient == _assetRecipient, the pair will receive less trade fees than expected. For example, if the inputAmount is 100, protocolFee is 30, royaltyTotal is 60, and tradeFeeAmount is 20, the pair will receive only 10 trade fees instead of the expected 20. 

Sudorandom Labs proposed a solution in PR#59 which was then verified by Spearbit. The proposed solution was to only skip the transfer of trade fees when _feeRecipient == _assetRecipient but allow the subtraction to revert on any underflows. This solution should fix the problem and result in the expected trade fees being received.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
LSSVMPairETH.sol#L48-L55

## Description
Depending on the values of protocol fee and royalties, if `_feeRecipient == _assetRecipient`, the pair will receive less trade fees than expected.

Assume a scenario where:
- `inputAmount == 100`
- `protocolFee == 30`
- `royaltyTotal == 60`
- `tradeFeeAmount == 20`

This will result in a revert because of underflow in `saleAmount -= tradeFeeAmount;` when `_feeRecipient != _assetRecipient`. However, when `_feeRecipient == _assetRecipient`, the pair will receive trade fees of `100 - 30 - 60 = 10`, whereas it normally would have expected `20`.

## Recommendation
One option is to only skip the transfer of trade fees when `_feeRecipient == _assetRecipient` but allow the subtraction to revert on any underflows.

## Additional Information
**Sudorandom Labs:** Solved in PR#59.  
**Spearbit:** Verified that this is fixed by PR#59.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Sudoswap LSSVM2 |
| Report Date | N/A |
| Finders | Gerard Persoon, Shodan, Rajeev, Lucas Goiriz, David Chaparro |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/SudoswapLSSVM2-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

