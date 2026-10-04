---
# Core Classification
protocol: Scroll Phase 1 Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32935
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/scroll-phase-1-audit
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

L2 Standard ERC-20 Token Metadata Can Be Set Arbitrarily

### Overview


This bug report discusses an issue with the ERC-20 gateway contract on L2. When a new ERC-20 token is deposited, the contract fetches its metadata and deploys a clone contract on L2 with this information. However, an attacker could exploit this by setting arbitrary metadata during the first deposit, causing confusion for users and potential harm to projects. To fix this, the report suggests not updating the token mapping until a successful withdrawal from L2. This has been resolved in a recent update to the contract.

### Original Finding Content

When an ERC-20 is first deposited on L2 through the standard ERC-20 gateway contract, the [contract fetches](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/gateways/L1StandardERC20Gateway.sol#L150) the symbol, name and decimals of the ERC-20 token. These are [ABI encoded](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/gateways/L1StandardERC20Gateway.sol#L153) alongside the `_data` passed by the user, and the message is forwarded to the L2. On the L2 side, as this token is seen for the first time, the metadata is [decoded from the data](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L2/gateways/L2StandardERC20Gateway.sol#L162). A [call to the `ScrollStandardERC20Factory`](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L2/gateways/L2StandardERC20Gateway.sol#L161) is then made and a clone of the `ScrollStandardERC20` contract is deployed and [initialized](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L2/gateways/L2StandardERC20Gateway.sol#L166) with the symbol, name and decimals.


However, an attacker can use the lack of atomicity when bridging to set arbitrary metadata when an ERC-20 is bridged to L2 for the first time. An example of this would involve two transactions:


1. The attacker first calls the [deposit](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/gateways/L1StandardERC20Gateway.sol#L114) function to deposit a new ERC-20 token with a very low `_gasLimit` parameter. Because the ERC-20 address is not yet in `tokenMapping`, the contract fetches its [metadata](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/gateways/L1StandardERC20Gateway.sol#L150) information and [encodes](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/gateways/L1StandardERC20Gateway.sol#L153) it alongside the `_data` parameter. The token is then added to the `tokenMapping`, the message is relayed and reverts on L2 with an out-of-gas exception.
2. The attacker then calls the [deposit](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/gateways/L1StandardERC20Gateway.sol#L114) function again with a `_data` parameter containing an [ABI encoding of arbitrary metadata](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/gateways/L1StandardERC20Gateway.sol#L153). Because the `tokenMapping` now contains the ERC-20 address, the call would be directly transmitted to L2 without fetching the ERC-20 metadata. As it is the first time the L2 sees this token, a `ScrollStandardERC20` clone is deployed with symbol, name and decimals decoded from the `_data` parameter set by the attacker.


The token contract would thus have its metadata set by the attacker. Additionally, this contract and the factory are [immutable](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/libraries/token/ScrollStandardERC20.sol#L15), and the address to which a clone is deployed is deterministic meaning it cannot be redeployed easily. This would be complex to fix in practice. In terms of impact, it would be very confusing for users, having to deal with tokens with different metadata in the UIs depending on whether the token is on L1 or L2, and could be used to intentionally grief specific projects.


Consider not updating `tokenMapping[_token]` on the first partially successful L1 deposit, but only when a token is successfully withdrawn from L2 in the [`finalizeWithdrawERC20` function](https://github.com/scroll-tech/scroll/blob/3bc8a3f5c6ac816ddffadca41024331dcf4d3064/contracts/src/L1/gateways/L1StandardERC20Gateway.sol#L88). This strikes a good balance by ensuring that tokens can be deployed even if a first transaction fails on L2, as the metadata would be sent again, while avoiding wasting gas by querying this information on each deposit forever.


***Update:** Resolved in [pull request #606](https://github.com/scroll-tech/scroll/pull/606) at commit [2f76991](https://github.com/scroll-tech/scroll/pull/606/commits/2f76991ddbddcf92bef5fbd0103124e6636c6f2c).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Scroll Phase 1 Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/scroll-phase-1-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

