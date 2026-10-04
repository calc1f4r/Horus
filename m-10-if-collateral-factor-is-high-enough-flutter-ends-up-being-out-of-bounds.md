---
# Core Classification
protocol: USSD - Autonomous Secure Dollar
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19150
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/82
source_link: none
github_link: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/889

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
  - algo-stables

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - neumo
  - J4de
---

## Vulnerability Title

M-10: If collateral factor is high enough, flutter ends up being out of bounds

### Overview


This bug report is about an issue with the `USSDRebalancer` contract, in which a rebalance call reverts if the collateral factor is greater than all the elements of the `flutterRatios` array. This is because the `flutter` value, which is calculated as the lowest index of the `flutterRatios` array for which the collateral factor is smaller than the flutter ratio, is set to equal the length of the `flutterRatios` array if the collateral factor is greater than all the elements. This `flutter` value is then used in two places, where it can cause an index out of bounds error if it is greater than the length of `flutterRatios` array.

The impact of this issue is high, as it can make a rebalance call always revert. The code snippet for this issue can be found at https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSDRebalancer.sol#L178-L184. The issue was found through manual review.

The recommendation for this issue is to check that the `flutter` value is always less than the length of the `flutterRatios` array when checking `collateral[i].ratios[flutter]`. The issue was escalated for 10 USDC, and it was found to be a valid low issue. It was also found that the flutterRatios array can be adjusted by the admin.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/889 

## Found by 
J4de, neumo
## Summary
In `USSDRebalancer` contract, function `SellUSSDBuyCollateral` will revert everytime a rebalance calls it, provided the collateral factor is greater than all the elements of the `flutterRatios` array.

## Vulnerability Detail
Function `SellUSSDBuyCollateral` calculates `flutter` as the lowest index of the `flutterRatios` array for which the collateral factor is smaller than the flutter ratio.
```solidity
uint256 cf = IUSSD(USSD).collateralFactor();
uint256 flutter = 0;
for (flutter = 0; flutter < flutterRatios.length; flutter++) {
	if (cf < flutterRatios[flutter]) {
	  break;
	}
}
```
The problem arises when, if collateral factor is greater than all flutter values, after the loop `flutter = flutterRatios.length`.

This `flutter` value is used afterwards here:
```solidity
...
if (collateralval * 1e18 / ownval < collateral[i].ratios[flutter]) {
  portions++;
}
...
```
 And here:
 ```solidity
...
if (collateralval * 1e18 / ownval < collateral[i].ratios[flutter]) {
  if (collateral[i].token != uniPool.token0() || collateral[i].token != uniPool.token1()) {
	// don't touch DAI if it's needed to be bought (it's already bought)
	IUSSD(USSD).UniV3SwapInput(collateral[i].pathbuy, daibought/portions);
  }
}
...
```

As we can see in the tests of the project, the flutterRatios array and the collateral ratios array are set to be of the same length, so if flutter = flutterRatios.length, any call to that index in the `ratios` array will revert with an index out of bounds.

## Impact
High, when the collateral factor reaches certain level, a rebalance that calls `SellUSSDBuyCollateral` will always revert.

## Code Snippet
https://github.com/sherlock-audit/2023-05-USSD/blob/main/ussd-contracts/contracts/USSDRebalancer.sol#L178-L184

## Tool used
Manual review.


## Recommendation
When checking `collateral[i].ratios[flutter]` always check first that flutter is `< flutterRatios.length`.





## Discussion

**neumoxx**

Escalate for 10 USDC
The issue is marked as duplicate of #940, and in that issue there's a comment from the judge that states `This is an admin input, requires admin error to cause problems`. The issue does not depend on an admin input to arise. The flutter ratios are set in the tests according to values mentioned in the whitepaper: https://github.com/sherlock-audit/2023-05-USSD/blob/6d7a9fdfb1f1ed838632c25b6e1b01748d0bafda/ussd-contracts/test/USSDsimulator.test.js#L391-L393. 
The collateral factor:
https://github.com/sherlock-audit/2023-05-USSD/blob/6d7a9fdfb1f1ed838632c25b6e1b01748d0bafda/ussd-contracts/contracts/USSD.sol#L179-L191
can grow beyond the last value of the flutter ratios array and that would make the `SellUSSDBuyCollateral` function to revert.

**sherlock-admin**

 > Escalate for 10 USDC
> The issue is marked as duplicate of #940, and in that issue there's a comment from the judge that states `This is an admin input, requires admin error to cause problems`. The issue does not depend on an admin input to arise. The flutter ratios are set in the tests according to values mentioned in the whitepaper: https://github.com/sherlock-audit/2023-05-USSD/blob/6d7a9fdfb1f1ed838632c25b6e1b01748d0bafda/ussd-contracts/test/USSDsimulator.test.js#L391-L393. 
> The collateral factor:
> https://github.com/sherlock-audit/2023-05-USSD/blob/6d7a9fdfb1f1ed838632c25b6e1b01748d0bafda/ussd-contracts/contracts/USSD.sol#L179-L191
> can grow beyond the last value of the flutter ratios array and that would make the `SellUSSDBuyCollateral` function to revert.

You've created a valid escalation for 10 USDC!

To remove the escalation from consideration: Delete your comment.

You may delete or edit your escalation comment anytime before the 48-hour escalation window closes. After that, the escalation becomes final.

**ctf-sec**

[here](https://github.com/sherlock-audit/2023-05-USSD/blob/6d7a9fdfb1f1ed838632c25b6e1b01748d0bafda/ussd-contracts/contracts/USSDRebalancer.sol#L62)

```solidity
    function setFlutterRatios(uint256[] calldata _flutterRatios) public onlyControl {
      flutterRatios = _flutterRatios;
    }
```

flutterRatios can be adjusted by admin

Valid low

**hrishibhat**

Result:
Medium
Has duplicates
This is a valid issue where the rebalance reverts in certain conditions due to the unexpected final loop flutter values. 

**sherlock-admin**

Escalations have been resolved successfully!

Escalation status:
- [neumoxx](https://github.com/sherlock-audit/2023-05-USSD-judging/issues/889/#issuecomment-1605375095): accepted

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | USSD - Autonomous Secure Dollar |
| Report Date | N/A |
| Finders | neumo, J4de |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-05-USSD-judging/issues/889
- **Contest**: https://app.sherlock.xyz/audits/contests/82

### Keywords for Search

`vulnerability`

