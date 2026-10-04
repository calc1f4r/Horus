---
# Core Classification
protocol: Joyn
chain: everychain
category: uncategorized
vulnerability_type: inheritance

# Attack Vector Details
attack_type: inheritance
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1757
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-joyn-contest
source_link: https://code4rena.com/reports/2022-03-joyn
github_link: https://github.com/code-423n4/2022-03-joyn-findings/issues/108

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
  - inheritance

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - peritoflores
---

## Vulnerability Title

[H-06] STORAGE COLLISION BETWEEN PROXY AND IMPLEMENTATION (LACK EIP 1967)

### Overview


This bug report is about a storage collision that could occur when implementing proxies. This collision can cause conflicts and override sensible variables. To prevent this, EIP1967 was proposed. This would set proxy variables at fixed positions. For example, according to the standard, the slot for logic address should be a specific hexadecimal value. To explain this scenario in more detail, the OpenZeppelin site provides a table under the section "Unstructured Storaged Proxies". The tools used to detect this vulnerability were manual code review. The recommended mitigation step is to consider using EIP1967.

### Original Finding Content

_Submitted by peritoflores_

Storage collision because of lack of EIP1967 could cause conflicts and override sensible variables

### Proof of Concept

    contract CoreProxy is Ownable {
           address private immutable _implement;

When you implement proxies, logic and implementation share the same storage layout.    In order to avoid storage conflicts  EIP1967 was proposed.(<https://eips.ethereum.org/EIPS/eip-1967>)   The idea is to set proxy variables at fixed positions (like  `impl` and `admin` ).

For example, according to the standard,  the slot for for logic address should be

`0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc` (obtained as `bytes32(uint256(keccak256('eip1967.proxy.implementation')) - 1)`  ).

In this case, for example, as you inherits from `Ownable` the variable \_owner is at the first slot and can be overwritten in the implementation.   There is a table at OZ site that explains this scenario more in detail

<https://docs.openzeppelin.com/upgrades-plugins/1.x/proxies>

section  "Unstructured Storaged Proxies"


### Recommended Mitigation Steps

Consider using EIP1967


**[sofianeOuafir (Joyn) confirmed and commented](https://github.com/code-423n4/2022-03-joyn-findings/issues/108#issuecomment-1099710973):**
 > This is an issue we want to investigate and fix if our investigation suggests we indeed need to make improvement on that end.
> 
> At the same time, I have little idea of what is the impact of this issue. I'm not sure if it's a high risk item

**[deluca-mike (judge) commented](https://github.com/code-423n4/2022-03-joyn-findings/issues/108#issuecomment-1106035099):**
 > Impact would be that an upgrade could brick a contract by simply rearranging inheritance order, or adding variables to an inherited contract, since the implantation slot will not be where it is expected. As the warden suggests, its critical that the implementation slot be fixed at an explicit location, and not an implicit location derived purely from inheritance and declaration order.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Joyn |
| Report Date | N/A |
| Finders | peritoflores |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-joyn
- **GitHub**: https://github.com/code-423n4/2022-03-joyn-findings/issues/108
- **Contest**: https://code4rena.com/contests/2022-03-joyn-contest

### Keywords for Search

`Inheritance`

