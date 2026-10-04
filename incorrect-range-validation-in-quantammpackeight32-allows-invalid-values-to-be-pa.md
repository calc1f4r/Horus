---
# Core Classification
protocol: Quantamm
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44298
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
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
  - 0kage
  - immeas
---

## Vulnerability Title

Incorrect range validation in `quantAMMPackEight32` allows invalid values to be packed

### Overview


The report highlights a bug in the `ScalarQuantAMMBaseStorage::quantAMMPackEight32` function, which is used in the `QuantAMMWeightedPool::setWeights` function to pack weight values. Due to incorrect validation logic, the function fails to properly check the minimum bounds for six out of eight input parameters. This could lead to unexpected behavior in weight calculations, although it is unlikely to occur during the running of the pool. The bug has been fixed in a recent commit.

### Original Finding Content

**Description:** The `ScalarQuantAMMBaseStorage::quantAMMPackEight32` function contains incorrect validation logic that fails to properly check minimum bounds for six out of eight input parameters. The require statement incorrectly reuses `_firstInt` for minimum bound checks instead of checking each respective input parameter.

```solidity
require(
    _firstInt <= MAX32 &&
        _firstInt >= MIN32 &&
        _secondInt <= MAX32 &&
        _secondInt >= MIN32 &&
        _thirdInt <= MAX32 &&
        _firstInt >= MIN32 &&  // @audit should be _thirdInt
        _fourthInt <= MAX32 &&
        _firstInt >= MIN32 &&  // @audit should be _fourthInt
        _fifthInt <= MAX32 &&
        _firstInt >= MIN32 &&  // @audit should be _fifthInt
        _sixthInt <= MAX32 &&
        _firstInt >= MIN32 &&  // @audit should be _sixthInt
        _seventhInt <= MAX32 &&
        _firstInt >= MIN32 &&  // @audit should be _seventhInt
        _eighthInt <= MAX32 &&
        _firstInt >= MIN32,    // @audit should be _eighthInt
    "Overflow"
);
```
This function is called by `quantAMMPack32Array` which inturn is used in the `QuantAMMWeightedPool::setWeights` function to pack weight values.

**Impact:** While the `setWeights` function is protected by access controls (only callable by `updateWeightRunner`), allowing invalid values to be packed could lead to unexpected behavior in weight calculations.

**Proof of Concept:** TBD

**Recommended Mitigation:** Consider updating the require statement to properly validate minimum bounds for all input parameters:

**QuantAmm:**
We use the pack in setInitialWeights which is used in the initialise function. Given the absolute guard rail logic etc I do not think it is mathematically possible for this to be triggered during running of the pool I think they may only fail the deployment of the pool if a pool is initialised with bad weights. Fixed in commit [`408ba20`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/408ba203c1b6c4abfd3474e4baa448af3752ea6e).

**Cyfrin:** Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Quantamm |
| Report Date | N/A |
| Finders | 0kage, immeas |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

