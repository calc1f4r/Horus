---
# Core Classification
protocol: Fantium
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28065
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Fantium/Fantium/README.md#13-use-general-safetransferfrom
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

Use general safeTransferFrom

### Overview


This bug report is about the commit e79ed7dddabc482c56f7828bd9a8725fbbeca2f5 of the FantiumNFTV1 smart contract. It is required to check the success of the transfer at the lines 372 and 380 of the contract. The recommendation is to always use the `safeTransferFrom()` function when sending tokens. This is an important bug report to take into account when dealing with smart contracts.

### Original Finding Content

##### Description

In commit e79ed7dddabc482c56f7828bd9a8725fbbeca2f5, it is required to check the success of the transfer at the following lines:
- https://github.com/metaxu-art/fantium-smart-contracts/blob/e79ed7dddabc482c56f7828bd9a8725fbbeca2f5/contracts/FantiumNFTV1.sol#L372
- https://github.com/metaxu-art/fantium-smart-contracts/blob/e79ed7dddabc482c56f7828bd9a8725fbbeca2f5/contracts/FantiumNFTV1.sol#L380.

##### Recommendation

It is recommended to always use the `safeTransferFrom()` function when sending tokens.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Fantium |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Fantium/Fantium/README.md#13-use-general-safetransferfrom
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

