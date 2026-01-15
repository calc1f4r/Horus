---
# Core Classification
protocol: Lotaheros
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21024
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-04-13-Lotaheros.md
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
  - AuditOne
---

## Vulnerability Title

Lack of re-entrancy guard for \_mint[Hero](https://github.com/Crelde/IOTA-Heroes-Contracts/blob/3e345747f723637c0a1ce884d1ae0e1584015e98/contracts/HeroNFT.sol#L68)

### Overview


This bug report is about the mintHero function in the HeroNFT.sol contract. This function is used to mint the Hero NFT, and it uses the safeMint process to verify if the receiver address is able to receive the NFT. After minting the NFT, the count is increased. However, the process allows for reentrancy, which can be exploited. The recommendation is to add non-reentrancy protection in the following places: mintHero function in the HeroNFT.sol contract, the Factory.sol contract at lines 49, 72, 155, and 172.

### Original Finding Content

**Description:**

 \_[mintHero fu](https://github.com/Crelde/IOTA-Heroes-Contracts/blob/3e345747f723637c0a1ce884d1ae0e1584015e98/contracts/HeroNFT.sol#L68)nction can be called by the minter to mint the Hero NFT.

This function can be called in above mentioned places.

When we see the minting place,it uses the safeMint which means that during minting,the process verified whether the receiver address is able to receiee the NFTby calling the onERC721Received.selector. This places allows for reentrancy.

after minting the NFT,count is increased.

**Recommendations:** 

Add non reentrancy protection in following places

[https://github.com/Crelde/IOTA-Heroes-Contracts/blob/3e345747f723637c0a1ce884d1ae0e1584015 e98/contracts/HeroNFT.sol#L68 ](https://github.com/Crelde/IOTA-Heroes-Contracts/blob/3e345747f723637c0a1ce884d1ae0e1584015e98/contracts/HeroNFT.sol#L68)[https://github.com/Crelde/IOTA-Heroes-Contracts/blob/3e345747f723637c0a1ce884d1ae0e1584015 e98/contracts/Factory.sol#L49 ](https://github.com/Crelde/IOTA-Heroes-Contracts/blob/3e345747f723637c0a1ce884d1ae0e1584015e98/contracts/Factory.sol#L49)[https://github.com/Crelde/IOTA-Heroes-Contracts/blob/3e345747f723637c0a1ce884d1ae0e1584015 e98/contracts/Factory.sol#L72 ](https://github.com/Crelde/IOTA-Heroes-Contracts/blob/3e345747f723637c0a1ce884d1ae0e1584015e98/contracts/Factory.sol#L72)[https://github.com/Crelde/IOTA-Heroes-Contracts/blob/3e345747f723637c0a1ce884d1ae0e1584015 e98/contracts/Factory.sol#L155 ](https://github.com/Crelde/IOTA-Heroes-Contracts/blob/3e345747f723637c0a1ce884d1ae0e1584015e98/contracts/Factory.sol#L155)[https://github.com/Crelde/IOTA-Heroes-Contracts/blob/3e345747f723637c0a1ce884d1ae0e1584015 e98/contracts/Factory.sol#L172](https://github.com/Crelde/IOTA-Heroes-Contracts/blob/3e345747f723637c0a1ce884d1ae0e1584015e98/contracts/Factory.sol#L172)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Lotaheros |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-04-13-Lotaheros.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

