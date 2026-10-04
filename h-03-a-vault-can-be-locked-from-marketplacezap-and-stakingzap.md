---
# Core Classification
protocol: NFTX
chain: everychain
category: uncategorized
vulnerability_type: wrong_math

# Attack Vector Details
attack_type: wrong_math
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1216
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-nftx-contest
source_link: https://code4rena.com/reports/2021-12-nftx
github_link: https://github.com/code-423n4/2021-12-nftx-findings/issues/107

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 2

# Context Tags
tags:
  - wrong_math

protocol_categories:
  - dexes
  - cross_chain
  - rwa
  - leveraged_farming
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 9
finders:
  - GreyArt
  - pauliax
  - cmichel
  - leastwood
  - WatchPug
---

## Vulnerability Title

[H-03] A vault can be locked from MarketplaceZap and StakingZap

### Overview


This bug report is about a vulnerability in the NFTXMarketplaceZap.sol and NFTXStakingZap.sol contracts. Any user that owns a vToken of a particular vault can lock the functionalities of these contracts for everyone. This is because of a check that is performed by the marketplace when dealing with vToken minting. A malicious user could transfer any amount > 0 of a vault’vToken to the marketplace (or staking) zap contracts, thus making the vault functionality unavailable for every user on the marketplace. The proof of concept can be found at two Github links. To mitigate this vulnerability, the logic should be removed from the marketplace and staking zap contracts, and added to the vaults if necessary.

### Original Finding Content

_Submitted by p4st13r4, also found by cmichel, GreyArt, hyh, jayjonah8, leastwood, pauliax, shenwilly, and WatchPug_

Any user that owns a vToken of a particular vault can lock the functionalities of `NFTXMarketplaceZap.sol` and `NFTXStakingZap.sol` for everyone.

Every operation performed by the marketplace, that deals with vToken minting, performs this check:

```jsx
require(balance == IERC20Upgradeable(vault).balanceOf(address(this)), "Did not receive expected balance");
```

A malicious user could transfer any amount > 0 of a vault’vToken to the marketplace (or staking) zap contracts, thus making the vault functionality unavailable for every user on the marketplace

#### Proof of Concept

<https://github.com/code-423n4/2021-12-nftx/blob/main/nftx-protocol-v2/contracts/solidity/NFTXMarketplaceZap.sol#L421>

<https://github.com/code-423n4/2021-12-nftx/blob/main/nftx-protocol-v2/contracts/solidity/NFTXMarketplaceZap.sol#L421>

#### Recommended Mitigation Steps

Remove this logic from the marketplace and staking zap contracts, and add it to the vaults (if necessary)

**[0xKiwi (NFTX) confirmed, but disagreed with high severity and commented](https://github.com/code-423n4/2021-12-nftx-findings/issues/107#issuecomment-1003193410):**
 > Valid concern, confirmed. And disagreeing with severity.

**[0xKiwi (NFTX) resolved](https://github.com/code-423n4/2021-12-nftx-findings/issues/107)**

**[LSDan (judge) commented](https://github.com/code-423n4/2021-12-nftx-findings/issues/107#issuecomment-1064511914):**
 > In this case I agree with the warden's severity. The attack would cause user funds to be locked and is incredibly easy to perform.



***

 


### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 2/5 |
| Audit Firm | Code4rena |
| Protocol | NFTX |
| Report Date | N/A |
| Finders | GreyArt, pauliax, cmichel, leastwood, WatchPug, shenwilly, jayjonah8, hyh, p4st13r4 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-nftx
- **GitHub**: https://github.com/code-423n4/2021-12-nftx-findings/issues/107
- **Contest**: https://code4rena.com/contests/2021-12-nftx-contest

### Keywords for Search

`Wrong Math`

