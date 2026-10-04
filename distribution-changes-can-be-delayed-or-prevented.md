---
# Core Classification
protocol: Radiant Riz Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35163
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/radiant-riz-audit
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
  - OpenZeppelin
---

## Vulnerability Title

Distribution Changes Can Be Delayed or Prevented

### Overview


The `YRizStrategy.sol` file has a function called `setFullPoolDistribution` that allows for new "distributions" to be set up for the strategy. However, a bug has been found where pools with a balance cannot be removed from the distribution set. This means that a bad actor can prevent changes to the distribution set by front-running the function with a transfer of tokens from a pool that is being removed. This can have negative effects, such as keeping interest rates low or high for certain pools. The bug has been fixed in a recent update.

### Original Finding Content

Within `YRizStrategy.sol`, the [`setFullPoolDistribution` function](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/vaults/YRizStrategy.sol#L133) allows a new set of "distributions" to be set up for the strategy. Old distributions can be removed and new distributions can be added. Inside the [`_checkPoolsWithBalanceAreIncluded` function](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/vaults/YRizStrategy.sol#L266), pools where the `YRizStrategy` contract has a balance [cannot be removed](https://github.com/radiant-capital/riz/blob/65ca7bb55550d30388e2b2277fefe5686ab7e4e8/src/vaults/YRizStrategy.sol#L279-L283). If any pool which is being removed has a balance at this point, the entire call will revert. This can be taken advantage of by a bad actor to delay or prevent changes to the distribution set. Any user may front\-run calls to `setFullPoolDistribution` with a transfer of tokens from a pool which is being removed, and the entire pool distribution change will be stopped. Even in chains where front\-running is not possible, a user may be able to simply transfer a single token every time they detect the balance of the strategy contract is `0`. Note that a user may have many incentives for doing this, such as keeping interest rates low or high for certain pools (by preventing strategy deposits or withdrawals) or may desire to keep the `bps` for some pool at a certain level. Note that this front\-running stops changes to all pools, not just the one which is associated with the transferred tokens.


Consider implementing an automated withdrawal from the removed pools, rather than a reversion when its balance differs from zero.


***Update:** Resolved in [pull request \#100](https://github.com/radiant-capital/riz/pull/100) at commit [e15ba56](https://github.com/radiant-capital/riz/pull/100/commits/e15ba565f3ca3647b4d87e389ad2fcd9949fb8a3).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Radiant Riz Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/radiant-riz-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

