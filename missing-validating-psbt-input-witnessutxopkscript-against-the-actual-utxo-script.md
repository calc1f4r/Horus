---
# Core Classification
protocol: Lombard Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46320
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/3a1c4f65-6ef7-4d26-97f4-480f8093801d
source_link: https://cdn.cantina.xyz/reports/cantina_lombard_december2024.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Haxatron
  - dontonka
  - Bernd
---

## Vulnerability Title

Missing validating PSBT input WitnessUtxo.PkScript against the actual UTXO ScriptPubKey allows bypassing address validation 

### Overview

See description below for full details.

### Original Finding Content

## Context
- `internal/approver/strategy/cubist/common.go#L139-L140`
- `internal/approver/strategy/cubist/common.go#L106-L109`

## Description
In `validateStakingInputs()` and `validateDepositInputs()`, the PSBT's Input are enumerated, and the address is extracted from the input's witness script via `txscript.ExtractPkScriptAddrs()`. The extracted address is then subsequently validated to ensure it is a valid and expected address. 

However, the PSBT inputs are just metadata; they are not guaranteed to match the actual transaction (`UnsignedTx`). Therefore, it is necessary to double-check the inputs against the Bitcoin network to ensure they are legitimate UTXOs. 

While this is done in `validateStakingInputs()` and `validateDepositInputs()` by calling `c.blockchainService.GetTxOut(&outPoint)` to retrieve and validate the UTXO's value, it is missing to validate `in.WitnessUtxo.PkScript` against the actual UTXO's `ScriptPubKey` in `validateDepositInputs()` and `validateStakingInputs()`. 

As a result, it is possible to bypass the address validation by using a different `WitnessUtxo.PkScript` in the PSBT's Input than the actual UTXO's `ScriptPubKey`.

## Recommendation
Consider validating that the `WitnessUtxo.PkScript` matches the actual UTXO's `ScriptPubKey` to ensure the address validation is accurate.

## Lombard
Fixed in PR 61.

## Cantina Managed
Fix looks good.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Lombard Finance |
| Report Date | N/A |
| Finders | Haxatron, dontonka, Bernd |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_lombard_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/3a1c4f65-6ef7-4d26-97f4-480f8093801d

### Keywords for Search

`vulnerability`

