---
# Core Classification
protocol: dForce
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36546
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/dForce/sUSX/README.md#1-mintcap-check-missing-in-cross-chain-transfer
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
  - MixBytes
---

## Vulnerability Title

MintCap Check Missing in Cross-Chain Transfer

### Overview


The `outboundTransferShares` function in the `sUSX` contract has a bug that could allow an attacker to bypass the `MSDController.mintCap` limit and potentially weaken the collateralization guarantees of the `sUSX` interest. This could happen through a cross-chain transfer where the `totalMint` value exceeds the `mintCap` limit. To fix this, a check should be implemented in the `outboundTransferShares` function to ensure that the `totalMint` value does not exceed the `mintCap` limit. This bug is classified as high severity and could have serious consequences.

### Original Finding Content

##### Description
The issue was identified within the [`outboundTransferShares`](https://github.com/dforce-network/OFT/blob/2ff5d7a8f9a509006557bf5de72fabf40d1138a5/src/sUSX.sol#L276) function of the `sUSX` contract.

There is no check to ensure that the total mint amount does not exceed the `MSDController.mintCap` parameter. This oversight could lead to an attack vector where the mintCap limit is bypassed through cross-chain transfers. The following scenario outlines the potential attack:
1. `sUSX.totalMint` equals `MSDController.mintCap(sUSX)`, preventing direct USX withdrawals on the current network.
2. A cross-chain transfer is performed to a chain where the mintCap limit hasn't been reached.
3. The `unstakedAmount` on the sending network increases by the `assets` value, causing `sUSX.totalMint` to surpass the `MSDController.mintCap(sUSX)` value.
4. On the receiving chain, the `stakedAmount` increases by the `assets` amount.
5. Assets are withdrawn on the receiving chain, decreasing the `unstakedAmount` by the same value, thereby the `totalMint` value on the receiving chain remains unchanged.

This manipulation allows the number of minted USX token rewards to exceed the sum of mintCaps on all chains, potentially bypassing the collateralization limits of the `sUSX` interest.

The issue is classified as **high** severity as it can significantly weaken the collateralization guarantees of the `sUSX` interest.

##### Recommendation
We recommend implementing a check to ensure that the `totalMint()` value after `_burn` does not exceed the `MSDController.mintCap(sUSX)` in `outBoundTransferShares` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | dForce |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/dForce/sUSX/README.md#1-mintcap-check-missing-in-cross-chain-transfer
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

