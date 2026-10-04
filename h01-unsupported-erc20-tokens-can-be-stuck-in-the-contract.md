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
solodit_id: 11282
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/endaoment-audit/
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

[H01] Unsupported ERC20 tokens can be stuck in the contract

### Overview


This bug report is about the use of contract interfaces in the codebase of the Endaoment project. The `ERC20` token implementation by OpenZeppelin is used in the `Fund` and `Org` contracts instead of using the interface. The address of the `ERC20` token to be used is passed as an input parameter. This can lead to transactions calling those functions failing due to a mismatch between the `ERC20` OpenZeppelin contract and the target implementation. Furthermore, if someone accidentally deposits an `ERC20` token which has a different implementation from the OpenZeppelin one, those funds are stuck forever in the contract and can’t be transferred out. As a solution, it is suggested to use the `IERC20` interface importing it from the `openzeppelin-contracts` package to allow interoperation with any possible implementation of the `ERC20` token standard and avoid the loss of the funds deposited in the contracts. The bug has been fixed in pull request #68.

### Original Finding Content

**Update:** *Fixed in [pull request #68](https://github.com/endaoment/endaoment-contracts/pull/68).*


[Contract interfaces](https://solidity.readthedocs.io/en/latest/contracts.html#interfaces) are contracts that declare function signatures without implementing them. They are used as an specification that decouples the signature of the functions from their implementation, allowing to interoperate with different implementations as long as they adhere to the specification.  

In the codebase, the `ERC20` token implementation by OpenZeppelin [is used](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/Org.sol#L7) in the [`Fund`](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/Fund.sol#L124-L131) and [`Org`](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/Org.sol#L95) contracts, instead of using the interface.  

The address of the `ERC20` token to be used [is passed as input parameter](https://github.com/endaoment/endaoment-contracts/blob/f60aa253d3d869ad6460877f23e6092acb313add/contracts/Org.sol#L91).


Given the fact that one can pass arbitrary addresses whether or not they represent valid `ERC20` tokens and that not every `ERC20` contract is implemented exactly as the OpenZeppelin one, it can happen that transactions calling those functions fail due to a mismatch between the `ERC20` OpenZeppelin contract and the target implementation represented by the `tokenAddress`.


Another consequence is that, since anyone can transfer arbitrary `ERC20` tokens to the `Fund` or `Org` contract, if someone accidentally deposits an `ERC20` token which has a different implementation from the OpenZeppelin one, those funds are stuck forever in the contract and can’t be transferred out.


As suggested in [[N03]](#n03), consider using the `IERC20` interface importing it from the `openzeppelin-contracts` package to allow interoperation with any possible implementation of the `ERC20` token standard and avoid the loss of the funds deposited in the contracts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
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

