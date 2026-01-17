---
# Core Classification
protocol: DeFi Money
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33565
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DeFi%20Money/Core/README.md#2-stablecoin-separate-ownership
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

Stablecoin separate ownership

### Overview

See description below for full details.

### Original Finding Content

##### Description
Generally, each system contract follows the pattern indicating the Core contract on deployment.
E.g. `MainController`:
- https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/MainController.vy#L280

As a result, a single system owner is stored on the `Core` contract allowing transferring the ownership of the whole system only on `Core`.

But this is not the case for `StableCoin` - it inherits from `Ownable`, so that a separate owner address is stored on the smart contract.
- https://github.com/defidotmoney/dfm-core/blob/e22732083f79a5fb13bdb69132622017ebe79a59/contracts/testing/StableCoin.sol#L14

Thus, there are two owners within the system. They are the same address on deployment.
But they can become different in case of the ownership transfer.

##### Recommendation
We recommend following the pattern with `Core` for `StableCoin`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DeFi Money |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DeFi%20Money/Core/README.md#2-stablecoin-separate-ownership
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

