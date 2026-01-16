---
# Core Classification
protocol: Key Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 26764
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2023-05-01-Key Finance.md
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
  - Guardian Audits
---

## Vulnerability Title

LPS-3 | Fee-On-Transfer Tokens

### Overview


This bug report concerns the `LPStaker` contract, which is not compatible with fee-on-transfer tokens for the `rewardToken`. This is because the `uint` returned from the `uniswapV3Staker` `claimReward` function is used to increment the reward mapping, but fee-on-transfer tokens will cause this returned value to be inaccurate, potentially leaving users unable to claim their rewards and potentially locked in the contract. It is also noted that rebase tokens or other balance altering tokens will not be accurately accounted for in a similar way.

The recommendation is to consider if fee-on-transfer, rebase, or any similar tokens should be supported. If so, before and after balance checks for the `claimReward` function should be added to measure the reward claimed accurately.

The resolution is that the `rewardToken` will never be a fee-on-transfer token.

### Original Finding Content

**Description**

The `LPStaker` contract is not compatible with fee-on-transfer tokens for the `rewardToken` as it relies on the `uint` returned from the `uniswapV3Staker` `claimReward` function to increment the reward mapping.
Fee on transfer tokens will cause this returned value to be inaccurate and potentially leave users unable to claim their rewards and potentially locked in the contract.
It should also be noted that rebase tokens or other balance altering tokens will not be accurately accounted for in a similar way.

**Recommendation**

Consider if fee-on-transfer, rebase, or any similar tokens should be supported. If so, add before and after balance checks for the `claimReward` function to measure the reward claimed accurately.

**Resolution**

Key Team: The `rewardToken` will never be a fee-on-transfer token.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Guardian Audits |
| Protocol | Key Finance |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2023-05-01-Key Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

