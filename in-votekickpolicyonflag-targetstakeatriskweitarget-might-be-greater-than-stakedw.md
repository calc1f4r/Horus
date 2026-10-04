---
# Core Classification
protocol: Streamr
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27153
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
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
  - Hans
---

## Vulnerability Title

In `VoteKickPolicy.onFlag()`, `targetStakeAtRiskWei[target]` might be greater than `stakedWei[target]` and `_endVote()` would revert.

### Overview


This bug report is about `targetStakeAtRiskWei[target]` in `onFlag()` which might be greater than `stakedWei[target]`, causing an underflow during reward distribution. This could happen when `streamrConfig.minimumStakeWei()` is increased after a reconfiguration and the target has staked less than the new minimum stake. The impact of this bug is that operators with small staked funds wouldn't be kicked forever.

The recommended mitigation for this bug is to check if a target has staked enough funds for rewards and handle it separately if not. The client has fixed this bug in commit [05d9716](https://github.com/streamr-dev/network-contracts/commit/05d9716b8e19668fea70959327ab8e896ab0645d). Flag targets with not enough stake (to pay for the review) will be kicked out without review. Since this can only happen after the admin changes the minimum stake requirement, the flag target is not at fault and will not be slashed. They can stake back again with the new minimum stake if they want. The bug has been verified by Cyfrin.

### Original Finding Content

**Severity:** Medium

**Description:** `targetStakeAtRiskWei[target]` might be greater than `stakedWei[target]` in `onFlag()`.

```solidity
targetStakeAtRiskWei[target] = max(stakedWei[target], streamrConfig.minimumStakeWei()) * streamrConfig.slashingFraction() / 1 ether;
```

For example,
- At the first time, `streamrConfig.minimumStakeWei() = 100` and an operator(=target) has staked 100.
- `streamrConfig.minimumStakeWei()` was increased to 2000 after a reconfiguration.
- `onFlag()` is called for target and `targetStakeAtRiskWei[target]` will be `max(100, 2000) * 10% = 200`.
- In `_endVote()`, `slashingWei = _kick(target, slashingWei)` will be 100 because target has staked 100 only.
- So it will revert due to underflow during the reward distribution.

**Impact:** Operators with small staked funds wouldn't be kicked forever.

**Recommended Mitigation:** `onFlag()` should check if a target has staked enough funds for rewards and handle separately if not.

**Client:** Fixed in commit [05d9716](https://github.com/streamr-dev/network-contracts/commit/05d9716b8e19668fea70959327ab8e896ab0645d). Flag targets with not enough stake (to pay for the review) will be kicked out without review. Since this can only happen after the admin changes the minimum stake requirement (e.g. by increasing reviewer rewards), the flag target is not at fault and will not be slashed. They can stake back again with the new minimum stake if they want.

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Streamr |
| Report Date | N/A |
| Finders | Hans |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-03-cyfrin-streamr.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

