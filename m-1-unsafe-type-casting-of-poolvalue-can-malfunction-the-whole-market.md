---
# Core Classification
protocol: Float Capital
chain: everychain
category: uncategorized
vulnerability_type: type_casting

# Attack Vector Details
attack_type: type_casting
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3509
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/15
source_link: none
github_link: https://github.com/sherlock-audit/2022-11-float-capital-judging/issues/45

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 5

# Context Tags
tags:
  - type_casting
  - signed/unsigned

protocol_categories:
  - dexes
  - cdp
  - services
  - derivatives
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WATCHPUG
---

## Vulnerability Title

M-1: Unsafe type casting of `poolValue` can malfunction the whole market

### Overview


This bug report is about an issue in the Float Capital Market smart contract related to unsafe type casting of `poolValue`. This issue was found by WATCHPUG and was reported on GitHub. 

When `poolValue` is a negative number due to loss in `valueChange` and `funding`, the unsafe type casting from `int256` to `uint256` will result in a huge number close to `2**255` which will revert `_rebalancePoolsAndExecuteBatchedActions()` due to overflow when multiplied by 1e18 at line 163. This can happen when the funding rate is 100% per year and the `EPOCH_LENGTH` is 4 days, as the funding fee for each epoch can be as much as ~1% on the effectiveValue.

The impact of this issue is that `_rebalancePoolsAndExecuteBatchedActions` will revert and cause the malfunction of the whole market. The code snippet related to this issue can be found at the following link: https://github.com/sherlock-audit/2022-11-float-capital/blob/main/contracts/market/template/MarketCore.sol#L118-L185.

The recommended solution to this issue is to consider adding a new function to properly handle the bankruptcy of a specific pool. It was also discussed that a safe guard could be added to check that with both funding and value change, 99% is the maximum a pool can lose in any single iteration. It was also suggested to add checks to the epoch length on construction to ensure the smart contract is safe.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-11-float-capital-judging/issues/45 

## Found by 
WATCHPUG

## Summary

When `poolValue` is a negative number due to loss in `valueChange` and `funding`, the unsafe type casting from `int256` to `uint256` will result in a huge number close to `2**255` which will revert `_rebalancePoolsAndExecuteBatchedActions()` due to overflow when multiplied by 1e18 at L163.

## Vulnerability Detail

If the funding rate is 100% per year and the `EPOCH_LENGTH` is 4 days, the funding fee for each epoch can be as much as ~1% on the effectiveValue.

Plus, the loss from `valueChange` is capped at 99%, but combining both can still result in a negative `poolValue` at L146.

At L163 `uint256 price = uint256(poolValue).div(tokenSupply);` the type casting from `int256` to `uint256` will result in a huge number close to `2**255`.

`MathUintFloat.div()` will overflow when a number as large as `2**255` is multiplied by 1e18.

## Impact

`_rebalancePoolsAndExecuteBatchedActions` will revert and cause the malfunction of the whole market.

## Code Snippet

https://github.com/sherlock-audit/2022-11-float-capital/blob/main/contracts/market/template/MarketCore.sol#L118-L185

## Tool used

Manual Review

## Recommendation

Consider adding a new function to properly handle the bankruptcy of a specific pool.

## Discussion

**JasoonS**

We seed the pools initially with sufficient un-extractable capital such that this shouldn't be an issue (it should never get close to 0 - even after millions of years and trillions of transactions that may have rounding down and all users withdrawing their funds).

We could create a safe cast function to check - but we made `poolValue` an int256 so that it is easier to operate on with other signed integers - not because it is ever possible for it to be negative. So it would be redundant in this case.

**moose-code**

@JasoonS Want to relook at this. @WooSungD @Stentonian maybe you also have thoughts. 

I believe watchpug is explaining something different. 

They are saying that poolValue can be negative, as a 99% capped loss of poolValue, in conjunction with a 1% funding fee (imagine the side is very overbalanced), will result in the pool value losing more than 100% in total. 

A safe guard would be to check that with BOTH funding and value change, 99% is the maximum a pool can lose in any single iteration. 

Given system parameterizations, where epoch length will never be that long and funding rate should never be that high, its unlikely this would be an issue in practice, but likely still worth making a change for. 

Let me know if anyone has thoughts 

**JasoonS**

Yes, you're right, went through these too fast.

We've discussed this internally a few times. This point should've made it into the readme.

We could add checks to the epoch length on construction to ensure were safe

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Float Capital |
| Report Date | N/A |
| Finders | WATCHPUG |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-11-float-capital-judging/issues/45
- **Contest**: https://app.sherlock.xyz/audits/contests/15

### Keywords for Search

`Type casting, Signed/Unsigned`

