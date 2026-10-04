---
# Core Classification
protocol: Vibe
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27822
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Vibe/README.md#2-lack-of-checks-in-the-init-function-of-nftmintsale-and-nftmintsalemultiple-contracts
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
  - MixBytes
---

## Vulnerability Title

Lack of checks in the `init` function of `NFTMintSale` and `NFTMintSaleMultiple` contracts

### Overview


A bug has been identified in the `init` function of both the `NFTMintSale` and `NFTMintSaleMultiple` contracts, which are both part of the Vibe-contract repository. This bug can potentially lead to unintended consequences such as the reinitalization of the contract with the complete loss of ownership, as there is no check to ensure that the `proxy` argument is not set to the zero address. Additionally, there are no checks to verify that `endTime >= beginTime` and that `beginTime > block.timestamp`, which are essential to maintain the integrity of the contract and prevent violations of the specified invariants.

In order to fix this bug, it is recommended to implement the mentioned checks within the `init` function of both the `NFTMintSale` and `NFTMintSaleMultiple` contracts. This can be done by accessing the Vibe-contract repository on GitHub, where the code for both contracts can be found.

### Original Finding Content

##### Description
The `init` function in both the `NFTMintSale` and `NFTMintSaleMultiple` contracts currently lacks checks to prevent certain scenarios that can lead to unintended consequences. Firstly, there is no check to ensure that the `proxy` argument is not set to the zero address which can potentially lead to the reinitalization of the contract with the complete loss of ownership. Additionally, there are no checks to verify that `endTime >= beginTime` and that `beginTime > block.timestamp`. These checks are essential to maintain the integrity of the contract and prevent violations of the specified invariants.

##### Recommendation
We recommend implementing the stated checks within the `init` function of both the `NFTMintSale` https://github.com/vibexyz/vibe-contract/blob/d08057edbaf83b00d94dcaca2a05e3c44a45e4d9/contracts/mint/NFTMintSale.sol#L31 and `NFTMintSaleMultiple` https://github.com/vibexyz/vibe-contract/blob/d08057edbaf83b00d94dcaca2a05e3c44a45e4d9/contracts/mint/NFTMintSaleMultiple.sol#L30 contracts.

***

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Vibe |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Vibe/README.md#2-lack-of-checks-in-the-init-function-of-nftmintsale-and-nftmintsalemultiple-contracts
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

