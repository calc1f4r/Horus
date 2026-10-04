---
# Core Classification
protocol: Convex Platform
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28498
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Convex%20Platform/README.md#1-inconsistent-minted-and-deposited-lp-tokens-amount
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

Inconsistent minted and deposited LP tokens amount

### Overview


A bug has been reported in the `Booster` function, defined at the given link, that affects the amount of tokens that are minted for users. The `deposit` function accepts an `_amount` of LP tokens, however the amount of tokens actually deposited to the gauge may not be the same as the amount of LP tokens deposited to the `Booster` contract. This is due to the fact that someone may have sent LP tokens directly to the `Booster` contract before the user deposits. To fix this issue, it is recommended that the actual deposited `_amount` be passed to the `sendTokensToGauge` function and used as the amount of tokens for depositing to the gauge.

### Original Finding Content

##### Description
Function `deposit` in `Booster` defined at https://github.com/convex-eth/platform/blob/754d9e700693246275b613e895b4044b63ce9ed5/contracts/contracts/Booster.sol#L275 allows to deposit curve pools LP token and mint wrapped convex tokens with 1:1 proportions. However minted tokens amount for user can be different from deposited LP tokens amount:
 - At line https://github.com/convex-eth/platform/blob/754d9e700693246275b613e895b4044b63ce9ed5/contracts/contracts/Booster.sol#L278 contract accepts `_amount` LP tokens 
 - At line https://github.com/convex-eth/platform/blob/754d9e700693246275b613e895b4044b63ce9ed5/contracts/contracts/Booster.sol#L265 contract deposit `bal` tokens to gauge
 - `bal != _amount` if before user deposit someone send LP token directly to `Booster` contract, so here we got that amount of deposited tokens to gauge not equal to LP tokens amount deposited to `Booster`

##### Recommendation
We recommend to pass actual deposited `_amount` to `sendTokensToGauge` function and use it as amount of tokens for depositing to gauge.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Convex Platform |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Convex%20Platform/README.md#1-inconsistent-minted-and-deposited-lp-tokens-amount
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

