---
# Core Classification
protocol: GooseFX v2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47701
audit_firm: OtterSec
contest_link: https://www.goosefx.io/
source_link: https://www.goosefx.io/
github_link: https://github.com/GooseFX1/gfx-ssl-v2

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
finders_count: 4
finders:
  - OtterSec
  - Robert Chen
  - Ajay Kunapareddy
  - Thibault Marboud
---

## Vulnerability Title

Account Validation

### Overview

See description below for full details.

### Original Finding Content

## Vulnerability Report

The program does not ensure that trusted entities like Pyth or Switchboard own oracle accounts, opening up the possibility of malicious actors creating `PoolRegistry` and pairs with unauthorized or tampered oracle accounts. Malicious actors may create fake oracle accounts or tamper with existing ones, providing inaccurate price information to the single-sided liquidity pools. This may result in incorrect pricing calculations within the protocol.

Furthermore, `CrankPriceHistories.process` fails to verify whether the `OraclePriceHistory` account, represented by `price_history`, belongs to the expected pool in the `pool_registry` passed in as part of the instructions accounts.

## Remediation

Implement thorough ownership checks for oracle accounts where only trusted or authorized entities may provide price information. Additionally, verify that each `OraclePriceHistory` account corresponds to a valid SSL pool according to the `pool_registry` account passed in the instruction.

## Patch

Fixed in `ee572ad`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | GooseFX v2 |
| Report Date | N/A |
| Finders | OtterSec, Robert Chen, Ajay Kunapareddy, Thibault Marboud |

### Source Links

- **Source**: https://www.goosefx.io/
- **GitHub**: https://github.com/GooseFX1/gfx-ssl-v2
- **Contest**: https://www.goosefx.io/

### Keywords for Search

`vulnerability`

