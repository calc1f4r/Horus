---
# Core Classification
protocol: Nouns DAO
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21329
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf
github_link: none

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
  - yield
  - cross_chain
  - rwa
  - nft_marketplace

# Audit Details
report_date: unknown
finders_count: 5
finders:
  - tchkvsky
  - Christos Papakonstantinou
  - Rajeev
  - r0bert
  - hyh
---

## Vulnerability Title

Upgrading timelock without transferring the nouns from old timelock balance will increase adjusted total supply

### Overview


This bug report is regarding the total supply of a token. The severity of the bug is medium risk. The context of the bug is ProposeTimelockMigrationCleanupMainnet.s.sol#L94. The bug states that there is one noun on timelock V1 balance, and can be others as of migration time. Changing ds.timelock without nouns transfer will increase adjusted total supply and cause a loss per noun or cumulatively for all nouns holders. The recommendation is to consider adding to ProposeTimelockMigrationCleanupMainnet the step of moving the treasury nouns from timelock V1 to timelock V2 contract to keep adjustedTotalSupply() reading unchanged. The nouns have been fixed in PR 721 and the fix looks okay on the condition that timelockV1 owns no other nouns besides 687as of time of the upgrade. 

In summary, this bug report is about the total supply of a token. The severity of the bug is medium risk and the context is ProposeTimelockMigrationCleanupMainnet.s.sol#L94. It states that changing ds.timelock without nouns transfer will increase adjusted total supply and cause a loss per noun or cumulatively for all nouns holders. The recommendation is to consider adding the step of moving the treasury nouns from timelock V1 to timelock V2 contract to keep adjustedTotalSupply() reading unchanged. The nouns have been fixed in PR 721 and the fix looks okay on the condition that timelockV1 owns no other nouns besides 687as of time of the upgrade.

### Original Finding Content

## Severity: Medium Risk

## Context
ProposeTimelockMigrationCleanupMainnet.s.sol#L94

## Description
There is one noun on timelock V1 balance, and there can be others as of migration time:

- [Etherscan Token Link](https://etherscan.io/token/0x9c8ff314c9bc7f6e59a9d9225fb22946427edc03?a=0x0BC3807Ec262cB779b38D65b38158acC3bfedE10)

Changing `ds.timelock` without nouns transfer will increase adjusted total supply:

- NounsDAOV3Fork.sol#L199-L201

```solidity
function adjustedTotalSupply(NounsDAOStorageV3.StorageV3 storage ds) internal view returns (uint256) {
    return ds.nouns.totalSupply() - ds.nouns.balanceOf(address(ds.timelock)) - ds.forkEscrow.numTokensOwnedByDAO(); 
}
```

As of the time of this writing, `adjustedTotalSupply()` will be increased by 1 due to treasury token reclassification. The upgrade will cause a 

```
(13470 + 14968) * 1733.0 * (1 / 742 - 1 / 743) = 89 USD loss per noun
or
(13470 + 14968) * 1733.0 / 743 = 66330 USD cumulatively for all nouns holders.
```

Per high likelihood and low impact, the severity is set to medium.

## Recommendation
Consider adding to ProposeTimelockMigrationCleanupMainnet the step of moving the treasury nouns from timelock V1 to timelock V2 contract to keep `adjustedTotalSupply()` reading unchanged.

## Nouns
Fixed in PR 721.

## Spearbit
Fix looks okay. Conditional on that `timelockV1` owns no other nouns besides 687 as of the time of the upgrade.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Nouns DAO |
| Report Date | N/A |
| Finders | tchkvsky, Christos Papakonstantinou, Rajeev, r0bert, hyh |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Nouns-Spearbit-Security-Review.pdf

### Keywords for Search

`vulnerability`

