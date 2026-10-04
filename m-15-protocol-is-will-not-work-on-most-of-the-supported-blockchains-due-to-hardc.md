---
# Core Classification
protocol: Derby
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 12310
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/13
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-derby-judging/issues/308

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:

protocol_categories:
  - dexes
  - cdp
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - HonorLt
  - gogo
---

## Vulnerability Title

M-15: Protocol is will not work on most of the supported blockchains due to hardcoded WETH contract address.

### Overview


This bug report is about the Protocol not working on most of the supported blockchains due to a hardcoded WETH contract address. The WETH address is hardcoded in the Swap library, meaning that on different chains like Polygon, several functionalities will not work. This will impact the Protocol not working on most of the supported blockchains. The code snippet for this bug is the WETH variable in the Swap library. Manual Review was used to identify this bug. The recommendation to fix this bug is to make the WETH variable immutable in the Vault contract, and the Wrapped Native Token contract address should be passed in the Vault constructor on each separate deployment.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-derby-judging/issues/308 

## Found by 
HonorLt, gogo

## Summary

The WETH address is hardcoded in the `Swap` library.

## Vulnerability Detail

As stated in the README.md, the protocol will be deployed on the following EVM blockchains - Ethereum Mainnet, Arbitrum, Optimism, Polygon, Binance Smart Chain. While the project has integration tests with an ethereum mainnet RPC, they don't catch that on different chains like for example Polygon saveral functionallities will not actually work because of the hardcoded WETH address in the Swap.sol library:

```solidity
address internal constant WETH = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
```
https://github.com/sherlock-audit/2023-01-derby/blob/main/derby-yield-optimiser/contracts/libraries/Swap.sol#L28

## Impact

Protocol will not work on most of the supported blockchains.

## Code Snippet

```solidity
address internal constant WETH = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
```
https://github.com/sherlock-audit/2023-01-derby/blob/main/derby-yield-optimiser/contracts/libraries/Swap.sol#L28

## Tool used

Manual Review

## Recommendation

The WETH variable should be immutable in the Vault contract instead of a constant in the Swap library and the Wrapped Native Token contract address should be passed in the Vault constructor on each separate deployment.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Derby |
| Report Date | N/A |
| Finders | HonorLt, gogo |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-derby-judging/issues/308
- **Contest**: https://app.sherlock.xyz/audits/contests/13

### Keywords for Search

`vulnerability`

