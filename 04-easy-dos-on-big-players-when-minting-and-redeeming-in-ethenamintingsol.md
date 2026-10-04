---
# Core Classification
protocol: Ethena Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 29391
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-10-ethena
source_link: https://code4rena.com/reports/2023-10-ethena
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

protocol_categories:
  - staking_pool
  - decentralized_stablecoin

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[04] Easy DoS on big players when minting and redeeming in EthenaMinting.sol

### Overview

See description below for full details.

### Original Finding Content

As indicated on the audit description, users intending to mint/redeem a large amount will need to mint/redeem over several blocks due to `maxMintPerBlock` or `maxRedeemPerBlock`. However, these RFQ's are prone to DoS because [`mintedPerBlock[block.number] + mintAmount > maxMintPerBlock`](https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/EthenaMinting.sol#L98) or [`redeemedPerBlock[block.number] + redeemAmount > maxRedeemPerBlock`](https://github.com/code-423n4/2023-10-ethena/blob/main/contracts/EthenaMinting.sol#L105) could revert by only 1 wei in excess.

While these issues could be sorted by the backend to make a full use of `maxMintPerBlock` or `maxRedeemPerBlock` per block, it will make the intended logic a lot more efficient by auto reducing the RFQ amount to perfectly fill up the remaining quota for the current block. Better yet, set up a queue system where request amount running in hundreds of thousands or millions may be auto split up with multiple orders via only one signature for batching.



### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ethena Labs |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2023-10-ethena
- **GitHub**: N/A
- **Contest**: https://code4rena.com/reports/2023-10-ethena

### Keywords for Search

`vulnerability`

