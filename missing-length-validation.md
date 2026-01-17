---
# Core Classification
protocol: Flooring Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47658
audit_firm: OtterSec
contest_link: https://fp.io/
source_link: https://fp.io/
github_link: https://github.com/flooringlab/smart_contract

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
  - Nicholas R. Putra
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Missing Length Validation

### Overview


The bug report states that there is an issue with the "slice" function in the Array.sol file. This function allows for the extraction of a portion of an array by specifying a starting index and length. However, it does not properly check the length parameter, which could lead to accessing memory beyond the bounds of the data array. This can cause out-of-bounds reads and potentially lead to errors. To fix this issue, the length parameter needs to be properly validated. The bug has been fixed in version 4df0c0c.

### Original Finding Content

## Issues with the `slice` Function in Array

The `slice` function in Array lacks proper boundary checks for the inputted length. The `slice` function enables the extraction of a portion of an array by specifying the starting index and length of the desired sub-array. However, it does not verify the length parameter.

## Array.sol (SOLIDITY)

```solidity
function slice(uint256[] memory data, uint256 start, uint256 length) internal pure 
    returns (uint256[] memory res) 
{
    res = new uint256[](length);
    unchecked {
        start *= 0x20;
        length *= 0x20;
    }
    for (uint256 i = 0x20; i <= length;) {
        assembly {
            mstore(add(res, i), mload(add(data, add(i, start))))
        }
        unchecked {
            i += 0x20;
        }
    }
}
```

The function utilizes inline assembly to access memory (`mload` and `mstore`) without explicitly checking whether the provided length parameter exceeds the actual length of the data array. As a result, it may attempt to access memory beyond the bounds of the data array, leading to out-of-bounds reads.

## Remediation

Ensure proper validation of the length parameter.

## Patch

Fixed in commit `4df0c0c`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Flooring Protocol |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Robert Chen, OtterSec |

### Source Links

- **Source**: https://fp.io/
- **GitHub**: https://github.com/flooringlab/smart_contract
- **Contest**: https://fp.io/

### Keywords for Search

`vulnerability`

