---
# Core Classification
protocol: Contracts V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52271
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/lucid-labs/contracts-v1
source_link: https://www.halborn.com/audits/lucid-labs/contracts-v1
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
  - Halborn
---

## Vulnerability Title

Missing Duration Validation Enables Zero Division in Base Asset Bridge

### Overview

See description below for full details.

### Original Finding Content

##### Description

The BaseAssetBridge.sol contract uses a `duration` variable as a divisor in multiple functions without validating that it's non-zero. The duration is set in the constructor and cannot be modified afterwards, but lacks zero-value validation:

```
constructor(
    address _owner,
    uint256 _duration,// @audit No validation that it is > 0
    address[] memory _bridges,
    uint256[] memory _mintingLimits,
    uint256[] memory _burningLimits
) OwnableInit(_owner) {
    duration = _duration;// @audit - Directly assigned without checks// ...
}
```

  

The duration variable is used as a divisor in several critical functions:

```
function _changeMinterLimit(address _bridge, uint256 _limit) internal {
// ...
    bridges[_bridge].minterParams.ratePerSecond = _limit / duration;// @audit - Division by duration// ...
}

function _changeBurnerLimit(address _bridge, uint256 _limit) internal {
// ...
    bridges[_bridge].burnerParams.ratePerSecond = _limit / duration;// @audit - Division by duration// ...
}
```

  

If duration is set to 0 during deployment:

* All functions using division by duration will revert
* The bridge becomes completely unusable
* A new contract deployment is required to fix the issue

##### BVSS

[AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C (0.0)](/bvss?q=AO:A/AC:L/AX:L/C:N/I:N/A:N/D:N/Y:N/R:N/S:C)

##### Recommendation

It is recommended to add a duration validation in the constructor :

```
constructor(
    address _owner,
    uint256 _duration,
    address[] memory _bridges,
    uint256[] memory _mintingLimits,
    uint256[] memory _burningLimits
) OwnableInit(_owner) {
    if (_duration == 0) revert InvalidDuration();
    duration = _duration;
// ...
}
```

##### Remediation

**SOLVED:** Duration and addresses are now validated in AssetController's constructor.

##### Remediation Hash

<https://github.com/LucidLabsFi/demos-contracts-v1/commit/4cc5a41f2bc5a36523668f9285e5afd110029982>

##### References

[LucidLabsFi/demos-contracts-v1/contracts/modules/chain-abstraction/BaseAssetBridge.sol#L81](https://github.com/LucidLabsFi/demos-contracts-v1/blob/main/contracts/modules/chain-abstraction/BaseAssetBridge.sol#L81)

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Contracts V1 |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/lucid-labs/contracts-v1
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/lucid-labs/contracts-v1

### Keywords for Search

`vulnerability`

