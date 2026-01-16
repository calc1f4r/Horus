---
# Core Classification
protocol: Berachain Beaconkit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 52810
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Beacon-kit-Spearbit-Security-Review-October-2024.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Beacon-kit-Spearbit-Security-Review-October-2024.pdf
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
finders_count: 4
finders:
  - Dtheo
  - Guido Vranken
  - Sujith Somraaj
  - Shotes
---

## Vulnerability Title

BlobSidecars data availability race condition

### Overview


This bug report describes a race condition that occurs when processing a block in the CometBFT system. Two event handlers, handleBeaconBlockFinalization() and handleFinalSidecarsReceived(), run in parallel and can cause a non-deterministic outcome when accessing the AvailabilityStore. This can lead to an error when trying to finalize the block. The report recommends waiting for the completion of handleFinalSidecarsReceived() before checking for data availability in handleBeaconBlockFinalization(). This issue has been fixed in the Berachain system with commit 711ce6fd and has been verified in the Spearbit system. 

### Original Finding Content

## Medium Risk Severity Report

**Context:** `beacon/blockchain/process.go#L74-L78`

## Description
During the `FinalizeBlock()` call from CometBFT, Beacon-Kit will begin processing on two different event handlers at `abci.go#L345-L356`, namely `async.FinalBeaconBlockReceived` and `async.FinalSidecarsReceived`. These calls handle `handleBeaconBlockFinalization()` and `handleFinalSidecarsReceived()` respectively. These functions run in parallel with each other, which presents the following race condition:

- In `handleFinalSidecarsReceived()`, the sidecars will be written to the `AvailabilityStore` at `da/pkg/blob/processor.go#L129`.
- In `handleBeaconBlockFinalization()`, the sidecars are checked to see if they have been included in the `AvailabilityStore` by calling `IsDataAvailable()` at `beacon/blockchain/process.go#L74-L78`.

The `AvailabilityStore` is being written to and read at the same time. Thus, it can be non-deterministic whether or not the `IsDataAvailable()` check will pass during `FinalizeBlock()`. If the data is not available when the check happens, then the validator will return an error for `FinalizeBlock()`.

**Note:** This `IsDataAvailable()` check is absolutely necessary due to the fact that the block proposal is the only source of distributing `BlobSidecars`. If this check did not exist, a malicious proposer could purposefully not include a `BlobSidecar` that correlates with a `KZGCommitment` in the `BeaconBlock`. This would result in the chain continuing on without ever having the blob data made available. In my opinion, this check should happen in `ProcessProposal()`, so that an invalid proposal may be punished properly in the future.

## Recommendation
The check in `beacon/blockchain/process.go#L74-L78` should await the return of `handleFinalSidecarsReceived()`. To allow for some partial parallel processing (processing the sidecars at the same time as processing the state transition), this check could await a dispatcher event for a new event like `async.BlobDataAvailable`.

## Berachain
Fixed in commit `711ce6fd`.

## Spearbit
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Berachain Beaconkit |
| Report Date | N/A |
| Finders | Dtheo, Guido Vranken, Sujith Somraaj, Shotes |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Beacon-kit-Spearbit-Security-Review-October-2024.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Berachain-Beacon-kit-Spearbit-Security-Review-October-2024.pdf

### Keywords for Search

`vulnerability`

