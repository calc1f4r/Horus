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
solodit_id: 28413
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Feed/README.md#2-possible-admin-control-loss
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

Possible admin control loss

### Overview


This bug report is about the current version of a protocol, in which an admin can set the address of a new admin to zero. This means that no one can call admin functions after that. To fix this issue, the report recommends adding a simple check to ensure that the new admin address is not set to zero. This check can be implemented by adding the following code to the protocol: `require(newAdmin != 0, "Incorrect admin address");`

### Original Finding Content

##### Description
In the current version of protocol, admin can set address of a new admin to zero, which means that nobody can call admin functions after that:
https://github.com/lidofinance/steth-price-feed/blob/459495f07c97d04f6e3839e7a3b32acfcade22ad/contracts/PriceFeedProxy.sol#L106
https://github.com/lidofinance/steth-price-feed/blob/459495f07c97d04f6e3839e7a3b32acfcade22ad/contracts/StEthPriceFeed.vy#L151
##### Recommendation
We recommend to add simple check:
```solidity=
require(newAdmin != 0, "Incorrect admin address");
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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/stETH%20Price%20Feed/README.md#2-possible-admin-control-loss
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

