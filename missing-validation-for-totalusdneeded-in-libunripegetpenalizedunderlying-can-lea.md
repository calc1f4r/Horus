---
# Core Classification
protocol: Beanstalk Part 3
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33294
audit_firm: Codehawks
contest_link: https://www.codehawks.com/contests/clvo5kwin00078k6jhhjobn22
source_link: none
github_link: https://github.com/Cyfrin/2024-05-Beanstalk-Part-3

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - KiteWeb3
---

## Vulnerability Title

Missing validation for ```totalUsdNeeded``` in ```LibUnripe::getPenalizedUnderlying``` can lead to the ```urBean``` chopping block 

### Overview

See description below for full details.

### Original Finding Content

### Relevant GitHub Links
<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2024-05-Beanstalk-3/blob/662d26f12ee219ee92dc485c06e01a4cb5ee8dfb/protocol/contracts/libraries/LibUnripe.sol#L167">https://github.com/Cyfrin/2024-05-Beanstalk-3/blob/662d26f12ee219ee92dc485c06e01a4cb5ee8dfb/protocol/contracts/libraries/LibUnripe.sol#L167</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2024-05-Beanstalk-3/blob/662d26f12ee219ee92dc485c06e01a4cb5ee8dfb/protocol/contracts/beanstalk/barn/UnripeFacet.sol#L89-L93">https://github.com/Cyfrin/2024-05-Beanstalk-3/blob/662d26f12ee219ee92dc485c06e01a4cb5ee8dfb/protocol/contracts/beanstalk/barn/UnripeFacet.sol#L89-L93</a>

<a data-meta="codehawks-github-link" href="https://github.com/Cyfrin/2024-05-Beanstalk-3/blob/662d26f12ee219ee92dc485c06e01a4cb5ee8dfb/protocol/contracts/libraries/LibChop.sol#L33">https://github.com/Cyfrin/2024-05-Beanstalk-3/blob/662d26f12ee219ee92dc485c06e01a4cb5ee8dfb/protocol/contracts/libraries/LibChop.sol#L33</a>


## Summary
The ```LibUnripe::getPenalizedUnderlying()``` calculates the penalized amount of Ripe Tokens corresponding to the amount of Unripe Tokens that are chopped, according to the current chop rate into the protocol. When the Beanstalk is fully recapitalized, the ```totalUsdNeeded``` variable becomes ```0```. In the possible scenario where all ```urLP``` is chopped before ```urBeans```, the division by zero error causes the transaction to revert preventing users from chopping ```urBean``` into Ripe Bean.

## Vulnerability Details
```solidity
    function getPenalizedUnderlying(
        address unripeToken,
        uint256 amount,
        uint256 supply
    ) internal view returns (uint256 redeem) {
        require(isUnripe(unripeToken), "not vesting");
        AppStorage storage s = LibAppStorage.diamondStorage();
     
	    uint256 totalUsdNeeded = unripeToken == C.UNRIPE_LP ? LibFertilizer.getTotalRecapDollarsNeeded(supply) 
            : LibFertilizer.getTotalRecapDollarsNeeded();
       
        uint256 underlyingAmount = s.u[unripeToken].balanceOfUnderlying;
@>        redeem = underlyingAmount.mul(s.recapitalized).div(totalUsdNeeded).mul(amount).div(supply);
       
        if(redeem > underlyingAmount) redeem = underlyingAmount;
    }
```

## Impact
When the Beanstalk is fully recapitalized the ```urToken``` holders should be able to redeem the ripe underlying assets at a 1:1 rate. This can't happen in the scenario where all ```urLP``` is chopped before ```urBeans```. 

Considering the scenario where the recapitalization is completed and all ```urLP``` is chopped before ```urBeans```:  the ```totalUsdNeeded``` variable is 0  (the ```LibFertilizer.getTotalRecapDollarsNeeded()``` return 0 because ```C.unripeLP().totalSupply()``` is 0). 
The ```LibUnripe::getPenalizedUnderlying()```will perform a divion by zero error causing the transaction to revert preventing users from chopping ```urBean``` into Ripe Bean. The  ```urBean``` chop into Ripe Bean can't happen and the funds are stuck.

Impact: high because funds are directly at risk.

Likelihood: low because all ```urLP``` should be chopped before ```urBeans```. 

## Tools Used
Manual review

## Recommendations
To handle this scenario, appropriate checks should be added to ensure that in the case of full recapitalization the users can redeem at the new chop rate also in the case where all ```urLP``` is chopped before ```urBeans```.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beanstalk Part 3 |
| Report Date | N/A |
| Finders | KiteWeb3 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-05-Beanstalk-Part-3
- **Contest**: https://www.codehawks.com/contests/clvo5kwin00078k6jhhjobn22

### Keywords for Search

`vulnerability`

