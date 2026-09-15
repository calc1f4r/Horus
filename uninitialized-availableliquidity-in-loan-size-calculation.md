---
# Core Classification
protocol: AAVE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28714
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/AAVE/protocol%20v2/README.md#uninitialized-availableliquidity-in-loan-size-calculation
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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Uninitialized `availableLiquidity` in Loan Size Calculation.

### Overview


This bug report concerns the ValidationLogic.sol file in the Aave Protocol V2. It states that the `vars.availableLiquidity` field is not initialized before usage, which could lead to incorrect calculations. The recommendation is to add proper initialization to the code. This bug report is important as it could lead to incorrect calculations, which could have a negative impact on the Aave Protocol V2.

### Original Finding Content

##### Description

https://github.com/aave/protocol-v2/blob/f435b2fa0ac589852ca3dd6ae2b0fbfbc7079d54/contracts/libraries/logic/ValidationLogic.sol#L200

The `vars.availableLiquidity` field is not initialized before usage.

```solidity
//calculate the max available loan size in stable rate mode as a percentage of the
//available liquidity
uint256 maxLoanSizeStable = vars.availableLiquidity.percentMul(maxStableLoanPercent);
```
##### Recommendation
Proper initialization should be added.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | AAVE |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/AAVE/protocol%20v2/README.md#uninitialized-availableliquidity-in-loan-size-calculation
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

