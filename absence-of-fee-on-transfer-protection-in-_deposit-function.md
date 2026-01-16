---
# Core Classification
protocol: Enjoyoors
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49877
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Enjoyoors/EVM%20Vaults/README.md#1-absence-of-fee-on-transfer-protection-in-_deposit-function
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

Absence of Fee-on-transfer Protection in `_deposit` Function

### Overview


This bug report is about a problem found in the `_deposit` function of the `EnjoyoorsVaultDeposits` contract. The issue is that there is no protection in place for transfer fees, which can lead to incorrect allocation of user amounts. This can result in users claiming more than they are entitled to, and can ultimately cause the contract to break down. The severity of this issue is classified as medium. The recommendation is to add a fee-on-transfer protection in the function by checking the token balance before and after the transfer, and also adding a `nonReentrant` check to prevent any potential attacks. 

### Original Finding Content

##### Description
An oversight has been detected within the `_deposit` function of the `EnjoyoorsVaultDeposits` contract. 

The issue arises from the absence of a fee-on-transfer protection mechanism. This could result in incorrect setting of user amounts. Consequently, users might be in a position to claim more than they are entitled to. It gravely threatens the contract's integrity since this scenario inevitably leads to a situation where the last user cannot claim any funds, given there are insufficient funds on the contract due to the over-claims made by the preceding users.

This issue is classified as **Medium** severity due to its potential to distort the distribution of deposits and consequently funds, which could lead to the breakdown of the contract's operation.

##### Recommendation
We strongly suggest the addition of a fee-on-transfer protection within the `_deposit` function. This would ensure the correct amount is allocated to the user upon executing a deposit transaction, especially for tokens with transfer fees. This can be done by adding balance checks for the token before and after the `transferFrom` call. Note that it is crucial to add a `nonReentrant` check to protect the function from the reentrancy attack.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Enjoyoors |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Enjoyoors/EVM%20Vaults/README.md#1-absence-of-fee-on-transfer-protection-in-_deposit-function
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

