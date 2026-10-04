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
solodit_id: 53122
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/94ed2bd9-47c1-4299-a94e-f32a01f495db
source_link: https://cdn.cantina.xyz/reports/cantina_competition_berachain_january2025.pdf
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
finders_count: 1
finders:
  - Christoph Michel
---

## Vulnerability Title

Malicious proposer can include additional transactions in BeaconBlock 

### Overview


There is a bug in the code that allows a malicious user to include extra transactions in BeaconBlock, causing unnecessary computations and potentially crashing other nodes. This can also lead to a decrease in available disk space. The likelihood of this happening is medium and the impact is also medium. The recommendation is to verify the transaction list length and disable any additional transactions. The bug has been fixed in a recent commit.

### Original Finding Content

## Context
`finalize_block.go#L63`

## Description
A malicious proposer can include additional transactions in `BeaconBlock` besides the `BeaconBlock` and Sidecars transaction. These are essentially ignored but the code still iterates over them and sets their transaction result to invalid in `FinalizeBlock`.

```go
// Iterate over all raw transactions in the proposal and attempt to execute
// them, gathering the execution results.
//
// NOTE: Not all raw transactions may adhere to the sdk.Tx interface, e.g.
// vote extensions, so skip those.
txResults := make([]*cmtabci.ExecTxResult, len(req.Txs))
for i := range req.Txs {
    //nolint:mnd // its okay for now.
    txResults[i] = &cmtabci.ExecTxResult{
        Codespace: "sdk",
        Code: 2,
        Log: "skip decoding",
        GasWanted: 0,
        GasUsed: 0,
    }
}
```

## Impact Explanation
**Medium** - A malicious proposer includes spam transactions to reach the block limit of CometBFT (currently 4MiB but needs to be changed to around 100 MiB, see other issues). All validators are required to accept and store the block, shrinking the available disk space, while performing unnecessary computations by iterating over all transactions and allocating memory for their results. A hash must be computed over the returned transaction results (`LastResultsHash` included in the next block header).

## Likelihood Explanation
**Medium** - There's some incentive by hoping to crash competitors' nodes that run on weaker hardware or delay their block production to get them slashed (in the future).

## Recommendation
As there's no use of any other cometBFT transactions right now, consider verifying that the transaction list length is 2, disabling any additional transactions.

## Berachain
Fixed in commit `36741168`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Berachain |
| Report Date | N/A |
| Finders | Christoph Michel |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_competition_berachain_january2025.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/94ed2bd9-47c1-4299-a94e-f32a01f495db

### Keywords for Search

`vulnerability`

