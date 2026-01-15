---
# Core Classification
protocol: Fantium
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27940
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Fantium/Fantium%20v2/README.md#16-the-nft-contract-allows-multiple-ways-to-avoid-kyc
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

The NFT contract allows multiple ways to avoid KYC

### Overview


The KYC system for NFT minting is not working properly. The `FantiumNFTV3.batchMintTo()` function checks that `msg.sender` is KYCed but allows the minted NFT to be sent to someone who is not KYCed. Additionally, NFTs are transferable, meaning a KYCed account can buy an NFT and transfer it to anyone. Due to these issues, we recommend making necessary changes for the KYC system or removing it.

### Original Finding Content

##### Description

The KYC system for NFT minting does not work. Some easy ways:
1) `FantiumNFTV3.batchMintTo()` checks that `msg.sender` is KYCed but allows specifying `to` who will receive the minted NFT. So, the true NFT receiver is not KYCed.
- https://github.com/FantiumAG/smart-contracts/blob/a2d126453c1105028f12277b8f342d2cdbf01a77/contracts/FantiumNFTV3.sol#L325-L388
3) NFT is transferable. So, a KYCed account can buy an NFT and transfer it to anyone.

##### Recommendation

We recommend making necessary changes for the KYC system or removing it.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Fantium |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Fantium/Fantium%20v2/README.md#16-the-nft-contract-allows-multiple-ways-to-avoid-kyc
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

