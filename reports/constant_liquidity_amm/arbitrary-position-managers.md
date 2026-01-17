---
# Core Classification
protocol: UNCX UniswapV3 Liquidity Locker Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32621
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/uncx-uniswapv3-liquidity-locker-audit
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
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Arbitrary Position Managers

### Overview


The `UNCX_ProofOfReservesV2_UniV3` contract allows users to specify their own position manager contract for any "UniswapV3-like" protocol. However, a potential bug has been identified where a malicious contract could bypass the lock creation fee, collect fee, and provide incorrect information to the UNCX locker contract, rendering it ineffective. The suggested solution is to implement a whitelist system for position manager contracts, with the contract owner having the power to add permitted managers. This bug has been resolved in a recent update.

### Original Finding Content

The [`UNCX_ProofOfReservesV2_UniV3`](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/blob/342c621cc93a13882601b30e547907877f3e3f86/contracts/UNCX_ProofOfReservesV2_UniV3.sol) contract is meant to work with any "UniswapV3-like" protocol. It does this by allowing users to [specify their own position manager contract](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/blob/342c621cc93a13882601b30e547907877f3e3f86/contracts/IUNCX_ProofOfReservesV2_UniV3.sol#L36). This gives complete execution control to an arbitrary contract that could be tailored specifically to attack the `UNCX_ProofOfReservesV2_UniV3` contract.


Consider a contract that simply refuses to cooperate. It wraps all of its methods around a well-behaved NFT position manager contract (e.g., UniswapV3's). However, if it sees a call to `collect` from the UNCX contract, it simply does nothing and does not pass the call on to the actual NFT position manager. In this manner, the contract can bypass the lock creation fee, the collect fee, and can supply the wrong `maxTick` to pass the non-full-range positions from the correct manager to the UNCX locker contract. It can even refuse to `safeTransferFrom` the NFT to the UNCX contract, rendering the lock contract completely ineffective.


Consider implementing a whitelist system for the position manager contracts with the contract owner having the power to add (but not remove) permitted position managers.


***Update**: Resolved in [pull request #1](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/pull/1) at commit [ea8b60a](https://github.com/uncx-private-repos/liquidity-locker-univ3-contracts/pull/1/commits/ea8b60a34fe8913335dde902d40c5c3225c9740b).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | UNCX UniswapV3 Liquidity Locker Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/uncx-uniswapv3-liquidity-locker-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

