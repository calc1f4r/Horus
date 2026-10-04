---
# Core Classification
protocol: Mochi
chain: everychain
category: economic
vulnerability_type: front-running

# Attack Vector Details
attack_type: front-running
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 934
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-mochi-contest
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/92

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:
  - front-running

protocol_categories:
  - dexes
  - cdp
  - cross_chain
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - leastwood
---

## Vulnerability Title

[H-13] Tokens Can Be Stolen By Frontrunning VestedRewardPool.vest() and VestedRewardPool.lock()

### Overview


A bug has been discovered in the `VestedRewardPool.sol` contract of the Mochi project. This contract is used to vest tokens for a minimum of 90 days before allowing the recipient to withdraw their `mochi`. The `vest()` and `lock()` functions do not utilize `safeTransferFrom()` to ensure that vested tokens are correctly allocated to the recipient, making it possible to frontrun a call to `vest()` and effectively steal a recipient's vested tokens. This has been confirmed with manual code review and discussions with the Mochi team. To mitigate this issue, it is recommended that users understand that this function should not be interacted directly as this could result in lost `mochi` tokens. Additionally, it might be worthwhile creating a single externally facing function which calls `safeTransferFrom()`, `vest()` and `lock()` in a single transaction.

### Original Finding Content

## Handle

leastwood


## Vulnerability details

## Impact

The `VestedRewardPool.sol` contract is a public facing contract aimed at vesting tokens for a minimum of 90 days before allowing the recipient to withdraw their `mochi`. The `vest()` function does not utilise `safeTransferFrom()` to ensure that vested tokens are correctly allocated to the recipient. As a result, it is possible to frontrun a call to `vest()` and effectively steal a recipient's vested tokens. The same issue applies to the `lock()` function.

## Proof of Concept

https://github.com/code-423n4/2021-10-mochi/blob/main/projects/mochi-core/contracts/emission/VestedRewardPool.sol#L36-L46
https://github.com/code-423n4/2021-10-mochi/blob/main/projects/mochi-core/contracts/emission/VestedRewardPool.sol#L54-L64

## Tools Used

Manual code review
Discussions with the Mochi team

## Recommended Mitigation Steps

Ensure that users understand that this function should not be interacted directly as this could result in lost `mochi` tokens. Additionally, it might be worthwhile creating a single externally facing function which calls `safeTransferFrom()`, `vest()` and `lock()` in a single transaction.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | leastwood |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/92
- **Contest**: https://code4rena.com/contests/2021-10-mochi-contest

### Keywords for Search

`Front-Running`

