---
# Core Classification
protocol: Caldera
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47467
audit_firm: OtterSec
contest_link: https://www.caldera.xyz/
source_link: https://www.caldera.xyz/
github_link: https://github.com/ConstellationCrypto/celestia-bedrock

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
finders_count: 2
finders:
  - James Wang
  - Robert Chen
---

## Vulnerability Title

Missing Timeout Check

### Overview


The bug report describes an issue where a function called "downloadS3Data" is being invoked without a specified timeout in the context. This can cause the program to hang indefinitely if the S3 service experiences issues or becomes unresponsive. This can potentially block the chain derivation process, which is critical to the system's stability and responsiveness. The suggested solution is to add a timeout context when requesting data from the S3 service, which will cancel the request after a specified period of time. The bug has been resolved in version 1d92897.

### Original Finding Content

## DataFromEVMTransactions

Within `DataFromEVMTransactions`, `downloadS3Data` is invoked without a specified timeout in the context (`ctx`). If the S3 service experiences issues or becomes unresponsive, `downloadS3Data` may hang indefinitely without a timeout. This absence of a timeout introduces the possibility of the chain derivation process being indefinitely blocked, awaiting a response from the S3 service. Chain derivation is a critical part of the system, and any prolonged blocking will impact the overall stability and responsiveness of the system.

```go
// op-node/rollup/derive/calldata_source.go
func DataFromEVMTransactions(ctx context.Context, config *rollup.Config, daCfg *rollup.DAConfig,
    batcherAddr common.Address, txs types.Transactions, log log.Logger) ([]eth.Data, error)
{
    [...]
    data, err := downloadS3Data(ctx, daCfg, tx.Data())
    [...]
}
```

## Remediation

Add a timeout context when requesting Amazon Web Services S3. This ensures that if the S3 request takes too long to complete, the program will cancel it after a specified timeout period. Optimism may fall back to fetching data from Celestia.

## Patch

Resolved in 1d92897.

© 2024 Otter Audits LLC. All Rights Reserved. 6/12

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Caldera |
| Report Date | N/A |
| Finders | James Wang, Robert Chen |

### Source Links

- **Source**: https://www.caldera.xyz/
- **GitHub**: https://github.com/ConstellationCrypto/celestia-bedrock
- **Contest**: https://www.caldera.xyz/

### Keywords for Search

`vulnerability`

