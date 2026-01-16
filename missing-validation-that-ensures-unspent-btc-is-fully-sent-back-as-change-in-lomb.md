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
solodit_id: 46313
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/3a1c4f65-6ef7-4d26-97f4-480f8093801d
source_link: https://cdn.cantina.xyz/reports/cantina_lombard_december2024.pdf
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
  - Haxatron
  - dontonka
  - Bernd
---

## Vulnerability Title

Missing validation that ensures unspent BTC is fully sent back as change in Lombard trans- fer signing strategy 

### Overview


The report discusses a bug in the Lombard transfer signing strategy, which is used to transfer BTC from one wallet to another. The bug occurs because there is no validation in place to ensure that the BTC miner fee is reasonable and that the remaining unspent BTC is sent back to one of Lombard's staking addresses. This could result in a situation where only a fraction of the input BTC is spent, with the rest going to the miner. The recommendation is to add validation to determine the unspent BTC and deduct a reasonable miner fee before returning the remaining BTC as change. The bug has been fixed in PR 78 and a related issue has been addressed in commit bc8274f6. 

### Original Finding Content

## Lombard Transfer Signing Strategy

## Context
`common.go#L166-L203`

## Description
The Lombard transfer signing strategy is used to transfer BTC from the Cubist deposit wallets to the Cubist staking hot wallets. The function `validateLombardTransferRequest()` ensures that the transfer request is valid before approving it.

However, there is no validation that ensures that the BTC miner fee is reasonable and that the remaining unspent BTC is sent back as change to one of Lombard's staking addresses. This could lead to a situation where the UTXO outputs only spend a fraction of the input BTC, with the remaining BTC going to the miner.

## Recommendation
Consider summing the UTXO input and output values to determine the unspent BTC, which should be returned as change after deducting a reasonable miner fee.

## Lombard
Fixed in PR 78.

## Cantina Managed
Shouldn't `validateDepositInputs()` also validate `in.WitnessUtxo.Value == int64(txOut.Value*1e8)`?

## Lombard
Added in commit `bc8274f6`.

## Cantina Managed
Fix looks good.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

