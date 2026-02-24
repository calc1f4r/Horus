---
# Core Classification
protocol: GainsNetwork-July
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40194
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-July.md
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
finders_count: 1
finders:
  - Pashov Audit Group
---

## Vulnerability Title

[H-01] Storage slot collision

### Overview


This bug report is about a miscalculation in the storage layout allocation for the `PriceAggregatorStorage` struct. This leads to a potential storage slot collision with `OtcStorage`, causing data corruption. The issue is with the `jobIds` field, which is incorrectly calculated to take up 64 bits instead of 64 bytes. This causes the `PriceAggregatorStorage` to occupy 52 slots instead of the intended 50 slots, overlapping with the first two slots of `OtcStorage`. To fix this, the recommendation is to reduce the size of the `__gap` array or change the starting slot for `OtcStorage` to ensure no overlap. 

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Medium

## Description

There is a miscalculation in the storage layout allocation for the `PriceAggregatorStorage` struct, which leads to a potential storage slot collision with `OtcStorage`.

The key issue is with the bytes32[2] jobIds field. It's incorrectly calculated as taking up 64 bits, but in reality, it occupies 64 bytes (512 bits), spanning 2 full storage slots.

```solidity
    struct PriceAggregatorStorage {
        IChainlinkFeed linkUsdPriceFeed; // 160 bits
        uint24 twapInterval; // 24 bits
        uint8 minAnswers; // 8 bits
        bytes32[2] jobIds; // 64 bits @audit 64 bytes instead of 64 bits
        // ... other fields
        uint256[41] __gap;
    }
```

This miscalculation causes the `PriceAggregatorStorage` to actually occupy 52 slots instead of the intended 50 slots. The storage slots are allocated as follows:

```solidity
    uint256 internal constant GLOBAL_PRICE_AGGREGATOR_SLOT = 551;
    uint256 internal constant GLOBAL_OTC_SLOT = 601;
```

With PriceAggregatorStorage occupying 52 slots starting from slot 551, it will overlap with the first two slots of OtcStorage, which starts at slot 601. This overlap will cause data corruption, as the first two slots of OtcStorage will be overwritten by the last two slots of PriceAggregatorStorage.

## Recommendations

Reduce the \_\_gap array size to 39 in `PriceAggregatorStorage` or change `GLOBAL_OTC_SLOT` to start from slot 603 to ensure no overlap.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | GainsNetwork-July |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-July.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

