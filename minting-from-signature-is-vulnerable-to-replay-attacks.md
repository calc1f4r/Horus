---
# Core Classification
protocol: Hyperware
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53134
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/d9967b88-dde1-4383-a17a-f74bf11d4258
source_link: https://cdn.cantina.xyz/reports/cantina_hyperware_december2024.pdf
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
finders_count: 2
finders:
  - Blockdev
  - Rikard Hjort
---

## Vulnerability Title

Minting from signature is vulnerable to replay attacks 

### Overview


This bug report discusses a potential issue in the KinoAccountMinterUpgradable.sol code, specifically in the mintBySignature function. The issue is related to replay attacks, which occur when a signature used for a transaction on one chain can be reused on another chain. This can lead to unintended transactions and potential financial loss. The report identifies three main issues with the code and provides a proof of concept scenario to demonstrate how the bug can be exploited. The recommendation is to implement a domain separator to prevent replay attacks, and this has already been fixed in the code by the developers. 

### Original Finding Content

## Replay Attack Vulnerability in KinoAccountMinterUpgradable

## Context
KinoAccountMinterUpgradable.sol#L72-L91

## Description
A replay attack occurs when a signature used for a transaction on one chain can be reused on another chain other than where it was intended. There is no replay protection on `mintBySignature()` as implemented in `KinoAccountUpgradable` and inherited in `KinoAccount9CharCommitMinter`, `KinoAccountMinter`, and, most relevantly, `KinoAccountPermissionedMinter`.

### Key Issues
1. The same mint request can be replayed on another chain that was not intended.
2. Due to the lack of a domain separator, it may not be clear to certain wallets what is being signed. As a result, it may not be obvious whether the signature is valid and properly separated. Furthermore, contract upgrades may not be performed safely, and clean new semantics cannot be guaranteed since old signatures will not automatically be invalidated.

## Proof of Concept

### Scenario 1:
- A user, Alice, mints an ERC721 using `mintBySignature` on chain A. For instance, a user, Bob, may have paid Alice for minting him a token.
- Bob can extract the signature used in `mintBySignature` from the transaction on chain A, either from the mempool or the blocks, and create a new transaction to call `mintBySignature` on chain B.
- Bob can now mint the same token on chain B. Assuming Alice possesses the same parent token on chain B, Bob can replay Alice's transactions from chain A until he gets the correct next nonce, allowing him to mint the token he paid for on chain A also on chain B.
- Bob can replicate this process on all chains where Alice holds the parent token.

## Recommendation
Implement a domain separator on `KinoAccountMinterUpgradable`. Refer to the [EIP712 specification](https://eips.ethereum.org/EIPS/eip-712) and, for example, the [Metamask documentation](https://docs.metamask.io/guide/signing-ethereum-versions.html) for client-side signature requests.

## Hyperware
Fixed in PR 10.

## Cantina Managed
Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Hyperware |
| Report Date | N/A |
| Finders | Blockdev, Rikard Hjort |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_hyperware_december2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/d9967b88-dde1-4383-a17a-f74bf11d4258

### Keywords for Search

`vulnerability`

