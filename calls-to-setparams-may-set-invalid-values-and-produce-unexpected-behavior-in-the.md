---
# Core Classification
protocol: 0x Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17394
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf
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
finders_count: 4
finders:
  - Gustavo Grieco
  - Robert Tonic
  - Rajeev Gopalakrishna
  - Michael Colburn
---

## Vulnerability Title

Calls to setParams may set invalid values and produce unexpected behavior in the staking contracts

### Overview


This bug report is about access controls in the staking/contracts/src/staking_pools/MixinStakingPool.sol file. It has been classified as a medium difficulty bug. The bug occurs when certain parameters of the contract can be configured to invalid values, causing a variety of issues and breaking expected interactions between contracts. This is due to the lack of sanity/threshold/limit checks on all parameters when they are reparameterized using the _setParams function. 

The bug has two exploit scenarios. In the first, the owner of the staking contracts accidentally includes invalid values for cobbDouglasAlphaNumerator or cobbDouglasAlphaDenominator parameters when reparameterizing. This causes any contract depending on the cobbDouglas function to return invalid values or revert, breaking several important interactions between them. In the second, an investor makes estimations based on the current parameters to determine if it is economically viable to invest, but at the same time the owner of the staking contracts changes some parameters. This leads to the investor's decision resulting in an economic loss.

To fix the bug, short term, the _setParams function should have proper validation checks on all parameters. If the validation procedure is unclear or too complex to implement on-chain, document the potential issues that could produce invalid values. Long term, use Echidna and Manticore to locate missing parameter checks.

### Original Finding Content

## Type: Access Controls  
**Target:** staking/contracts/src/staking_pools/MixinStakingPool.sol  

### Difficulty: Medium  

## Description  
Certain parameters of the contracts can be configured to invalid values, causing a variety of issues and breaking expected interactions between contracts. 

`setParams` allows the owner of the staking contracts to reparameterize critical parameters. However, reparameterization lacks sanity/threshold/limit checks on all parameters. Once a parameter change is performed, the `_setParams` function will set up the new values as shown below.

```solidity
function _setParams (
    uint256 _epochDurationInSeconds,
    uint32 _rewardDelegatedStakeWeight,
    uint256 _minimumPoolStake,
    uint256 _maximumMakersInPool,
    uint32 _cobbDouglasAlphaNumerator,
    uint32 _cobbDouglasAlphaDenominator
) private {
    epochDurationInSeconds = _epochDurationInSeconds;
    rewardDelegatedStakeWeight = _rewardDelegatedStakeWeight;
    minimumPoolStake = _minimumPoolStake;
    maximumMakersInPool = _maximumMakersInPool;
    cobbDouglasAlphaNumerator = _cobbDouglasAlphaNumerator;
    cobbDouglasAlphaDenominator = _cobbDouglasAlphaDenominator;
    emit ParamsSet (
        _epochDurationInSeconds,
        _rewardDelegatedStakeWeight,
        _minimumPoolStake,
        _maximumMakersInPool,
        _cobbDouglasAlphaNumerator,
        _cobbDouglasAlphaDenominator
    );
}
```
*Figure 21.1: The `_setParams` function.*  

Critical staking parameters are reparameterized without any sanity/threshold/limit checks.  

## Exploit Scenario  
This issue has two exploit scenarios:  

- **Scenario 1:** Alice is the owner of the staking contracts and decides to update the parameters. However, she accidentally includes invalid values for `cobbDouglasAlphaNumerator` or `cobbDouglasAlphaDenominator` parameters. After the update, any contract depending on the `cobbDouglas` function will return invalid values or revert, breaking several important interactions between them.  

- **Scenario 2:** Alice wants to either start a new pool or join one. She makes estimations based on the current parameters to determine if it is economically viable to invest. At the same time, the owner of the staking contracts, Bob, is deciding to change some parameters. Alice decides to interact with the contracts at the same time that the parameters are changed. As a result, Alice’s decision could lead to an economic loss for her.  

## Recommendation  
Short term, add proper validation checks on all parameters in `setParams`. If the validation procedure is unclear or too complex to implement on-chain, document the potential issues that could produce invalid values.  

Long term, use Echidna and Manticore to locate missing parameter checks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | 0x Protocol |
| Report Date | N/A |
| Finders | Gustavo Grieco, Robert Tonic, Rajeev Gopalakrishna, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/0x-protocol.pdf

### Keywords for Search

`vulnerability`

