---
# Core Classification
protocol: Possumadapters
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44154
audit_firm: Shieldify
contest_link: none
source_link: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PossumAdapters-Security-Review.md
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

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

[L-05] `increaseAllowances()` Can Not Be Called Again Until the Entire Allowance of `principalToken` Is Used

### Overview

See description below for full details.

### Original Finding Content

## Severity

Low Risk

## Reported By

[CaeraDenoir](https://twitter.com/0xCaera)

## Description

Possible DoS depending on the amount of portal tokens in existence (future risk). This is due to `increaseAllowances()` increasing the allowance of the principal token with `safeIncreaseAllowance()`, which will revert if the allowance is not 0.

This is due to the `safeIncreaseAllowance()` itself and how it works since it has no overflow prevention.

The function `increaseAllowances()` passes the maximum amount possible for a `uint256`, which makes the entire `increaseAllowances()` revert if the oldAllowance does not equal 0. Not allowing `PSM` and `portalEnergyToken` to get their allowances increased after the first time. There is a comment stating `For ERC20 that require allowance to be 0 before increasing (e.g. USDT) add the following:`, but regardless of the token itself, the function will revert due to the SafeERC20 `safeIncreaseAllowance()` implementation.

It should be noted that if a lot of `portalEnergyToken` tokens are able to be minted, there is an easy way to deplete the allowance in the `AdapterV1` contract by calling `burnPortalEnergyToken()` and `mintPortalEnergyToken()` on loop.

## Impact

The impact on the `AdapterV1.sol` is high, but highly improbable in current conditions. Any inflation on the `portalEnergyToken` total supply (regardless if it is the current implementation or a different portal contract) would make the attack viable.

## Location of Affected Code

File: [src/AdapterV1.sol#L771](https://github.com/shieldify-security/SPP-Adapters/blob/335351b51a87ce3d20ea471d0f686776ce7d2393/src/AdapterV1.sol#L771)

## Recommendation

Regardless of the requirement of the allowance being 0, the `principalToken.approve(address(PORTAL), 0);` should not be commented.

## Team Response

Fixed as proposed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Shieldify |
| Protocol | Possumadapters |
| Report Date | N/A |
| Finders | Shieldify Security |

### Source Links

- **Source**: https://github.com/shieldify-security/audits-portfolio-md/blob/main/PossumAdapters-Security-Review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

