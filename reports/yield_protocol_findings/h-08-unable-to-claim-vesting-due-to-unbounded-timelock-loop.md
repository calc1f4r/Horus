---
# Core Classification
protocol: Boot Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 967
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-boot-finance-contest
source_link: https://code4rena.com/reports/2021-11-bootfinance
github_link: https://github.com/code-423n4/2021-11-bootfinance-findings/issues/120

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - privacy

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - WatchPug
  - leastwood
  - nathaniel
  - pauliax
---

## Vulnerability Title

[H-08] Unable to claim vesting due to unbounded timelock loop

### Overview


This bug report is about an issue with the Vesting.sol contract, which is part of the 2021-11-bootfinance repository on GitHub. The issue is that the timelocks for any beneficiary can be vested by someone who is not the beneficiary. This means that a malicious actor can repeatedly call the `vest()` function with minute amounts to make the array large enough, such that when it comes to claiming, it will exceed the gas limit and revert, rendering the vestment for the beneficiary unclaimable. This could be done to each beneficiary, locking up all the vestments.

The bug was discovered through manual code review, and the proof of concept can be found in the links provided in the report. The recommended mitigation steps are to create a minimum on the vestment amounts, such that it won't be feasible for a malicious actor to create a large amount of vestments, and to restrict the vestment contribution of a beneficiary with `require(beneficiary == msg.sender)`.

### Original Finding Content

_Submitted by nathaniel, also found by WatchPug, leastwood, and pauliax_

#### Impact

The timelocks for any *beneficiary* are unbounded, and can be vested by someone who is not the *beneficiary*. When the array becomes significantly big enough, the vestments will no longer be claimable for the *beneficiary*.

The `vest()` function in Vesting.sol does not check the *beneficiary*, hence anyone can vest for anyone else, pushing a new timelock to the `timelocks[_beneficiary]`.
The `_claimableAmount()` function (used by `claim()` function), then loops through the `timelocks[_beneficiary]` to determine the amount to be claimed.
A malicious actor can easy repeatedly call the `vest()` function with minute amounts to make the array large enough, such that when it comes to claiming, it will exceed the gas limit and revert, rendering the vestment for the beneficiary unclaimable.
The malicious actor could do this to each *beneficiary*, locking up all the vestments.

#### Proof of Concept

- <https://github.com/code-423n4/2021-11-bootfinance/blob/main/vesting/contracts/Vesting.sol#L81>
- <https://github.com/code-423n4/2021-11-bootfinance/blob/main/vesting/contracts/Vesting.sol#L195>
- <https://github.com/code-423n4/2021-11-bootfinance/blob/main/vesting/contracts/Vesting.sol#L148>

#### Tools Used

Manual code review

#### Recommended Mitigation Steps

*   Create a minimum on the vestment amounts, such that it won't be feasible for a malicious actor to create a large amount of vestments.
*   Restrict the vestment contribution of a *beneficiary* where `require(beneficiary == msg.sender)`

**[chickenpie347 (Boot Finance) confirmed](https://github.com/code-423n4/2021-11-bootfinance-findings/issues/120)**



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Boot Finance |
| Report Date | N/A |
| Finders | WatchPug, leastwood, nathaniel, pauliax |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-bootfinance
- **GitHub**: https://github.com/code-423n4/2021-11-bootfinance-findings/issues/120
- **Contest**: https://code4rena.com/contests/2021-11-boot-finance-contest

### Keywords for Search

`vulnerability`

