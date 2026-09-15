---
# Core Classification
protocol: Yearn Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27807
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/yETH-bootstrap/README.md#1-double-voting-in-bootstrapvy-in-case-of-violation-of-time-intervals
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

Double voting in `Bootstrap.vy` in case of violation of time intervals

### Overview


This bug report is about a vulnerability in the Bootstrap contract, which is deployed by the owner setting key periods using the functions set_whitelist_period(), set_incentive_period(), set_deposit_period(), set_vote_period(), and set_lock_end(). If the deposit_end and vote_end parameters in the Bootstrap contract end up being higher than lock_end, a hacker can call claim() to withdraw their funds in styETH, sell them for ETH, and vote again. This process can be repeated multiple times, potentially using a flash loan, and the hacker can accumulate votes to claim 99.99% of all incentives from winning projects.

To fix this issue, it is recommended to check the invariant vote_end < lock_end in the set_vote_period() function. This will ensure that the vote_end parameter is always lower than the lock_end parameter, preventing the vulnerability from being exploited.

### Original Finding Content

##### Description

- https://github.com/yearn/yETH-bootstrap/blob/2dd219d3af49952275934638e8c9d50d0fef0d8f/contracts/Bootstrap.vy#L423

The Bootstrap contract is deployed by the owner setting key periods using the following functions: 
- set_whitelist_period()
- set_incentive_period()
- set_deposit_period()
- set_vote_period()
- set_lock_end()

There is a scenario in which the `deposit_end` and `vote_end` parameters in the `Bootstrap` contract end up being higher than `lock_end`. This can happen, for example, if the management initially sets the correct values for the time intervals but later decides to manually extend the voting by calling `set_deposit_period()` and `set_vote_period()` with increased values, forgetting to also call `set_lock_end()`.

Calling `set_deposit_period()` with increased values will work without an error because requirement `_begin >= self.whitelist_begin` will be satisfied. Calling `set_vote_period()` with increased values will also work without an error because condition `_begin >= self.deposit_begin` will be satisfied.

If `deposit_end` and `vote_end` are increased enough to be higher than `lock_end`, a hacker can call `claim()` to withdraw their funds in styETH, sell them for ETH, and vote again repeating this process multiple times. Potentially, it can be done with a flash loan if the hacker finds a place to sell styETH or yETH, for example, via a curve stable pool. By accumulating votes, the hacker can claim 99.99% of all incentives from winning projects.

##### Recommendation

It is recommended to check invariant `vote_end < lock_end` in the `set_vote_period()` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Yearn Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/yETH-bootstrap/README.md#1-double-voting-in-bootstrapvy-in-case-of-violation-of-time-intervals
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

