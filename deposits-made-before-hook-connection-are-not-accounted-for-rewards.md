---
# Core Classification
protocol: Euler
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55525
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Euler/HookTargetStakeDelegator/README.md#2-deposits-made-before-hook-connection-are-not-accounted-for-rewards
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Deposits Made Before Hook Connection are not Accounted for Rewards

### Overview


The `HookTargetStakeDelegator` contract has a bug that affects users who have made deposits before the hook was connected. Their rewards are not properly accounted for until they withdraw and redeposit their funds. The recommended solution is to implement a migration process, but the client says this is not possible due to potential issues with rewards overlap. They prefer that users manually withdraw and redeposit their funds to avoid any problems.

### Original Finding Content

##### Description
This issue has been identified within the `HookTargetStakeDelegator` contract. When the hook is connected after deposits have been made, the reward vault balance is not properly initialized. As a result, any funds that were deposited before the hook connection cannot be accounted for in the rewards system until they are fully withdrawn and redeposited. This creates a situation where users who deposited before the hook connection will not receive rewards for their existing deposits, effectively losing potential rewards until they perform a complete withdrawal and redeposit cycle.
<br/>
##### Recommendation
We recommend implementing a migration process that can be triggered by users (only account owners) to properly account for their existing deposits without requiring a full withdrawal and redeposit cycle. This process should:
   - Check if the account has already performed migration (using a mapping to track migration status)
   - If not migrated, read the account's current balance in eVault
   - Compare it with the `rewardVault's` balance and add the difference to the balance of the account's owner
   - Mark the account as migrated to prevent double initialization

The migration process should be automatically invoked if an account with an unsynced balance in the EVault and RewardVault is met.

> **Client's Commentary:**
> We acknowledge the scenario described in the audit and have considered it during the design of the smart contract. Unfortunately, the recommended solution is not feasible. The vaults on which the `HookTargetStakeDelegator` will be installed are already participating in the Proof of Liquidity (POL) and allow their shares (ETokens) to be staked in the Reward Vaults. The installation of the `HookTargetStakeDelegator` on the vault will initiate a transition period where rewards will cease flowing to the EToken Reward Vaults and will start flowing to the `ERC20ShareRepresentation` Reward Vaults. Depending on how this process is executed, there is a possibility of rewards overlap, which could lead to a situation where part of the users' stake is counted twice - once in the EToken Reward Vaults and once in the `ERC20ShareRepresentation` Reward Vaults. To avoid potential issues arising from this, we prefer that users manually migrate their stake by first withdrawing (which enforces unstaking in the EToken Reward Vaults) and then redepositing (which will automatically delegate stake in the `ERC20ShareRepresentation` Reward Vaults).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Euler |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Euler/HookTargetStakeDelegator/README.md#2-deposits-made-before-hook-connection-are-not-accounted-for-rewards
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

