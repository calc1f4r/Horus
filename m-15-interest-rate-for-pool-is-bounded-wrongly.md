---
# Core Classification
protocol: Ajna
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 6312
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/32
source_link: none
github_link: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/96

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

protocol_categories:
  - dexes
  - cdp
  - services
  - launchpad
  - synthetics

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - yixxas
---

## Vulnerability Title

M-15: Interest rate for pool is bounded wrongly

### Overview


This bug report is about an issue found in the PoolDeployer.sol contract, which is part of the Sherlock Audit project. The issue is that the interest rate for pools is bounded incorrectly, limiting pools from being deployed with the intended range of 1-10%. The issue was found by yixxas, and the code snippet responsible for this issue can be found on Github. 

The issue is that in the PoolDeployer.sol contract, the `MIN_RATE` and `MAX_RATE` are set to 0.01 and 0.1 respectively, which indicates the 1% and 10% value in which we should allow interest rate to be set. However, in the `canDeploy` modifier, a more than or equal sign is used to do the comparison, and reverts when the condition is true. This means that we can only set interest rate in the range of 2-9%, which is not intended. 

The impact of this issue is that interest rate is bounded wrongly, limiting pools from being deployed with the intended range. The recommendation to fix this issue is to change to a strict comparison instead when doing the comparison.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/96 

## Found by 
yixxas

## Summary
It is documented that pools can be created for tokens with interest rate between 1-10%.

> Pool creators: create pool by providing a fungible token for quote and collateral and an interest rate between 1-10%

However, due to a wrong implementation, pools can only be created between 2-9%.

## Vulnerability Detail
In PoolDeployer.sol contract we have `MIN_RATE = 0.01 * 1e18` and `MAX_RATE = 0.1 * 1e18`. This indicates the 1% and 10% value in which we should allow interest rate to be set. 

However, in our `canDeploy` modifier, it causes a revert when the following condition is true.

> `if (MIN_RATE >= interestRate_ || interestRate_ >= MAX_RATE)         revert IPoolFactory.PoolInterestRateInvalid()`

A more than or equal sign is used to do the comparison, and reverts. This means that we can only set interest rate in the range of 2-9%, which I believe is not intended.

## Impact
Interest rate is bounded wrongly, limiting pools from being deployed with the intended range.

## Code Snippet
https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/base/PoolDeployer.sol#L13-L14
https://github.com/sherlock-audit/2023-01-ajna/blob/main/contracts/src/base/PoolDeployer.sol#L38-L43

## Tool used

Manual Review

## Recommendation
Change to a strict comparison instead when doing the comparison.

```diff
- if (MIN_RATE >= interestRate_ || interestRate_ >= MAX_RATE)         revert IPoolFactory.PoolInterestRateInvalid();
+ if (MIN_RATE > interestRate_ || interestRate_ > MAX_RATE)         revert IPoolFactory.PoolInterestRateInvalid();
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 5/5 |
| Audit Firm | Sherlock |
| Protocol | Ajna |
| Report Date | N/A |
| Finders | yixxas |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-01-ajna-judging/issues/96
- **Contest**: https://app.sherlock.xyz/audits/contests/32

### Keywords for Search

`vulnerability`

