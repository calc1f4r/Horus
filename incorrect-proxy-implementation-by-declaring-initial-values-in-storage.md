---
# Core Classification
protocol: ZeroLend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40822
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/6d383aaf-8554-4a06-a224-86189f81f531
source_link: https://cdn.cantina.xyz/reports/cantina_competition_zerolend_jan2024.pdf
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
finders_count: 3
finders:
  - giraffe0x
  - Saaj
  - waﬄemakr
---

## Vulnerability Title

Incorrect proxy implementation by declaring initial values in storage 

### Overview


The reviewer found an issue with the StreamedVesting.sol contract, where two variables (dead and duration) are declared with initial values but not updated in the initialize() function. This can cause critical errors when interacting with the contract through a proxy contract. It is important to initialize these variables in the initialize function to ensure that the correct values are stored in the proxy's storage. Failure to do so can result in a default value of 0 for duration, which can have a significant impact on the contract's functionality. The recommendation is to initialize both variables in the initialize function to avoid any potential issues.

### Original Finding Content

## Context

(No context files were provided by the reviewer)

## Description

`StreamedVesting.sol` has two storage variables (`dead` and `duration`) that are declared with initial values and are not updated in `initialize()`. As an upgradeable contract, this would lead to critical errors when interacted with by a proxy contract:

```solidity
address public dead = address(0xdead);
uint256 public duration = 3 * 30 days; // 3 months vesting
```

These values will be set when the contract is deployed, but they won't be stored in the proxy's state. If you do `delegatecall` with a proxy, it expects `duration` to be `3 * 30 days`, but it won't find this value in the proxy's state. Instead, it will be the default value for its type, which is `0` for `uint256`.

This is why it's important to initialize state variables in the `initialize` function found within upgradeable contracts, to ensure that the initial values are correctly set in the proxy's storage. 

There's no impact for `dead` as it defaults to `address(0)`. However, for `duration`, it has a significant impact as there would effectively be zero vesting duration since `penalty()` will return `0%` (i.e., no penalty):

```solidity
function penalty(
    uint256 startTime,
    uint256 nowTime
) public view returns (uint256) {
    // After vesting is over, then penalty is 0%
    if (nowTime > startTime + duration) return 0;
}
```

## Recommendation

Initialize both variables in the `initialize` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | ZeroLend |
| Report Date | N/A |
| Finders | giraffe0x, Saaj, waﬄemakr |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_zerolend_jan2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/6d383aaf-8554-4a06-a224-86189f81f531

### Keywords for Search

`vulnerability`

