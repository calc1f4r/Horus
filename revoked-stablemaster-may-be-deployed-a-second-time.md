---
# Core Classification
protocol: Angle
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19188
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Revoked StableMaster May be Deployed A Second Time

### Overview

See description below for full details.

### Original Finding Content

## Description
The Core smart contract is able to deploy StableMaster contracts which represent a new stable coin. The Core also has the ability to `revokeStableMaster()`, which essentially disowns a stablecoin.

When a StableMaster contract is revoked it is possible to add the contract back again by calling `deployStableMaster()`. This will call `StableMaster.deploy()` adding the current guardian and governor roles, without removing the previous ones.

## Recommendations
Consider adding a state variable in Core which stores a mapping `address => boolean` as to whether an address has been deployed as a StableMaster or not yet.

## Resolution
In commit `4cd59ce`, a state variable was added to Core, that is, `deployedStableMasterMap`. The variable enables checking whether a StableMaster has been deployed previously or not. The check is conducted on line [114] in function `deployStableMaster()`:

```solidity
require(!deployedStableMasterMap[stableMaster], "stableMaster previously deployed");
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Angle |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/angle/review.pdf

### Keywords for Search

`vulnerability`

