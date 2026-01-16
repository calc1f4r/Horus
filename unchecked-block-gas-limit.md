---
# Core Classification
protocol: Skip Protocol Block-SDK
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47777
audit_firm: OtterSec
contest_link: https://skip.money/
source_link: https://skip.money/
github_link: https://github.com/skip-mev/block-sdk

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
  - James Wang
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Unchecked Block Gas Limit

### Overview


The bug report discusses an issue with the Cosmos-sdk, which is a software development kit that allows for the creation of blockchain networks. The current implementation does not properly check the gas limit, which is the amount of computational resources needed to execute a transaction, against the maximum block size. This could potentially allow for validators to propose blocks that exceed the gas limit and result in partial execution of transactions. The bug has been resolved in a recent patch.

### Original Finding Content

## Cosmos-SDK Configuration for Block Size and Gas Limit

The Cosmos-sdk allows chains to configure both the maximum block size and gas limit. The current implementation only checks the total block size against the maximum block size and does not validate gas limits.

## Code Snippet

```go
// block-sdk/block/base/handlers.go
func (l *BaseLane) DefaultPrepareLaneHandler() PrepareLaneHandler {
    return func(
        ctx sdk.Context,
        proposal block.BlockProposal,
        maxTxBytes int64
    ) ([][]byte, []sdk.Tx, error) {
        [...]
        for iterator := l.Select(ctx, nil); iterator != nil; iterator = iterator.Next() {
            tx := iterator.Tx()
            txBytes, hash, err := utils.GetTxHashStr(l.TxEncoder(), tx)
            [...]
            txSize := int64(len(txBytes))
            if updatedSize := totalSize + txSize; updatedSize > maxTxBytes {
                [...]
                break
            }
            [...]
            totalSize += txSize
            txs = append(txs, txBytes)
        }
        return txs, txsToRemove, nil
    }
}
```

This would allow validators to propose blocks that exceed gas limits and, in the worst-case scenario, result in partial execution of MEV bundled transactions.

## Remediation

Check accumulated gas limit against max block gas.

## Patch

Resolved in `b9d6761`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Skip Protocol Block-SDK |
| Report Date | N/A |
| Finders | James Wang, Robert Chen, OtterSec |

### Source Links

- **Source**: https://skip.money/
- **GitHub**: https://github.com/skip-mev/block-sdk
- **Contest**: https://skip.money/

### Keywords for Search

`vulnerability`

