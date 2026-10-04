---
# Core Classification
protocol: BadgerDAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1048
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-badgerdao-zaps-contest
source_link: https://code4rena.com/reports/2021-11-badgerzaps
github_link: https://github.com/code-423n4/2021-11-badgerzaps-findings/issues/71

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

protocol_categories:
  - liquid_staking
  - dexes
  - bridge
  - cdp
  - yield

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WatchPug
  - gzeon
---

## Vulnerability Title

[M-05] No slippage control on deposit of IbbtcVaultZap.sol

### Overview


A bug was found in the IbbtcVaultZap.sol smart contract, which is part of the Badger-Finance/badger-ibbtc-utility-zaps repository. The bug causes a lack of slippage control on the `deposit` function, which exposes users to a sandwich attack. A sandwich attack is when an attacker can "sandwich" a deposit between two other transactions, potentially resulting in the user losing funds. This can be especially dangerous when the pool is not balanced.

The bug was identified by the handle gzeon and proof of concept can be found at the provided GitHub link. The recommended mitigation step to fix the bug is to add a _minOut in line with the mint function of other contacts, and pass it as a parameter on line 174 of IbbtcVaultZap.sol. This should help to prevent a sandwich attack and protect users from potential losses.

### Original Finding Content

## Handle

gzeon


## Vulnerability details

## Impact
There is no slippage control on `deposit` of IbbtcVaultZap.sol, which expose user to sandwich attack.

## Proof of Concept
https://github.com/Badger-Finance/badger-ibbtc-utility-zaps/blob/6f700995129182fec81b772f97abab9977b46026/contracts/IbbtcVaultZap.sol#L174
Any deposit can be sandwiched, especially when the pool is not balanced.

## Tools Used

## Recommended Mitigation Steps
Add a _minOut in line with the mint function of other contacts, and pass it as a parameter on L174

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | BadgerDAO |
| Report Date | N/A |
| Finders | WatchPug, gzeon |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-badgerzaps
- **GitHub**: https://github.com/code-423n4/2021-11-badgerzaps-findings/issues/71
- **Contest**: https://code4rena.com/contests/2021-11-badgerdao-zaps-contest

### Keywords for Search

`vulnerability`

