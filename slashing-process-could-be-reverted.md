---
# Core Classification
protocol: Forta Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10590
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/forta-protocol-audit/
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
  - services
  - liquidity_manager
  - leveraged_farming
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Slashing process could be reverted

### Overview


This bug report is about the FortaStaking contract from the Forta protocol. The SLASHER_ROLE role has the ability to slash a subject and all the users that have staked on it by calling the slash function. The value that should be taken from inactive and active stake is calculated and the slashed funds are transferred to the _treasury address.

However, if the _treasury address is set as zero either during the initialization of the contract or by the DEFAULT_ADMIN_ROLE role with the setTreasury function, the slashing mechanism will not work because the FORT token does not allow to transfer tokens to the zero address.

In order to prevent this potential issue, it is necessary to validate that the _treasury address is not zero when initializing the contract or when a new treasury address is being set. This issue has been fixed on commit b2c4d5aa398530d1ae5af14cf84eb438a377af5e in pull request 56.

### Original Finding Content

When a certain subject under-performed or has done actions against the correct operation of the protocol, the `SLASHER_ROLE` role can slash that subject and all the users that have staked on it by calling the [`slash` function](https://github.com/forta-protocol/forta-token/blob/92d7a7ddd6672a7530a4bfc532d0d697e7f12744/contracts/components/staking/FortaStaking.sol#L286) from the `FortaStaking` contract. After the [value that should be taken from inactive and active stake is computed](https://github.com/forta-protocol/forta-token/blob/92d7a7ddd6672a7530a4bfc532d0d697e7f12744/contracts/components/staking/FortaStaking.sol#L299-L300), the slashed funds are [transferred to the `_treasury` address](https://github.com/forta-protocol/forta-token/blob/92d7a7ddd6672a7530a4bfc532d0d697e7f12744/contracts/components/staking/FortaStaking.sol#L305).


However, if the `_treasury` address is being set as zero either during the [initialization](https://github.com/forta-protocol/forta-token/blob/92d7a7ddd6672a7530a4bfc532d0d697e7f12744/contracts/components/staking/FortaStaking.sol#L117) of the contract or by the `DEFAULT_ADMIN_ROLE` role with the [`setTreasury` function](https://github.com/forta-protocol/forta-token/blob/92d7a7ddd6672a7530a4bfc532d0d697e7f12744/contracts/components/staking/FortaStaking.sol#L493), the whole slashing mechanism will not work because the `FORT` token [does not allow to transfer tokens to the zero address](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/v4.4.2/contracts/token/ERC20/ERC20Upgradeable.sol#L233).


In order to prevent the possible reversion of the slashing process, consider always validating that the `_treasury` address is not zero when initializing the contract or when a new treasury address is being set.


***Update:** Fixed on [commit `b2c4d5aa398530d1ae5af14cf84eb438a377af5e` in pull request 56](https://github.com/forta-protocol/forta-token/pull/56/commits/b2c4d5aa398530d1ae5af14cf84eb438a377af5e).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Forta Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/forta-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

