---
# Core Classification
protocol: Cosmos LSM
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46748
audit_firm: OtterSec
contest_link: https://cosmos.network/
source_link: https://cosmos.network/
github_link: https://github.com/cosmos/cosmos-sdk

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
  - James Wang
  - Robert Chen
  - Tuyết Dương
---

## Vulnerability Title

Slash Evasion Through Liquid Staking

### Overview

See description below for full details.

### Original Finding Content

## Tokenizing Shares and Redeeming Tokens for Shares

**Process Overview:**

TokenizeShares and RedeemTokensForShares immediately unbond, followed by a Delegate call. As a result, they do not track the old delegation in the UndelegationQueue or RedelegationQueue. 

The UndelegationQueue and RedelegationQueue are mechanisms that track unbonded or redelegated shares, ensuring they remain slashable if the validator commits an infraction during the lock-in period. By skipping these queues, any infractions committed by the validator after the shares are unbonded will not affect the shares that were tokenized or redeemed.

## Remediation

- Add a record to track liquid-staking-related delegation movements for future slashing.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Cosmos LSM |
| Report Date | N/A |
| Finders | James Wang, Robert Chen, Tuyết Dương |

### Source Links

- **Source**: https://cosmos.network/
- **GitHub**: https://github.com/cosmos/cosmos-sdk
- **Contest**: https://cosmos.network/

### Keywords for Search

`vulnerability`

