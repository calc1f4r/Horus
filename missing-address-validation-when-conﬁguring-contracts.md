---
# Core Classification
protocol: Liquity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18024
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
github_link: none

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
finders_count: 4
finders:
  - Gustavo Grieco
  - Alexander Remie
  - Maximilian Krüger
  - Michael Colburn
---

## Vulnerability Title

Missing address validation when conﬁguring contracts

### Overview

See description below for full details.

### Original Finding Content

## Type: Timing
## Target: LUSDToken.sol, LQTYToken.sol

### Difficulty: Low

### Description
As part of the post-deployment setup of the Liquity system, several contracts have `setAddresses` functions that initialize links to other system components (Figure 7.1). These functions are each callable only once as the final step of each is to renounce ownership of the contract. However, none of these addresses are validated in any way before being set. If an incorrect address is set, then that contract must be redeployed, and due to the connections between most contracts, this is likely to result in the entire system having to be redeployed.

```solidity
function setAddresses (
    address _troveManagerAddress,
    address _activePoolAddress
)
external
onlyOwner
{
    troveManagerAddress = _troveManagerAddress;
    activePoolAddress = _activePoolAddress;
    emit TroveManagerAddressChanged(_troveManagerAddress);
    emit ActivePoolAddressChanged(_activePoolAddress);
    _renounceOwnership();
}
```

Figure 7.1: An example `setAddresses` function, from the DefaultPool contract.

This missing validation is present in configuration functions throughout the contracts. The affected functions are:
- All contracts with a `setAddresses` function
- `SortedTroves.setParams`

### Exploit Scenario
An error or typo in the deployment script causes the contract address of one of the system components to be recorded as `0x0` in each of the system's contracts. As a result, the entire system must be redeployed at significant gas cost.

### Recommendation
Short term, add some basic input validation to all configuration functions. For example, check for the `0x0` address as this is the default value for an uninitialized address. 

Long term, always perform some type of input validation. Use Slither to detect functions that would benefit from a `0x0` address check.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Liquity |
| Report Date | N/A |
| Finders | Gustavo Grieco, Alexander Remie, Maximilian Krüger, Michael Colburn |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Liquity.pdf

### Keywords for Search

`vulnerability`

