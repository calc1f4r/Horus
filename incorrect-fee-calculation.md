---
# Core Classification
protocol: MetaLeX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37848
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/LeXscrow/README.md#4-incorrect-fee-calculation
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Incorrect fee calculation

### Overview


The report discusses a potential issue with rounding errors in a specific line of code. This error may occur if a token's decimals are significantly less than 18, resulting in the fee being calculated incorrectly. The report suggests using basis points for fee calculation instead of token decimals to improve precision. 

### Original Finding Content

##### Description
A potential rounding error exists at the [specified line](https://github.com/MetaLex-Tech/LeXscrow/blob/94ca277528bb25b8421dc127941c18915144eb29/src/TokenLexscrowFactory.sol#L117). The `_feeDenominatorAdjusted` may round down to 0 if a token's `_decimals` are significantly less than 18, leading to the ONE constant being used as `_feeDenominatorAdjusted`. This results in the fee equating to `_totalAmount` at the [next line](https://github.com/MetaLex-Tech/LeXscrow/blob/94ca277528bb25b8421dc127941c18915144eb29/src/TokenLexscrowFactory.sol#L123) Conversely, if `_decimals` exceed 18, `_feeDenominatorAdjusted` does not accurately represent a fraction of `_totalAmount`, resulting in a lower-than-expected `_fee`. Additionally, tokens with decimals = 0 will encounter a similar issue, as `_feeDenominatorAdjusted` will not reflect the correct proportion of `_totalAmount`.

##### Recommendation
We recommend introducing basis points as the denominator for fee calculation and specifying the desired share of `_totalAmount` as the numerator. The fee calculation would then be: 
```
_fee = _totalAmount * _fee_share / BASIS_POINTS;
```
It will lead to increased precision during the fee calculation.
We also recommend not using token decimals in the fee calculation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | MetaLeX |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/MetaLeX/LeXscrow/README.md#4-incorrect-fee-calculation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

