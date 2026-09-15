---
# Core Classification
protocol: UMA DVM 2.0 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10454
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uma-dvm-2-0-audit/
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
  - dexes
  - bridge
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Imprecise function name

### Overview

See description below for full details.

### Original Finding Content

In the `DesignatedVotingV2` contract, the [`retrieveRewards`](https://github.com/UMAprotocol/protocol/blob/7938617bf79854811959eb605237edf6bdccbc90/packages/core/contracts/oracle/implementation/DesignatedVotingV2.sol#L109) function name suggests that the caller will gain possession of the rewards; this assumption is further reinforced by the docstring’s [description of the return value](https://github.com/UMAprotocol/protocol/blob/7938617bf79854811959eb605237edf6bdccbc90/packages/core/contracts/oracle/implementation/DesignatedVotingV2.sol#L107) as “amount of rewards that the user should receive”. However, instead of transferring rewards to the user, the `retrieveRewards` function restakes user’s rewards.


To avoid confusion, consider renaming the `retrieveRewards` function to `withdrawAndRestakeRewards` or some other name that more accurately describes its behavior.


**Update:** *Fixed as of commit [`284c6842ed05b13cfdc82cb3b5dd897507696e8f`](https://github.com/UMAprotocol/protocol/pull/4071/commits/284c6842ed05b13cfdc82cb3b5dd897507696e8f) in [pull request #4071](https://github.com/UMAprotocol/protocol/pull/4071).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UMA DVM 2.0 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uma-dvm-2-0-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

