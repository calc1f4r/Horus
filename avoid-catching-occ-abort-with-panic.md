---
# Core Classification
protocol: Sei OCC
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47437
audit_firm: OtterSec
contest_link: https://www.sei.io/
source_link: https://www.sei.io/
github_link: https://github.com/sei-protocol

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
  - Naoya Okanami
  - James
  - Tuyết
---

## Vulnerability Title

Avoid Catching OCC Abort With Panic

### Overview


The bug report discusses an issue that occurs when using panic to handle optimistic concurrency control aborts, specifically in the function mvkv::Get. When encountering an Estimate value, a panic is triggered to signal a transaction failure to the scheduler. However, if this panic is caught before reaching the optimistic concurrency control abort recovery middleware in runTx, the scheduler may fail to handle it appropriately. The suggested remediation is to not rely on panic recovery to differentiate between optimistic concurrency aborts and normal transaction errors, and instead check for abort messages passed through the abort channel. The bug has been resolved in commit e8a28d3.

### Original Finding Content

## Issue with Utilizing Panic to Handle Optimistic Currency Control Aborts

An issue arises with utilizing panic to handle optimistic currency control aborts, particularly in `mvkv::Get`. When encountering an Estimate value, a panic is triggered to signal a transaction failure to the scheduler. However, if this panic is caught before reaching the optimistic currency control abort recovery middleware in `runTx`, the scheduler may fail to handle it appropriately.

## Code Snippet: `store/multiVersion/mvkv.go`

```go
func (store *VersionIndexedStore) Get(key []byte) []byte {
    [...]
    if mvsValue != nil {
        if mvsValue.IsEstimate() {
            abort := scheduler.NewEstimateAbort(mvsValue.Index())
            store.abortChannel <- abort
            panic(abort)
        }
        [...]
    }
    [...]
}
```

## Code Snippet: `sei-cosmos/tasks/scheduler.go`

```go
func (server msgServer) EVMTransaction(goCtx context.Context, msg *types.MsgEVMTransaction) (serverRes *types.MsgEVMTransactionResponse, err error) {
    [...]
    defer func() {
        if pe := recover(); pe != nil {
            ctx.Logger().Error(fmt.Sprintf("EVM PANIC: %s", pe))
            panic(pe)
        }
        [...]
    }()
    [...]
}
```

## Remediation

Do not rely on the panic recovery values to differentiate between optimistic currency aborts and normal transaction errors. Check for abort messages passed through the abort channel instead.

## Patch

Resolved in e828d3.

© 2024 Otter Audits LLC. All Rights Reserved. 11/16

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Sei OCC |
| Report Date | N/A |
| Finders | Naoya Okanami, James, Tuyết |

### Source Links

- **Source**: https://www.sei.io/
- **GitHub**: https://github.com/sei-protocol
- **Contest**: https://www.sei.io/

### Keywords for Search

`vulnerability`

