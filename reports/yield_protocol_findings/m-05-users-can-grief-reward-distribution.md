---
# Core Classification
protocol: Aura Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25014
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-05-aura
source_link: https://code4rena.com/reports/2022-05-aura
github_link: https://github.com/code-423n4/2022-05-aura-findings/issues/180

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

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-05] Users can grief reward distribution

### Overview


This bug report is about a vulnerability in the ExtraRewardsDistributor.sol contract, which is part of the Aura Finance system. The bug allows users to grief reward distributions by spending dust. This is done by targeting rewards for an epoch in the past and then front-running the transaction in the mempool. This would cause the transaction in the mempool to revert due to the code in line 74 of the ExtraRewardsDistributor.sol contract.

The recommended mitigation steps proposed are to allow backdating of rewards, which will cost more gas. This was acknowledged by 0xMaharishi (Aura Finance) but they disagreed with the severity of the bug. They resolved the issue by applying fixes to the code-423n4/2022-05-aura#6 and aurafinance/aura-contracts#84 pull requests.

### Original Finding Content

_Submitted by IllIllI_

Users can grief reward distributions by spending dust.

### Proof of Concept

If a reward is targeted for an epoch in the past, a user can front-run the txn in the mempool and call `addRewardToEpoch()` with a dust amount at an epoch after the one in question. This will cause the transaction in the mempool to revert

```solidity
File: contracts/ExtraRewardsDistributor.sol   #1

74               require(len == 0 || rewardEpochs[_token][len - 1] < _epoch, "Cannot backdate to this epoch");
```

[ExtraRewardsDistributor.sol#L74](https://github.com/code-423n4/2022-05-aura/blob/4989a2077546a5394e3650bf3c224669a0f7e690/contracts/ExtraRewardsDistributor.sol#L74)

### Recommended Mitigation Steps

Allow the backdating of rewards, which will cost more gas

**[0xMaharishi (Aura Finance) acknowledged, but disagreed with severity and commented](https://github.com/code-423n4/2022-05-aura-findings/issues/180#issuecomment-1139658412):**
 > Fair finding; however, this is a peripheral contract and only affects user reward claiming. In the Aura system, rewards are only added to the current epoch so should be fine.

**[0xMaharishi (Aura Finance) resolved](https://github.com/code-423n4/2022-05-aura-findings/issues/180):**
 > [All code4rena fixes code-423n4/2022-05-aura#6](https://github.com/code-423n4/2022-05-aura/pull/6)<br>
 > [code4rena aurafinance/aura-contracts#84](https://github.com/aurafinance/aura-contracts/pull/84)



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Aura Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-05-aura
- **GitHub**: https://github.com/code-423n4/2022-05-aura-findings/issues/180
- **Contest**: https://code4rena.com/reports/2022-05-aura

### Keywords for Search

`vulnerability`

