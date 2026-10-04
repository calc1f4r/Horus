---
# Core Classification
protocol: Sofamon-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41369
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Sofamon-security-review-August.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] Updating protocolFeeTo

### Overview


This bug report discusses a high severity bug in the SofamonWearable smart contract. The likelihood of this bug occurring is low. The contract has a function called `updateRoyaltyFeeTo()` that is used to update the fee receiver. However, there are some potential issues with this function. Firstly, if the function is never called, the `royaltyFeeTo` variable will be set to `address(0)`, which means that any royalties will be sent to an empty address. Secondly, the `machine` variable can be updated, which could result in royalties being sent to a deprecated address. Lastly, if the `protocolFeeTo` variable is updated in the `machine` variable, royalties will be sent to the old `protocolFeeTo` address. To fix this bug, it is recommended to always read the `protocolFeeTo` variable from the `ISofamonWearableFactory` contract instead of storing it on the `SofamonWearable` contract. Additionally, the `updateRoyaltyFeeTo()` function can be removed.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

SofamonWearable has the following functions to update the fee receiver.

```solidity
    function updateRoyaltyFeeTo() public {
        royaltyFeeTo = ISofamonWearableFactory(machine).protocolFeeTo();

        emit NewRoyaltyFeeTo(royaltyFeeTo);
    }
```

So, `royaltyFeeTo` should always be updated manually.

Some bad scenarios are possible:

1. By default it is set to `address(0)` if the function was never called => royalties sent to zero address
2. `machine` can be updated => royalties sent to the deprecated address
3. `protocolFeeTo` can be updated in `machine` => royalties sent to the old `protocolFeeTo` address

## Recommendations

Consider reading `ISofamonWearableFactory(machine).protocolFeeTo()` always, not storing the address on `SofamonWearable`. `updateRoyaltyFeeTo()` can be removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Sofamon-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Sofamon-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

