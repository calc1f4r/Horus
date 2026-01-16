---
# Core Classification
protocol: Goat Tech
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54271
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/404911dd-3a50-4b63-90d4-e0b9164a34a5
source_link: https://cdn.cantina.xyz/reports/cantina_competition_goat_mar2024.pdf
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
finders_count: 3
finders:
  - Haxatron
  - Vijay
  - etherhood
---

## Vulnerability Title

Premature unlocking of goat tokens upon transfer of lock 

### Overview


The Vester.sol contract has a bug where the `startedAt` timestamp is not being updated when an investor's lock is transferred to another account using the `transferLock` function. This means that the investor's tokens will be unlocked immediately, regardless of the vesting schedule. To fix this, the `lockData.startedAt` value for the "to" account should be updated in the `transferLock` function.

### Original Finding Content

## Vester.sol Contract Issue Report

## Context
Vester.sol#L52-L71

## Description
In the Vester.sol contract, the admin has the capability to transfer an investor's lock to another account via the `transferLock` function. However, during this transfer, the `startedAt` timestamp is not being updated. As a result, Goat tokens of the investor will be unlocked right away, irrespective of the vesting schedule.

Since `startedAt` isn't set in the `transferLock` function, the `startedAt` value for the "to" account will stay zero even after calling the `transferLock` function. Due to this, `pastTime` in the function below will always be calculated against `block.timestamp`.

```solidity
function restDuration(SLock memory lockData_) internal view returns(uint) {
    if (lockData_.startedAt > block.timestamp) {
        return lockData_.duration + lockData_.startedAt - block.timestamp;
    }
    uint pastTime = block.timestamp - lockData_.startedAt;
    if (pastTime < lockData_.duration) {
        return lockData_.duration - pastTime;
    } else {
        return 0;
    }
}
```

As `duration` will be way lesser than `block.timestamp`, `rest duration` will always be returned as zero, and the entire amount of Goat tokens of the investor will be unlocked when the `Unlock` function is called.

## Recommendation
Update the `lockData.startedAt` value for the "to" account in the `transferLock` function as follows:

```solidity
fixed lockData = lockData[to]; 
lockData.startedAt = block.timestamp;
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Goat Tech |
| Report Date | N/A |
| Finders | Haxatron, Vijay, etherhood |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_goat_mar2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/404911dd-3a50-4b63-90d4-e0b9164a34a5

### Keywords for Search

`vulnerability`

