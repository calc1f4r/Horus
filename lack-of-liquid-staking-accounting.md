---
# Core Classification
protocol: Cosmos LSM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46743
audit_firm: OtterSec
contest_link: https://cosmos.network/
source_link: https://cosmos.network/
github_link: https://github.com/cosmos/cosmos-sdk

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
finders_count: 3
finders:
  - James Wang
  - Robert Chen
  - Tuyết Dương
---

## Vulnerability Title

Lack of Liquid Staking Accounting

### Overview


The bug report states that there is an issue with the CreateValidator function, which is responsible for setting up a validator in a blockchain network. This function is missing some important bookkeeping steps that are present in the Delegate function. These steps involve checking and updating the staked tokens and shares for liquid staking, which is a process of converting staked tokens into shares in the validator. This results in the global liquid staking cap and the per-validator cap not being updated properly. The solution to this bug is to incorporate the missing bookkeeping steps from the Delegate function into the CreateValidator function. This issue has been fixed in a recent update, specifically in PR#22719. 

### Original Finding Content

## Validator Issues in Liquid Staking

CreateValidator lacks the liquid staking-related bookkeeping present in Delegate. In Delegate, specific checks and updates are performed when the delegation is initiated by a liquid staking provider, converting the staked tokens into an equivalent number of shares in the validator and safely updating the global liquid stake and validator liquid shares. However, no such checks or updates are performed for liquid staking when self-delegating the initial stake during validator creation. As a result, the global liquid staking cap and the per-validator cap will not be updated.

## Remediation

Ensure that the liquid staking bookkeeping logic from Delegate is incorporated into CreateValidator.

## Patch

Fixed in PR#22719.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cosmos LSM |
| Report Date | N/A |
| Finders | James Wang, Robert Chen, Tuyết Dương |

### Source Links

- **Source**: https://cosmos.network/
- **GitHub**: https://github.com/cosmos/cosmos-sdk
- **Contest**: https://cosmos.network/

### Keywords for Search

`vulnerability`

