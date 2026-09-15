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
solodit_id: 33850
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#1-rounding-errors
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

Rounding errors

### Overview


This bug report explains that due to rounding errors, users will always have a small amount of leftover tokens when converting from stETH to wstETH. To fix this, the report recommends adding a new method that allows users to convert their stETH shares into wstETH shares.

### Original Finding Content

##### Description
Due to rounding errors users will always retain some dust on L2 https://github.com/lidofinance/lido-l2-with-steth/blob/792071cdeaf61de927cc144e8c1c02d5f5996a01/contracts/token/ERC20RebasableBridged.sol#L86-L94. This problem can be mitigated by adding a method that allows users to unwrap stETH shares into wstETH shares.

##### Recommendation
We recommend adding a method that allows users to unwrap stETH shares into wstETH shares.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20on%20Optimism/README.md#1-rounding-errors
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

