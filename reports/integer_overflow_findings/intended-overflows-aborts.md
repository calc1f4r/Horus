---
# Core Classification
protocol: LayerZero Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48504
audit_firm: OtterSec
contest_link: https://layerzero.network/
source_link: https://layerzero.network/
github_link: https://github.com/LayerZero-Labs/layerzero-internal/

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
finders_count: 3
finders:
  - Shiva Shankar
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Intended Overflows Aborts

### Overview


The bug report states that in the solidity version 0.8.X, certain arithmetic operations are failing due to the usage of checked arithmetic operations by default. This is causing issues in cases where integer overflows or underflows are intended, such as when calculating integer masks. The suggested solution is to use unchecked arithmetic operations for these calculations. The report also includes a code snippet showing the proposed changes to fix the bug. The bug has been resolved in a specific patch.

### Original Finding Content

## Solidity Version 0.8.X: Checked Arithmetic Operations

In the Solidity version 0.8.X, checked arithmetic operations are used by default. Operations that may result in integer overflows or underflows will fail. In certain circumstances, however, these overflows are intended, such as when calculating integer masks.

## Remediation

Use unchecked arithmetic operations for calculations when there is an intended integer overflow/underflow.

## Code Diff

```diff
--- a/contracts/proof/utility/Buffer.sol
+++ b/contracts/proof/utility/Buffer.sol
@@ -145,12 +145,15 @@ library Buffer {
}
// Copy remaining bytes
- uint mask = 256**(32 - len) - 1;
- assembly {
- let srcpart := and(mload(src), not(mask))
- let destpart := and(mload(dest), mask)
- mstore(dest, or(destpart, srcpart))
+ unchecked {
+ uint mask = 256**(32 - len) - 1;
+ assembly {
+ let srcpart := and(mload(src), not(mask))
+ let destpart := and(mload(dest), mask)
+ mstore(dest, or(destpart, srcpart))
+ }
}
+
return buf;
}
```

## Patch

Resolved in f1e06e3.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | LayerZero Protocol |
| Report Date | N/A |
| Finders | Shiva Shankar, Robert Chen, OtterSec |

### Source Links

- **Source**: https://layerzero.network/
- **GitHub**: https://github.com/LayerZero-Labs/layerzero-internal/
- **Contest**: https://layerzero.network/

### Keywords for Search

`vulnerability`

