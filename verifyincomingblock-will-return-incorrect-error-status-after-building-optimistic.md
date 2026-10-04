---
# Core Classification
protocol: Berachain
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53116
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/94ed2bd9-47c1-4299-a94e-f32a01f495db
source_link: https://cdn.cantina.xyz/reports/cantina_competition_berachain_january2025.pdf
github_link: none

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
finders_count: 1
finders:
  - zigtur
---

## Vulnerability Title

VerifyIncomingBlock will return incorrect error status after building optimistic payload 

### Overview


The VerifyIncomingBlock function in the CometBFT process does not properly handle errors when verifying the state root of an incoming block. This means that invalid blocks can continue to be processed and finalized, leading to potential issues. The recommendation is to return the error from the verifyStateRoot function instead of the error from GetLatestExecutionPayloadHeader. This bug has been fixed in a recent commit.

### Original Finding Content

## Context
`process_proposal.go#L222-L257`

## Description
The `VerifyIncomingBlock` function is called during the `ProcessProposal` step of CometBFT. This function verifies the state root of the incoming block by calling `verifyStateRoot`. 

However, when the optimistic payload builds configuration is set, the function will not return errors occurring in `verifyStateRoot` but will return the error result from the optimistic build. This means that failing blocks will proceed as they don't return any error.

On the impact side, this leads the `ProcessProposal` to continue execution of the block despite this block being invalid. This will then lead `finalizeBlock` to finalize invalid blocks.

In `VerifyIncomingBlock`, a call to `verifyStateRoot` is made. If it fails (i.e., the block is invalid), an optimistic payload is built. However, the result from the optimistic payload is returned instead of the error from `verifyStateRoot`.

```go
// Verify the state root of the incoming block.
err := s.verifyStateRoot(
    ctx,
    postState,
    beaconBlk,
    consensusTime,
    proposerAddress,
)
if err != nil { // @POC: There was an error in `verifyStateRoot`
    s.logger.Error(
        "Rejecting incoming beacon block ",
        "state_root",
        beaconBlk.GetStateRoot(),
        "reason",
        err,
    )
    if s.shouldBuildOptimisticPayloads() {
        var lph *ctypes.ExecutionPayloadHeader
        lph, err = preState.GetLatestExecutionPayloadHeader() // @POC: Override `err` with `nil` as it succeeds
        if err != nil {
            return err
        }
        go s.handleRebuildPayloadForRejectedBlock(
            ctx,
            preState,
            payloadtime.Next(
                consensusTime,
                lph.GetTimestamp(),
                true, // buildOptimistically
            ),
        )
    }
    return err // @POC: `nil` is returned instead of the error!!!
}
```

## Recommendation
Return the error from `verifyStateRoot` instead of the error from `GetLatestExecutionPayloadHeader`.

## Diff
```diff
diff --git a/beacon/blockchain/process_proposal.go b/beacon/blockchain/process_proposal.go
index 9043527..0ec7c76 100644
--- a/beacon/blockchain/process_proposal.go
+++ b/beacon/blockchain/process_proposal.go
@@ -237,8 +237,10 @@ func (s *Service[
    if s.shouldBuildOptimisticPayloads() {
        var lph *ctypes.ExecutionPayloadHeader
        - lph, err = preState.GetLatestExecutionPayloadHeader()
        - if err != nil {
        + lph, err2 := preState.GetLatestExecutionPayloadHeader()
        + if err2 != nil {
        + // If we fail to get the latest execution payload header,
        + // then return `verifyStateRoot` error
        return err
        }
    }
```

**Berachain:** Fixed in commit `1a9aeae6`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Berachain |
| Report Date | N/A |
| Finders | zigtur |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_berachain_january2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/94ed2bd9-47c1-4299-a94e-f32a01f495db

### Keywords for Search

`vulnerability`

