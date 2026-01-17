---
# Core Classification
protocol: Tidal
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27172
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2023/05/tidal/
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
finders_count: 2
finders:
  - Heiko Fisch
  -  David Oz

---

## Vulnerability Title

Missing Validation Checks in execute ✓ Fixed

### Overview


This bug report is about a problem in the `Pool` contract, which is used to implement a threshold voting mechanism. This voting mechanism allows either the pool manager or a committee member to propose a change to the contract state by calling certain functions. If the threshold is reached during a given period, then anyone can call `execute` to execute the state change.

The problem is that some validation checks are implemented in the proposal phase, but not in the functions that execute the state change. This means that if two requests are made in a row, with the second one made before the first one reaches the threshold, then both requests will be executed successfully, leading to undesired results.

Examples of this problem are given in two functions: `_executeRemoveFromCommittee` and `_executeChangeCommitteeThreshold`. The recommendation is to apply the same validation checks in the functions that execute the state change. The bug was fixed in [3bbafab926df0ea39f444ef0fd5d2a6197f99a5d](https://github.com/TidalFinance/tidal-contracts-v2/tree/3bbafab926df0ea39f444ef0fd5d2a6197f99a5d) by implementing the auditor's recommendations.

### Original Finding Content

#### Resolution



Fixed in [3bbafab926df0ea39f444ef0fd5d2a6197f99a5d](https://github.com/TidalFinance/tidal-contracts-v2/tree/3bbafab926df0ea39f444ef0fd5d2a6197f99a5d) by implementing the auditor’s recommendations.


#### Description


The `Pool` contract implements a threshold voting mechanism for some changes in the contract state, where either the pool manager or a committee member can propose a change by calling `claim`, `changePoolManager`, `addToCommittee`, `removeFromCommittee`, or `changeCommitteeThreshold`, and then the committee has a time period for voting. If the threshold is reached during this period, then anyone can call `execute` to execute the state change.


While some validation checks are implemented in the proposal phase, this is not enough to ensure that business logic rules around these changes are completely enforced.


1. `_executeRemoveFromCommittee` – While the `removeFromCommittee` function makes sure that `committeeArray.length > committeeThreshold`, i.e., that there should always be enough committee members to reach the threshold, the same validation check is not enforced in `_executeRemoveFromCommittee`. To better illustrate the issue, let’s consider the following example: `committeeArray.length = 5`, `committeeThreshold = 4`, and now `removeFromCommittee` is called two times in a row, where the second call is made before the first call reaches the threshold. In this case, both requests will be executed successfully, and we end up with `committeeArray.length = 3` and `committeeThreshold = 4`, which is clearly not desired.
2. `_executeChangeCommitteeThreshold` – Applying the same concept here, this function lacks the validation check of `threshold_ <= committeeArray.length`, leading to the same issue as above. Let’s consider the following example: `committeeArray.length = 3`, `committeeThreshold = 2`, and now `changeCommitteeThreshold`is called with `threshold_ = 3`, but before this request is executed, `removeFromCommittee` is called. After both requests have been executed successfully, we will end up with `committeeThreshold = 3` and `committeeArray.length = 2`, which is clearly not desired.


#### Examples


**contracts/Pool.sol:L783**



```
function \_executeRemoveFromCommittee(address who\_) private {

```
**contracts/Pool.sol:L796**



```
function \_executeChangeCommitteeThreshold(uint256 threshold\_) private {

```
#### Recommendation


Apply the same validation checks in the functions that execute the state change.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Tidal |
| Report Date | N/A |
| Finders | Heiko Fisch,  David Oz
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2023/05/tidal/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

