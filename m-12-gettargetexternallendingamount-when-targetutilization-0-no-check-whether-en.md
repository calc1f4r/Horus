---
# Core Classification
protocol: Notional Update #5
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30175
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/142
source_link: none
github_link: https://github.com/sherlock-audit/2023-12-notional-update-5-judging/issues/51

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
  - bin2chen
---

## Vulnerability Title

M-12: getTargetExternalLendingAmount() when targetUtilization == 0  no check whether enough externalUnderlyingAvailableForWithdraw

### Overview


This bug report discusses an issue with the `getTargetExternalLendingAmount()` function in the `ExternalLending.sol` contract. When the `targetUtilization` is set to 0, the function directly returns a `targetAmount` of 0 without checking if there is enough `externalUnderlyingAvailableForWithdraw`. This can cause the `_rebalanceCurrency()` function to revert due to insufficient balance for withdrawal. The vulnerability can be triggered by setting all targets to zero, which may occur if governance wants to pull funds quickly from an external lending protocol. The impact of this bug could be significant as it could prevent the rebalancing of funds and potentially result in a loss. The recommendation is to remove the direct return of 0 and allow the subsequent logic to handle a `targetUtilization` of 0. 

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-12-notional-update-5-judging/issues/51 

## Found by 
bin2chen
## Summary
in `getTargetExternalLendingAmount()`
When `targetUtilization == 0`, it directly returns `targetAmount=0`.
It lacks the judgment of whether there is enough `externalUnderlyingAvailableForWithdraw`.
This may cause `_rebalanceCurrency()` to `revert` due to insufficient balance for `withdraw`.

## Vulnerability Detail

when `setRebalancingTargets()`  , we can setting all the targets to zero to immediately exit money
it will call `_rebalanceCurrency() -> _isExternalLendingUnhealthy() -> getTargetExternalLendingAmount()` 
```solidity
    function getTargetExternalLendingAmount(
        Token memory underlyingToken,
        PrimeCashFactors memory factors,
        RebalancingTargetData memory rebalancingTargetData,
        OracleData memory oracleData,
        PrimeRate memory pr
    ) internal pure returns (uint256 targetAmount) {
        // Short circuit a zero target
@>      if (rebalancingTargetData.targetUtilization == 0) return 0;

....
        if (targetAmount < oracleData.currentExternalUnderlyingLend) {
            uint256 forRedemption = oracleData.currentExternalUnderlyingLend - targetAmount;
            if (oracleData.externalUnderlyingAvailableForWithdraw < forRedemption) {
                // increase target amount so that redemptions amount match externalUnderlyingAvailableForWithdraw
                targetAmount = targetAmount.add(
                    // unchecked - is safe here, overflow is not possible due to above if conditional
                    forRedemption - oracleData.externalUnderlyingAvailableForWithdraw
                );
            }
        }
```

When `targetUtilization==0`, it returns `targetAmount ==0`.
It lacks the other judgments of whether the current `externalUnderlyingAvailableForWithdraw` is sufficient.
Exceeding `externalUnderlyingAvailableForWithdraw` may cause `_rebalanceCurrency()` to revert.

For example:
`currentExternalUnderlyingLend = 100`
`externalUnderlyingAvailableForWithdraw = 99`
If `targetUtilization` is modified to `0`,
then `targetAmount` should be `1`, not `0`.
`0` will cause an error due to insufficient available balance for withdrawal.

So, it should still try to withdraw as much deposit as possible first, wait for replenishment, and then withdraw the remaining deposit until the deposit is cleared.

## Impact

A too small `targetAmount` may cause AAVE withdraw to fail, thereby causing the inability to `setRebalancingTargets()` to fail.

## Code Snippet
https://github.com/sherlock-audit/2023-12-notional-update-5/blob/main/contracts-v3/contracts/internal/balances/ExternalLending.sol#L44
## Tool used

Manual Review

## Recommendation

Remove `targetUtilization == 0` directly returning 0.

The subsequent logic of the method can handle `targetUtilization == 0` normally and will not cause an error.

```diff
    function getTargetExternalLendingAmount(
        Token memory underlyingToken,
        PrimeCashFactors memory factors,
        RebalancingTargetData memory rebalancingTargetData,
        OracleData memory oracleData,
        PrimeRate memory pr
    ) internal pure returns (uint256 targetAmount) {
        // Short circuit a zero target
-       if (rebalancingTargetData.targetUtilization == 0) return 0;
```



## Discussion

**sherlock-admin2**

1 comment(s) were left on this issue during the judging contest.

**takarez** commented:
>  valid because {valid medium and a duplicate of 052}



**nevillehuang**

@jeffywu Is the impact of this significant and can compound to cause a material enough loss due to inability to rebalance? Also who is responsible for maintaining a high enough `externalUnderlyingAvailableForWithdraw`?

**jeffywu**

Hmm, I guess this would be tripped if governance tries to set the target utilization to zero. Likely, this occurs if we want to pull funds very quickly from an external lending protocol. The check is important to ensure that we pull as much funds as we can without reverting.

This issue would significantly hamper our ability to get out of a lending protocol quickly. A higher severity could be justified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Notional Update #5 |
| Report Date | N/A |
| Finders | bin2chen |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-12-notional-update-5-judging/issues/51
- **Contest**: https://app.sherlock.xyz/audits/contests/142

### Keywords for Search

`vulnerability`

