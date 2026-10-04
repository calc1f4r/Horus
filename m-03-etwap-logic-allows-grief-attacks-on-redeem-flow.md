---
# Core Classification
protocol: Covenant_2025-08-18
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62825
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Covenant-security-review_2025-08-18.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-03] ETWAP logic allows grief attacks on redeem flow

### Overview


The report discusses a bug in the ETWAP's implementation. This bug allows an attacker to manipulate the eTWAPBaseTokenSupply, which can prevent legitimate users from redeeming their tokens for several minutes. This can be done easily on smaller markets and can also cause DoS attacks on larger markets during periods of volatility. The report recommends applying the same logic in both directions to fix this issue.

### Original Finding Content


_Resolved_

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The  ETWAP's implementation is used to ensure that users can redeem approximately 25% every 1 hour. The `_calculateMarketState()` updates the `lastETWAPBaseSupply` logically when the base token supply drops and sets it immediately when `baseTokenSupply` is greater than or equal to `lastETWAPBaseSupply`:
```solidity
            // If baseTokenSupply has decreased since the last update, then decrease the ETWAPBaseSupply tracker
        if (marketState.baseTokenSupply < marketState.lexState.lastETWAPBaseSupply)
                marketState.lexState.lastETWAPBaseSupply =
                    marketState.lexState.lastETWAPBaseSupply.rayMul(updateFactor) +
                    marketState.baseTokenSupply.rayMul(WadRayMath.RAY - updateFactor); // eTWAP update if baseSupply decreased vs last update           <<@
```
```solidity
        // if baseTokenSupply has increased (even in same timeblock), update record
        if (marketState.baseTokenSupply >= marketState.lexState.lastETWAPBaseSupply)
            marketState.lexState.lastETWAPBaseSupply = marketState.baseTokenSupply; // immediatedly update if baseSupply increased vs last update                <<@

```
This `lastETWAPBaseSupply` is then passed onto `_checkRedeemCap()`, which reverts if the `remainingBaseSupply` is smaller than 75% of `eTWAPBaseTokenSupply`:
```solidity
    function _checkRedeemCap(
        uint256 marketBaseTokenSupply,
        uint256 eTWAPBaseTokenSupply,
        uint256 redeemAmount
    ) internal pure virtual {
        // OK to redeem any amount if marketBaseTokenSupply < MAX_REDEEM_NO_CAP
        // ie, for small markets there is no limit on how much can be redeemed.
        // But for bigger markets, approx. 25% can be redeemed every 1hr
        // (this is based on ETWAP_MIN_HALF_LIFE and MAX_REDEEM_FACTOR_CAP values)
        if (eTWAPBaseTokenSupply > MAX_REDEEM_NO_CAP) {
            uint256 remainingBaseSupply;
            unchecked {
                remainingBaseSupply = (marketBaseTokenSupply > redeemAmount) ? marketBaseTokenSupply - redeemAmount : 0;
            }
            if (remainingBaseSupply < eTWAPBaseTokenSupply.percentMul(MAX_REDEEM_FACTOR_CAP))
                revert LSErrors.E_LEX_RedeemCapExceeded();
        }
    }
```
However, the logic used here can be gamed by using the following attack:

1. A legitimate user holds some synth tokens that they would like to redeem.
2. The attacker can front-run such a transaction by leveraging a flash loan, calling the `mint()` function using a large amount, and immediately redeeming them in the same transaction.
3. This attack would spike the `eTWAPBaseTokenSupply` and, when orchestrated correctly, deny legitimate users from making a redemption till the `eTWAPBaseTokenSupply` normalises back, which would take several minutes.

This can be done easily on smaller markets and grief users for a brief period of time, and, if done methodically during volatility on larger markets, it can DoS a large chunk of users from redeeming.

## Recommendations

This issue arises due to the eTWAP logic considering only the base supply plunge; it is recommended to apply the same in both directions.





### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Covenant_2025-08-18 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Covenant-security-review_2025-08-18.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

