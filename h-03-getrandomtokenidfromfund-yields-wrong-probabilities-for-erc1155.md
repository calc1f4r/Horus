---
# Core Classification
protocol: NFTX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 42182
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2021-05-nftx
source_link: https://code4rena.com/reports/2021-05-nftx
github_link: https://github.com/code-423n4/2021-05-nftx-findings/issues/56

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

protocol_categories:
  - dexes
  - cross_chain
  - rwa
  - leveraged_farming
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[H-03] `getRandomTokenIdFromFund` yields wrong probabilities for ERC1155

### Overview


The `NFTXVaultUpgradeable.getRandomTokenIdFromFund` function is not working correctly with ERC1155 tokens. This means that when trying to randomly select a token, it does not take into account the quantity of tokens that have been deposited. This can lead to an unfair distribution of tokens, making it easier for an attacker to redeem more valuable NFTs. This bug has been acknowledged by the developer and a design change may be needed to fix it. A judge has marked this as a high-risk issue as it could put users' funds at risk.

### Original Finding Content


`NFTXVaultUpgradeable.getRandomTokenIdFromFund` does not work with ERC1155 as it does not take the deposited `quantity1155` into account.

Assume `tokenId0` has a count of 100, and `tokenId1` has a count of 1.
Then `getRandomId` would have a pseudo-random 1:1 chance for token 0 and 1 when in reality it should be 100:1.

This might make it easier for an attacker to redeem more valuable NFTs as the probabilities are off.

Recommend taking the quantities of each token into account (`quantity1155`) which probably requires a design change as it is currently hard to do without iterating over all tokens.

**[0xKiwi (NFTX) acknowledged](https://github.com/code-423n4/2021-05-nftx-findings/issues/56)**

**[cemozer (Judge) commented](https://github.com/code-423n4/2021-05-nftx-findings/issues/56#issuecomment-848266608):**
 > Marking this as high risk as an attacker can weed out high-value NFTs from a vault putting other users funds at risk



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | NFTX |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-05-nftx
- **GitHub**: https://github.com/code-423n4/2021-05-nftx-findings/issues/56
- **Contest**: https://code4rena.com/reports/2021-05-nftx

### Keywords for Search

`vulnerability`

