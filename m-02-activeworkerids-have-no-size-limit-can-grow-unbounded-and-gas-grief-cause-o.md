---
# Core Classification
protocol: Subsquid
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58250
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Subsquid-security-review.md
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] `activeWorkerIds` have no size limit, can grow unbounded and gas-grief / cause OOG errors

### Overview


The bug report describes a problem in the `WorkerRegistration.sol` contract where anyone can register as a worker without proper checks. This can cause high gas costs for other users, potentially leading to a denial of service attack. To fix this, the report recommends implementing a whitelist and limiting the size of the `activeWorkerIds` array.

### Original Finding Content

## Severity

**Impact**: High, Denial of service and high gas costs to users

**Likelihood**: Low, unprofitable due to bond submitted

## Description

The function `register` in `WorkerRegistration.sol` contract adds a new element to the `activeWorkerIds` array whenever a new worker is registered. There are no checks for registered `peerId`s, so anyone can register any peerId as a worker. The only restriction is that the user has to submit a bond amount of tokens in order to do so, which will get unlocked later.

The issue is that if this array grows too large, it will cause excessive gas costs for other users, since plenty functions loop over this array. An extreme scenario is when the gas cost to loop over the array exceeds the block gas limit, DOSing operations.

An example of such loops over `activeWorkerIds` is shown below.

```solidity
function deregister(bytes calldata peerId) external whenNotPaused {
    for (uint256 i = 0; i < activeWorkerIds.length; i++) {
        if (activeWorkerIds[i] == workerId) {
            activeWorkerIds[i] = activeWorkerIds[
                activeWorkerIds.length - 1
            ];
            activeWorkerIds.pop();
            break;
        }
    }
```

```solidity
function getActiveWorkers() public view returns (Worker[] memory) {
    for (uint256 i = 0; i < activeWorkerIds.length; i++) {
        uint256 workerId = activeWorkerIds[i];
        Worker storage worker = workers[workerId];
        if (isWorkerActive(worker)) {
            activeWorkers[activeIndex] = worker;
            activeIndex++;
        }
    }
```

This is also valid for the functions `getActiveWorkerIds` and `getActiveWorkerCount`.

Since a user can increase the gas costs of other users at no cost to themselves, this is an issue. The malicious user can always come back after the lock period and deregister and withdraw their bond amount. However, users who interacted with the protocol in between pays inflated gas amounts due to this manipulation.

An unlikely scenario is when the inflated array is too large to traverse in a single block due to the block gas limit and DOSes the entire protocol. However this will not be profitable by the attacker.

## Recommendations

Use a whitelist of `peerIds`, and limit the size of the `activeWorkerIds` array to a reasonable amount.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Subsquid |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Subsquid-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

