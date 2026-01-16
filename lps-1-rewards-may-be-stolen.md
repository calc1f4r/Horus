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
solodit_id: 26754
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2023-05-01-Key Finance.md
github_link: none

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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Guardian Audits
---

## Vulnerability Title

LPS-1 | Rewards May Be Stolen

### Overview


This bug report concerns the `uniswapV3Staker` and `LPStaker` contracts. These contracts are used to stake tokens and earn rewards. The bug was that any arbitrary address could call the `unstakeToken` function and unstake for any depositor after the incentive key `endTime`. This meant that malicious stakers could unstake for other stakers and immediately claim their rewards as their own. 

The team recommended that a modified version of the `uniswapV3Staker` be used where the depositor must always be the one to unstake. Alternatively, they suggested managing incentive keys carefully and not allowing any to reach their `endTime` while users had staked for them. 

The team implemented a modified version of the `uniswapV3Staker` to resolve the issue. This should ensure that only the depositor can unstake tokens and prevent malicious stakers from claiming rewards that do not belong to them.

### Original Finding Content

**Description**

The `uniswapV3Staker` contract which the `LPStaker` interacts with allows any arbitrary address to directly call the `unstakeToken` function and unstake for any depositor after the incentive key `endTime`.
When a deposit is unstaked from an incentive key directly from the `uniswapV3Staker`, those rewards will be incremented for the `LPStaker` contract, but not credited towards the user who staked. Therefore malicious stakers may unstake for other stakers and immediately claim their rewards as their own by unstaking through the `LPStaker` contract.

**Recommendation**

Consider using a modified version of the `uniswapV3Staker` where the depositor must always be the one to unstake. Otherwise be sure to manage the incentive keys extremely carefully and never allow an incentive key to reach its `endTime` while users have staked for it.

**Resolution**

Key Team: A modified version of the `uniswapV3Staker` was implemented.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

