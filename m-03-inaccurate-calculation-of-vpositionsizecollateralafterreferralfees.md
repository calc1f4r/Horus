---
# Core Classification
protocol: GainsNetwork-February
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37800
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
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

[M-03] Inaccurate calculation of `v.positionSizeCollateralAfterReferralFees`

### Overview


This report describes a bug where the calculation for referral fees is incorrect. When calculating the referral reward, a different formula is used compared to when calculating the actual referral fee. As a result, the value used for calculating the position size after referral fees is incorrect, which leads to incorrect calculations for the government fee. The recommendation is to use the actual referral reward when calculating the position size after referral fees.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

When calculating v.positionSizeCollateralAfterReferralFees and reward1 (the actual referral reward), the following calculation will be used:

```solidity
    // ...
    if (_getMultiCollatDiamond().getTraderActiveReferrer(_trade.user) != address(0)) {
        // Use this variable to store position size for dev/gov fees after referral fees
        // and before volumeReferredUsd increases
>>>     v.positionSizeCollateralAfterReferralFees =
            (v.positionSizeCollateral *
                (100 *
                    PRECISION -
                    _getMultiCollatDiamond().calculateFeeAmount(
                        _trade.user,
                        _getMultiCollatDiamond().getReferralsPercentOfOpenFeeP(_trade.user)
                    ))) /
            100 /
            PRECISION;

>>>     v.reward1 = _distributeReferralReward(
            _trade.collateralIndex,
            _trade.user,
            _getMultiCollatDiamond().calculateFeeAmount(_trade.user, v.positionSizeCollateral), // apply fee tiers here to v.positionSizeCollateral itself to make correct calculations inside referrals
            _getMultiCollatDiamond().pairOpenFeeP(_trade.pairIndex),
            v.gnsPriceCollateral
        );

        _sendToVault(_trade.collateralIndex, v.reward1, _trade.user);

        _trade.collateralAmount -= uint120(v.reward1);

        emit ITradingCallbacksUtils.ReferralFeeCharged(_trade.user, _trade.collateralIndex, v.reward1);
    }
    // ...
```

Where the percentage of referral open fee is from `getReferralsPercentOfOpenFeeP` and using this formula :

```solidity
    function getPercentOfOpenFeeP_calc(uint256 _volumeReferredUsd) internal view returns (uint256 resultP) {
        IReferralsUtils.ReferralsStorage storage s = _getStorage();
        uint startReferrerFeeP = s.startReferrerFeeP;
        uint openFeeP = s.openFeeP;
        resultP =
            (openFeeP *
                (startReferrerFeeP *
                    PRECISION +
                    (_volumeReferredUsd * PRECISION * (100 - startReferrerFeeP)) /
                    1e18 /
                    s.targetVolumeUsd)) /
            100;

        resultP = resultP > openFeeP * PRECISION ? openFeeP * PRECISION : resultP;
    }
```

However, when calculating `reward1`, it will use `getReferrerFeeP`, which has a different formula to calculate the referrer fee :

```solidity
    function getReferrerFeeP(uint256 _pairOpenFeeP, uint256 _volumeReferredUsd) internal view returns (uint256) {
        IReferralsUtils.ReferralsStorage storage s = _getStorage();

        uint256 maxReferrerFeeP = (_pairOpenFeeP * 2 * s.openFeeP) / 100;

        uint256 minFeeP = (maxReferrerFeeP * s.startReferrerFeeP) / 100;

        uint256 feeP = minFeeP + ((maxReferrerFeeP - minFeeP) * _volumeReferredUsd) / 1e18 / s.targetVolumeUsd;

        return feeP > maxReferrerFeeP ? maxReferrerFeeP : feeP;
    }
```

This will result in `v.positionSizeCollateralAfterReferralFees` not being based on the actual referral fee. Consequently, when `v.positionSizeCollateralAfterReferralFees` is passed to `_handleGovFees` for calculating `govFee`, it will process the wrong value.

## Recommendations

Use the actual `reward1` instead when calculating `v.positionSizeCollateralAfterReferralFees` :

```solidity
v.positionSizeCollateralAfterReferralFees = v.positionSizeCollateral - v.reward1
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | GainsNetwork-February |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/GainsNetwork-security-review-February.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

