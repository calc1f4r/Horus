---
# Core Classification
protocol: Omni X
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40429
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/c44dcd35-a8c7-446d-9e99-95a57974a979
source_link: https://cdn.cantina.xyz/reports/cantina_omnix_jun2024.pdf
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Emile Baizel
  - Sujith Somraaj
  - Denis Miličević
---

## Vulnerability Title

Fee calculation in _sendDeposits is done for overall msg.value instead of bridged value 

### Overview


The OmniXMultisender contract has a bug in its sendDeposits function that affects its ability to bridge gas tokens. This function is used to charge a 1% fee on all transfers, but the fee is mistakenly calculated based on the overall message value instead of just the bridged native token value. This can result in a higher fee being charged than intended. The impact of this bug is considered high and it is recommended that the fee logic be changed to only charge fees on the bridged native token value. The bug has been fixed in PR 13 and confirmed by Cantina Managed. This is a medium risk bug.

### Original Finding Content

## OmniXMultisender Contract Overview

## Context
`OmniXMultisender.sol#L288`

## Description
The **OmniXMultisender** contract implements a function `sendDeposits` to utilize Layerzero's native airdrop functionality to bridge gas tokens. 

To offer such a service, **OmniX** charges a flat **1% fee** on all transfers, which is discounted based on the number of **OmniX NFTs** the user holds.

In a deposit scenario, the `msg.value` includes two components: the value to pay Layerzero verification network (DVN) and the relayer fees, which also includes the native airdrop value. The fee calculation currently estimates **1%** based on the overall `msg.value`, thus potentially overestimating the fee.

## Impact
- **Likelihood:** HIGH
- **Impact:** HIGH  
This is considered a **HIGH severity** bug.

## Recommendation
Consider changing the fee logic to charge fees only on the bridged native token value instead of the overall `msg.value`, as it may account for more than **1%** of the fee collected.

## Status
- **OmniX:** Fixed in PR 13.
- **Cantina Managed:** Confirmed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Omni X |
| Report Date | N/A |
| Finders | Emile Baizel, Sujith Somraaj, Denis Miličević |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_omnix_jun2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/c44dcd35-a8c7-446d-9e99-95a57974a979

### Keywords for Search

`vulnerability`

