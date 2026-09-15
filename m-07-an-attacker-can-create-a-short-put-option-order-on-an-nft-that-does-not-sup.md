---
# Core Classification
protocol: Putty
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 2940
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-06-putty-contest
source_link: https://code4rena.com/reports/2022-06-putty
github_link: https://github.com/code-423n4/2022-06-putty-findings/issues/16

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
  - synthetics
  - leveraged_farming
  - payments
  - options_vault

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - cccz
  - IllIllI  minhquanym
---

## Vulnerability Title

[M-07] An attacker can create a short put option order on an NFT that does not support ERC721 (like cryptopunk), and the user can fulfill the order, but cannot exercise the option

### Overview


This bug report is about an issue with PuttyV2.sol, a smart contract. An attacker can create a short put option on cryptopunk, a non-fungible token (NFT). When the user fulfills the order, the baseAsset will be transferred to the contract. However, since cryptopunk does not support ERC721, the user cannot exercise the option because the safeTransferFrom function call fails. The attacker can get a premium and get back the baseAsset after the option expires. The code for this vulnerability can be found in lines 343-346 and 628-629 of PuttyV2.sol. To mitigate this issue, the developers should consider adding a whitelist to NFTs in the order, or consider supporting exercising on cryptopunk.

### Original Finding Content

_Submitted by cccz, also found by IllIllI and minhquanym_

An attacker can create a short put option on cryptopunk. When the user fulfills the order, the baseAsset will be transferred to the contract. 

However, since cryptopunk does not support ERC721, the user cannot exercise the option because the safeTransferFrom function call fails. Attacker can get premium and get back baseAsset after option expires.

### Proof of Concept

<https://github.com/code-423n4/2022-06-putty/blob/3b6b844bc39e897bd0bbb69897f2deff12dc3893/contracts/src/PuttyV2.sol#L343-L346>

<https://github.com/code-423n4/2022-06-putty/blob/3b6b844bc39e897bd0bbb69897f2deff12dc3893/contracts/src/PuttyV2.sol#L628-L629>

### Recommended Mitigation Steps

Consider adding a whitelist to nfts in the order, or consider supporting exercising on cryptopunk.

**[STYJ (warden) commented](https://github.com/code-423n4/2022-06-putty-findings/issues/16#issuecomment-1174823604):**
 > Putty uses solmate's `ERC721.safeTransferFrom` which requires that the NFT contract implements `onERC721Received`. For the case of OG NFTs like punks and rocks, this will fail, https://github.com/Rari-Capital/solmate/blob/main/src/tokens/ERC721.sol#L120

**[thereksfour (warden) commented](https://github.com/code-423n4/2022-06-putty-findings/issues/16#issuecomment-1175910424):**
 > The user does not need to send cryptopunk to the contract when fulfilling the short put option order, but the user will pay a premium to the order creator. Later, when the user wants to exercise the option, since the cryptopunk does not support safetransferfrom, the user cannot exercise the option.

**[STYJ (warden) commented](https://github.com/code-423n4/2022-06-putty-findings/issues/16#issuecomment-1176031452):**
 > > The user does not need to send cryptopunk to the contract when fulfilling the short put option order, but the user will pay a premium to the order creator. Later, when the user wants to exercise the option, since the cryptopunk does not support safetransferfrom, the user cannot exercise the option.
> 
> Sorry, I did not consider this path. You are correct to say that a maker can create a short put option order with cryptopunks as a token and the holder of the long put option will not be able to exercise since cryptopunks cannot be transferred with `safeTransferFrom`. From that perspective, this is a valid issue. Thank you for bringing it up. I will defer to the judge for the final decision.

**[outdoteth (Putty Finance) acknowledged, but disagreed with severity and commented](https://github.com/code-423n4/2022-06-putty-findings/issues/16#issuecomment-1178923868):**
 > We dont intend to support cryptopunks or cryptokitties.
> If users wish to use these tokens then they can get wrapped versions (ex: wrapped cryptopunks).

**[HickupHH3 (judge) decreased severity to Medium and commented](https://github.com/code-423n4/2022-06-putty-findings/issues/16#issuecomment-1181762798):**
 > I thought cryptokitties are ERC721? I think they were the ones who popularized the standard actually :p 
> Probably meant etherrocks.
> 
> In general, non-compliant ERC-721 NFTs can be supported through wrappers, though some users might be unaware... Downgrading to med severity, similar to [this issue from another contest](https://github.com/code-423n4/2022-02-foundation-findings/issues/74).
> 
> 

**hyh (warden) reviewed mitigation:**
 > Similar to [M-01](https://github.com/code-423n4/2022-06-putty-findings/issues/50), [M-02](https://github.com/code-423n4/2022-06-putty-findings/issues/227).

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Putty |
| Report Date | N/A |
| Finders | cccz, IllIllI  minhquanym |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-putty
- **GitHub**: https://github.com/code-423n4/2022-06-putty-findings/issues/16
- **Contest**: https://code4rena.com/contests/2022-06-putty-contest

### Keywords for Search

`vulnerability`

