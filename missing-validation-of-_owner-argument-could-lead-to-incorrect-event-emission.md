---
# Core Classification
protocol: Uniswap V3 Core
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16842
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/UniswapV3Core.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/UniswapV3Core.pdf
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
finders_count: 3
finders:
  - Dominik Teiml
  - Alexander Remie
  - Josselin Feist
---

## Vulnerability Title

Missing validation of _owner argument could lead to incorrect event emission

### Overview

See description below for full details.

### Original Finding Content

## Timing: UniswapV3Pool.sol

## Difficulty: Medium

### Description
Because the `setOwner` lacks input validation, the owner can be updated to the existing owner. Although such an update wouldn’t change the contract state, it would emit an event falsely indicating the owner had been changed.

```solidity
function setOwner(address _owner) external override {
    require(msg.sender == owner, 'OO');
    emit OwnerChanged(owner, _owner);
    owner = _owner;
}
```
*Figure 2.1: setOwner in UniswapV3Factory.sol*

### Exploit Scenario
Alice has set up monitoring of the `OwnerChanged` event to track transfers of the owner role. Bob, the current owner, calls `setOwner` to update the owner to his address (not actually making a change). Alice is notified that the owner was changed but upon closer inspection discovers it was not.

### Recommendation
- **Short term:** Add a check ensuring that the `_owner` argument does not equal the existing owner.
- **Long term:** Carefully inspect the code to ensure that configuration functions do not allow a value to be updated as the existing value. Such updates are not inherently problematic but could cause confusion among users monitoring the events.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Uniswap V3 Core |
| Report Date | N/A |
| Finders | Dominik Teiml, Alexander Remie, Josselin Feist |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/UniswapV3Core.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/UniswapV3Core.pdf

### Keywords for Search

`vulnerability`

