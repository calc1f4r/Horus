---
# Core Classification
protocol: Mochi
chain: everychain
category: economic
vulnerability_type: sandwich_attack

# Attack Vector Details
attack_type: sandwich_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 933
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-10-mochi-contest
source_link: https://code4rena.com/reports/2021-10-mochi
github_link: https://github.com/code-423n4/2021-10-mochi-findings/issues/65

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
  - sandwich_attack

protocol_categories:
  - dexes
  - cdp
  - cross_chain
  - rwa
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - jonah1005
---

## Vulnerability Title

[H-12] feePool is vulnerable to sandwich attack.

### Overview


This bug report is about a vulnerability in the FeePoolV0.sol function `distributeMochi`. This function is permissionless, meaning anyone can trigger it. This creates a vulnerability where an attacker can launch a sandwich attack with a flash loan to steal all the funds in the pool. This is considered a high-risk issue due to the potential for large losses. As examples of similar issues, the report references the yDai Incident and the Mushrooms-finance-theft incident. To mitigate this vulnerability, the dev should add a slippage control to the contract to calculate a minimum return based on a Time Weighted Average Price (TWAP).

### Original Finding Content

## Handle

jonah1005


## Vulnerability details

## Impact
There's a permissionless function `distributeMochi` in FeePoolV0. Since everyone can trigger this function, an attacker can launch a sandwich attack with flashloan to steal the funds.
[FeePoolV0.sol#L55-L62](https://github.com/code-423n4/2021-10-mochi/blob/main/projects/mochi-core/contracts/feePool/FeePoolV0.sol#L55-L62)
The devs have mentioned this concern in the comment. An attacker can steal the funds with a flash loan attack. 

Attackers can steal all the funds in the pool. I consider this is a high-risk issue. 

## Proof of Concept
[FeePoolV0.sol#L55-L62](https://github.com/code-423n4/2021-10-mochi/blob/main/projects/mochi-core/contracts/feePool/FeePoolV0.sol#L55-L62)

Please refer to [yDai Incident](https://peckshield.medium.com/the-ydai-incident-analysis-forced-investment-2b8ac6058eb5) to check the severity of a `harvest` function without slippage control.

Please refer to [Mushrooms-finance-theft]( https://medium.com/immunefi/mushrooms-finance-theft-of-yield-bug-fix-postmortem-16bd6961388f) to check how likely this kind of attack might happen.

## Tools Used

None

## Recommended Mitigation Steps
If the dev wants to make this a permissionless control, the contract should calculate a min return based on TWAP and check the slippage.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mochi |
| Report Date | N/A |
| Finders | jonah1005 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-10-mochi
- **GitHub**: https://github.com/code-423n4/2021-10-mochi-findings/issues/65
- **Contest**: https://code4rena.com/contests/2021-10-mochi-contest

### Keywords for Search

`Sandwich Attack`

