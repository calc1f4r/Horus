---
# Core Classification
protocol: Vibe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27843
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Vibe/README.md#13-missing-zero-address-and-zero-total-checks-in-claimearnings
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

Missing zero address and zero total checks in `claimEarnings`

### Overview

See description below for full details.

### Original Finding Content

##### Description
There is a `claimEarnings` function here - https://github.com/vibexyz/vibe-contract/blob/d08057edbaf83b00d94dcaca2a05e3c44a45e4d9/contracts/mint/MintSaleBase.sol#LL88C14-L88C27. It accepts the `proceedRecipient` address as a parameter and uses the `total` variable which represents the contract balance in pre-defined `paymentToken`. In cases when the `total` is zero ,`claimEarnings` call would still be completed. Also, it is possible to transfer funds to a zero address. 

##### Recommendation
We recommend adding checks that `proceedRecipient` is not a zero address and `total` is not equal to zero.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Vibe |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Vibe/README.md#13-missing-zero-address-and-zero-total-checks-in-claimearnings
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

