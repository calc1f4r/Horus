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
solodit_id: 41214
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#2-potential-mismanagement-of-updated-withdrawal-vault-addresses
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

Potential Mismanagement of Updated Withdrawal Vault Addresses

### Overview


The bug report is about an issue found in a function called "\_processWithdrawalProof" in a contract called CSVerifier. The current code checks if the withdrawal address matches a specific address called "WITHDRAWAL_ADDRESS". However, if the withdrawal vault address is changed through a contract upgrade, this check may fail for old deposits, which can cause problems with handling withdrawals and potentially affect users' funds. The severity of the issue is classified as medium and the recommendation is to either track previous withdrawal vault addresses or make sure the code is compatible with changes to the withdrawal vault address.

### Original Finding Content

##### Description
The issue is identified within the function [\_processWithdrawalProof](https://github.com/lidofinance/community-staking-module/blob/a898d045b63303294752d1a60ad9dfe8d8ba69ca/src/CSVerifier.sol#L308-L310) of the contract `CSVerifier`. The current implementation verifies that the `withdrawalAddress` matches `WITHDRAWAL_ADDRESS`. However, if the withdrawal vault address is updated through a contract upgrade, this check may fail for old deposits, leading to incorrect handling of those withdrawal processes.

The issue is classified as **Medium** severity because it can cause inconsistencies in withdrawal processing, potentially affecting users' funds and the contract's reliability.

##### Recommendation
We recommend implementing a mechanism to track historical withdrawal vault addresses or ensuring backward compatibility when updating the withdrawal vault address.

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

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/CSM/README.md#2-potential-mismanagement-of-updated-withdrawal-vault-addresses
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

