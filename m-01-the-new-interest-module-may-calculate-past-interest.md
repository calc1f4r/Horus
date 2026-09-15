---
# Core Classification
protocol: Ionprotocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36435
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
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

[M-01] The new interest module may calculate past interest

### Overview


This bug report discusses an issue with the `updateInterestRateModule` function in the Ion Protocol. This function allows the Ion Protocol to change the module used for calculating interest for lenders and borrowers. However, it has been observed that this function does not trigger the `_accrueInterest` function or update the `ilk.lastRateUpdate` values, which could result in unexpected interest accrual amounts for borrowers and lenders. The report recommends triggering the `_accrueInterest` function before changing the interest rate module, or updating all `ilk.lastRateUpdate` values after the change to ensure it only affects future interest accrual. The Ion Protocol team is aware of this issue but has decided not to fix it, as it currently serves as a way to revert a misbehaving interest rate module.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

`updateInterestRateModule` can be called by Ion Protocol to change `interestRateModule` that will be used when calculating interest for lenders and borrowers.

```solidity
    function updateInterestRateModule(InterestRate _interestRateModule) external onlyRole(ION) {
        // @audit - should trigger accrueInterest here? or at least must update timestamp last
        if (address(_interestRateModule) == address(0)) revert InvalidInterestRateModule(_interestRateModule);

        IonPoolStorage storage $ = _getIonPoolStorage();

        // Sanity check
        if (_interestRateModule.COLLATERAL_COUNT() != $.ilks.length) {
            revert InvalidInterestRateModule(_interestRateModule);
        }
        $.interestRateModule = _interestRateModule;

        emit InterestRateModuleUpdated(address(_interestRateModule));
    }
```

However, it can be observed that `_accrueInterest` is not triggered, and neither are all `ilk.lastRateUpdate` values updated to the current `block.timestamp`. This could cause issues, as if `_accrueInterest` was not previously called for a considerable amount of time, the new `interestRateModule` will be used to calculate interest for past lenders' and borrowers' performance.

```solidity
    function _calculateRewardAndDebtDistributionForIlk(
        uint8 ilkIndex,
        uint256 totalEthSupply
    )
        internal
        view
        returns (
            uint256 supplyFactorIncrease,
            uint256 treasuryMintAmount,
            uint104 newRateIncrease,
            uint256 newDebtIncrease,
            uint48 timestampIncrease
        )
    {
        // ...
        uint256 totalDebt = _totalNormalizedDebt * ilk.rate; // [WAD] * [RAY] = [RAD]

        (uint256 borrowRate, uint256 reserveFactor) =
>>>         $.interestRateModule.calculateInterestRate(ilkIndex, totalDebt, totalEthSupply);
        if (borrowRate == 0) return (0, 0, 0, 0, 0);

        // Calculates borrowRate ^ (time) and returns the result with RAY precision
>>>     uint256 borrowRateExpT = _rpow(borrowRate + RAY, block.timestamp - ilk.lastRateUpdate, RAY);

        // Unsafe cast OK
        timestampIncrease = uint48(block.timestamp) - ilk.lastRateUpdate;

        // ...
        newRateIncrease = ilk.rate.rayMulUp(borrowRateExpT - RAY).toUint104(); // [RAY]

        // ...
    }
```

This behavior may result in unexpected interest accrual amounts for borrowers or lenders.

**Recommendations**

Consider triggering `_accrualInterest` before changing the `interestRateModule`. If the previous `interestRateModule` is broken or causes calls to revert, update all `ilk.lastRateUpdate` to `block.timestamp` after changing `interestRateModule`, ensuring it will only be used for future interest accrual.

**Ion Protocol comments**

We are aware of this behavior. It is true that the admin can change the IRM without accruing interest.

- But this is currently thought of as a feature, as this is the only way to revert a misbehaving IRM. If there was a significant flaw in the ARM, the admin can redeploy the interest rate module without accruing interest. (`pause()` will accrue interest).

Acknowledged, but will not fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ionprotocol |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/IonProtocol-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

