---
# Core Classification
protocol: Augur Core v2 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11520
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/augur-core-v2-audit/
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
  - cdp
  - services
  - prediction_market
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[M08] Factories may unexpectedly fail to create proxies

### Overview


This bug report is about Augur's factories, which are CloneFactory contracts responsible for creating clones of minimal proxies. The target address of these proxies is queried from the Augur contract by calling its lookup function with a particular key. The problem is that if a key has not been registered in the Augur contract, the lookup function defaults to return the zero address, which will then be set as the target address of the created minimal proxy. When the proxy is wrapped with the corresponding interface and the target's initialize function is called, the transaction is unexpectedly reverted without a clear nor informative reason.

The Augur team was recommended to implement validations on the address returned by the lookup function to make sure it is different from the zero address, but they decided not to move forward with this recommendation as the transaction is reverted when calling the initialize function on a clone that points to the zero address.

### Original Finding Content

Augur’s [factories](https://github.com/AugurProject/augur/tree/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/factories) are [`CloneFactory`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/libraries/CloneFactory.sol) contracts in charge of creating clones of minimal proxies (following [EIP 1167](https://eips.ethereum.org/EIPS/eip-1167)). The target addresses of such proxies are queried from the `Augur` contract by calling its [`lookup`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/Augur.sol#L103) [function](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/Augur.sol#L103) with a particular key.


A problem may arise when a key has not been registered in the `Augur` contract, since the `lookup` function always defaults to return the zero address in such case. This address will then be set as the target address of the created minimal proxy, which will therefore attempt to delegate all calls to the zero address. After wrapping the proxy with the corresponding interface, all factories call the target’s `initialize` function and expect a boolean value in return. As this value will *not* be present in the data returned by the proxy’s target contract, the transaction will be unexpectedly reverted without a clear nor informative reason.


Consider implementing, in all factories, the necessary validations on the address returned by the [`lookup`](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/Augur.sol#L103) [function](https://github.com/AugurProject/augur/blob/9a33c3269e812d0cb66d49b61a72db58e32e4749/packages/augur-core/source/contracts/Augur.sol#L103) to make sure it is different from the zero address, thus avoiding unexpected failures in Augur’s factories.


***Update****: The Augur team decided not to move forward with our recommendation, since the transaction is reverted when calling the* *`initialize`* *function on a clone that points to the zero address.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Augur Core v2 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/augur-core-v2-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

