---
# Core Classification
protocol: Zer0 - zBanc
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 13393
audit_firm: ConsenSys
contest_link: none
source_link: https://consensys.net/diligence/audits/2021/05/zer0-zbanc/
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

protocol_categories:
  - dexes
  - cdp
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - David Oz Kashi
  - Martin Ortner
---

## Vulnerability Title

zBanc - DynamicLiquidTokenConverter input validation ✓ Fixed

### Overview


This bug report describes an issue with the zBanc/solidity/contracts/converter/types/liquid-token/DynamicLiquidTokenConverter.sol contract. The issue is that the contract allows values of 0 to 4.294,967295% to be used for the `PPM` value, which can lead to functionality not working correctly. In order to fix this issue, the checks for `_validReserveWeight` should be reintroduced to make sure that the value is within valid bounds `_weight > 0 && _weight <= PPM_RESOLUTION`. This would help to catch obviously wrong and often erroneously passed parameters early. The bug has been fixed with [zer0-os/[email protected]`ff3d913`](https://github.com/zer0-os/zBanc/commit/ff3d91390099a4f729fe50c846485589de4f8173) by checking that the provided values are at least 0% < p <= 100%.

### Original Finding Content

#### Resolution



fixed with [zer0-os/[email protected]`ff3d913`](https://github.com/zer0-os/zBanc/commit/ff3d91390099a4f729fe50c846485589de4f8173) by checking that the provided values are at least 0% < p <= 100%.


#### Description


Check that the value in `PPM` is within expected bounds before updating system settings that may lead to functionality not working correctly. For example, setting out-of-bounds values for `stepWeight` or `setMinimumWeight` may make calls to `reduceWeight` fail. These values are usually set in the beginning of the lifecycle of the contract and misconfiguration may stay unnoticed until trying to reduce the weights. The settings can be fixed, however, by setting the contract inactive and updating it with valid settings. Setting the contract to inactive may temporarily interrupt the normal operation of the contract which may be unfavorable.


#### Examples


Both functions allow the full `uint32` range to be used, which, interpreted as `PPM` would range from `0%` to `4.294,967295%`


**zBanc/solidity/contracts/converter/types/liquid-token/DynamicLiquidTokenConverter.sol:L75-L84**



```
function setMinimumWeight(uint32 \_minimumWeight)
    public
    ownerOnly
    inactive
{
    //require(\_minimumWeight > 0, "Min weight 0");
    //\_validReserveWeight(\_minimumWeight);
    minimumWeight = \_minimumWeight;
    emit MinimumWeightUpdated(\_minimumWeight);
}

```
**zBanc/solidity/contracts/converter/types/liquid-token/DynamicLiquidTokenConverter.sol:L92-L101**



```
function setStepWeight(uint32 \_stepWeight)
    public
    ownerOnly
    inactive
{
    //require(\_stepWeight > 0, "Step weight 0");
    //\_validReserveWeight(\_stepWeight);
    stepWeight = \_stepWeight;
    emit StepWeightUpdated(\_stepWeight);
}

```
#### Recommendation


Reintroduce the checks for `_validReserveWeight` to check that a percent value denoted in `PPM` is within valid bounds `_weight > 0 && _weight <= PPM_RESOLUTION`. There is no need to separately check for the value to be `>0` as this is already ensured by `_validReserveWeight`.


Note that there is still room for misconfiguration (step size too high, min-step too high), however, this would at least allow to catch obviously wrong and often erroneously passed parameters early.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | ConsenSys |
| Protocol | Zer0 - zBanc |
| Report Date | N/A |
| Finders | David Oz Kashi, Martin Ortner |

### Source Links

- **Source**: https://consensys.net/diligence/audits/2021/05/zer0-zbanc/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

