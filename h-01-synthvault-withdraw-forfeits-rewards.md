---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 486
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-spartan-protocol-contest
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/168

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 1.00
financial_impact: high

# Scoring
quality_score: 5
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[H-01] SynthVault withdraw forfeits rewards

### Overview


A bug report has been submitted regarding the 'SynthVault.withdraw' function. It has been identified that this function does not claim the user's rewards, which decreases the user's weight and forfeits their accumulated rewards. Additionally, the 'synthReward' variable in '_processWithdraw' is never used. 

The impact of this bug is that a user that withdraws loses all their accumulated rewards. The recommended mitigation step is to claim the rewards with the user's deposited balance first in 'withdraw'.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

## Vulnerability Details

The `SynthVault.withdraw` function does not claim the user's rewards.
It decreases the user's weight and therefore they are forfeiting their accumulated rewards.
The `synthReward` variable in `_processWithdraw` is also never used - it was probably intended that this variable captures the claimed rewards.

## Impact
Usually, withdrawal functions claim rewards first but this one does not.
A user that withdraws loses all their accumulated rewards.

## Recommended Mitigation Steps
Claim the rewards with the user's deposited balance first in `withdraw`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 5/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/168
- **Contest**: https://code4rena.com/contests/2021-07-spartan-protocol-contest

### Keywords for Search

`Business Logic`

