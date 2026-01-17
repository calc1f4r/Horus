---
# Core Classification
protocol: Endaoment Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11291
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/endaoment-audit/
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L05] Misleading docstrings

### Overview

See description below for full details.

### Original Finding Content

**Update:** *Partially fixed in [pull request #78](https://github.com/endaoment/endaoment-contracts/pull/78). Most of the docstrings have been fixed, some of them have been added or refactored.*


Several docstrings throughout the code base were found to contain misleading information and should be fixed. In particular:


* [Line 16 of the `Fund`](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/Fund.sol#L16) contract is incorrectly assuming that the token transfer is done using the `SafeMath` library, but since the token address used to do the transfer [is arbitrary](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/Fund.sol#L119), then the `transfer` implementation can be different and then the assumption doesn’t hold.
* [Lines 14,15 and 16](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/FundFactory.sol#L14-L16) of the `FundFactory` contract state that it provides a way for fetching individual `Org` contract addresses and a list of `allowedOrgs` but there is no way of retrieving such information from the contract.
* [Lines 231 and 232 of the `EndaomentAdmin` contract](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/EndaomentAdmin.sol#L231-L232) are stating that the permitted roles to pass the modifier’s restrictions have to be a “bot commander (0)” or a “pauser (1)”. In reality, the modifier can be called with any of the [six roles permitted](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/interfaces/IEndaomentAdmin.sol#L13) and it only checks if that role exists or if it’s paused. Moreover it’s not clear what “bot commander” means.
* [Line 182](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/EndaomentAdmin.sol#L182), [172](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/EndaomentAdmin.sol#L172) and [158](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/EndaomentAdmin.sol#L158) of the `EndaomentAdmin` contract say “External” when the function visibility is `public`.
* [Lines 27 an 28](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/Administratable.sol#L27-L28) of the `Administratable` contract, the comment says that the only admitted roles are `ADMIN`, `ACCOUNTANT` and `REVIEWER` while the modifier actually checks also for the `FUND_FACTORY` and `ORG_FACTORY` roles.
* [Line 184](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/EndaomentAdmin.sol#L184) of the `EndaomentAdmin` contract says `admin` where it should be the `holder` or `roleAddress` as the returned named parameter. The same happens in the [`IEndaomentAdmin.getRoleAddress`](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/interfaces/IEndaomentAdmin.sol#L33) function definition.
* [Line 79](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/Fund.sol#L79) and [116](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/Fund.sol#L116) of the `Fund` contract and [line 88](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/Org.sol#L88) of the `Org` contract are mentioning stablecoins. There is actually no restriction on the type of `ERC20` tokens that can be passed as input parameter in the functions making use of them and any mention should therefore be removed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Endaoment Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/endaoment-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

