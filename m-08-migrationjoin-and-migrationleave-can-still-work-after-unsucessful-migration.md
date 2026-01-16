---
# Core Classification
protocol: Fractional
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3009
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-07-fractional-v2-contest
source_link: https://code4rena.com/reports/2022-07-fractional
github_link: https://github.com/code-423n4/2022-07-fractional-findings/issues/250

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - bridge
  - yield
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - 0x52  codexploder
  - hansfriese
---

## Vulnerability Title

[M-08] Migration.join() and Migration.leave() can still work after unsucessful migration.

### Overview


This bug report is about the issue of join() and leave() functions in the code of the Migration.sol file. These functions can still work after an unsuccessful migration, which can cause unexpected withdrawal logic. This bug was found using the Solidity Visual Developer of VSCode. 

The impact of this bug is that the withdrawal logic after an unsuccessful migration is different from the initial leave() logic and can be messy if users call join() and leave() after unsuccessful migration. 

The recommended mitigation steps for this bug are to add restrictions to the join() and leave() functions so that users can only call these functions for 7 days before the migration is committed. This can be done by adding conditions to the join() and leave() functions.

### Original Finding Content

_Submitted by hansfriese, also found by 0x52 and codexploder_

<https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L105>

<https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L141>

### Impact

`Migration.join()` and `Migration.leave()` can still work after unsucessful migration.
As I submitted with my high-risk finding "Migration.`withdrawContribution()` might work unexpectedly after unsuccessful migration.", withdraw logic after unsuccessful migration is different from the initial `leave()` logic and the withdrawal logic would be messy if users call `join()` and `leave()` after unsuccessful migration.

### Proof of Concept

According to the [explanation](https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L23), join() and leave() functions must be called for 7 days before commition.

Currently, such a scenario is possible.

*   Alice creates a new migration and commits after some joins.
*   The migration ended unsuccessfully after 4 days.
*   Then users can call `leave()` or `withdrawContribution()` to withdraw their deposits but it wouldn't work properly because we should recalculate eth/fractional amounts with returned amounts after unsuccessful migration.

### Tools Used

Solidity Visual Developer of VSCode

### Recommended Mitigation Steps

We should add some restrictions to `join()` and `leave()` functions so that users can call these functions for 7 days before the migration is committed.

We should add these conditions to [join()](https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L118) and [leave()](https://github.com/code-423n4/2022-07-fractional/blob/8f2697ae727c60c93ea47276f8fa128369abfe51/src/modules/Migration.sol#L150).

    require(!migrationInfo[_vault][_proposalId].isCommited, "committed already");
    require(block.timestamp <= proposal.startTime + PROPOSAL_PERIOD, "proposal over");

**[Ferret-san (Fractional) confirmed](https://github.com/code-423n4/2022-07-fractional-findings/issues/250)** 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Fractional |
| Report Date | N/A |
| Finders | 0x52  codexploder, hansfriese |

### Source Links

- **Source**: https://code4rena.com/reports/2022-07-fractional
- **GitHub**: https://github.com/code-423n4/2022-07-fractional-findings/issues/250
- **Contest**: https://code4rena.com/contests/2022-07-fractional-v2-contest

### Keywords for Search

`Business Logic`

