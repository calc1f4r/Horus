---
# Core Classification
protocol: P2P.org
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43424
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/P2P.org/ETH%20Allocation%20Share/README.md#2-missing-zero-address-check
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

Missing Zero Address Check

### Overview

See description below for full details.

### Original Finding Content

##### Description
This issue has been identified within the `recoverEther` function of the `MerkleAirdrop` contract.
The function [does not check](https://github.com/p2p-org/eth-merkle-drop/blob/dd05a846fc427b92b9fd60c8aeed990b16270286/src/MerkleAirdrop.sol#L49-L52) whether the `_recipient` address is a zero address before attempting to transfer the contract's balance. This could result in the loss of funds if a zero address is mistakenly passed as the recipient.

The issue is classified as **Low** severity because in rare cases it can lead to funds loss.

##### Recommendation
We recommend adding a check to ensure that `_recipient` is not a zero address before transferring the balance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | P2P.org |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/P2P.org/ETH%20Allocation%20Share/README.md#2-missing-zero-address-check
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

