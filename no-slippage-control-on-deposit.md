---
# Core Classification
protocol: Filament
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45614
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
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
finders_count: 1
finders:
  - Zokyo
---

## Vulnerability Title

No Slippage Control On Deposit

### Overview


This bug report describes an issue with the addLiquidity function when using USDC in the lp token contract. The problem is that the number of shares received by the user may be different than expected if there are withdrawals or deposits happening at the same time. The severity of this issue is high, but it has been marked as invalid. A recommendation to fix this problem is to have slippage control on vault deposits.

### Original Finding Content

**Severity** - High

**Status** - Invalid

**Description**

When adding liquidity (addLiquidity function) USDC is deposited into the lp token contract which is similar to an ERC4626 vault . It is possible that in the period between the user submitting an addLiquidity transaction and that transaction getting included in a block, the number of shares expected could change (due to withdrawals/deposits) and that can cause the user to receive fewer shares than expected.

**Recommendation**:

Have slippage control on vault deposits.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Filament |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-08-15-Filament.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

