---
# Core Classification
protocol: Tokemak
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27110
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/101
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-tokemak-judging/issues/824

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
finders_count: 3
finders:
  - carrotsmuggler
  - saidam017
  - xiaoming90
---

## Vulnerability Title

M-18: Slashing during `LSTCalculatorBase.sol` deployment can show bad apr for months

### Overview


The contract `LSTCalculatorBase.sol` has a function to calculate the rough APR expected from a liquid staking token. The issue is that the function `calculateAnnualizedChangeMinZero` has a floor of 0, so if the backing of the LST decreases due to a slashing event in the initial 9 day period, the initial APR and `baseApr` will be set to 0. This can lead to wrong APR values being shown for up to 3 months, which can cause the protocol to sub optimally allocate funds for months, losing potential yield. It is recommended to initialize the APR with a specified value, rather than calculating it over the initial 9 days. This would prevent the wrong APR values from being shown for long periods of time and ensure that the protocol is optimally allocating funds.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-tokemak-judging/issues/824 

## Found by 
carrotsmuggler, saidam017, xiaoming90

Slashing during `LSTCalculatorBase.sol` deployment can show bad apr for months

## Vulnerability Detail

The contract `LSTCalculatorBase.sol` has some functions to calculate the rough APR expected from a liquid staking token. The contract is first deployed, and the first snapshot is taken after `APR_FILTER_INIT_INTERVAL_IN_SEC`, which is 9 days. It then calculates the APR between the deployment and this first snapshot, and uses that to initialize the APR value. It uses the function `calculateAnnualizedChangeMinZero` to do this calculation.

The issue is that the function `calculateAnnualizedChangeMinZero` has a floor of 0. So if the backing of the LST decreases over that 9 days due to a slashing event in that interval, this function will return 0, and the initial APR and `baseApr` will be set to 0.

The calculator is designed to update the APR at regular intervals of 3 days. However, the new apr is given a weight of 10% and the older apr is given a weight of 90% as seen below.

```solidity
return ((priorValue * (1e18 - alpha)) + (currentValue * alpha)) / 1e18;
```

And alpha is hardcoded to 0.1. So if the initial APR starts at 0 due to a slashing event in the initial 9 day period, a large number of updates will be required to bring the APR up to the correct value.

Assuming the correct APR of 6%, and an initial APR of 0%, we can calculate that it takes upto 28 updates to reflect close the correct APR. This transaltes to 84 days. So the wrong APR cann be shown for upto 3 months. Tha protocol uses these APR values to justify the allocation to the various protocols. Thus a wrong APR for months would mean the protocol would sub optimally allocate funds for months, losing potential yield.

## Impact

The protocol can underperform for months due to slashing events messing up APR calculations close to deployment date.

## Code Snippet

https://github.com/sherlock-audit/2023-06-tokemak/blob/main/v2-core-audit-2023-07-14/src/stats/calculators/base/LSTCalculatorBase.sol#L108-L110

## Tool used

Manual Review

## Recommendation

It is recommended to initialize the APR with a specified value, rather than calculate it over the initial 9 days. 9 day window is not good enough to get an accurate APR, and can be easily manipulated by a slashing event.



## Discussion

**codenutt**

This behavior is acceptable. If we happen to see a slash > 12 bps over the initial 9 days, yes, we set it to 0. It increases the ramp time for that LST so pools with that LST will be set aside for a while until some APR (incentive, etc) comes up. For larger slashes that are more material (> 25bps), we have a 90 day penalty anyway.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Tokemak |
| Report Date | N/A |
| Finders | carrotsmuggler, saidam017, xiaoming90 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-tokemak-judging/issues/824
- **Contest**: https://app.sherlock.xyz/audits/contests/101

### Keywords for Search

`vulnerability`

