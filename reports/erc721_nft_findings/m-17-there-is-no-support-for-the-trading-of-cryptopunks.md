---
# Core Classification
protocol: Foundation
chain: everychain
category: uncategorized
vulnerability_type: cryptopunks

# Attack Vector Details
attack_type: cryptopunks
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1595
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-foundation-contest
source_link: https://code4rena.com/reports/2022-02-foundation
github_link: https://github.com/code-423n4/2022-02-foundation-findings/issues/74

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
  - cryptopunks

protocol_categories:
  - dexes
  - cdp
  - services
  - indexes
  - liquidity_manager

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - leastwood
---

## Vulnerability Title

[M-17] There is no Support For The Trading of Cryptopunks

### Overview


This bug report is about the Foundation protocol not supporting the trading of Cryptopunks, a type of Non-Fungible Token (NFT). This puts the Foundation protocol at a severe disadvantage compared to other marketplaces, as Cryptopunks have their own internal marketplace which allows users to trade their NFTs to other users. The bug report includes a proof of concept implementation of what it might look like to integrate Cryptopunks into the Foundation protocol. The bug report recommends mitigating the issue by designing a wrapper contract for Cryptopunks to facilitate standard ERC721 transfers. This will ensure the user experience is not impacted.

### Original Finding Content

_Submitted by leastwood_

Cryptopunks are at the core of the NFT ecosystem. As one of the first NFTs, it embodies the culture of NFT marketplaces. By not supporting the trading of cryptopunks, Foundation is at a severe disadvantage when compared to other marketplaces. Cryptopunks have their own internal marketplace which allows users to trade their NFTs to other users. As such, cryptopunks does not adhere to the `ERC721` standard, it will always fail when the protocol attempts to trade them.

### Proof of Concept

Here is an example [implementation](https://github.com/code-423n4/2021-12-nftx/blob/main/nftx-protocol-v2/contracts/solidity/NFTXStakingZap.sol#L417-L424) of what it might look like to integrate cryptopunks into the Foundation protocol.

### Recommended Mitigation Steps

Consider designing a wrapper contract for cryptopunks to facilitate standard `ERC721` transfers. The logic should be abstracted away from the user such that their user experience is not impacted.

**[NickCuso (Foundation) acknowledged and commented](https://github.com/code-423n4/2022-02-foundation-findings/issues/74#issuecomment-1058006585):**
 > Yes, crypto punks is an important part of the ecosystem and this is on our radar. We are not planning on adding support at this time but we will revisiting this in the future.
> 
> I like the idea of using a wrapper contract of sorts. We will be looking for a way to keep the complexity out of the market contract itself like you suggest if at all possible.



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Foundation |
| Report Date | N/A |
| Finders | leastwood |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-foundation
- **GitHub**: https://github.com/code-423n4/2022-02-foundation-findings/issues/74
- **Contest**: https://code4rena.com/contests/2022-02-foundation-contest

### Keywords for Search

`CryptoPunks`

