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
solodit_id: 3656
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/8
source_link: none
github_link: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/180

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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
finders_count: 1
finders:
  - 0xRajeev
---

## Vulnerability Title

H-18: Lien buyout with new terms does not update the slope of public vaults

### Overview


This bug report is about an issue in the code of the AstariaRouter and PublicVault contracts, which are part of the Sherlock Audit 2022-10-astaria-judging project. The issue, found by 0xRajeev, is that when a lien is bought out with new terms, the slope for the public vault is not updated. This can lead to liquidations with a public vault involved reverting, and the implied value of a public vault being incorrect. The code snippet for the issue is from the VaultImplementation.sol and LienToken.sol contracts, and the tool used for finding the issue was manual review. The recommendation is to calculate the slope of the lien before the buyout, subtract the calculated slope value from the PublicVault.slope, update the lien terms, recalculate the slope and add the new updated slope value to the PublicVault.slope.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/180 

## Found by 
0xRajeev

## Summary

Lien buyout with new terms does not update the slope of public vaults leading to reverts and potential insolvency of vaults.

## Vulnerability Detail

In the `VaultImplementation.buyoutLien` function, a lien is bought out with new terms. Terms of a lien (last, start, rate, duration) will have changed after a buyout. This changes the slope calculation, however, after the buyout, the slope for the public vault is not updated.

## Impact

There are multiple parts of the code affected by this.

1) When liquidating, the vault slope is adjusted by the liens slope (see https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/AstariaRouter.sol#L385-L387). In case of a single lien, the PublicVault.updateVaultAfterLiquidation function can revert if the lien terms have changed previously due to a buyout (https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/PublicVault.sol#L532). Hence, liquidations with a public vault involved, will revert.

2) The PublicVault contract calculates the implied value of a vault (ie. totalAssets) with the use of the slope value (see https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/PublicVault.sol#L412). As the slope value can be outdated, this leads to undervalue or overvalue of a public vault and thus vault share calculations will be incorrect.

## Code Snippet

1. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/VaultImplementation.sol#L280-L304
2. https://github.com/sherlock-audit/2022-10-astaria/blob/main/src/LienToken.sol#L150-L153

## Tool used

Manual Review

## Recommendation

Calculate the slope of the lien before the buyout in the `VautImplementation.buyoutLien` function, subtract the calculated slope value from `PublicVault.slope`, update lien terms, recalculate the slope and add the new updated slope value to `PublicVault.slope`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Astaria |
| Report Date | N/A |
| Finders | 0xRajeev |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-10-astaria-judging/issues/180
- **Contest**: https://app.sherlock.xyz/audits/contests/8

### Keywords for Search

`vulnerability`

