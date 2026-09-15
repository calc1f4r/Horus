---
# Core Classification
protocol: Trufin Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33021
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/trufin-audit
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Some Functions Are Not ERC-4626 Compliant

### Overview

See description below for full details.

### Original Finding Content

Since the `TruStakeMATICv2` contract is an [ERC-4626](https://eips.ethereum.org/EIPS/eip-4626) vault, it is important that it complies with all the specifications of the standard. Some functionality of the vault diverges from the standard:


* The `maxDeposit` and `maxMint` functions must not revert under any circumstances.


	+ The [`maxDeposit`](https://github.com/TruFin-io/staker-audit-april/blob/9f199451b5220f73cfc1eb95dc13381acf804b15/contracts/main/TruStakeMATICv2.sol#L231) function in `TruStakeMATICv2` will revert if `cap` < `totalStaked()`.
	+ The [`maxMint`](https://github.com/TruFin-io/staker-audit-april/blob/9f199451b5220f73cfc1eb95dc13381acf804b15/contracts/main/TruStakeMATICv2.sol#L237) function would also revert under the same circumstance as it makes a call to the `maxDeposit` function.
* The ERC-4626 standard stipulates that an approved EIP-20 spender is able to call the `deposit`, `mint`, `withdraw` and `redeem` functions on behalf of the asset/share owner and deposit/withdraw the assets.


	+ In the `TruStakeMATICv2` contract, only the owner of the tokens/shares can call these functions.
* The standard also stipulates that the `withdraw` and `redeem` functions are the functions in which assets are transferred to the recipient. If an implementation requires pre-requesting to the vault before a withdrawal can be performed then those methods should be performed separately.


	+ In `TruStakeMATICv2` contract, the `withdraw` and `redeem` functions are used to unstake MATIC from the validator. The actual transfer happens by calling the `withdrawClaim` function after 80 checkpoints.


Contracts that integrate with the `TruStakeMATICv2` vault may wrongly assume that the functions are EIP-4626 compliant, which can cause integration problems in the future, potentially leading to a wide range of issues for both parties, including loss of funds.


Consider making all functions ERC-4626 compliant to prevent any integration issues.


***Update:** Partially resolved in [pull request #1](https://github.com/TruFin-io/staker-audit-april/pull/1) at commit [4514cfb](https://github.com/TruFin-io/staker-audit-april/pull/1/commits/4514cfb0754ce794285f42970a0a820d1b09944f). Functions that are not compliant with the ERC-4626 standard are documented.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Trufin Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/trufin-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

