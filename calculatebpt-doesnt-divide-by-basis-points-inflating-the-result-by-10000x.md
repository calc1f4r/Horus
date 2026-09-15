---
# Core Classification
protocol: Alchemix
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38219
audit_firm: Immunefi
contest_link: https://immunefi.com/bounty/alchemix-boost/
source_link: none
github_link: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31478%20-%20%5bSC%20-%20High%5d%20calculateBPT%20doesnt%20divide%20by%20basis%20points%20infl....md

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - dexes
  - yield
  - cross_chain
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Holterhus
---

## Vulnerability Title

`calculateBPT()` doesn't divide by basis points, inflating the result by 10000x

### Overview


This bug report is about a problem in the code for a smart contract on the website https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/FluxToken.sol. The problem is that the `calculateBPT()` function in the code is not dividing by the correct amount, causing an inflation of the result by 10000 times. This means that users are receiving 10000 times more FLUX tokens than they should be, which can be used to boost bribe payments in an unfair way. A test has been provided to demonstrate the issue, and the code reference for the affected function is also included. This bug can potentially lead to theft of unclaimed royalties.

### Original Finding Content

Report type: Smart Contract


Target: https://github.com/alchemix-finance/alchemix-v2-dao/blob/main/src/FluxToken.sol

Impacts:
- Theft of unclaimed royalties

## Description
## Brief/Intro

The `calculateBPT()` function in `FluxToken.sol` (which is used when claiming FLUX for NFT holders) inflates the result by 10000x, as it doesn't divide by basis points.

## Vulnerability Details

`bptMultiplier` sets the ratio of FLUX that patron NFT holders receive. It is intended to set the value to `0.4%` by setting it to `40` and dividing by `BPS`.
```solidity
/// @notice The ratio of FLUX patron NFT holders receive (.4%)
uint256 public bptMultiplier = 40;
```
However, when BPT is calculated, we never divide by BPS:
```solidity
function calculateBPT(uint256 _amount) public view returns (uint256 bptOut) {
    bptOut = _amount * bptMultiplier;
}
```

## Impact Details

This function is used when calculating the amount of FLUX that is claimable for NFT holders. The result is that this value will be inflated by 10000x, so 10000x more FLUX will be claimed than should be. This excess FLUX can be used for boosting bribe payments in an unfair manner (since the user should not have as much boosting ability as they receive).

## References

`FluxToken.sol`


## Proof of Concept

The following test can be added to `FluxToken.t.sol`. It should return 0.4% of amount, which would equal `40`, but instead returns `400_000`.

```solidity
function test_InflatedBPT() external {
    uint256 amount = 10_000;
    uint256 bptCalculation = flux.calculateBPT(amount);
    assertEq(bptCalculation, 400_000);
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Immunefi |
| Protocol | Alchemix |
| Report Date | N/A |
| Finders | Holterhus |

### Source Links

- **Source**: N/A
- **GitHub**: https://raw.githubusercontent.com/immunefi-team/Bounty_Boosts/main/Alchemix/31478%20-%20%5bSC%20-%20High%5d%20calculateBPT%20doesnt%20divide%20by%20basis%20points%20infl....md
- **Contest**: https://immunefi.com/bounty/alchemix-boost/

### Keywords for Search

`vulnerability`

