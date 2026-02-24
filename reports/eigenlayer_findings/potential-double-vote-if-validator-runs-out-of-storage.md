---
# Core Classification
protocol: Omni Halo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41501
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Omni-Halo-Spearbit-Security-Review-August-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Omni-Halo-Spearbit-Security-Review-August-2024.pdf
github_link: none

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
  - Dtheo
  - Shotes
  - Justin Traglia
---

## Vulnerability Title

Potential double-vote if validator runs out of storage

### Overview


This bug report discusses a problem in the Voter::Vote() function where the updated voting state is not saved to disk if there is not enough storage space available. This can lead to a double-vote when the node restarts, as it will load the outdated state. The issue is caused by the WriteFileAtomic() function, which fails to create a temporary file due to the lack of storage space. The recommendation is to stop the validator instead of restarting the stream if saving the state to disk fails. The bug has been fixed in the Spearbit application.

### Original Finding Content

## Severity: Medium Risk

## Context
voter.go#L316-L328

## Description
In `Voter::Vote()`, if `v.saveUnsafe()` (which saves the voting state to disk) returns an error because the node is out of storage, the changes to `v.latest` and `v.available` will still persist. Since the vote was created, we believe it will still be propagated, but the updated state will not be saved to disk. In this situation, there is potential for a double-vote when the node restarts.

When the node starts back up, it will load the outdated state. It calls `getFromHeightAndOffset()` to get `skipBeforeOffset`. Because the state on disk is expected to be out-of-date, `skipBeforeOffset` will come from the latest "approved" attestation. We believe there is an opportunity for the latest propagated attestation to be newer than the latest approved on-chain attestation; otherwise, why would it compare against the value from the local state?

```go
// WriteFileAtomic creates a temporary file with data and provided perm and
// swaps it atomically with filename if successful.
func WriteFileAtomic(filename string, data []byte, perm os.FileMode) (err error) {
```

The `v.safeUnsafe()` function uses `WriteFileAtomic()` to save the state to disk. `WriteFileAtomic()` will attempt to create a temporary file. Since there is no available storage space, the write operation will fail when trying to write to the temporary file. This failure will result in an error being returned by the function, and the original file will remain unchanged.

## Recommendation
If saving the state to disk fails, stop the validator instead of restarting the stream.

## Omni
Fixed in 519e3342 by aborting the application if persistence fails.

## Spearbit
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Omni Halo |
| Report Date | N/A |
| Finders | Dtheo, Shotes, Justin Traglia |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Omni-Halo-Spearbit-Security-Review-August-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Omni-Halo-Spearbit-Security-Review-August-2024.pdf

### Keywords for Search

`vulnerability`

