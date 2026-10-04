---
# Core Classification
protocol: SKALE
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1609
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-skale-contest
source_link: https://code4rena.com/reports/2022-02-skale
github_link: https://github.com/code-423n4/2022-02-skale-findings/issues/26

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

protocol_categories:
  - dexes
  - cdp
  - yield
  - launchpad
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[M-10] NFT owner can change token URI

### Overview


This bug report concerns the ERC721OnChain implementation, which is a type of non-fungible token (NFT). The bug is that the owner of the token can set the token's URI, which usually points to data defining the NFT (attributes, images, etc.). This means that a user that owns an NFT can spoof any other NFT data by changing the token URI to any of the other NFTs. The recommended mitigation step is to disallow the owner of an NFT to change its token URI. This would prevent the user from being able to spoof any other NFT data.

### Original Finding Content

_Submitted by cmichel_

In the `ERC721OnChain` implementation the *token owner* can set the token's URI using `setTokenURI`.

Usually, this is token URI points to data defining the NFT (attributes, images, etc.).
It's usually set by the *contract* owner.
A user that owns an NFT can just spoof any other NFT data by changing the token URI to any of the other NFTs.

### Recommended Mitigation Steps

Disallow the owner of an NFT to change its token URI


**[DimaStebaev (SKALE) disputed and commented](https://github.com/code-423n4/2022-02-skale-findings/issues/26#issuecomment-1064987630):**
 > Acknowledged,`ERC721OnChain` is a default implementation. If the token is sensitive to URI change SKALE chain owner can use another one.
> Not all ERC721 require that URI can't be changed.

**[GalloDaSballo (judge) commented](https://github.com/code-423n4/2022-02-skale-findings/issues/26#issuecomment-1143990919):**
 > Because the argument for this being a setting can be made I am excluding a high severity.
> 
> However the code was brought into scope, the implementation under scrutiny does allow the owner to change the URI which is a known admin privilege.
> 
> For those reasons I believe the finding to be valid and of medium severity



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | SKALE |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-skale
- **GitHub**: https://github.com/code-423n4/2022-02-skale-findings/issues/26
- **Contest**: https://code4rena.com/contests/2022-02-skale-contest

### Keywords for Search

`vulnerability`

