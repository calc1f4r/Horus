---
# Core Classification
protocol: Astaria
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 21851
audit_firm: Spearbit
contest_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
source_link: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
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
  - rwa
  - staking_pool
  - nft_lending
  - cdp
  - dexes

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Saw-Mon and Natalie
  - Jonah1005
  - Blockdev
---

## Vulnerability Title

A malicious collateralized NFT token can block liquidation and also epoch processing for public vaults

### Overview


This bug report discusses a vulnerability in the CollateralToken and PublicVault contracts. When a lien is liquidated, the CollateralToken attempts to create a Seaport auction for the underlying token. During this process, the CollateralToken sends an approval to the ERC721 token, which could be malicious or compromised. If the approval call reverts, the lien cannot be liquidated, and the epoch processing for the public vault is halted. 

To mitigate this vulnerability, the strategist or public vault owner/delegate should ensure that the ERC721 tokens have been checked to make sure they won't revert the approval call. Alternatively, the approval could be moved to the conduit step when a lien is committed or opened, so that if the call reverts, the lien is not created. This comes with some risks, as the conduit would hold the token approval for a longer period than the current implementation.

### Original Finding Content

## Severity: Medium Risk

## Context
- CollateralToken.sol#L523-L526
- PublicVault.sol#L353-L357

## Description
When a lien gets liquidated, the `CollateralToken` tries to create a Seaport auction for the underlying token. One of the steps in this process is to give approval for the token id to the `CollateralToken`'s conduit:

```solidity
ERC721(orderParameters.offer[0].token).approve(
    s.CONDUIT,
    orderParameters.offer[0].identifierOrCriteria
);
```

A malicious/compromised `ERC721(orderParameters.offer[0].token)` can take advantage of this step and revert the `approve(...)`. There are few consequences for this, with the last being the most important one:

1. One would not be able to liquidate the expired lien.
2. Because of 1, the epoch processing for a corresponding public vault will be halted, since one can only process the current epoch if all of its open liens are paid for or liquidated:
   ```solidity
   if (s.epochData[s.currentEpoch].liensOpenForEpoch > 0) {
       revert InvalidVaultState(InvalidVaultStates.LIENS_OPEN_FOR_EPOCH_NOT_ZERO);
   }
   ```

### Recommendations
1. The strategist or the public vault owner/delegate needs to make sure to only sign roots of the trees with the leaves such that their corresponding ERC721 tokens have been thoroughly checked to ensure they will not be able to revert the approve call.
2. Alternatively, one can move the approval to the conduit step when a lien is committed to/opened. This way, if the call reverts, a lien is not created, so the epoch processing for the public vault would not be halted. This comes with some risks, as the conduit would hold the token approval for a longer period compared to the current implementation where it only has the approval during the liquidation phase.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Spearbit |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | Saw-Mon and Natalie, Jonah1005, Blockdev |

### Source Links

- **Source**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/spearbit/portfolio/blob/master/pdfs/Astaria-Spearbit-Security-Review-July.pdf

### Keywords for Search

`vulnerability`

