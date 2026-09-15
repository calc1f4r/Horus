---
# Core Classification
protocol: Sherlock Protocol V2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 16636
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/Sherlockv2.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/Sherlockv2.pdf
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
finders_count: 1
finders:
  - Alexander Remie Simone Monica
---

## Vulnerability Title

Certain functions lack zero address checks

### Overview


This bug report describes an issue with certain functions in contracts/managers/(AaveV2Strategy|SherlockProtocolManager|SherDistributionManager|Manager).sol and contracts/Sherlock.sol, where they do not validate incoming arguments, meaning that important state variables can be set to the zero address. This would cause calls to claimRewards to revert, preventing any Aave rewards from being claimed. The following functions are missing zero address checks: Manager.setSherlockCoreAddress, AaveV2Strategy.sweep, SherDistributionManager.sweep, SherlockProtocolManager.sweep, and Sherlock.constructor.

The exploit scenario in this report is that Bob deploys AaveV2Strategy with aaveLmReceiver set to the zero address, meaning that all calls to claimRewards will revert.

The report recommends that, in the short term, zero address checks should be added to all function arguments to ensure users cannot accidentally set incorrect values. In the long term, it is recommended to use Slither, which will catch functions that do not have zero address checks.

### Original Finding Content

## Vulnerability Report: Undefined Behavior

**Difficulty:** High  
**Type:** Undefined Behavior  

## Affected Contracts
- `contracts/managers/(AaveV2Strategy|SherlockProtocolManager|SherDistributionManager|Manager).sol`
- `contracts/Sherlock.sol`

## Description
Certain functions fail to validate incoming arguments, allowing callers to accidentally set important state variables to the zero address. 

For instance, the `AaveV2Strategy` contract’s constructor function does not validate the `aaveLmReceiver`, which is the address that receives Aave rewards on calls to `AaveV2Strategy.claimRewards`.

```solidity
constructor(IAToken _aWant, address _aaveLmReceiver) {
    aWant = _aWant;
    // This gets the underlying token associated with aUSDC (USDC)
    want = IERC20(_aWant.UNDERLYING_ASSET_ADDRESS());
    // Gets the specific rewards controller for this token type
    aaveIncentivesController = _aWant.getIncentivesController();
    aaveLmReceiver = _aaveLmReceiver;
}
```
*Figure 2.1: `managers/AaveV2Strategy.sol:39-47`*

If the `aaveLmReceiver` variable is set to the zero address, the Aave contract will revert with `INVALID_TO_ADDRESS`, preventing any Aave rewards from being claimed for the designated token.

### Missing Zero Address Checks
The following functions are missing zero address checks:
- `Manager.setSherlockCoreAddress`
- `AaveV2Strategy.sweep`
- `SherDistributionManager.sweep`
- `SherlockProtocolManager.sweep`
- `Sherlock.constructor`

## Exploit Scenario
Bob deploys `AaveV2Strategy` with `aaveLmReceiver` set to the zero address. All calls to `claimRewards` revert.

## Recommendations
- **Short term:** Add zero address checks on all function arguments to ensure that users cannot accidentally set incorrect values.
- **Long term:** Use Slither, which will identify functions that do not have zero address checks.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Sherlock Protocol V2 |
| Report Date | N/A |
| Finders | Alexander Remie Simone Monica |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/Sherlockv2.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/Sherlockv2.pdf

### Keywords for Search

`vulnerability`

