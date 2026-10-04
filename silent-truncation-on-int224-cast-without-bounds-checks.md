---
# Core Classification
protocol: API3 - Data Feed Proxy Combinators
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61343
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/api-3-data-feed-proxy-combinators/f5a9fb67-a96b-4db2-9828-623fd975d158/index.html
source_link: https://certificate.quantstamp.com/full/api-3-data-feed-proxy-combinators/f5a9fb67-a96b-4db2-9828-623fd975d158/index.html
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Yamen Merhi
  - Adrian Koegl
  - Hytham Farah
---

## Vulnerability Title

Silent Truncation on `int224` Cast without Bounds Checks

### Overview


This report highlights a bug in three different contracts, `ProductApi3ReaderProxyV1.sol`, `NormalizedApi3ReaderProxyV1.sol`, and `InverseApi3ReaderProxyV1.sol`. These contracts perform unchecked casts from `int256` to `int224`, which can lead to incorrect outputs due to values being truncated. This bug is caused by Solidity not reverting on narrowing conversions, which means that high-order bits can be discarded without warning. The recommendation is to insert explicit range checks or use a function from OpenZeppelin to prevent this issue. Additionally, the comments in the affected contracts should be updated to accurately describe the casting behavior and remove references to nonexistent overflow reverts. 

### Original Finding Content

**Update**
Acknowledged in: `94ae5e9`. The client provided the following explanation:

> The absence of explicit bounds checks for the int256 to int224 cast in ProductApi3ReaderProxyV1.sol and NormalizedApi3ReaderProxyV1.sol is a deliberate trade-off for gas optimization in the read() functions. This design choice means that silent truncation may occur if the intermediate int256 result exceeds int224 limits, a behavior now clearly documented in their respective NatSpec comments. For InverseApi3ReaderProxyV1.sol, the read() function's formula was updated to value = int224(1e36) / baseValue;. With this change, the division occurs directly between int224 types, and thus the specific concern regarding silent truncation from an intermediate int256 cast is not directly applicable to this revised calculation. Its NatSpec comment has been updated to accurately reflect the current operation.

**File(s) affected:**`ProductApi3ReaderProxyV1.sol`, `NormalizedApi3ReaderProxyV1.sol`, `InverseApi3ReaderProxyV1.sol`

**Description:** Multiple contracts perform unchecked casts from `int256` to `int224`, which can silently truncate values exceeding the `int224` range, leading to incorrect and misleading outputs. Solidity does not revert on narrowing conversions, so these casts may discard high-order bits without warning:

*   `ProductApi3ReaderProxyV1.read()`: Multiplies two proxy values and divides by 1e18 before casting to `int224` without checking bounds, risking overflow and silent truncation.
*   `NormalizedApi3ReaderProxyV1.read()`: Scales a Chainlink feed value (up or down) and casts to `int224` without verifying that the result fits within range.
*   `InverseApi3ReaderProxyV1.read()`: Inverts a proxy value using 1e36 divided by the feed value, then casts to `int224`, with a misleading comment implying a revert on overflow.

**Recommendation:** Insert explicit range checks before casting to `int224` to prevent silent truncation, or use `SafeCast.toInt224()` from OpenZeppelin. Update comments to correctly describe casting behavior and eliminate references to nonexistent overflow reverts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | API3 - Data Feed Proxy Combinators |
| Report Date | N/A |
| Finders | Yamen Merhi, Adrian Koegl, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/api-3-data-feed-proxy-combinators/f5a9fb67-a96b-4db2-9828-623fd975d158/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/api-3-data-feed-proxy-combinators/f5a9fb67-a96b-4db2-9828-623fd975d158/index.html

### Keywords for Search

`vulnerability`

