---
# Core Classification
protocol: Limit Break
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44748
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-12-Limit Break.md
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
  - Zokyo
---

## Vulnerability Title

Edge case in business logic leads to stolen funds

### Overview


This bug report describes a critical issue in the PaymentProcessor contract. The contract has a structure called MatchOrder which has a property called protocol that identifies whether an NFT token is ERC1155 or ERC721. However, this property can be manipulated by a seller or buyer, allowing them to change it from ERC1155 to ERC721. This can cause problems when the contract tries to transfer the NFT, as it will call the wrong function and may fail. The recommendation is to add the protocol property to the signatures of both the seller and buyer to prevent this issue. A proof of concept has been provided to demonstrate the problem. The bug has been resolved.

### Original Finding Content

**Severity**: Critical

**Status**: Resolved

**Description**

In contract PaymentProcessor.sol, to identify if the nft token is either ERC1155 or ERC721 the structure MatchOrder have a property named protocol, which is an enum and can have the values TokenProtocols.ERC1155 or TokenProtocols.ERC721, this check is done so that the contact knows which transferFrom function to call, safeTransferFrom in the case of ERC1155 or transferFrom in the case of ERC721, However this can be exploited because that parameter is not part of neither the buyer or the seller signature so it can be manipulated, let’s take the following example: 
Alice (Seller) and Bob(buyer) agree to make an otc deal where Alice sells 1 ERC1155 token at 1 eth. 
They both sign the details and everything looks normal. 
Before sending the transaction Alice changed the value of the protocol property from the MatchOrder structure from ERC1155 to ERC721.
Alice calls the buySingleListing with the correct signatures however the protocol parameter is modified. 
When the execution logic from _executeMatchOrder  will be at line #1306 where it will choose what function to call, because the protocol value is ERC721 instead of ERC1155 will call the transferFrom function, if the transferFrom function will not exist in ERC1155 the execution will revert, however if the ERC1155 will have an empty fallback function implemented, the execution will succeed but in reality no nft’s will be transferred.

**Recommendation**: 

Add the property protocol from MatchOrder structure in the both seller and buyer signatures.

**POC** : https://hackmd.io/@QyPimM2nQzSOYG0jHv2aIg/HkOuspaz3

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Limit Break |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-12-Limit Break.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

