---
# Core Classification
protocol: Vertex Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48387
audit_firm: OtterSec
contest_link: https://vertexprotocol.io/
source_link: https://vertexprotocol.io/
github_link: github.com/vertex-protocol/vertex-evm.

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
finders_count: 4
finders:
  - Shiva Shankar
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Incorrect Math Operations In MathHelper Library

### Overview


The MathHelper Library has a bug where the overflow and underflow checks for add, sub, and sqrt do not work for signed integers. This means that when using the add function, if x equals 40 and y equals -20, the resulting value will be incorrect. The same issue occurs with the sub function, where the resulting value is also incorrect. Additionally, the sqrt function is not properly handling negative integers and is returning an incorrect value of 1. To fix this bug, the data type of variables should be changed to unsigned or the checks should be modified to work for signed integers. This bug has been fixed in version #96 of the library.

### Original Finding Content

## MathHelper Library Vulnerability Overview

In the MathHelper Library, the overflow and underflow checks for `add`, `sub`, and `sqrt` fail for signed integers.

## Add Function

In the `add` function, if `x` equals 40 and `y` equals -20, then `z`, which equals `x + y`, will equal 20. As this value is less than `x`, this equation fails.

```solidity
contracts/libraries/MathHelper.sol

function add(int256 x, int256 y) internal pure returns (int256 z) {
    require((z = x + y) >= x, "ds-math-add-overflow");
}
```

## Sub Function

In the `sub` function, if `x` equals 40 and `y` equals -20, then `x`, which equals `x - y`, will equal 60. As this value is greater than `x`, this equation fails as well.

```solidity
contracts/libraries/MathHelper.sol

function sub(int256 x, int256 y) internal pure returns (int256 z) {
    require((z = x - y) <= x, "ds-math-sub-underflow");
}
```

## Sqrt Function

Since the `sqrt` function is taking signed integers, an error needs to result for the square root of negative integers. Instead, it is returning 1 as the output.

```solidity
contracts/libraries/MathHelper.sol

function sqrt(int256 y) internal pure returns (int256 z) {
    if (y > 3) {
        z = y;
        int256 x = y / 2 + 1;
        while (x < z) {
            z = x;
            x = (y / x + x) / 2;
        }
    } else if (y != 0) {
        z = 1;
    }
}
```

## Vertex Protocol Audit 04 | Vulnerabilities

## Remediation

Change either the datatype of variables to unsigned or make the presented checks work for signed integers.

## Patch

Overflow and underflow checks have been modified to work for signed integers. Fixed in #96.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Vertex Protocol |
| Report Date | N/A |
| Finders | Shiva Shankar, Robert Chen, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://vertexprotocol.io/
- **GitHub**: github.com/vertex-protocol/vertex-evm.
- **Contest**: https://vertexprotocol.io/

### Keywords for Search

`vulnerability`

