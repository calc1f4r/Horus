---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28446
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Oracle/README.md#2-possible-zero-price-for-token
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

Possible zero price for token

### Overview


A bug has been identified in the new version of the Oracle Smart Contract. The price for stETH is set to 0 until the user calls the `submitState` function. To fix this issue, it is recommended to add a check to the code requiring that the stETH price be greater than 0. This can be done by adding the following line of code: `require(stethPrice > 0, "PRICE_NOT_INITIALIZED");`.

### Original Finding Content

##### Description
In the new version of the oracle smart contract, the price for stETH = 0 until user calls the `submitState` function:
https://github.com/lidofinance/curve-merkle-oracle/blob/ae093b308999a564ed3f23d52c6c5dce946dbfa7/contracts/StableSwapStateOracle.sol#L268

##### Recommendation
We recommend to add following check:
```solidity=
require(stethPrice > 0, "PRICE_NOT_INITIALIZED");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Oracle/README.md#2-possible-zero-price-for-token
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

