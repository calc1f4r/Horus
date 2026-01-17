---
# Core Classification
protocol: Dahlia
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46378
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/ed6235a0-67c8-4339-a4da-8550f4c0d443
source_link: https://cdn.cantina.xyz/reports/cantina_dahlia_november2024.pdf
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
finders_count: 3
finders:
  - Saw-mon and Natalie
  - kankodu
  - Yorke Rhodes
---

## Vulnerability Title

Inconsistency between precision factors / dimensional analysis 

### Overview


This bug report is about a precision/dimensional analysis issue in the code for the WrappedVault and VaultMarketHub contracts. The problem arises when comparing the incentivesRatesRequested and previewRateAfterDeposit functions, as they should have the same precision/dimension but do not always match. This is because the precision of these functions depends on the decimals of the reward and deposit tokens. The recommendation is to ensure that the rewardsRate returned by previewRateAfterDeposit is correctly scaled according to the difference in decimals between the reward and deposit tokens.

### Original Finding Content

## Context

**File:** WrappedVault.sol  
**Lines:** 511-516

## Description

The precision/dimensional analysis for `rewardsRate` and `dahliaRate` are matching:

```
1018[I]
[T][L]
```

In this case where `[I] = [L]` simplifies to:

```
[T]
```

The discrepancy arises when one looks at the code in `VaultMarketHub.allocateOffer(...)`:

**File:** VaultMarketHub.sol  
**Lines:** 232-234

```solidity
offer.incentivesRatesRequested[i] >
WrappedVault(offer.targetVault).previewRateAfterDeposit(offer.incentivesRequested[i], fillAmount),
```

In this comparison, both sides should have the same precision/dimension. According to the NatSpec for `incentivesRatesRequested`:

**File:** VaultMarketHub.sol  
**Lines:** 23-24

```solidity
/// @custom:field incentivesRatesRequested The desired incentives per input token per second to fill the offer, measured in,
/// wei of incentives per wei of deposited assets per second, scaled up by 1e18 to avoid precision loss
```

In other words:

```
[incentivesRatesRequested] = 10^18 · (10^18/10 dI)[I]
[T](10^18/10 dL)[L] = 10^(18+dL−dI)[I]
[T][L]
```

In the finding, the notation `[·]` represents the precision (`prec = 10^x`) or dimension of a quantity.

| Parameter | Description                                                             |
|-----------|-------------------------------------------------------------------------|
| I         | reward                                                                  |
| L         | DEPOSIT_ASSET or loan token of the corresponding Dahlia market.        |
| T         | timestamp in seconds                                                    |
| dX        | X.decimals()                                                           |

As soon as the reward and deposit token do not have the same decimals, the precision of `WrappedVault(offer.targetVault).previewRateAfterDeposit(...)` and `offer.incentivesRatesRequested[I]` would not match.

## Recommendation

Make sure that `rewardsRate` (WrappedVault.sol#L517) returned by `previewRateAfterDeposit` is scaled (up or down) accordingly with the factor of `10^(dL−dI)`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Dahlia |
| Report Date | N/A |
| Finders | Saw-mon and Natalie, kankodu, Yorke Rhodes |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_dahlia_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/ed6235a0-67c8-4339-a4da-8550f4c0d443

### Keywords for Search

`vulnerability`

