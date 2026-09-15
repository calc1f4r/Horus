---
# Core Classification
protocol: Morpho
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46707
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/4d01ab83-48c3-4ca2-ba71-237f46d2fd6a
source_link: https://cdn.cantina.xyz/reports/cantina_morpho_september2024.pdf
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
  - cdp
  - derivatives
  - dexes
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Om Parikh
  - 0xdeadbeef
  - tnch
---

## Vulnerability Title

Unfair pricing of metamorpho share when it is used as collateral in morpho market 

### Overview


The report discusses an issue with the MetaMorpho software where the pricing of a vault's share is not accurate in certain situations. This is due to the use of the MorphoChainlinkOracleV2.sol feature, which does not properly account for lost assets in the vault. The developers suggest modifying the oracle to adjust the share price based on offchain risk assessment and implementing circuit breakers to temporarily halt certain functions. The developers are aware of the issue but do not believe it requires any changes to the code. Cantina Managed has acknowledged the issue.

### Original Finding Content

## MetaMorpho Vault Pricing Issue

## Context
(No context files were provided by the reviewer)

## Description
MetaMorpho uses `MorphoChainlinkOracleV2.sol` for fair pricing of the vault's share. However, in the case of a vault that supports **lostAssets** (i.e., no share price decrease feature), if `lostAssets > 0` and bad debt is not repaid externally, the oracle would give the inflated price. 

As per discussion with the morpho team in this comment:

> For a vault with 50% of bad debt, it is highly more likely that it will experience bad debt, sooner or later. When it will happen, users will not be able to get anything out of their shares. Is it sound to price shares at $0.5? Not sure. But in this case, lenders lending against these shares already lost, so it's not even very useful to care about the price.

It is still important that shares are priced closest to the actual redeemable price since that would allow borrowers to be liquidated and lenders a fair chance to participate in a bank-run for the remaining 50%. Morpho Labs believes that it's not a good idea to lend against a vault that has significant lost assets, so pricing the vault in such situations should not be cared about.

Though it is true that lending will pause against such a vault when off-chain consensus is reached that the debt hole is large enough, the majority of the impact is from capital already at stake and not then newly anticipated incoming assets.

## Recommendation
The current oracle should be modified for vaults supporting **lostAssets** to:

- Assess the risk off-chain for bad debt and adjust the share price by some tolerance threshold. Since the price is only used for computing borrowable and liquidation, once bad debt has started accruing, the effective price can be aggressively reduced, and after a certain point, it can be a step function switching it to 0.
- Have circuit breakers in place to revert in the `price()` function temporarily until a fair price is assessed off-chain and put on-chain. This will also revert liquidations and borrows temporarily.

## Acknowledgments
**Morpho Labs:** Acknowledged. We are aware of this issue, as mentioned, and we don't think that it requires any change in the code.  
**Cantina Managed:** Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Morpho |
| Report Date | N/A |
| Finders | Om Parikh, 0xdeadbeef, tnch |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_morpho_september2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/4d01ab83-48c3-4ca2-ba71-237f46d2fd6a

### Keywords for Search

`vulnerability`

