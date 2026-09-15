---
# Core Classification
protocol: Dyad
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44037
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Dyad-Security-Review.md
github_link: none

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
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Shieldify Security
---

## Vulnerability Title

[H-02] Insufficient Exogenous Collateral Check in `VaultManagerV2::liquidate()` function

### Overview


This bug report discusses an issue with the code for a protocol called Code4rena, specifically with the liquidation process. The report explains that if a user's collateral backing falls below 100% but their overall backing is still above 150%, they will not be liquidated. This can lead to problems with the overall collateral backing of the system and may cause users to withdraw their funds. The report recommends allowing liquidations when the collateral backing falls below 100% to prevent the system from becoming fractionally collateralized. The team has acknowledged the issue and may consider making changes to the code.

### Original Finding Content

## Severity

High Risk

## Description

Code4rena issue #338 linked [here](https://github.com/code-423n4/2024-04-dyad-findings/issues/338).

The issue shows that liquidations do not go through if the exogenous collateral does not sufficiently back the `DYAD` minted.

The protocol lays down 2 ground rules:

1. Exo collateral backs `DYAD` at least 1:1 (100%)
2. Kerosene can be used to keep the minimum backing to 150%.

So for this to function properly, a user must have exo-backing of 100% and exo+kerosene backing of 150%. But if a user's exo-backing falls below 100% but their exo+kerosene backing is still above 150%, they won't get liquidated:

```solidity
if (collatRatio(id) >= MIN_COLLAT_RATIO) revert CrTooHigh();
```

This can lead to systematic problems with collateral backing.For instance, if there is 1 million USD worth of exo collateral, and 1 million DYAD minted. Let's also say 600k USD worth of kerosene is in the vaults as well.

Now, Exo collateral backing = 1 million / 1 million = 100%
Total backing = `1.6 / 1 = 160%`.

Now, say the price of the exo collateral drops so there is only 950k USD worth of exo collateral left. Exo collateral backing = 950k / 1 million = 95%
Total backing = `1.55 / 1 = 155 %`.

If this was a single vault, this wouldn't be liquidatable since the CR is still above 150%.

The overall backing of the system is not 100% with exo collateral anymore. This can lead to people closing and withdrawing funds from their vaults, which further reduces the TVL of the system.

The main idea is that the system and individual vaults can reach a state where some of the `DYAD` is backed by kerosene, and not by other exo collateral. This would make it a fractionally collateralized stablecoin, like `FRAX` or `DEI`, both of which had stability issues and `FRAX` later voted to fully collateralize itself.

## Location of Affected Code

File [src/core/VaultManagerV2.sol#L179](https://github.com/DyadStablecoin/contracts/blob/37b4d8bbbb59de52b25056fa8b9759203fe2bc1d/src/core/VaultManagerV2.sol#L179)

## Recommendation

Consider allowing liquidations when exo collateral backing goes below 100% as well. This will prevent the total exo collateral backing from going below 100% unless it is a large bad debt event.

## Team Response

Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Dyad |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/Dyad-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

