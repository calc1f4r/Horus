---
# Core Classification
protocol: Gamma
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13285
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2022/02/gamma/
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
finders_count: 2
finders:
  - Sergii Kravchenko
  -  David Oz Kashi

---

## Vulnerability Title

Hypervisor.withdraw - Possible reentrancy ✓ Fixed

### Overview


A bug was discovered in the `Hypervisor` contract, which is used by liquidity providers to withdraw their deposits. The bug could be exploited by malicious actors to mint extra shares, which could be later redeemed for tokens stolen from other depositors. To fix the bug, the `ReentrancyGuard` was implemented in both `Hypervisor.withdraw` and `Hypervisor.deposit`. The ReentrancyGuard is a security measure that helps protect against reentrant calls, which are calls that are made within the execution of a function, before the function has returned. By adding this guard, the bug was successfully resolved.

### Original Finding Content

#### Resolution



Fixed in [GammaStrategies/[email protected]`9a7a3dd`](https://github.com/GammaStrategies/hypervisor/commit/9a7a3dd88e8e8b106bf5d0e4c56e879442a72181) by implementing the auditor’s recommendation.


#### Description


`Hypervisor.withdraw` can be used by a liquidity provider to withdraw its deposit from the `Hypervisor` contract. A user can get his deposited liquidity back in exchange for the burn of his `shares`. The function is transferring `token0,1` to the user first and then burns his `shares`. In theory, the contracts of `token0,1` may hijack the execution call-flow causing a reentrant call to `deposit`, which will use the stale value for `totalSupply()` to evaluate the number of shares to be minted. Since this value will be greater than what it should be, the attacker will be able to mint `shares` for free, that could be later redeemed for actual tokens stolen from other depositors.


#### Recommendation


Consider adding a [`ReentrancyGuard`](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/security/ReentrancyGuard.sol) both to `Hypervisor.withdraw` and `Hypervisor.deposit`

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Gamma |
| Report Date | N/A |
| Finders | Sergii Kravchenko,  David Oz Kashi
 |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2022/02/gamma/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

