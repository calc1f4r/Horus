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
solodit_id: 35863
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

LP funds can be locked up cheaply at low-interest rates

### Overview


This bug report describes a medium risk issue with the HyperdriveShort.sol code, specifically on line 79. The problem is that when opening shorts, LPs (liquidity providers) may end up providing the base part of the bonds at the current price, while traders only pay the implied fixed interest. This means that LP funds are locked up and cannot be redeemed directly for the base asset, only for withdrawal shares that are slowly converted. This creates a large ratio of trader funds paid and LP funds locked up, especially when the fixed interest rate is low. This can be exploited in a griefing attack, where a large percentage of LP funds can be locked up by opening shorts at low interest rates. The report suggests that this issue may also occur naturally due to circumstances in the underlying protocol. The recommendation is to potentially adjust pool configuration parameters to reduce the impact of this issue, but it may require a redesign of how shorts work in the protocol. 

### Original Finding Content

## Medium Risk Alert

**Severity:** Medium Risk  
**Context:** HyperdriveShort.sol#L79  

## Description
Opening shorts can be seen as LPs providing the base part of the bonds at the current price and traders paying only the implied fixed interest part on them. The LP funds are locked up (technically removed from the reserves until the shorts are closed) and LP shares cannot directly be redeemed for the base asset anymore, only for withdrawal shares that are slowly converted as LPs receive their proceeds. The ratio of trader funds paid and LP funds locked up is especially large when the fixed interest rate is low.

This allows a griefing attack where a large percentage of LP funds can be locked up by opening shorts at low-interest rates. This can also happen naturally when circumstances in the underlying protocol lead to many shorts being opened.

## Recommendation
It's not clear how to fix this issue without redesigning how shorts work in the protocol. There are some pool configuration parameters that might reduce the impact of the issue, for example, keeping the position durations short.

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

