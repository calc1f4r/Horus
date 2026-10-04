---
# Core Classification
protocol: Joyn
chain: everychain
category: uncategorized
vulnerability_type: royalty

# Attack Vector Details
attack_type: royalty
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1763
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-03-joyn-contest
source_link: https://code4rena.com/reports/2022-03-joyn
github_link: https://github.com/code-423n4/2022-03-joyn-findings/issues/130

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.60
financial_impact: medium

# Scoring
quality_score: 3
rarity_score: 2

# Context Tags
tags:
  - royalty
  - erc2981

protocol_categories:
  - dexes
  - cdp
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - leastwood
---

## Vulnerability Title

[M-03] `RoyaltyVault.sol` is Not Equipped to Handle On-Chain Royalties From Secondary Sales

### Overview


A bug has been identified in the Joyn documentation which states that Joyn royalty vaults should be equipped to handle revenue generated on a collection's primary and secondary sales. Currently, `CoreCollection.sol` allows the collection owner to receive a fee on each token mint, but there is no existing implementation which allows the owner of a collection to receive fees on secondary sales. After discussion with the Joyn team, it appears that this will be gathered from Opensea which does not have an on-chain royalty mechanism. This introduces further centralisation risk and users can avoid paying the secondary fee by using other marketplaces such as Foundation. 

To address this, it is recommended to implement the necessary functionality to allow for the collection of fees through an on-chain mechanism. `ERC2981` outlines the appropriate behaviour for this.

### Original Finding Content

_Submitted by leastwood_

<https://github.com/code-423n4/2022-03-joyn/blob/main/core-contracts/contracts/CoreCollection.sol>

<https://github.com/code-423n4/2022-03-joyn/blob/main/royalty-vault/contracts/RoyaltyVault.sol>

### Impact

The Joyn documentation mentions that Joyn royalty vaults should be equipped to handle revenue generated on a collection's primary and secondary sales. Currently, `CoreCollection.sol` allows the collection owner to receive a fee on each token mint, however, there is no existing implementation which allows the owner of a collection to receive fees on secondary sales.

After discussion with the Joyn team, it appears that this will be gathered from Opensea which does not have an on-chain royalty mechanism. As such, each collection will need to be added manually on Opensea, introducing further centralisation risk. It is also possible for users to avoid paying the secondary fee by using other marketplaces such as Foundation.

### Recommended Mitigation Steps

Consider implementing the necessary functionality to allow for the collection of fees through an on-chain mechanism. `ERC2981` outlines the appropriate behaviour for this.


**[sofianeOuafir (Joyn) confirmed and commented](https://github.com/code-423n4/2022-03-joyn-findings/issues/130#issuecomment-1099679515):**
 > This is a great observation. Something we are aware of and intend to fix as well. 👍 



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 3/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | Joyn |
| Report Date | N/A |
| Finders | leastwood |

### Source Links

- **Source**: https://code4rena.com/reports/2022-03-joyn
- **GitHub**: https://github.com/code-423n4/2022-03-joyn-findings/issues/130
- **Contest**: https://code4rena.com/contests/2022-03-joyn-contest

### Keywords for Search

`Royalty, ERC2981`

