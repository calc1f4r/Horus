---
# Core Classification
protocol: Frax Solidity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 17935
audit_firm: TrailOfBits
contest_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
source_link: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
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
  - Samuel Moelius Maximilian Krüger Troy Sargent
---

## Vulnerability Title

minVeFXSForMaxBoost can be manipulated to increase rewards

### Overview


This bug report is about an exploit scenario in FraxCrossChainFarmSushi.sol, a smart contract used to stake Uniswap V2 LP tokens. The exploit occurs when an attacker manipulates the spot price of the pool prior to staking LP tokens. This causes the reward boost to be skewed upward, resulting in the attacker earning outsized rewards relative to the amount of liquidity provided.

The exploit is enabled by the function minVeFXSForMaxBoost, which is calculated based on the current spot price when a user stakes Uniswap V2 LP tokens. The attacker sells a large amount of FRAX through the incentivized Uniswap V2 pool, increasing the amount of FRAX in the reserve. By calling stakeLocked and depositing LP tokens, the attacker's reward boost increases due to the large trade, giving the attacker outsized rewards. The attacker then swaps their tokens back through the pool to prevent losses.

To address this exploit, it is recommended to not use the Uniswap spot price to calculate reward boosts in the short term. In the long term, it is recommended to use canonical and audited rewards contracts for Uniswap V2 liquidity mining, such as MasterChef.

### Original Finding Content

## FraxCrossChainFarmSushi.sol Vulnerability Assessment

**Difficulty:** Medium

**Type:** Undefined Behavior

**Target:** FraxCrossChainFarmSushi.sol

## Description

`minVeFXSForMaxBoost` is calculated based on the current spot price when a user stakes Uniswap V2 LP tokens. If an attacker manipulates the spot price of the pool prior to staking LP tokens, the reward boost will be skewed upward, thereby increasing the amount of rewards earned. The attacker will earn outsized rewards relative to the amount of liquidity provided.

```solidity
function fraxPerLPToken() public view returns (uint256) {
    // Get the amount of FRAX 'inside' of the lp tokens
    uint256 frax_per_lp_token;
    // Uniswap V2
    // ============================================
    {
        [...]
        uint256 total_frax_reserves;
        (uint256 reserve0, uint256 reserve1,) = (stakingToken.getReserves());
    }
}
```
**Figure 22.1:** contracts/Staking/FraxCrossChainFarmSushi.sol#L242-L250

```solidity
function userStakedFrax(address account) public view returns (uint256) {
    return (fraxPerLPToken()).mul(_locked_liquidity[account]).div(1e18);
}
```

```solidity
function minVeFXSForMaxBoost(address account) public view returns (uint256) {
    return (userStakedFrax(account)).mul(vefxs_per_frax_for_max_boost).div(MULTIPLIER_PRECISION);
}
```

```solidity
function veFXSMultiplier(address account) public view returns (uint256) {
    if (address(veFXS) != address(0)) {
        // The claimer gets a boost depending on amount of veFXS they have relative
        // to the amount of FRAX 'inside' of their locked LP tokens
        uint256 veFXS_needed_for_max_boost = minVeFXSForMaxBoost(account);
        [...]
    }
}
```

**Figure 22.2:** contracts/Staking/FraxCrossChainFarmSushi.sol#L260-L272

## Exploit Scenario

An attacker sells a large amount of FRAX through the incentivized Uniswap V2 pool, increasing the amount of FRAX in the reserve. In the same transaction, the attacker calls `stakeLocked` and deposits LP tokens. The attacker's reward boost, `new_vefxs_multiplier`, increases due to the large trade, giving the attacker outsized rewards. The attacker then swaps his tokens back through the pool to prevent losses.

## Recommendations

- **Short term:** Do not use the Uniswap spot price to calculate reward boosts.
- **Long term:** Use canonical and audited rewards contracts for Uniswap V2 liquidity mining, such as MasterChef.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | TrailOfBits |
| Protocol | Frax Solidity |
| Report Date | N/A |
| Finders | Samuel Moelius Maximilian Krüger Troy Sargent |

### Source Links

- **Source**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/trailofbits/publications/blob/master/reviews/FraxQ42021.pdf

### Keywords for Search

`vulnerability`

