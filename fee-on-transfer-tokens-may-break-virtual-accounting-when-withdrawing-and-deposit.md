---
# Core Classification
protocol: Vaultcraft
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45894
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-12-31-VaultCraft.md
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
  - Zokyo
---

## Vulnerability Title

Fee On Transfer Tokens May Break Virtual Accounting When Withdrawing And Depositing

### Overview


This bug report discusses an issue in DeFi tokenized vaults, where users can deposit tokens and earn yield. The problem arises when the contract tries to calculate the amount of tokens owed to the user during a withdrawal. This is caused by the use of virtual accounting, which can be affected by fees that can be enabled by token owners at any time. To fix this issue, it is recommended to check the balance of the deposited token before and after critical functions, such as depositing, withdrawing, redeeming, and minting. This can be done by using a modifier that can be accessed by multiple functions. The severity of this issue is medium and it has been acknowledged by the team.

### Original Finding Content

**Severity**: Medium	

**Status**: Acknowledged

**Description**

In DeFi tokenized vaults allow users to deposit their tokens and earn yield on those tokens deposited. These instances of ERC7540 make use of virtual accounting when attempting to calculate how many tokens are owed to the user when processing an asynchronous withdrawal. This is denoted in the internal _fulfillRedeem function within the BaseControlledAsyncRedeem contract when modifying claimable assets and shares as well as pending shares. Vault deposit and withdrawal work similarly to the ERC4626 standard however, commonly used tokens such as USDC and USDT have functionalities which enable those token owners to enable fees at any time which may cause breakages in the vault contract accounting.

**Recommendation**:

It is recommended that the balance of the deposited token is taken before and after critical function executions such as depositing, withdrawing, redeeming and minting to assert that the correct amount has in fact been transferred to the contract in addition to fees which may or may not exist. This could be done by using a modifier to make it widely accessible to multiple functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultcraft |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-12-31-VaultCraft.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

