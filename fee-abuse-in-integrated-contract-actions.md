---
# Core Classification
protocol: Mantle Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43403
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Mantle%20Network/cMETH/README.md#4-fee-abuse-in-integrated-contract-actions
github_link: none

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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Fee Abuse in Integrated Contract Actions

### Overview


This bug report is about a problem in the `DelayedWithdraw` contract of the cMETH-boring-vault project. The issue allows an attacker to manipulate the deposit and withdrawal processes to take advantage of fees and negatively affect the exchange rate for other users. The attack involves depositing a large amount, creating a withdrawal request, canceling it, and repeating the process. This causes inefficiencies and potential loss for regular users. The report recommends a solution to recalculate user shares when a withdrawal request is canceled or updated, preventing the attacker from unfairly earning yield.

### Original Finding Content

##### Description
This issue has been identified within the [cancelWithdraw](https://github.com/Se7en-Seas/cMETH-boring-vault/blob/d6e2d18f45a3e05d749d34966139fc85fc47f7e6/src/base/Roles/DelayedWithdraw.sol#525) and [requestWithdraw](https://github.com/Se7en-Seas/cMETH-boring-vault/blob/d6e2d18f45a3e05d749d34966139fc85fc47f7e6/src/base/Roles/DelayedWithdraw.sol#428) functions of the `DelayedWithdraw` contract.

The issue allows for a potential exploit where an attacker can manipulate the deposit and withdrawal processes to abuse fees and negatively affect the exchange rate for other users.

The attack involves the following steps:
1. The attacker deposits a large portion of the total value locked (TVL).
2. The attacker creates a withdrawal request.
3. The attacker waits until the protocol withdraws the underlying assets from the integrated protocol to fulfill the withdrawal request, then cancels the request.
4. After canceling the withdrawal, the attacker waits for the protocol to reallocate assets and repeats the process.

This cycle forces strategists to keep a significant portion of assets locked, which negatively impacts the yield for other users. Moreover, the attacker can exploit withdrawal and deposit fees from integrated contracts while continuing to earn yield, reducing the protocol’s efficiency and motivating users to withdraw their funds.

The issue is classified as **medium severity** because it impacts the protocol's overall performance, causing inefficiencies and potential loss for regular users.

##### Recommendation
We recommend recalculating user shares when a withdrawal request is canceled or updated by using the lower of the saved rate at the time of the request creation or the rate at the time of cancellation or updating. This would prevent the attacker from unfairly earning yield while canceling and recreating requests.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Mantle Network |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Mantle%20Network/cMETH/README.md#4-fee-abuse-in-integrated-contract-actions
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

