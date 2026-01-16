---
# Core Classification
protocol: Marco Polo
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48591
audit_firm: OtterSec
contest_link: https://marcopolo.so/
source_link: https://marcopolo.so/
github_link: https://github.com/marcopolo-org/Dex

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
  - Akash Gurugunti
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Incorrect Farm Reward Distribution

### Overview


The report discusses a bug in a system where rewards for a provider are not properly accumulated and distributed when there is a change in the provider's share amount. This results in the provider not receiving the correct amount of rewards when they withdraw their shares. The bug has been identified and fixed in the system's code.

### Original Finding Content

## Provider Rewards Accumulation

The rewards for a provider are accumulated using the `farm.update_accumulator` function into the `farm.accumulated_seconds_per_share`. Whenever there is a change in the share amount, the reward amount that is collected up to that point should be either stored somewhere or transferred to the provider.

## Proof of Concept

Consider the following scenario:

1. A pool and a farm are initiated by the admin.
2. A provider is created by a user with some initial tokens.
3. After some time, the user withdraws 90% of his shares.
4. Now if the user tries to withdraw the remaining 10% of his shares, he will only get rewards for 10% of his shares.

## Remediation

The rewards should be calculated and distributed whenever there is a change in the provider shares, i.e., in `add_tokens` and `withdraw_shares`.

## Patch

Resolved in commits `39431e3`, `a7e042d`, and `c249da4`.

© 2022 OtterSec LLC. All Rights Reserved. 8 / 23

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Marco Polo |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, OtterSec |

### Source Links

- **Source**: https://marcopolo.so/
- **GitHub**: https://github.com/marcopolo-org/Dex
- **Contest**: https://marcopolo.so/

### Keywords for Search

`vulnerability`

