---
# Core Classification
protocol: Ondo RWA Internal
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55267
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Ondo-Spearbit-Security-Review-March-2025.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Ondo-Spearbit-Security-Review-March-2025.pdf
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
  - CarrotSmuggler
  - Anurag Jain
  - Desmond Ho
---

## Vulnerability Title

PSMSource.sol:availableToWithdraw does not check available USDS liquidity

### Overview

See description below for full details.

### Original Finding Content

## Severity: Low Risk

## Context 
PSMSource.sol#L187

## Description
The USDS peg stabilization module can be used to swap USDS for USDC tokens and vice versa at 1:1 ratios. The current USDS PSM actually just uses the older DAI PSM module underneath it. Thus, during a USDC to USDS swap, the following steps take place:

1. USDC is transferred from the user to the USDS PSM contract at `0xA188EEC8F81263234dA3622A406892F3D630f98c`.
2. The USDS PSM contract uses the USDC to buy DAI from the DAI PSM contract at `0xf6e72Db5454dd049d0788e411b06CfAF16853042`.
3. The DAI is then migrated to USDS.

Thus, this flow only works as long as there is enough DAI in the DAI PSM module. The `availableToWithdraw` in this contract, however, reports the amount of USDS available as the USDC balance of the contract itself. This can be incorrect in case not enough DAI is available in the PSM contracts. The `availableToWithdraw` reports a value higher than is actually available, which can lead to reverts in the Ondo token router contract since it always expects the reported available balance to be withdrawable.

## Recommendation
When reporting the available amount of USDS tokens, the amount of DAI available in the DAI PSM contract needs to be considered.

## Ondo Finance
Fixed in commit `89a5f6ad`.

## Spearbit
Fix verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Ondo RWA Internal |
| Report Date | N/A |
| Finders | CarrotSmuggler, Anurag Jain, Desmond Ho |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Ondo-Spearbit-Security-Review-March-2025.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Ondo-Spearbit-Security-Review-March-2025.pdf

### Keywords for Search

`vulnerability`

