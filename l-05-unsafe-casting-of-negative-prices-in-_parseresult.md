---
# Core Classification
protocol: Opendollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 34080
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/OpenDollar-security-review.md
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

[L-05] Unsafe Casting of Negative Prices in `_parseResult`

### Overview

See description below for full details.

### Original Finding Content

The `_parseResult` function performs a conversion from `int256` to `uint256` on Chainlink feed results. Chainlink price feeds may return negative prices under certain conditions. Currently, the function does not check the sign of the price before casting it to `uint256`. This can lead to incorrect results, as casting a negative `int256` to `uint256` results in a very large number close to the maximum value of `uint256`, potentially leading to unexpected behavior or financial inaccuracies in the system.

To prevent incorrect data handling and potential vulnerabilities associated with overflow, it is recommended to modify the `_parseResult` function to include a check for negative values before casting. If a negative price is detected, the function should revert or handle the case appropriately. Here is a suggested implementation:

```diff
function _parseResult(int256 _chainlinkResult) internal view returns (uint256 _result) {
+    require(_chainlinkResult >= 0, "Negative price value not allowed");

    if (MULTIPLIER == 0) {
        return uint256(_chainlinkResult);
    } else if (MULTIPLIER > 0) {
        return uint256(_chainlinkResult) * (10 ** uint256(MULTIPLIER));
    } else {
        return uint256(_chainlinkResult) / (10 ** _abs(MULTIPLIER));
    }
}
```

**Open Dollar comments**

_Implemented the recommended change._

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Opendollar |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/OpenDollar-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

