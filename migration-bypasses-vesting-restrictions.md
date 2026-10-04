---
# Core Classification
protocol: Qiibee Token Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11946
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/qiibee-token-audit-b19c03262f99/
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

protocol_categories:
  - dexes
  - services
  - indexes
  - leveraged_farming
  - payments

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Migration bypasses vesting restrictions

### Overview


This bug report is about the Qiibee Token contract, which allows all users to migrate their tokens to a new contract regardless of whether their assets are fully transferable or locked in a vesting scheme. This can cause issues since any vesting restrictions are removed during the migration process. 

The recommended solution is to only allow transferable tokens to be available for migrations. An alternative solution is to create a new migrateVestedTokens function that will copy the vesting configuration to the migration target contract. 

The bug has been fixed in a commit by checking if the amount of tokens is within the transferableTokens limit at the moment of migration.

### Original Finding Content

All of the users are allowed to [`migrate`](https://github.com/qiibee/qb-contracts/blob/d40368c9a7a536572a5bb03cb031d658ccb34f24/contracts/QiibeeToken.sol#L109) their tokens to a new contract regardless of whether their assets are fully transferable or locked in a vesting scheme. Moreover, once they migrate the tokens any vesting restrictions are removed.


We recommend only allowing `transferableTokens` to be available for migrations. An alternative solution is to implement a new `migateVestedTokens` function that will copy the vesting configuration to the migration target contract.


***Update:** Fixed in [this](https://github.com/qiibee/qb-contracts/commit/25efdbf5bc29de12a724450c540218f6c8e59129) commit by [checking](https://github.com/qiibee/qb-contracts/blob/25efdbf5bc29de12a724450c540218f6c8e59129/contracts/QiibeeToken.sol#L120) if the amount of tokens is within the `transferableTokens` limit at the moment of migration.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Qiibee Token Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/qiibee-token-audit-b19c03262f99/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

