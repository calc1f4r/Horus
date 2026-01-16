---
# Core Classification
protocol: Sonic Gateway Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 43957
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/sonic-gateway-audit
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
  - OpenZeppelin
---

## Vulnerability Title

User-Provided Deposit and Withdraw IDs Can Cause Collisions

### Overview


The Bridge and TokenDeposit contracts have a design flaw where they rely on users to provide unique IDs for claiming and withdrawal operations. This can result in multiple users submitting transactions with the same ID, which can be done intentionally by malicious users. This can cause a denial of service for a particular account by front-running its transaction with the same ID. To prevent this, it is suggested to implement an internal unique ID generation mechanism.

### Original Finding Content

The [`Bridge`](https://github.com/Fantom-foundation/Bridge/blob/558465d3aba2ffae1a4436a2fc14c723b82926df/contracts/Bridge.sol#L13) and [`TokenDeposit`](https://github.com/Fantom-foundation/Bridge/blob/558465d3aba2ffae1a4436a2fc14c723b82926df/contracts/TokenDeposit.sol#L17) contracts rely on users to provide unique IDs for claiming and withdrawal operations, as they lack an internal mechanism to generate unique IDs. This design can result in multiple users submitting a transaction with the same ID, either by mistake or even on purpose by malicious users, who then monitor the pending transactions and submit a transaction with the same ID before the original transaction is processed. Since the contract requires each ID to be unique, after the first transaction with a specific ID, all other transactions with the same ID will fail. This can be abused to cause a denial of service for a particular account by front\-running its transaction with the same ID.


Consider implementing an internal unique ID generation mechanism to prevent ID collisions and mitigate front\-running vulnerabilities.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Sonic Gateway Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/sonic-gateway-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

