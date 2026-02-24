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
solodit_id: 51781
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

INSUFFICIENT VALIDATION AND POTENTIAL INTEGER OVERFLOW

### Overview


This bug report discusses an issue with the `appendChangeTxOut` function in the Bitcoin transaction handling system. The function does not have proper checks in place to prevent integer underflow, which can occur when there is not enough input satoshis to cover the transfer amount and fee. This can result in incorrect calculations and potentially cause problems with transactions. The report recommends implementing checks to prevent underflow and using a dynamically calculated fee instead of a hardcoded one. The RuneMine team has since solved the issue by implementing these recommendations.

### Original Finding Content

##### Description

The `appendChangeTxOut` function in the Bitcoin transaction handling system is responsible for calculating the change in satoshis after a transaction and appending outputs to a transaction. The function lacks proper validation checks for the calculated `changeSatoshis`, and does not consider the possibility of integer underflow, which can occur when the `inputSatoshis` is insufficient to cover the `transferAmount` and `transferFee`.

##### Proof of Concept

```
func appendChangeTxOut(inputSatoshis int64, transferAmount int64, a *adapter, request types.BridgeTransferRequest, chainConfig *chaincfg.Params, tx *wire.MsgTx) error {
	const transferFee = 10_000 // TODO: Calculate
	changeSatoshis := inputSatoshis - transferAmount - transferAmount - transferFee
```

The potential for integer underflow can be demonstrated by setting `inputSatoshis` to a value less than double the `transferAmount` plus `transferFee`, which will result in `changeSatoshis` becoming negative, subsequently interpreted as a large positive value due to integer underflow.

##### Score

Impact: 3  
Likelihood: 3

##### Recommendation

Implement checks to ensure that calculations involving satoshis do not result in underflow or overflow conditions. Further, replace the hardcoded `transferFee` with a dynamically calculated fee based on current network conditions to ensure transaction reliability and cost-effectiveness.

### Remediation Plan

**SOLVED:** The **RuneMine team** solved the issue by reimplementing the logic with appropriate checks.

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

