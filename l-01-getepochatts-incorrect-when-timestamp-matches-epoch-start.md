---
# Core Classification
protocol: Tanssi_2025-04-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 63297
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Tanssi-security-review_2025-04-30.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-01] `getEpochAtTs()` incorrect when timestamp matches epoch start

### Overview

See description below for full details.

### Original Finding Content


The function `OBaseMiddlewareReader.getEpochAtTs()` returns an incorrect epoch number when the input timestamp equals the `epochStart` of a given epoch. 
```solidity
    function getEpochAtTs(
        uint48 timestamp
    ) public view returns (uint48 epoch) {
        EpochCaptureStorage storage $ = _getEpochCaptureStorage();
        return (timestamp - $.startTimestamp) / $.epochDuration;
    }
```
According to the logic implemented in symbiotic epoch-handling functions (such as [`getCurrentEpoch()`](https://github.com/symbioticfi/middleware-sdk/blob/a65b247c0f468cabac9e05712119d5dc2292a46a/src/extensions/managers/capture-timestamps/EpochCapture.sol#L63)), the correct approach is to subtract 1 from the timestamp before performing the division:
```solidity
    function getCurrentEpoch() public view returns (uint48) {
        EpochCaptureStorage storage $ = _getEpochCaptureStorage();
        if (_now() == $.startTimestamp) {
            return 0;
        }

        return (_now() - $.startTimestamp - 1) / $.epochDuration;
    }
```

Although no usage of this function is currently identified in critical paths, this incorrect behavior could introduce subtle bugs or inconsistencies for other protocols or off-chain tools relying on accurate epoch identification.





### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Tanssi_2025-04-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Tanssi-security-review_2025-04-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

