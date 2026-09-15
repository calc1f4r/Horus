---
# Core Classification
protocol: Aera Contracts v3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58299
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review-April-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review-April-2025.pdf
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
  - Slowfi
  - Eric Wang
  - High Byte
---

## Vulnerability Title

Renouncing Ownership May Leave Vault and Fee Calculator in an Unmanageable State

### Overview


This report discusses a bug found in the `MultiDepositorVault` and `FeeVault` contracts. These contracts currently allow for the ownership to be renounced, which was previously used to finalize setup and operate in a permissionless mode. However, with the introduction of new functionality, this can lead to critical administrative functions becoming inaccessible. The recommendation is to either override the `renounceOwnership()` function or add a protocol-level safeguard to prevent this issue. The bug has been fixed in PR 340.

### Original Finding Content

## Severity: Medium Risk

## Context
(No context files were provided by the reviewers)

## Description
The current design allows ownership of `MultiDepositorVault` (and possibly `FeeVault`) to be renounced using the inherited `renounceOwnership()` function from `Auth2Step`. This was previously a valid pattern to allow protocols to "finalize" their vault setup and operate in a fully permissionless mode, relying only on the guardian root and whitelist for constraint enforcement.

However, with the introduction of new functionality in the `PriceAndFeeCalculator` contract — such as `setVaultPaused`, `resetHighestPrice`, and potentially other fee- or price-sensitive administrative controls — ownership is now required for core maintenance actions that affect safety and accounting. If `renounceOwnership()` is called, these paths become permanently inaccessible, which may prevent the vault from pausing in abnormal conditions or recovering from mispriced valuations.

## Recommendation
To avoid accidentally locking out critical administrative functions, consider overriding `renounceOwnership()` in `MultiDepositorVault` (and `FeeVault`, if applicable) to revert. Alternatively, add a protocol-level safeguard, such as a boolean flag `canRenounceOwnership` that must be explicitly disabled by governance before renouncing becomes possible.

If preserving the option for decentralization is important, documenting the risks clearly and requiring an explicit function to “seal” the vault may provide better UX than relying on `renounce` alone.

## Aera
Fixed on PR 340 by removing `renounceOwnership` function.

## Spearbit
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Aera Contracts v3 |
| Report Date | N/A |
| Finders | Slowfi, Eric Wang, High Byte |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review-April-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Gauntlet-Spearbit-Security-Review-April-2025.pdf

### Keywords for Search

`vulnerability`

