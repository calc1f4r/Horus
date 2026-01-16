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
solodit_id: 47697
audit_firm: OtterSec
contest_link: https://www.goosefx.io/
source_link: https://www.goosefx.io/
github_link: https://github.com/GooseFX1/gfx-ssl-v2

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
  - OtterSec
  - Robert Chen
  - Ajay Kunapareddy
  - Thibault Marboud
---

## Vulnerability Title

Fee Locking

### Overview


This bug report discusses an issue in the CreateSsl::process function where the addition of an initial deposit to the SSLPool leads to a portion of the fee from swap rewards being locked in the pool_fee_vault. This results in the fee related to the initial deposit remaining unclaimed and the initial transfer of the deposit to the pool_fee_vault being unnecessary. The report suggests avoiding adding the initial deposit to the total_liquidity_deposits if it is not meant to be included in fee calculations. This issue has been fixed in the latest patch.

### Original Finding Content

## Issues with SSLPool Fee Calculation

In `CreateSsl::process`, the addition of `initial_pool_deposit` to `SSLPool.total_liquidity_deposits` results in the locking of a portion of the fee from all swap rewards in `pool_fee_vault`. This is problematic since the rewards are later divided by `total_liquidity_deposits`, and the initial deposit (no authority exists) becomes part of this calculation. As a result, the fee part related to the initial deposit remains unclaimed. Additionally, the initial transfer of the `initial_pool_deposit` to the `pool_fee_vault` seems unnecessary, especially if it contributes to the abovementioned issue.

## Proof of Concept

1. An SSL pool is created with an initial deposit of 100 tokens (`initial_pool_deposit = 100`).
2. The `total_liquidity_deposits` in `SSLPool` is updated to 100.
3. Swaps occur in the system, and fees accumulate in the `pool_fee_vault`.
4. The fee calculation involves dividing rewards by the `total_liquidity_deposits`, including the initial deposit.
5. The fee part related to the `initial_pool_deposit` remains unclaimed as it is locked in the `pool_fee_vault`, and there is no authority to claim it.

## Remediation

Avoid adding `initial_pool_deposit` to `SSLPool.total_liquidity_deposits` if it is not meant to be part of the liquidity contributing to fee calculations.

## Patch

Fixed in `ee572ad`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

