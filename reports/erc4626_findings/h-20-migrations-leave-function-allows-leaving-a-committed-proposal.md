---
# Core Classification
protocol: Fractional
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3001
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-fractional-v2-contest
source_link: https://code4rena.com/reports/2022-07-fractional
github_link: https://github.com/code-423n4/2022-07-fractional-findings/issues/379

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

protocol_categories:
  - dexes
  - bridge
  - yield
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - kenzo
---

## Vulnerability Title

[H-20] Migration's `leave` function allows leaving a committed proposal

### Overview


This bug report is about a vulnerability in the 'leave' function of the project called '2022-07-fractional'. The 'leave' function allows users to leave a proposal even if it has been committed and failed, which is a duplicate functionality of the 'withdrawContributions' function. This vulnerability can cause users to receive a different amount of assets than they should, on the expense of other users. This is because 'leave' does not check if the proposal has been committed, so users can call it instead of 'withdrawContribution' and receive their original contribution back, instead of the adjusted amount returned from the buyout. To fix this, the developers should revert the 'leave' function if the proposal has been committed, or merge the functionality of 'leave' and 'withdrawContribution'.

### Original Finding Content

_Submitted by kenzo_

The `leave` function allows to leave a proposal even if the proposal has been committed and failed.
This makes it a (probably unintended) duplicate functionality of `withdrawContributions`, which is the function that should be used to withdraw failed contributions.

### Impact

User assets might be lost:
When withdrawing assets from a failed migration, users should get back a different amount of assets, according to the buyout auction result. (I detailed this in another issue - "Migration::withdrawContribution falsely assumes that user should get exactly his original contribution back").
But when withdrawing assets from a proposal that has not been committed, users should get back their original amount of assets, as that has not changed.
Therefore, if `leave` does not check if the proposal has been committed, users could call `leave` instead of `withdrawContribution` and get back a different amounts of assets than they deserve, on the expense of other users.

### Proof of Concept

The `leave` function [does not check](https://github.com/code-423n4/2022-07-fractional/blob/main/src/modules/Migration.sol#L141) anywhere whether `proposal.isCommited == true`.

Therefore, if a user calls it after a proposal has been committed and failed, it will continue to send him his original contribution back, instead of sending him the adjusted amount that has been returned from Buyout.

### Recommended Mitigation Steps

Revert in `leave` if `proposal.isCommited == true`.
You might be also able to merge the functionality of `leave` and `withdrawContribution`, but that depends on how you will implement the fix for `withdrawContribution`.

**[Ferret-san (Fractional) confirmed](https://github.com/code-423n4/2022-07-fractional-findings/issues/379)** 

**[HardlyDifficult (judge) commented](https://github.com/code-423n4/2022-07-fractional-findings/issues/379#issuecomment-1214481867):**
 > Users can withdraw more than expected after a failed proposal, which leads to a deficit and loss of assets for others. Agree with High risk.



***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Fractional |
| Report Date | N/A |
| Finders | kenzo |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-fractional
- **GitHub**: https://github.com/code-423n4/2022-07-fractional-findings/issues/379
- **Contest**: https://code4rena.com/contests/2022-07-fractional-v2-contest

### Keywords for Search

`vulnerability`

