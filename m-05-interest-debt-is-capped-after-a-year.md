---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3932
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-04-vader
github_link: https://github.com/code-423n4/2021-04-vader-findings/issues/219

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
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-05] Interest debt is capped after a year

### Overview


A bug has been found in the `Utils.getInterestOwed` function of a Solidity smart contract. This function computes the _interestPayment as a share of the payment over 1 year, but the `calcShare` function used caps the timeElapsed to _year, meaning that the owed interest does not grow after a year has elapsed. 

The impact of this bug is likely to be small as the only call so far computes the elapsed time as `block.timestamp - mapCollateralAsset_NextEra[collateralAsset][debtAsset]`, which is unlikely to go beyond a year. However, it is still recommended to fix the logic bug in case more functions are added that use the broken function.

The recommended mitigation step is to use a different function than `calcShare` that does not cap.

### Original Finding Content


The `Utils.getInterestOwed` function computes the `_interestPayment` as:

```solidity
uint256 _interestPayment =
  calcShare(
      timeElapsed,
      _year,
      getInterestPayment(collateralAsset, debtAsset)
  ); // Share of the payment over 1 year
```

However, `calcShare` caps `timeElpased` to `_year` and therefore the owed interest does not grow after a year has elapsed.

The impact is probably small because the only call so far computes the elapsed time as `block.timestamp - mapCollateralAsset_NextEra[collateralAsset][debtAsset];` which most likely will never go beyond a year.

It's still recommended to fix the logic bug in case more functions will be added that use the broken function.

Recommend using a different function than `calcShare` that does not cap.

**[strictly-scarce (vader) confirmed](https://github.com/code-423n4/2021-04-vader-findings/issues/219#issuecomment-830616264):**
 > A member who doesn't interact with the contract for more than a year misses out on some rewards, so severity:1



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-vader
- **GitHub**: https://github.com/code-423n4/2021-04-vader-findings/issues/219
- **Contest**: https://code4rena.com/contests/2021-04-vader-protocol-contest

### Keywords for Search

`vulnerability`

