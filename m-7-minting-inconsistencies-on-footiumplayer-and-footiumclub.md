---
# Core Classification
protocol: Footium
chain: everychain
category: uncategorized
vulnerability_type: mint_vs_safemint

# Attack Vector Details
attack_type: mint_vs_safemint
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18608
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/71
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-footium-judging/issues/342

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
  - mint_vs_safemint
  - erc721
  - nft

# Audit Details
report_date: unknown
finders_count: 37
finders:
  - 0xStalin
  - jasonxiale
  - ali\_shehab
  - shame
  - 0xPkhatri
---

## Vulnerability Title

M-7: Minting inconsistencies on FootiumPlayer and FootiumClub

### Overview


The bug report is about two contracts, FootiumPlayer.sol and FootiumClub.sol, related to the minting of NFTs. The FootiumClub.sol contract is using the `_mint()` function instead of the `_safeMint()` function, which can cause the contract to mint a club to a contract that does not support NFTs. This issue was found by a group of people, including 0xAsen, 0xHati, 0xLook, 0xPkhatri, 0xRobocop, 0xStalin, 0xeix, 0xhacksmithh, BAHOZ, Bauchibred, Bauer, Dug, GalloDaSballo, Koolex, PTolev, Phantasmagoria, TheNaubit, Tricko, ali_shehab, cergyk, chaithanya_gali, ctf_sec, cuthalion0x, deadrxsezzz, descharre, indijanc, jasonxiale, kiki_dev, lewisbroadhurst, nzm_, oualidpro, sashik_eth, shame, shogoki, tsueti_, tsvetanovv, and wzrdk3lly. The impact of this issue is that FootiumClub.sol might mint a club NFT to a contract that cannot handle NFTs. The code snippet that is related to the issue can be found at https://github.com/sherlock-audit/2023-04-footium/blob/main/footium-eth-shareable/contracts/FootiumClub.sol#L65. The issue was found using manual review. The recommendation is to use `_safeMint()` as in FootiumPlayer.sol.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-footium-judging/issues/342 

## Found by 
0xAsen, 0xHati, 0xLook, 0xPkhatri, 0xRobocop, 0xStalin, 0xeix, 0xhacksmithh, BAHOZ, Bauchibred, Bauer, Dug, GalloDaSballo, Koolex, PTolev, Phantasmagoria, TheNaubit, Tricko, ali\_shehab, cergyk, chaithanya\_gali, ctf\_sec, cuthalion0x, deadrxsezzz, descharre, indijanc, jasonxiale, kiki\_dev, lewisbroadhurst, nzm\_, oualidpro, sashik\_eth, shame, shogoki, tsueti\_, tsvetanovv, wzrdk3lly
## Summary

The `FootiumClub.sol` contract when minting uses `_mint()` instead of `_safeMint()` which can cause to mint a club to a contract who does not support nfts. On the other hand `FootiumPlayer.sol` uses `_safeMint()`.

## Vulnerability Detail

See summary.

## Impact

`FootiumClub.sol` might mint a club NFT to a contract that cannot handle nfts.

## Code Snippet

https://github.com/sherlock-audit/2023-04-footium/blob/main/footium-eth-shareable/contracts/FootiumClub.sol#L65

## Tool used

Manual Review

## Recommendation

Use `_safeMint()` as in FootiumPlayer.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Footium |
| Report Date | N/A |
| Finders | 0xStalin, jasonxiale, ali\_shehab, shame, 0xPkhatri, Dug, 0xeix, 0xAsen, tsvetanovv, 0xHati, Phantasmagoria, kiki\_dev, descharre, wzrdk3lly, ctf\_sec, deadrxsezzz, Bauer, 0xhacksmithh, Koolex, Tricko, 0xRobocop, Bauchibred, cuthalion0x, cergyk, lewisbroadhurst, PTolev, BAHOZ, GalloDaSballo, 0xLook, shogoki, tsueti\_, chaithanya\_gali, indijanc, sashik\_eth, TheNaubit, oualidpro, nzm\_ |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-footium-judging/issues/342
- **Contest**: https://app.sherlock.xyz/audits/contests/71

### Keywords for Search

`mint vs safeMint, ERC721, NFT`

