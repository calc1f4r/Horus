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
solodit_id: 41249
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#27-possible-multiple-signature-usage-in-depositsecuritymoduledepositbufferedether
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

Possible Multiple Signature Usage in `DepositSecurityModule.depositBufferedEther()`

### Overview

See description below for full details.

### Original Finding Content

##### Description
In certain cases, it is possible to use the same signature to invoke [`DepositSecurityModule.depositBufferedEther()`](https://github.com/lidofinance/core/blob/fafa232a7b3522fdee5600c345b5186b4bcb7ada/contracts/0.8.9/DepositSecurityModule.sol#L494-L523) without a revert more than once. This can happen if the following conditions are met:
1. The amount of buffered ETH in Lido was 0 during the first invocation.
2. The `depositRoot` did not change during the `minDepositBlockDistance` blocks.

`DepositSecurityModule.depositBufferedEther()` is permissionless (in case of the correct set of signatures), so it may be a problem.

##### Recommendation
We recommend reverting the `DepositSecurityModule.depositBufferedEther()` call if there is no buffered ETH at the moment of invocation.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#27-possible-multiple-signature-usage-in-depositsecuritymoduledepositbufferedether
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

