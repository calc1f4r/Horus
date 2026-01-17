---
# Core Classification
protocol: Entertainmint
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48441
audit_firm: OtterSec
contest_link: https://www.entertainmint.com/
source_link: https://www.entertainmint.com/
github_link: github.com/entertainmintlive/emint.

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
finders_count: 3
finders:
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Gas Optimizations

### Overview

See description below for full details.

### Original Finding Content

## Code Optimization in Smart Contracts

## Overview

In `RaiseCodec.sol` and `TokenCodec.sol`, the `decode` functions decode the data from bits by first left shifting the respective mask to the respective offset and then applying the bitwise AND operator on the bits. The result is again right shifted with the respective offset to get the field value.

### Remediation

This process can be optimized by repeatedly right shifting the bits and applying the respective mask to obtain the field values. Below is an example implementation of the `decode` function in `RaiseCodec.sol`:

```solidity
src/libraries/codecs/RaiseCodec.sol
```

```solidity
1 import {RaiseData, TierType} from "../../structs/RaiseData.sol";
2 import {ONE_BYTE, ONE_BYTE_MASK, FOUR_BYTES, FOUR_BYTE_MASK} from "../../constants/Codecs.sol";
3
4 uint240 constant PROJECT_ID_SIZE = uint240(FOUR_BYTES);
5 uint240 constant RAISE_ID_SIZE = uint240(FOUR_BYTES);
6 uint240 constant TIER_ID_SIZE = uint240(FOUR_BYTES);
7
8 function decode(bytes30 tokenData) external pure returns (RaiseData memory) {
9     uint240 bits = uint240(tokenData);
10
11     uint32 projectId = uint32(bits & FOUR_BYTE_MASK);
12     uint32 raiseId = uint32((bits >>= PROJECT_ID_SIZE) & FOUR_BYTE_MASK);
13     uint32 tierId = uint32((bits >>= RAISE_ID_SIZE) & FOUR_BYTE_MASK);
14     TierType tierType = uint8((bits >>= TIER_ID_SIZE) & ONE_BYTE_MASK);
15
16     return RaiseData({tierType: tierType, tierId: tierId, raiseId: raiseId, projectId: projectId});
17 }
```

## Description

In `RaiseToken.sol`, the `projectId` unnecessarily decodes the entire `tokenId` just to extract the `projectId`.

### Remediation

This can be optimized by retrieving the required `projectId` field from the `tokenId` using bitwise operators. Below is an example of the optimized implementation:

```solidity
src/libraries/RaiseToken.sol
```

```solidity
import {TokenCodec, DATA_OFFSET} from "./codecs/TokenCodec.sol";
import {RaiseCodec, PROJECT_ID_MASK} from "./codecs/RaiseCodec.sol";

function projectId(uint256 tokenId) internal pure returns (uint32 projectId) {
    uint32 projectId = uint32((tokenId >> DATA_OFFSET) & PROJECT_ID_MASK);
}
```

## Description

In `Raises.sol`, the `redeem` and `_mint` functions ensure that the `tierId` is within bounds by throwing an error if the given `tierId` is greater than the length of the `tiers` array minus one.

### Remediation

This condition can be optimized by changing it to check if the given `tierId` is greater than or equal to the length of the `tiers` array.

```solidity
src/Raises.sol DIFF
```

```solidity
242 // Get the tier if it exists
243 - if (tierId > tiers[projectId][raiseId].length - 1) revert NotFound();
244 + if (tierId >= tiers[projectId][raiseId].length) revert NotFound();
245 Tier storage tier = tiers[projectId][raiseId][tierId];
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Entertainmint |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec |

### Source Links

- **Source**: https://www.entertainmint.com/
- **GitHub**: github.com/entertainmintlive/emint.
- **Contest**: https://www.entertainmint.com/

### Keywords for Search

`vulnerability`

