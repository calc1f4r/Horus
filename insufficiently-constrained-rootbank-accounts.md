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
solodit_id: 48717
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

Insufficiently constrained RootBank accounts

### Overview


The report discusses a vulnerability in the Juiced Audit 04, where an attacker can exploit the system and make a profit of approximately 80 USDC. This is done by manipulating the deposit and withdraw functions, resulting in incorrect calculations and transfers. The report suggests verifying the root banks and storing the expected addresses in the Juiced account data or retrieving them from the mango_group account. The issue has been fixed in patch #576.

### Original Finding Content

## Juiced Audit 04 | Vulnerabilities

## Proof of Concept

Suppose a Juiced carton has 5,000 USDC in the sweeper vault, 5,000 USDC in the Mango account, and 10,000 minted pool tokens. Consider the following attack:

1. The attacker invokes deposit with the wBTC RootBank instead of the USDC RootBank, and transfers 10,000 USDC. The protocol mistakenly calculates the notional value to be ≈ 9,841 USDC. This corresponds with 10,000 pool tokens, so it mints ≈ 10,161 pool tokens to the attacker.
2. The attacker invokes withdraw with the correct USDC RootBank, and burns ≈ 10,161 pool tokens. The protocol calculates the notional value to be ≈ 20,000 USDC. This corresponds with 20,161 pool tokens, so it transfers ≈ 10,080 USDC to the attacker.

The attacker’s net profit is ≈ 80 USDC.

## Remediation

Verify that `usdc_root_bank` is the USDC root bank and `token_root_bank` is the BTC or SOL root bank (depending on the Juiced strategy). One option is to store the expected addresses in the Juiced account data. Another option is to retrieve them from the `mango_group` account, which is already verified properly.

## Patch

Fixed in #576.

© 2022 OtterSec LLC. All Rights Reserved. 10 / 23

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

