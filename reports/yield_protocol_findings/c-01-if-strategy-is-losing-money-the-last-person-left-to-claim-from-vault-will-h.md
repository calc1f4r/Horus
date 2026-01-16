---
# Core Classification
protocol: Protectorate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20626
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-Protectorate.md
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
  - Pashov
---

## Vulnerability Title

[C-01] If strategy is losing money the last person left to claim from vault will handle all losses

### Overview


This bug report outlines a potential issue with the `LendingVault` system. If funds are transferred out to chosen strategies and users can still withdraw funds from the vault's balance, the following scenario can occur: Alice, Bob, and Chris deposit funds into the vault. The strategy requests 200 ETH from the vault. Bob sees that the strategy is not doing well and withdraws his share, leaving the vault with 100 ETH balance and the strategy with 0 balance. As a result, Alice and Chris bear all of the loss of the strategy, while Bob gets 100% of his initial deposit. This has a high impact, as users bear substantial value losses, and a high likelihood, as it is possible that the strategy is losing money at a given time.

To address this issue, it is recommended that withdraws be forbidden while funds are lent out to a strategy, or another design for Vault-Strategy lending be considered.

### Original Finding Content

**Impact:**
High, as some users will bear substantial value losses

**Likelihood:**
High, as it is possible that strategy is losing money at a given time

**Description**

Currently, the way that `LendingVault` is designed, is that the funds in the vault are transferred out to chosen strategies. Due to the fact that users can still withdraw funds from the vault's balance while some of the funds are lent out to a strategy, the following scenario can happen:

1. Alice deposits 100 ETH to the Vault
2. Bob deposits 100 ETH to the Vault
3. Strategy requests 200 ETH from the Vault - now Vault balance is 0, Strategy balance is 200
4. Chris deposits 100 ETH to the Vault
5. Strategy is not doing good and is left with 100 ETH balance
6. Bob sees this, and withdraws his share, which is 100 ETH
7. Now the strategy is losing but funds are returned back, leaving the Vault with 100 ETH balance and Strategy with 0 balance
8. Now Alice and Chris will bear all of the loss of the strategy, while Bob managed to get 100% of his initial deposit despite of the loss.

**Recommendations**

Possibly forbid withdraws while funds are lent out to a strategy or think of another design for Vault-Strategy lending.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Protectorate |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-06-01-Protectorate.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

