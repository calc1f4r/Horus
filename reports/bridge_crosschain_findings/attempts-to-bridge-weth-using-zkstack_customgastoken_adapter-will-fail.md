---
# Core Classification
protocol: Across Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 56767
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-audit
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

Attempts to Bridge WETH Using ZkStack_CustomGasToken_Adapter Will Fail

### Overview


The `ZkStack_CustomGasToken_Adapter` contract has a function called `relayTokens` that can be used to bridge tokens from Ethereum to a ZkStack blockchain using a custom gas token. However, if the token being bridged is WETH, there is an issue with the `requestL2TransactionTwoBridges` function of the `BridgeHub` contract. This function requires the deposit amount to be 0 when bridging ETH, but in the `relayTokens` function, it is specified as a nonzero amount. This causes any attempt to bridge WETH to L2 to fail. The issue has been resolved in a pull request, and in the meantime, users can avoid this problem by setting the amount to be used in the second bridge's calldata to 0 when bridging WETH.

### Original Finding Content

In order to bridge tokens from Ethereum to a ZkStack blockchain using a custom gas token, the [`relayTokens` function](https://github.com/across-protocol/contracts/blob/5a0c67c984d19a3bb843a4cec9bb081734583dd1/contracts/chain-adapters/ZkStack_CustomGasToken_Adapter.sol#L141) of the `ZkStack_CustomGasToken_Adapter` contract can be used. In case the token to bridge is WETH, the token is first [converted](https://github.com/across-protocol/contracts/blob/5a0c67c984d19a3bb843a4cec9bb081734583dd1/contracts/chain-adapters/ZkStack_CustomGasToken_Adapter.sol#L155) to ETH, and then that ETH is bridged [using the `requestL2TransactionTwoBridges` function](https://github.com/across-protocol/contracts/blob/5a0c67c984d19a3bb843a4cec9bb081734583dd1/contracts/chain-adapters/ZkStack_CustomGasToken_Adapter.sol#L157-L168) of the `BridgeHub` contract. The `requestL2TransactionTwoBridges` function then [calls the `bridgeHubDeposit` function of the second bridge](https://etherscan.io/address/0x509da1be24432f8804c4a9ff4a3c3f80284cdd13#code#F1#L291) with the ETH amount specified by the caller.

However, the `bridgeHubDeposit` function [requires that the deposit amount specified equals 0](https://github.com/matter-labs/era-contracts/blob/aafee035db892689df3f7afe4b89fd6467a39313/l1-contracts/contracts/bridge/L1SharedBridge.sol#L328) in case when ETH is bridged, yet it [is specified as a nonzero amount](https://github.com/across-protocol/contracts/blob/5a0c67c984d19a3bb843a4cec9bb081734583dd1/contracts/chain-adapters/ZkStack_CustomGasToken_Adapter.sol#L167) inside the `relayTokens` function of the adapter. This will cause any attempt to bridge WETH to L2 to revert.

In cases where WETH is being bridged, consider setting the amount to be used in the second bridge's calldata to 0.

***Update:** Resolved in [pull request #743](https://github.com/across-protocol/contracts/pull/743) at commit [0bdad5b](https://github.com/across-protocol/contracts/pull/743/commits/0bdad5bdaacbbaaa9c89addac9e8ce8c36e8f8d5).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

