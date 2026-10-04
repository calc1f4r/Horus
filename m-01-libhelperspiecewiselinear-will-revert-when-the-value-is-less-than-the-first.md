---
# Core Classification
protocol: Angle Protocol
chain: everychain
category: uncategorized
vulnerability_type: missing_check

# Attack Vector Details
attack_type: missing_check
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20818
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-01-dev-test-repo
source_link: https://code4rena.com/reports/2022-01-dev-test-repo
github_link: https://github.com/code-423n4/2023-06-angle-findings/issues/40

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
  - missing_check

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - auditor0517
---

## Vulnerability Title

[M-01] LibHelpers.piecewiseLinear will revert when the value is less than the first element of the array

### Overview


This bug report is about a potential issue in the Angle Protocol's Transmuter contract. The issue occurs when the `LibHelpers.piecewiseLinear` method is used in the `Redeemer` contract, and the collateral ratio is below the first element of the `xRedemptionCurve`. In this case, the redemption will revert. The `xRedemptionCurveMem` is not limited, so `collatRatio` can be less than the first element of the array. The `LibHelpers.piecewiseLinear` method will then revert on the following line.

To mitigate this issue, the developers added a handler for this edge case. This handler was confirmed by the judge and full details are available in reports from Lambda, auditor0517, and Jeiwan.

### Original Finding Content


<https://github.com/AngleProtocol/angle-transmuter/blob/9707ee4ed3d221e02dcfcd2ebaa4b4d38d280936/contracts/transmuter/facets/Redeemer.sol#L156-L157> <br><https://github.com/AngleProtocol/angle-transmuter/blob/9707ee4ed3d221e02dcfcd2ebaa4b4d38d280936/contracts/transmuter/libraries/LibSetters.sol#L230-L240> <br><https://github.com/AngleProtocol/angle-transmuter/blob/9707ee4ed3d221e02dcfcd2ebaa4b4d38d280936/contracts/transmuter/libraries/LibHelpers.sol#L77-L80>

`LibHelpers.piecewiseLinear` reverts when the value is less than the first element of the array. This method is used in Redeemer contract and if the collateral ratio is below the first element of xRedemptionCurve, the redepmtion will revert.

### Proof of Concept

In `Redeemer._quoteRedemptionCurve`, a penalty factor is applied when the protocol is under-collateralized using `LibHelpers.piecewiseLinear`.

Redeemer.sol#L156-L157

```solidity
        uint64[] memory xRedemptionCurveMem = ts.xRedemptionCurve;
        penaltyFactor = uint64(LibHelpers.piecewiseLinear(collatRatio, xRedemptionCurveMem, yRedemptionCurveMem));
```

`xRedemptionCurveMem` is strictly increasing and upper bounded by `BASE_9`, and there's no more limitations.

LibSetters.sol

```solidity
230        (action == ActionType.Redeem && (xFee[n - 1] > BASE_9 || yFee[n - 1] < 0 || yFee[n - 1] > int256(BASE_9)))
           
233        for (uint256 i = 0; i < n - 1; ++i) {
234            if (
           
240                (action == ActionType.Redeem && (xFee[i] >= xFee[i + 1] || yFee[i] < 0 || yFee[i] > int256(BASE_9)))
```

So `collatRatio` can be less than the first element of `xRedemptionCurveMem`. In that case, `LibHelpers.findLowerBound` will return 0 and `LibHelpers.piecewiseLinear` will revert on the following line.

LibHelpers.sol#L77-L80

```solidity
    return
        yArray[indexLowerBound] +
        ((yArray[indexLowerBound + 1] - yArray[indexLowerBound]) * int64(x - xArray[indexLowerBound])) /
        int64(xArray[indexLowerBound + 1] - xArray[indexLowerBound]);
```

`Redeemer._redeem` calls `_quoteRedemptionCurve`, so the redemption will be blocked in this case.

### Recommended Mitigation Steps

We can add the following line to mitigate this issue.

```solidity
    if (indexLowerBound == 0 && x < xArray[0]) return yArray[0];
```

**[Picodes (Angle) confirmed and commented](https://github.com/code-423n4/2023-06-angle-findings/issues/40#issuecomment-1628608115):**
 > Indeed we are assuming throughout the test base that the first value is 0 but the check is missing in the code so there this could happen. It's kind of conditional to a misconfiguration though. Leaving it up to the judge.

**[hansfriese (Judge) commented](https://github.com/code-423n4/2023-06-angle-findings/issues/40#issuecomment-1628647579):**
 > @Picodes - Medium is appropriate because it's likely to happen with the current configuration.

**[Angle mitigated](https://github.com/code-423n4/2023-07-angle-mitigation/blob/main/README.md#mitigations-to-be-reviewed):**
> PR: https://github.com/AngleProtocol/angle-transmuter/commit/5f7635cdab52b75416309d45f8cd253609c705ff<br>
> Add a handler for this edge case.

**Status:** Mitigation confirmed. Full details in reports from [Lambda](https://github.com/code-423n4/2023-07-angle-mitigation-findings/issues/9), [auditor0517](https://github.com/code-423n4/2023-07-angle-mitigation-findings/issues/25), and [Jeiwan](https://github.com/code-423n4/2023-07-angle-mitigation-findings/issues/16).



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Angle Protocol |
| Report Date | N/A |
| Finders | auditor0517 |

### Source Links

- **Source**: https://code4rena.com/reports/2022-01-dev-test-repo
- **GitHub**: https://github.com/code-423n4/2023-06-angle-findings/issues/40
- **Contest**: https://code4rena.com/reports/2022-01-dev-test-repo

### Keywords for Search

`Missing Check`

