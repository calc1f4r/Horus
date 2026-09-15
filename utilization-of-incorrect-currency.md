---
# Core Classification
protocol: Adrena
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46813
audit_firm: OtterSec
contest_link: https://www.adrena.xyz/
source_link: https://www.adrena.xyz/
github_link: https://github.com/AdrenaDEX/adrena

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
finders_count: 2
finders:
  - Robert Chen
  - Tamta Topuria
---

## Vulnerability Title

Utilization of Incorrect Currency

### Overview

See description below for full details.

### Original Finding Content

## Add Genesis Liquidity Instruction Discrepancy

In the `add_genesis_liquidity` instruction, `custody.volume_stats.add_liquidity_usd` is incremented by the token amount (amount of USDC deposited). However, in the `add_liquidity` instruction, the same variable is incremented by the USD value of the token amount (considering the token price). This discrepancy creates an inconsistency in how the total USD value of added liquidity is tracked. Since `add_genesis_liquidity` currently only deals with USDC (stablecoin pegged to USD), the immediate impact will be minimal as the token amount and USD value are practically the same. Nevertheless, USD and USDC prices may not always align.

## Remediation

Update the `add_genesis_liquidity` instruction to also utilize the USD value of the deposited USDC to maintain consistency with `add_liquidity`.

### Patch

Resolved in b62b257a

© 2024 Otter Audits LLC. All Rights Reserved. 48/59

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Adrena |
| Report Date | N/A |
| Finders | Robert Chen, Tamta Topuria |

### Source Links

- **Source**: https://www.adrena.xyz/
- **GitHub**: https://github.com/AdrenaDEX/adrena
- **Contest**: https://www.adrena.xyz/

### Keywords for Search

`vulnerability`

