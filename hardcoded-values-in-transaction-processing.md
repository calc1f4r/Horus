---
# Core Classification
protocol: Bridge
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 51778
audit_firm: Halborn
contest_link: https://www.halborn.com/audits/RuneMine/bridge
source_link: https://www.halborn.com/audits/RuneMine/bridge
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
  - Halborn
---

## Vulnerability Title

HARDCODED VALUES IN TRANSACTION PROCESSING

### Overview


The Bitcoin transaction adapter code contains hardcoded values for `transferAmount` and `transferFee`, which are used to calculate transaction outputs and fees. This can cause incorrect payments or delays in transactions. The team has implemented a solution to dynamically calculate these values based on real-time data and network conditions. The issue has been resolved.

### Original Finding Content

##### Description

The Bitcoin transaction adapter code contains hardcoded values for `transferAmount` and `transferFee` within its transaction processing logic. These values are used to calculate transaction outputs and fees, which are critical for the correct execution of financial transactions over the Bitcoin network. The hardcoded `transferAmount` may not appropriately reflect the transaction's required value, leading to overpayments or underpayments, as reported the risk in another issue below. Similarly, a hardcoded `transferFee` might not align with the network's required fee, potentially causing transactions to be delayed or rejected.

##### Proof of Concept

```
func (a *adapter) Bridge(ctx context.Context, request types.BridgeTransferRequest) error {
	const transferAmount = 564 // TODO: Calculate
	chainConfig := &chaincfg.TestNet3Params

```

```
func appendChangeTxOut(inputSatoshis int64, transferAmount int64, a *adapter, request types.BridgeTransferRequest, chainConfig *chaincfg.Params, tx *wire.MsgTx) error {
	const transferFee = 10_000 // TODO: Calculate
	changeSatoshis := inputSatoshis - transferAmount - transferAmount - transferFee
```

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

Implement a mechanism to dynamically calculate `transferAmount` and `transferFee` based on real-time data and network conditions. This could involve querying network statistics or using algorithms designed to estimate fees based on recent block data.

### Remediation Plan

**SOLVED:** The **RuneMine team** solved the issue by implementing the dynamic fee checks.

##### Remediation Hash

7852ae0bd91fa0cb695394283f0a9a860b5eba16

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Halborn |
| Protocol | Bridge |
| Report Date | N/A |
| Finders | Halborn |

### Source Links

- **Source**: https://www.halborn.com/audits/RuneMine/bridge
- **GitHub**: N/A
- **Contest**: https://www.halborn.com/audits/RuneMine/bridge

### Keywords for Search

`vulnerability`

