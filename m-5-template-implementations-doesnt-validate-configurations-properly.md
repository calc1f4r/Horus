---
# Core Classification
protocol: NFTPort
chain: everychain
category: uncategorized
vulnerability_type: royalty

# Attack Vector Details
attack_type: royalty
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3550
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/14
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-nftport-judging/issues/83

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 0.80
financial_impact: medium

# Scoring
quality_score: 4
rarity_score: 5

# Context Tags
tags:
  - royalty
  - erc2981

protocol_categories:
  - dexes
  - services
  - liquidity_manager
  - nft_lending
  - payments

# Audit Details
report_date: unknown
finders_count: 12
finders:
  - pashov
  - cccz
  - JohnnyTime
  - joestakey
  - Dravee
---

## Vulnerability Title

M-5: Template implementations doesn't validate configurations properly

### Overview


This bug report is about a vulnerability in the NftPort template implementations which allows admins to set an invalid configuration, such as a royalty percentage higher than 100%, when initializing or updating contracts. This could lead to users paying a large amount of royalty, which could potentially result in insolvency of the protocol. 

The bug was found by ElKu, rvierdiiev, obront, pashov, ctf\_sec, joestakey, ak1, JohnnyTime, GimelSec, Dravee, JohnSmith, and cccz. It was identified through manual review.

The bug was fixed by hyperspacebunny in a pull request which checks `royaltiesBps` both in `initialize()` and `update()` functions, and uses `_validatePropertyChange()` to check values both in `initialize()` and `updateConfig()` functions. This was confirmed by rayn731. 

The issue serves as a reminder that even trustable entities can make mistakes, and any fields that might potentially result in insolvency of protocol should be thoroughly checked.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-nftport-judging/issues/83 

## Found by 
ElKu, rvierdiiev, obront, pashov, ctf\_sec, joestakey, ak1, JohnnyTime, GimelSec, Dravee, JohnSmith, cccz

## Summary

In past audits, we have seen contract admins claim that invalidated configuration setters are fine since “admins are trustworthy”. However, cases such as [Nomad got drained for over $150M](https://twitter.com/samczsun/status/1554260106107179010) and [Misconfiguration in the Acala stablecoin project allows attacker to steal 1.2 billion aUSD](https://web3isgoinggreat.com/single/misconfiguration-in-the-acala-stablecoin-project-allows-attacker-to-steal-1-2-billion-ausd) have shown again and again that even trustable entities can make mistakes. Thus any fields that might potentially result in insolvency of protocol should be thoroughly checked.

NftPort template implementations often ignore checks for config fields. For the rest of the issue, we take `royalty` related fields as an example to illustrate potential consequences of misconfigurations. Notably, lack of check is not limited to `royalty`, but exists among most config fields.

Admins are allowed to set a wrong `royaltiesBps` which is higher than `ROYALTIES_BASIS`. `royaltyInfo()` will accept this invalid `royaltiesBps` and users will pay a large amount of royalty.

## Vulnerability Detail

EIP-2981 (NFT Royalty Standard) defines `royaltyInfo()` function that specifies how much to pay for a given sale price. In general, royalty should not be higher than 100%. [NFTCollection.sol](https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/NFTCollection.sol#L348) checks that admins can't set royalties to more than 100%:
```solidity
    /// Validate a runtime configuration change
    function _validateRuntimeConfig(RuntimeConfig calldata config)
        internal
        view
    {
        // Can't set royalties to more than 100%
        require(config.royaltiesBps <= ROYALTIES_BASIS, "Royalties too high");

        ...
```

But `NFTCollection` only check `royaltiesBps` when admins call `updateConfig()`, it doesn't check `royaltiesBps` in `initialize()` function, leading to admins could set an invalid `royaltiesBps` (higher than 100%) when initializing contracts.

The same problem exists in ERC721NFTProduct and ERC1155NFTProduct. Both ERC721NFTProduct and ERC1155NFTProduct don't check `royaltiesBasisPoints` in `initialize()` function. Furthermore, these contracts also don't check `royaltiesBasisPoints` when admins call `update()` function. It means that admins could set an invalid `royaltiesBasisPoints` which may be higher than 100% in any time.

## Impact

EIP-2981 only defines `royaltyInfo()` that it should return royalty amount rather than royalty percentage. It means that if the contract has an invalid royalty percentage which is higher than 100%, `royaltyInfo()` doesn't revert and users will pay a large amount of royalty.

## Code Snippet

https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/NFTCollection.sol#L348
https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/NFTCollection.sol#L153
https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/ERC721NFTProduct.sol#L91
https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/ERC721NFTProduct.sol#L201
https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/ERC1155NFTProduct.sol#L96
https://github.com/sherlock-audit/2022-10-nftport/blob/main/evm-minting-master/contracts/templates/ERC1155NFTProduct.sol#L238


## Tool used

Manual Review

## Recommendation

Check `royaltiesBps <= ROYALTIES_BASIS` both in `initialize()` and `update()` functions.

## Discussion

**hyperspacebunny**

Fixed in https://github.com/nftport/evm-minting-sherlock-fixes/pull/11

**rayn731**

LGTM, It checks `royaltiesBps` both in `initialize()` and `update()` functions.
And uses `_validatePropertyChange()` to check values both in `initialize()` and `updateConfig()` functions.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 4/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | NFTPort |
| Report Date | N/A |
| Finders | pashov, cccz, JohnnyTime, joestakey, Dravee, ElKu, JohnSmith, ak1, rvierdiiev, obront, GimelSec, ctf\_sec |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-nftport-judging/issues/83
- **Contest**: https://app.sherlock.xyz/audits/contests/14

### Keywords for Search

`Royalty, ERC2981`

