---
# Core Classification
protocol: Morpho Protocol V1
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18125
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/MorphoLabs.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/MorphoLabs.pdf
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
finders_count: 3
finders:
  - Felipe Manzano
  - Bo Henderson
  - Michael Colburn
---

## Vulnerability Title

Lack of two-step process for contract ownership changes

### Overview


This bug report focuses on the IncentivesVault contract and other Ownable Morpho contracts. It is noted that the transferOwnership function, which allows for the changing of the contract's owner, can be error-prone and can lead to irrevocable mistakes. The report provides an exploit scenario in which Bob, the IncentivesVault owner, accidentally enters the wrong address when trying to change the contract's owner, resulting in him permanently losing access to the contract. 

The report provides two recommendations for addressing the issue. In the short term, it is suggested that a two-step process be implemented for contract ownership transfers in which the owner proposes a new address and the transfer is completed once the new address has executed a call to accept the role. In the long term, it is suggested that all possible actions that can be taken by privileged accounts are identified and documented, along with their associated risks. This will facilitate reviews of the codebase and prevent future mistakes.

### Original Finding Content

## Diﬃculty: High

## Type: Auditing and Logging

### Description
The owner of the `IncentivesVault` contract and other Ownable Morpho contracts can be changed by calling the `transferOwnership` function. This function internally calls the `_transferOwnership` function, which immediately sets the contract’s new owner. Making such a critical change in a single step is error-prone and can lead to irrevocable mistakes.

```solidity
contract IncentivesVault is IIncentivesVault, Ownable {
    ...
}
```
*Figure 1.1: Inheritance of contracts/compound/IncentivesVault.sol*

```solidity
function transferOwnership(address newOwner) public virtual onlyOwner {
    ...
}
```
*Figure 1.2: The `transferOwnership` function in @openzeppelin/contracts/access/Ownable.sol*

### Exploit Scenario
Bob, the `IncentivesVault` owner, invokes `transferOwnership()` to change the contract’s owner but accidentally enters the wrong address. As a result, he permanently loses access to the contract.

### Recommendations
- **Short term**: For contract ownership transfers, implement a two-step process, in which the owner proposes a new address and the transfer is completed once the new address has executed a call to accept the role.
- **Long term**: Identify and document all possible actions that can be taken by privileged accounts and their associated risks. This will facilitate reviews of the codebase and prevent future mistakes.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Morpho Protocol V1 |
| Report Date | N/A |
| Finders | Felipe Manzano, Bo Henderson, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/MorphoLabs.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/MorphoLabs.pdf

### Keywords for Search

`vulnerability`

