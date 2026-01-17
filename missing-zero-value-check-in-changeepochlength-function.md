---
# Core Classification
protocol: Pepper
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52223
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/pepper/pepper
source_link: https://www.halborn.com/audits/pepper/pepper
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

Missing Zero-Value Check in changeEpochLength Function

### Overview

See description below for full details.

### Original Finding Content

##### Description

The `changeEpochLength` function in the Pepper contract allows the owner to set the `EPOCH_LENGTH` without validating that the new value is non-zero. This oversight can lead to a critical issue in the contract's functionality, specifically:

* If `EPOCH_LENGTH` is set to zero, it will cause a divide-by-zero error in the `getCurrentEpoch` function:

  ```
  function getCurrentEpoch() public view returns (uint256 _epoch) {
      return (block.number - claimStartBlock) / EPOCH_LENGTH;
  }
  ```
* This divide-by-zero error would cause all calls to `getCurrentEpoch` to revert, effectively breaking core functionalities of the contract that rely on epoch calculations, such as the claiming mechanism.

This vulnerability could potentially render the contract unusable if the epoch length is accidentally set to zero.

##### BVSS

[AO:A/AC:L/AX:L/R:N/S:U/C:N/A:L/I:L/D:N/Y:N (3.1)](/bvss?q=AO:A/AC:L/AX:L/R:N/S:U/C:N/A:L/I:L/D:N/Y:N)

##### Recommendation

To address this issue, implement a non-zero check in the `changeEpochLength` function.

```
function changeEpochLength(uint16 epochLength) public onlyOwner {
    require(epochLength != 0, "Epoch length cannot be zero");
    EPOCH_LENGTH = epochLength;
    emit EpochLengthChanged(epochLength);
}
```

This change ensures that:

1. The `EPOCH_LENGTH` can never be set to zero, preventing potential divide-by-zero errors.
2. The contract maintains its integrity and functionality, particularly in epoch-based calculations.

##### Remediation

**SOLVED**: The **Pepper team** decided to remove the `changeEpochLength` function from the `Pepper` contract.

##### Remediation Hash

bccbd7a5747d4ef6586581ec93ac77e0d8a4de45

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Pepper |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/pepper/pepper
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/pepper/pepper

### Keywords for Search

`vulnerability`

