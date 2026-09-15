---
# Core Classification
protocol: Uniswap Hooks Library Milestone 1 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49304
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uniswap-hooks-library-milestone-1-audit
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

BaseDynamicFee Hook Can Be Poked Arbitrarily

### Overview


The BaseDynamicFee hook contract has a function called "poke" that allows anyone to update the fee for a pool at any time. However, this function can be manipulated by external factors, which could result in lower fees for certain users. To fix this, access control should be implemented for the poke function or it should only be used internally by inheriting contracts. The bug has been resolved in a recent update.

### Original Finding Content

The [`BaseDynamicFee` hook contract](https://github.com/OpenZeppelin/uniswap-hooks/blob/f051c147dbf296b2b854de92970905a880cd1d51/src/fee/BaseDynamicFee.sol#L21) has a `virtual` `external` [`poke` function](https://github.com/OpenZeppelin/uniswap-hooks/blob/f051c147dbf296b2b854de92970905a880cd1d51/src/fee/BaseDynamicFee.sol#L59) that allows any pool initiated with this hook to (re)set an updated LPFee by anyone at any time. The updated LPFee comes from the [`_getFee(poolKey)` virtual function](https://github.com/OpenZeppelin/uniswap-hooks/blob/f051c147dbf296b2b854de92970905a880cd1d51/src/fee/BaseDynamicFee.sol#L37), which could return any fee based on either the current pool state or any other external conditions. However, if the `_getFee` implementation depends on some external factors, it opens up the possibility of manipulating the LPFee and swapping in a single transaction.

For example, suppose that `_getFee` for a V4 pool is dependent on the token balance of a Uniswap V3 pool having the same token pair. Suppose also that the returned fee for the V4 pool is inversely correlated to the corresponding V3 pool token balance. That is, `_getFee` returns a lower value when the V3 pool has a large balance and otherwise returns a higher value. Now, an attacker could take a flash loan, deposit into the V3 pool temporarily, and then call `poke` on the V4 pool. Since the V3 pool balance would have increased, the swap fee will drop and the attacker can pay lesser fees for subsequent swaps. If the subsequent users do not `poke` in advance, they can enjoy cheap fees without having to do any manipulation.

Consider imposing access control on the `poke` function so that it cannot be called arbitrarily. Otherwise, the `poke` function can be made `internal`, allowing the inheriting contracts to decide how to appropriately incorporate it with their logic. Alternatively, consider updating the documentation of the `poke` function so that the risk described above is clear to the inheriting contracts.

***Update:** Resolved in [pull request #34](https://github.com/OpenZeppelin/uniswap-hooks/pull/34) at commit [7e81272](https://github.com/OpenZeppelin/uniswap-hooks/pull/34/commits/7e812726b392af7376de78d31453f82fecc072f3).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Uniswap Hooks Library Milestone 1 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uniswap-hooks-library-milestone-1-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

