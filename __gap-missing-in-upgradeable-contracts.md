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
solodit_id: 10584
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

__gap missing in upgradeable contracts

### Overview


This bug report discusses two contracts, VestingWallet and VestingWalletV2, which are upgradeable but do not contain a __gap variable. A __gap variable is necessary to manage storage collisions when upgrading the Vesting Wallet. To prevent errors, the report suggests implementing quality control steps such as checking all __gap variables before pushing code commits, leaving comments next to variables, and implementing a predictable inheritance structure for all contracts. The bug was fixed in commit 9b37ac5d4b852954552c69e33bf7f35de051d5b3 in pull request 50. The original VestingWallet contract without upgradeability slots was kept as the VestingWalletV0 contract and further extensions of it now include the __gap slots variable.

### Original Finding Content

The contracts [`VestingWallet`](https://github.com/forta-protocol/forta-token/blob/92d7a7ddd6672a7530a4bfc532d0d697e7f12744/contracts/vesting/VestingWallet.sol) and [`VestingWalletV2`](https://github.com/forta-protocol/forta-token/blob/92d7a7ddd6672a7530a4bfc532d0d697e7f12744/contracts/vesting/VestingWalletV2.sol) do not contain a `__gap` variable although they are upgradeable.


Consider adding a correct `__gap` variable to these contracts, or documenting a plan for managing storage collisions when upgrading the Vesting Wallet. Additionally, since upgradeable contracts with `__gap`s are used in many places within the contracts, consider implementing quality control steps for upgradeable contract development. For instance, make it a priority to check all `__gap` variables before pushing any new code commits, as well as leaving comments next to all variables in a contract indicating which storage slots they belong in. Consider leaving deprecated variables in the code, and leaving comments about the fact that they were deprecated to avoid confusion for future developers. Finally, consider implementing a predictable inheritance structure for all contracts and documenting it within each contract. Implementing these steps will reduce the surface for error and in the long run may save developer time by removing confusion about the storage layout of the contracts.


***Update:** Fixed on [commit `9b37ac5d4b852954552c69e33bf7f35de051d5b3` in pull request 50](https://github.com/forta-protocol/forta-token/pull/50/commits/9b37ac5d4b852954552c69e33bf7f35de051d5b3). The original `VestingWallet` contract without upgradeability slots was kept as the `VestingWalletV0` contract and further extensions of it now include the `__gap` slots variable.*

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

