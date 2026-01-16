---
# Core Classification
protocol: Core Contracts
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57211
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj
source_link: none
github_link: https://github.com/Cyfrin/2025-02-raac

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
  - amarfares
  - 0x23r0
  - kalii
---

## Vulnerability Title

`veRAACToken::_updateBoostState` function sets individual user voting power instead of system-wide totals

### Overview


The `_updateBoostState` function in the veRAACToken contract is incorrectly setting an individual user's voting power as the global state variable. This can lead to incorrect boost calculations, potentially affecting reward distributions and governance voting power. The issue can be fixed by using a system-wide metric instead of an individual user's voting power in the function.

### Original Finding Content

## Summary

the `_updateBoostState` function incorrectly assigns an individual user’s voting power to a global state variable, leading to erroneous boost calculations. This misassignment affects the denominator in boost computations, potentially skewing reward distributions and undermining the integrity of governance voting power.

## Vulnerability Details

In the [`_updateBoostState`](https://github.com/Cyfrin/2025-02-raac/blob/main/contracts/core/tokens/veRAACToken.sol#L568C1-L575C6) function, the contract updates several state variables related to boost calculations. While the overall intention appears to be tracking system-wide metrics for boost computations

```solidity
    function _updateBoostState(address user, uint256 newAmount) internal {
        // Update boost calculator state
        _boostState.votingPower = _votingState.calculatePowerAtTimestamp(user, block.timestamp);
        _boostState.totalVotingPower = totalSupply();
        _boostState.totalWeight = _lockState.totalLocked;
        
        _boostState.updateBoostPeriod();
    }

```

Here, the contract fetches the voting power of the specific user calling the function rather than aggregating the voting power of all users. As a result, `_boostState.votingPower` reflects only the individual’s power rather than the system-wide total. In contrast, `_boostState.totalVotingPower` is correctly set using `totalSupply()`, which implies a global perspective. This discrepancy means that subsequent boost calculations that rely on `_boostState.votingPower` are using an incorrect denominator, leading to miscalculation of boost multipliers.

## Impact

The boost multiplier, which is crucial for determining rewards, will be computed based on an incorrect denominator. This can lead to either inflated or deflated boost values.

## Tools Used

Manual Review

## Recommendations

Remove or refactor the line that sets `_boostState.votingPower` using the individual user's voting power. Instead, use a system-wide metric—such as the total supply of veRAAC tokens or an aggregate calculation of all users' voting power—to ensure that boost calculations are based on the correct global denominator.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Core Contracts |
| Report Date | N/A |
| Finders | amarfares, 0x23r0, kalii |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-02-raac
- **Contest**: https://codehawks.cyfrin.io/c/cm5vbyum90000ffs0xblmb4gj

### Keywords for Search

`vulnerability`

