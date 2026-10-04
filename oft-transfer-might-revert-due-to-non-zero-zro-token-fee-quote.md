---
# Core Classification
protocol: Across Protocol OFT Integration Differential Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58419
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/across-protocol-oft-integration-differential-audit
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

OFT Transfer Might Revert Due to Non-Zero ZRO Token Fee Quote

### Overview


The `OFTTransportAdapter` contract has a bug where it does not properly handle fees in ZRO tokens. This can lead to unexpected outcomes and even cause the transaction to fail. The team has fixed this issue in a recent update and has added tests to prevent similar issues in the future. It is recommended to update to the latest version to avoid any potential problems. 

### Original Finding Content

The `OFTTransportAdapter` contract implements the [`_transferViaOFT` function](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/libraries/OFTTransportAdapter.sol#L57), meant to interact with the OFT messenger and send the funds with that method. To do so, it first [quotes the fees](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/libraries/OFTTransportAdapter.sol#L85), which are returned as [native or ZRO token fees](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/interfaces/IOFT.sol#L18-L19). Later, this same output is used as [part of the message](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/libraries/OFTTransportAdapter.sol#L94).

Even though the `OFTTransportAdapter` contract instructs that it will [pay the fees in native tokens](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/libraries/OFTTransportAdapter.sol#L85), there is no validation that the value for fees in ZRO tokens is zero, meaning that it will be passed once again to the messenger. This means that if the implementation of the messenger outputs both quotes at the same time, it might not recognize with which asset it will be paid, resulting in a reversion if it tries to get paid with ZRO. As seen in an [example from LayerZero](https://docs.layerzero.network/v2/developers/evm/oft/quickstart#calling-send), in the case of paying in native tokens, the `lzTokenFee` parameter is set to zero.

In order to prevent unexpected outcomes and reversions, especially if the messenger deviates in behavior, consider asserting that the returned `lzTokenFee` is zero when quoting for the cost. Furthermore, consider adding more scenarios to the [mocked contracts](https://github.com/across-protocol/contracts/blob/c5d7541037d19053ce2106583b1b711037483038/contracts/test/MockOFTMessenger.sol#L18-L20) to validate proper integration with protocols.

***Update:** Resolved in [pull request #1029](https://github.com/across-protocol/contracts/pull/1029). The team stated:*

> *Added a zero-check for `lzTokenFee` and added some fee negative-scenario tests (partially addressing M-04).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Across Protocol OFT Integration Differential Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/across-protocol-oft-integration-differential-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

