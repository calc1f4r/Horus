---
# Core Classification
protocol: Mayan EVM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 54959
audit_firm: OtterSec
contest_link: https://mayan.finance/
source_link: https://mayan.finance/
github_link: https://github.com/mayan-finance/swap-bridge

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
  - Nicholas R. Putra
  - Ajay Shankar Kunapareddy
  - Robert Chen
  - Akash Gurugunti
---

## Vulnerability Title

Parsing and Offset Inconsistencies

### Overview


This bug report describes issues with the `unlockCompressedBatch` function in the `SwiftSource` implementation. The function incorrectly checks for `BATCH_UNLOCK` instead of `COMPRESSED_UNLOCK` and the encoded payload format does not follow the expected format. This can result in the wrong hash being computed and the function skipping the wrong number of bytes. To fix this, the action check should be updated, the `msgHash` offset should be changed, and the call to `processUnlocks` should start at 0. The bug has been resolved in commit `9e5981b`.

### Original Finding Content

## SwiftSource Implementation Issues

In the current implementation of `SwiftSource::unlockCompressedBatch`, the action check incorrectly verifies for `BATCH_UNLOCK` instead of `COMPRESSED_UNLOCK`. Furthermore, the current encoded payload format parser in `SwiftSource` does not follow the `SwiftDest` payload format. The `msgHash` is read starting at byte 1. However, the `SwiftDest` payload format specifies that the `msgHash` starts at byte 3. Thus, if the `msgHash` is extracted from the wrong offset, the computed hash may not match the expected value.

Also, the current implementation passes an offset of 33 to `processUnlocks`, which is meant to skip 1 byte for action and 32 bytes for the `msgHash`. However, the `encodedPayload` only contains the packed `unlockMsgs` and their length, not the full Wormhole payload. This implies the action and `msgHash` are not present in `encodedPayload`, and the offset should not skip 33 bytes.

## Remediation

1. Update the action check such that it is verifying for `COMPRESSED_UNLOCK`.
2. Adjust the `msgHash` offset to 3.
3. Update the call to `processUnlocks` to start at 0.

## Patch

Resolved in commit `9e5981b`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Mayan EVM |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Ajay Shankar Kunapareddy, Robert Chen, Akash Gurugunti |

### Source Links

- **Source**: https://mayan.finance/
- **GitHub**: https://github.com/mayan-finance/swap-bridge
- **Contest**: https://mayan.finance/

### Keywords for Search

`vulnerability`

