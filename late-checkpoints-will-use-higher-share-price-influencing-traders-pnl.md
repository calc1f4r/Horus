---
# Core Classification
protocol: Hyperdrive June 2023
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 35868
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
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
finders_count: 4
finders:
  - Saw-Mon and Natalie
  - Christoph Michel
  - Deivitto
  - M4rio.eth
---

## Vulnerability Title

Late checkpoints will use higher share price, influencing traders' PnL

### Overview


The bug report describes a medium risk bug in the Hyperdrive.sol code at line 67. The issue occurs when the checkpoint() function is called for a checkpoint in the past. Instead of using the correct share price, the code looks for the next checkpoint with a higher share price and retroactively applies it. This can result in incorrect share prices for both long and short positions, leading to losses or profits compared to closing them directly at maturity. The recommendation is to call checkpoint() during each checkpoint's time window and consider interpolating the share price between the closest older and newer checkpoints to simulate linear interest gains.

### Original Finding Content

## Severity: Medium Risk

## Context
Hyperdrive.sol#L67

## Description
Calling the `checkpoint(_checkpointTime)` function for a checkpoint in the past will look for the next checkpoint higher than `_checkpointTime`, then retroactively apply the later checkpoint's share price to it:

- Under normal circumstances, the earlier checkpoint would have a smaller share price (as the yield source has generated less interest up to this point).
- This closes longs/shorts at the higher share price. For example, in `calculateCloseLong`, the trader would receive fewer `shareProceeds`. The protocol essentially stops accruing interest for the trader's long position upon maturity. When closing shorts, this can influence both the `openSharePrice` and `closeSharePrice` in `closeShort` and lead to losses/profits compared to closing them directly at maturity.

## Recommendation
Ensure that `checkpoint()` is called during each checkpoint's time window to lock in a more accurate, current share price. Think about interpolating the share price between the closest older one and the closest newer one. This would simulate linear interest gains during that period for the underlying yield source.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Hyperdrive June 2023 |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Christoph Michel, Deivitto, M4rio.eth |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Delv-Spearbit-Security-Review-June-2023.pdf

### Keywords for Search

`vulnerability`

