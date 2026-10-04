---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28139
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#1-possible-blocking-of-the-contract
github_link: none

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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Possible blocking of the contract

### Overview


This bug report is about the code in the line https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.8.9/DepositSecurityModule.sol#L123. The problem is that the `owner` variable is initialized without checking the new value of the variable. If the value of the variable is equal to zero, then certain functions will stop working. These functions include `setOwner()`, `setNodeOperatorsRegistry()`, `setPauseIntentValidityPeriodBlocks()`, `setMaxDeposits()`, `setMinDepositBlockDistance()`, `setGuardianQuorum()`, `addGuardian()`, `addGuardians()`, `removeGuardian()`, and `unpauseDeposits()`.

The recommendation to fix this bug is to add a check for the value of the `newValue` variable to zero before initializing the `owner` variable. This way, the functions that rely on the `owner` variable will continue to work properly.

### Original Finding Content

##### Description
At the line 
https://github.com/lidofinance/lido-dao/blob/5b449b740cddfbef5c107505677e6a576e2c2b69/contracts/0.8.9/DepositSecurityModule.sol#L123 
initializes the `owner` variable without checking the new value of the variable.
If the value of the variable is equal to zero, then the following functions will stop working:
`setOwner()`, `setNodeOperatorsRegistry()`, `setPauseIntentValidityPeriodBlocks()`, `setMaxDeposits()`,
`setMinDepositBlockDistance()`, `setGuardianQuorum()`, `addGuardian()`, `addGuardians()`, `removeGuardian()`, `unpauseDeposits()`.
##### Recommendation
It is necessary to add a check for the value of the `newValue` variable to zero before initializing the `owner` variable.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Lido |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Lido/Deposit%20Security%20Module/README.md#1-possible-blocking-of-the-contract
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

