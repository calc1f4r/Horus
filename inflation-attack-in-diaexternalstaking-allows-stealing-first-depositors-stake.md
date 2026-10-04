---
# Core Classification
protocol: DIA
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57914
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#2-inflation-attack-in-diaexternalstaking-allows-stealing-first-depositors-stake
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

Inflation Attack in `DIAExternalStaking` Allows Stealing First Depositor's Stake

### Overview


The `DIAExternalStaking` contract has a vulnerability that allows an attacker to exploit the `addRewardToPool` function and steal user's funds. This happens when an attacker stakes a minimum amount in an empty pool, then unstakes almost all of their tokens, and finally frontruns a victim's transaction to call `addRewardToPool` with the victim's deposit. This results in the victim receiving 0 shares in the pool and the attacker being able to repeat the attack on an empty pool. To fix this, it is recommended to add a non-zero shares minted requirement to the `_stake` function or restrict who can call `addRewardToPool`. The issue has already been fixed in a recent commit. 

### Original Finding Content

##### Description
This issue has been identified within the `DIAExternalStaking` contract.
The contract is vulnerable to a classic inflation attack due to the permissionless nature of the `addRewardToPool` function and the way pool shares are calculated. An attacker can exploit this as follows in newly deployed pool:

1. The attacker stakes in an empty pool the minimum allowed amount (`minimumStake`), receiving `minimumStake` share of the pool.
2. The attacker then unstakes almost all of their tokens, leaving only a single token (i.e., unstakes `minimumStake - 1`).
3. At this point, the total pool shares and the total supply are both equal to 1.
4. The attacker sees in the mempool a transaction of victim and frontruns it, calling `addRewardToPool()` with amount == victim_deposit.
5. After this step there is 1 share in the pool and victim_deposit + 1 stake. So victim receives:
`poolSharesGiven = (amount * totalShareAmount) / totalPoolSize = victim_deposit * 1 / (victim_deposit + 1) = 0` shares
6. The attacker can unstake funds and repeat the attack on an empty pool.

The issue is classified as **Critical** severity because it allows a malicious actor to steal user's funds.
<br/>
##### Recommendation
We recommend adding a non-zero shares minted requirement to the `_stake` function or add a special variable which will be passed to the function by the user to control for the minimum shares minted. Also, we recommend restricting who can call `addRewardToPool` function.

> **Client's Commentary:**
> Client: The issue has been fixed in commit https://github.com/diadata-org/lumina-staking/commit/95aca806165c15ab1826ff19cdac8104019f6fd9

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | DIA |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/DIA/Lumina%20Staking/README.md#2-inflation-attack-in-diaexternalstaking-allows-stealing-first-depositors-stake
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

