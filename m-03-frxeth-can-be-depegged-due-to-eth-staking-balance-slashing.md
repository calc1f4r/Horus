---
# Core Classification
protocol: Frax Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25440
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-09-frax
source_link: https://code4rena.com/reports/2022-09-frax
github_link: https://github.com/code-423n4/2022-09-frax-findings/issues/113

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
  - cdp
  - yield
  - services

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-03] frxETH can be depegged due to ETH staking balance slashing

### Overview


This bug report is about the risk of slashing penalty in Ethereum 2.0 PoS staking. If the ETH gets slashed, the frxETH will not be pegged and the validator cannot maintain a minimum 32 ETH staking balance. The team can either choose to subsidize this, or let it float. The recommended mitigation steps are to add a mechanism to ensure the frxETH is pegged via burning in case of slashing, and to consider who is in charge of adding the ETH balance to increase the staking balance or withdrawing the ETH and distributing the funds. The severity was decreased to Medium, as users should be aware that there is no mechanism built in to deal with slashing and that the asset backed guarantee isn't without some risk of slashing.

### Original Finding Content


The main risk in ETH 2.0 POS staking is the slashing penalty, in that case the frxETH will not be pegged and the validator cannot maintain a minimum 32 ETH staking balance.

<https://cryptobriefing.com/ethereum-2-0-validators-slashed-staking-pool-error/>

### Recommended Mitigation Steps

We recommend the protocol to add mechanism to ensure the frxETH is pegged via burning if case the ETH got slashed.

And consider when the node does not maintain a minimum 32 ETH staking balance, who is in charge of adding the ETH balance to increase the staking balance or withdraw the ETH and distribute the fund.

**[FortisFortuna (Frax) commented](https://github.com/code-423n4/2022-09-frax-findings/issues/113#issuecomment-1257364420):**
 > We as the team can either choose to subsidize this, or let it float. ETH 2.0 does not allow unstaking yet. When it eventually does, we will redeploy this minting contract with updated logic that may be helpful.

**[0xean (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-09-frax-findings/issues/113#issuecomment-1278289553):**
 > I think this is valid but should be downgraded to Medium.  Users should be aware that there is no mechanism built in to deal with slashing and that the asset backed guarantee isn't without some (perhaps negligible) risk of slashing. 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Frax Finance |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-09-frax
- **GitHub**: https://github.com/code-423n4/2022-09-frax-findings/issues/113
- **Contest**: https://code4rena.com/reports/2022-09-frax

### Keywords for Search

`vulnerability`

