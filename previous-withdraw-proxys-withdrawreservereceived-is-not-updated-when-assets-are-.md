---
# Core Classification
protocol: Astaria
chain: everychain
category: logic
vulnerability_type: validation

# Attack Vector Details
attack_type: validation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 7324
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 4

# Context Tags
tags:
  - validation

protocol_categories:
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Zach Obront
  - Sawmon and Natalie
  - Blockdev
  - Noah Marconi
---

## Vulnerability Title

Previous withdraw proxy's withdrawReserveReceived is not updated when assets are drained from the current withdraw proxy to the previous

### Overview


This bug report is about the inconsistency in the behavior of draining assets from the current withdraw proxy to the previous. When assets are transferred from the public vault to the previous withdraw proxy, the public vault's s.withdrawReserve and the previous withdraw proxy's withdrawReserveReceived are both updated. However, when draining assets from the current withdraw proxy to the previous, the withdrawReserveReceived is not updated. This can lead to an actor manipulating the value of Bn-1-Wn-1 (previous withdraw proxy's asset balance minus previous withdraw proxy's withdrawReserveReceived) by sending assets to the public vault and the current withdraw proxy before calling transferWithdrawReserve. 

The recommendation is to update the withdrawReserveReceived when draining assets from the current withdraw proxy to the previous, to match the behavior when transferring assets from the public vault to the previous withdraw proxy. This would ensure that Bn-1-Wn-1 accurately represents the sum of all near-boundary auction payment's the previous withdraw proxy receives plus any assets that are transferred to it by an external actor.

### Original Finding Content

## Vulnerability Report

## Severity
**Medium Risk**

## Context
`PublicVault.sol#L378-L381`

## Description
When `drain` is called, we don't update the `s.epochData[s.currentEpoch - 1].withdrawReserveReceived`. This is in contrast to when withdraw reserves are transferred from the public vault to the withdraw proxy. This would unlink the previous withdraw proxy's `withdrawReserveReceived` storage parameter from the total amount of assets it has received from either the public vault or the current withdraw proxy.

An actor can manipulate `Bn-1` (the previous withdraw proxy's asset balance) and `Wn-1` (the previous withdraw proxy's `withdrawReserveReceived`) by sending assets to the public vault and the current withdraw proxy before calling `transferWithdrawReserve`. Here, `n` is the public vault's epoch. `Bn-1` and `Wn-1` should really represent the sum of all near-boundary auction payments the previous withdraw proxy receives plus any assets that are transferred to it by an external actor.

**Related Issue:** #46

## Recommendation
The current behavior of draining assets from the current withdraw proxy to the previous one is inconsistent compared to when assets are transferred from the public vault to the previous withdraw proxy, which:

- Updates the public vault's `s.withdrawReserve`.
- Transfers the assets.
- Updates the previous withdraw proxy's `withdrawReserveReceived`.

In the case of the `drain`, the first two points are performed, but the last one is missing. Based on the behavior and other calculations, it seems that `withdrawReserveReceived` would also need to be updated.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 4/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Zach Obront, Sawmon and Natalie, Blockdev, Noah Marconi |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review.pdf

### Keywords for Search

`Validation`

