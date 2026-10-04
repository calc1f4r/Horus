---
# Core Classification
protocol: Blueberry_2025-04-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61483
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-04-30.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] Small Amounts Burned When Bridging to L1

### Overview


The reported bug involves the bridgeToL1() function which transfers tokens from an escrow to a system address on the EVM to initiate a bridge to L1. However, if the EVM-side token has more decimal precision than expected, non-round values will result in burned tokens. This is a known issue and is due to how logs are parsed and how L1 crediting works. The recommended solution is to round down the amount before sending it to avoid permanent token loss.

### Original Finding Content


## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The bridgeToL1() function transfers tokens from the escrow to a system address on the EVM to initiate a bridge to L1. However, if the EVM-side token has extra decimal precision (i.e., more than the expected extraEvmWeiDecimals), non-round values (not divisible cleanly by 10**extraEvmWeiDecimals) will result in burned tokens. 
This behavior is noted in the protocol's caveats and is systemic to how logs are parsed and how L1 crediting works. However, the bridge logic does not pre-adjust or sanitize these amounts. This leads to permanent token loss.


## Recommendations

Before sending, round down the amount like this:
```solidity
uint256 factor = 10 ** details.extraEvmWeiDecimals;
amounts[i] = amounts[i] - (amounts[i] % factor); IERC20(details.evmContract).transfer(_assetSystemAddr(assetIndexes[i]), amounts[i]);

```





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Blueberry_2025-04-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Blueberry-security-review_2025-04-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

