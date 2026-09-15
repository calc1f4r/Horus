---
# Core Classification
protocol: Dapper Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19317
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/dapper-wallet/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/dapper-wallet/review.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Outdated ERC721 Implementation

### Overview


This bug report is about the Dapper Ethereum smart contract wallet, which implements the ERC721Receiver contract and as such, the onERC721Received() function. This function is not compliant with the ERC721 standard, as it does not take the right arguments as specified by the standard. This means that any ERC721 transfer to a Dapper smart contract wallet would fail. To resolve this issue, the ERC721Receiver and ERC721Receivable contracts need to be changed to comply with the ERC721 standard, specifically by changing the onERC721Received() function to take an additional address. The new version of the contract now supports both the final ERC721 specification and the previous one, and the bug has been resolved.

### Original Finding Content

## Description

The Dapper Ethereum smart contract wallet (CoreWallet, deployed in its cloned and full versions) inherits the `ERC721Receiver` contract and as such, implements the `onERC721Received()` function. This function is non-compliant with the ERC721 standard as it does not take the right arguments as specified by the standard:

- **ERC721 Standard [1]**: `onERC721Received(address, address, uint256, bytes);`
- **Dapper implementation (ERC721Receiver)**: `onERC721Received(address, uint256, bytes);`

This function is to be called by ERC721 contracts when a `safeTransferFrom` is made to a contract address. Typically, these contracts would implement a function which verifies that the recipient address, when a contract, is compliant with the `ERC721TokenReceiver` interface, expecting the `onERC721Received()` function of the Dapper contract to return `0x150b7a02` (equals to `bytes4(keccak256("onERC721Received(address,address,uint256,bytes)"))`). 

Since the Dapper wallet returns `0xf0b9e5ba` (equals to `bytes4(keccak256("onERC721Received(address,uint256,bytes)"))`), any ERC721 transfer to a Dapper smart contract wallet would effectively fail. This is illustrated in our test suite, refer to `tests/test_erc721.py`.

## Recommendations

Change the `ERC721Receiver` and `ERC721Receivable` contracts to comply with the ERC721 standard. Specifically, change the `onERC721Received()` function to take an additional address (i.e. the address calling the `safeTransferFrom()`).

## Resolution

The new version of the contract in commit `6b3784e` now supports both the final ERC721 specification (`ERC721ReceiverFinal`), and the previous one, `ERC721ReceiverDraft` (used for example by the CryptoKitties contract).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Dapper Labs |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/dapper-wallet/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/dapper-wallet/review.pdf

### Keywords for Search

`vulnerability`

