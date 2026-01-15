---
# Core Classification
protocol: Nibbl
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2824
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-nibbl-contest
source_link: https://code4rena.com/reports/2022-06-nibbl
github_link: https://github.com/code-423n4/2022-06-nibbl-findings/issues/317

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
  - services
  - cross_chain
  - leveraged_farming

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cccz
  - Picodes
---

## Vulnerability Title

[M-12] Basket NFT have no name and symbol

### Overview


This bug report is about a vulnerability in the `Basket` contract, which is intended to be used behind a proxy. The `ERC721` implementation used is not upgradeable and its constructor is called at deployment time on the implementation. This results in all proxies having a void name and symbol, breaking all potential integrations and listings. To prove this, it was shown that `ERC721("NFT Basket", "NFTB")` is called at deployment time, and sets private variables at the implementation level. Therefore, when loading the code during `delegateCall`, these variables will not be initialized. The recommended mitigation step is to pass this variable as immutable so they are hardcoded in the implementation byte code.

### Original Finding Content

_Submitted by Picodes, also found by cccz_

<https://github.com/code-423n4/2022-06-nibbl/blob/8c3dbd6adf350f35c58b31723d42117765644110/contracts/Basket.sol#L13>

<https://github.com/code-423n4/2022-06-nibbl/blob/8c3dbd6adf350f35c58b31723d42117765644110/contracts/Basket.sol#L6>

### Impact

The `Basket` contract is intended to be used behind a proxy. But the `ERC721` implementation used is not upgradeable, and its constructor is called at deployment time on the implementation. So all proxies will have a void name and symbol, breaking all potential integrations and listings.

### Proof of Concept

`ERC721("NFT Basket", "NFTB")` is called at deployment time, and sets private variable at the implementation level. Therefore when loading the code during `delegateCall`, these variables will not be initialized.

### Recommended Mitigation Steps

The easiest mitigation would be to pass this variable as immutable so they are hardcoded in the implementation byte code.

**[mundhrakeshav (Nibbl) confirmed](https://github.com/code-423n4/2022-06-nibbl-findings/issues/317)** 

**[Alex the Entreprenerd (warden) commented](https://github.com/code-423n4/2022-06-nibbl-findings/issues/317#issuecomment-1166657024):**
 > Finding is valid, impact is the name of the tokens.

**[HardlyDifficult (judge) decreased severity to QA and commented](https://github.com/code-423n4/2022-06-nibbl-findings/issues/317#issuecomment-1172563153):**
 > Confirmed this is an issue.
> 
> Assets are not at risk, and the function of the protocol is not impacted. All baskets created will have an empty name/symbol but generally there is no requirement that these values are populated. It's mostly for a better experience on frontends including etherscan. Downgrading and merging with the warden's QA report #314.

**[Picodes (warden) commented](https://github.com/code-423n4/2022-06-nibbl-findings/issues/317#issuecomment-1174704129):**
 > @HardlyDifficult Indeed it does not break the protocol's logic and funds are not at risk, but the name and the symbol of the NFTs are not the ones chosen by the sponsor, and as it's the core of EIP721Metadata we could argue that the function of the protocol are impacted. 
> Also the experience on frontends (etherscan, opensea, etc) would have been significantly degraded. It could easily be considered a medium issue to me - especially considering the previous comments / reactions and the label "confirmed" added by the sponsor while it was high.

**[HardlyDifficult (judge) increased severity to Medium and commented](https://github.com/code-423n4/2022-06-nibbl-findings/issues/317#issuecomment-1175198116):**
 > Thanks @Picodes! I can get onboard with that line of thinking. Given how significant these fields are for 3rd party integrators such as Etherscan and Opensea this can be considered to fall under that definition of Medium risk. I'll upgrade this report and the dupes to Medium.



***





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Nibbl |
| Report Date | N/A |
| Finders | cccz, Picodes |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-nibbl
- **GitHub**: https://github.com/code-423n4/2022-06-nibbl-findings/issues/317
- **Contest**: https://code4rena.com/contests/2022-06-nibbl-contest

### Keywords for Search

`vulnerability`

