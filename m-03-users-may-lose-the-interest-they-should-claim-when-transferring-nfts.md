---
# Core Classification
protocol: Harvestflowv2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 55530
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarvestFlowV2-Security-Review.md
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[M-03] Users May Lose the Interest They Should Claim When Transferring NFTs

### Overview


The report highlights a bug in the `LendingNFT` contract where the `claim()` function is not being called in the NFT's transfer hook. This means that the contract cannot guarantee that the NFT is claimed and transferred in the same block, which can result in users losing interest before maturity. To avoid this, users must either create their own contract or use a service like Flashbots, which may be difficult for regular users. The recommendation is to call `claim()` in the transfer hook to fix the issue. The team has responded that the bug has been fixed.

### Original Finding Content

## Severity

Medium Risk

## Description

In `LendingNFT`, `claim()` is not called in the NFT's [transfer hook](https://github.com/chiru-labs/ERC721A-Upgradeable/blob/main/contracts/ERC721AUpgradeable.sol#L690).

This means that the contract cannot guarantee that `claim()` and transfer of the NFT occur in the same block.
If users want to ensure that claiming and transferring an NFT happen in the same block and that claiming occurs before transferring, they can only achieve this by creating a contract themselves to call it or creating a bundle through Flashbots, which is obviously highly difficult for ordinary users.

Before maturity, interest will increase with the increase of `block.timestamp`.

```solidity
// Proportion of time interval from the beginning of the lending period until now to a year, scaled to the 1e18
uint256 proportionOfIntervalTotalScaled = ((Math.min(block.timestamp, maturity) - lendingAt) * 1e18) / year;
```

If the transfer of the NFT occurs in a block after the `claim()`, the interest generated during this period cannot be obtained by the previous owner.

For example:

1. Before maturity, Alice wants to transfer her NFT to Bob.
2. Alice first executes the `claim()` and then transfers the NFT.
3. Due to this vulnerability, Alice's two transactions may end up in different blocks, assuming they are separated by one block.
4. Alice cannot receive the interest for that one block, even though it rightfully belongs to her, as she still owned the NFT during this period.
5. Ultimately, the interest in that block, which should have belonged to Alice, ends up belonging to Bob.

## Location of Affected Code

File: [LendingNFT.sol#L622](https://github.com/tokyoweb3/HARVESTFLOW_Ver.2/blob/main/contracts/src/LendingNFT.sol#L622)

## Impact

Before maturity, if users want to transfer NFTs, they may lose the interest they are entitled to. To avoid this, users must either create their own contracts or use services like Flashbots, which is challenging for regular users.

## Recommendation

Call `claim()` in NFT's [transfer hook](https://github.com/chiru-labs/ERC721A-Upgradeable/blob/main/contracts/ERC721AUpgradeable.sol#L690)

## Team Response

Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Harvestflowv2 |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/HarvestFlowV2-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

