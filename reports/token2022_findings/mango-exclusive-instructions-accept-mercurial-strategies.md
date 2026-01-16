---
# Core Classification
protocol: Juiced
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48718
audit_firm: OtterSec
contest_link: https://juiced.fi/
source_link: https://juiced.fi/
github_link: github.com/juiced-fi/juiced-protocol.

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
  - Harrison Green
  - OtterSec
  - William Wang
---

## Vulnerability Title

Mango-exclusive instructions accept Mercurial strategies

### Overview


This bug report discusses a vulnerability in the Juiced Audit 04 protocol. The bug allows an attacker to withdraw 20,000 pool tokens and receive 13,330 USDC, resulting in a net profit of 3,330 USDC. The suggested solution is to explicitly require the strategy to be either BtcMangoFunding or SolMangoFunding in the deposit and withdraw instructions, and BtcMangoMercurial or SolMangoMercurial in the deposit_mercurial and withdraw_mercurial instructions. The bug has been fixed in issue #579.

### Original Finding Content

## Juiced Audit 04 | Vulnerabilities

2. The attacker invokes `withdraw_mercurial` and burns 20,000 pool tokens. The protocol calculates the notional value to be 19,995 USDC. This corresponds with 30,000 pool tokens, so it transfers ≈ 13,330 USDC to the attacker.  
   The attacker’s net profit is ≈ 3,330 USDC.

## Remediation
In the deposit and withdraw instructions, explicitly require the strategy to be `BtcMangoFunding` or `SolMangoFunding`. In the `deposit_mercurial` and `withdraw_mercurial` instructions, explicitly require the strategy to be `BtcMangoMercurial` or `SolMangoMercurial`.

## Patch
Fixed in #579.

© 2022 OtterSec LLC. All Rights Reserved. 12 / 23

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Juiced |
| Report Date | N/A |
| Finders | Harrison Green, OtterSec, William Wang |

### Source Links

- **Source**: https://juiced.fi/
- **GitHub**: github.com/juiced-fi/juiced-protocol.
- **Contest**: https://juiced.fi/

### Keywords for Search

`vulnerability`

