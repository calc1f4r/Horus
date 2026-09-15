---
# Core Classification
protocol: Notional Governance Contracts v2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 10752
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/notional-v2-audit-governance-contracts/
github_link: none

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 1

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - services
  - rwa
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M01] Approval process can be front-run

### Overview


This bug report focuses on the vulnerability of the ERC-20 standard `approve` function, which allows owners to specify a `spender` that may transfer a certain amount of tokens from the owner's balance. The same `approve` function is used to make changes to the limit imposed on a `spender`, by calling the function again and replacing the value in the `allowances` mapping. This is susceptible to front-running scenarios by an attacker, who can monitor the mempool for changes in the allowances and spend both the previous and new `allowances` limits.

The bug is acknowledged in a comment but not mitigated. A suggestion is made to use the `safeIncreaseAllowance` and the `safeDecreaseAllowance` methods from the OpenZeppelin's `SafeERC20` library. However, the bug is not fixed and Notional's statement for this issue is that it has to be dealt with client side anyway and if the client is savvy enough to be aware of those methods, it can also enforce that the allowance is set to zero before it is increased. In addition, allowances are generally set to MAX*UINT256 or 0 for most apps to simplify the user experience.

### Original Finding Content

The ERC-20 standard [`approve`](https://github.com/notional-finance/contracts-v2/blob/c37c89c9729b830637558a09b6f22fc6a735da64/contracts/external/governance/NoteERC20.sol#L110-L129) function lets `NOTE` owners specify a `spender` that may transfer up to `rawAmount` tokens from the owner’s balance.  

The same `approve` function is used to make changes to this limit imposed on a `spender`, by calling the function again which replaces the value in the [`allowances` mapping](https://github.com/notional-finance/contracts-v2/blob/c37c89c9729b830637558a09b6f22fc6a735da64/contracts/external/governance/NoteERC20.sol#L28).


Performing a direct overwrite of the value in the `allowances` mapping is susceptible to front-running scenarios by an attacker (e.g., an approved `spender`). By monitoring the mempool for changes in the allowances, an attacker could spend both the previous and new `allowances` limits.


Although this vulnerability is acknowledged [in a comment](https://github.com/notional-finance/contracts-v2/blob/c37c89c9729b830637558a09b6f22fc6a735da64/contracts/external/governance/NoteERC20.sol#L112), it is not mitigated. Consider using the `safeIncreaseAllowance` and the `safeDecreaseAllowance` methods from the [OpenZeppelin’s `SafeERC20` library](https://docs.openzeppelin.com/contracts/3.x/api/token/erc20#SafeERC20).


***Update:** Acknowledged, and will not fix. Notional’s statement for this issue:*



> 
>  \_Won’t fix, unclear how one would resolve this in the “approve” method without adding the separate atomic increaseAllowance and decreaseAllowance methods. My feeling on this issue is that it has to be dealt with client side anyway (increaseAllowance / decreaseAllowance are non-standard) and if the client is savvy enough to be aware of those methods it can also enforce that the allowance is set to zero before it is increased. Also just from a practical perspective, allowances are generally set to MAX*UINT256 or 0 for most apps anyway just to simplify the user experience.*
> 
> 
>

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 1/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Notional Governance Contracts v2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/notional-v2-audit-governance-contracts/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

