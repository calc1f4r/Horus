---
# Core Classification
protocol: Velocimeter
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36754
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/442
source_link: none
github_link: https://github.com/sherlock-audit/2024-06-velocimeter-judging/issues/168

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
finders_count: 7
finders:
  - eeyore
  - Audinarey
  - Ch\_301
  - Sentryx
  - mike-watson
---

## Vulnerability Title

M-3: `update_period(..)` leads to wrong calculation in weekly emissions breaking accounting for the protocol

### Overview


This bug report talks about a problem with the `update_period(..)` function that calculates the weekly emissions and `_teamEmissions` of FLOW. The calculation for `_teamEmissions` is overestimated, leading to incorrect results. This can cause issues with accounting for the protocol and third-party protocols that use the `circulating_supply()` function. The bug can be fixed by modifying the `update_period()` function.

### Original Finding Content

Source: https://github.com/sherlock-audit/2024-06-velocimeter-judging/issues/168 

## Found by 
Audinarey, Ch\_301, Ruhum, Sentryx, bbl4de, eeyore, mike-watson
## Summary

The `update_period(..)` function does the calculation and distribution of voter weekly and  `_teamEmissions` of FLOW. However, the `_teamEmissions` calculations is over estimated making the calculation wrong and more

## Vulnerability Detail

The `_teamEmissions` is calculated on top of normal weekly emissions in the `update_period()` function on L119

```solidity
File: Minter.sol
112:     function update_period() external returns (uint) { // @audit 
113:         uint _period = active_period;
114:         if (block.timestamp >= _period + WEEK && initializer == address(0)) { // only trigger if new week
115:             _period = (block.timestamp / WEEK) * WEEK;
116:             active_period = _period;
117:             uint256 weekly = weekly_emission(); // could be just 2k if voter has notified reward
118:             
119:  ->         uint _teamEmissions = (teamRate * weekly) /
120:  ->             (PRECISION - teamRate);
121:             uint _required =  weekly + _teamEmissions;
122:             uint _balanceOf = _flow.balanceOf(address(this));
123:             if (_balanceOf < _required) {
124:  ->             _flow.mint(address(this), _required - _balanceOf);
```

Ideally , the evaluation should work as follows 

- `weeklyPerGauge` = 2000e18, `teamRate` = 5% and `numberOfGauges` = 0
- it is expected that 100e18 be minted and transferred to the `teamEmissions` address and 2000e18 be  transferred to the `Voter` as rewards
- bringing the total distributed (both team and voter) to 2100e18 for that epoch.

However as shown below, the `teamEmissions` calculation breaks this accounting

```solidity
// uint _teamEmissions = = (teamRate * weekly) / (PRECISION - teamRate);
_teamEmissions = (50 * 2000e18) / (1000 - 50)
_teamEmissions = 105e18
```

Notice Now that 

- the evaluation of `_teamEmissions` is 105e18 bringing the total to 2105e18 emmited for that epoch
- also the actual value now recieved by  is `_teamEmissions` is 5.25% of the `weekly` emmisions instead of 5%

This descrepancy becomes larger as the `numberOfGauges` increases.

This can also lead to inflated values of `Minter.circulating_supply()` because the total supply of flow is increased contrary to the expected rate owing to each mint action (L124) that may occur due to excess `_teamEmissions` of FLOW calculated when `update_period` is called. This could break accounting also for protocol who integrate with VELOCIMETER and use the `circulating_supply()` function for core accounting

```solidity
File: Minter.sol
93:     function circulating_supply() public view returns (uint)
94:         return _flow.totalSupply() - _ve.totalSupply();
95:     }

```

## Impact

More FLOW is minted to team due to wrong calculation breaking accounting for the protocol and possible third party protocols who integrate with the protocol

## Code Snippet
https://github.com/sherlock-audit/2024-06-velocimeter/blob/main/v4-contracts/contracts/Minter.sol#L112-L120

## Tool used

Manual Review

## Recommendation

Modify the `Minter::update_period()` function as shown below

```diff
File: Minter.sol
112:     function update_period() external returns (uint) { // @audit
113:         uint _period = active_period;
114:         if (block.timestamp >= _period + WEEK && initializer == address(0)) { // only trigger if new week
115:             _period = (block.timestamp / WEEK) * WEEK;
116:             active_period = _period;
117:             uint256 weekly = weekly_emission(); // could be just 2k if voter has notified reward
118:
-119:             uint _teamEmissions = (teamRate * weekly) /
-120:               (PRECISION - teamRate);
+119:             uint _teamEmissions = (teamRate * weekly) /
+120:               (PRECISION);
121:             uint _required =  weekly + _teamEmissions;
122:             uint _balanceOf = _flow.balanceOf(address(this));
123:             if (_balanceOf < _required) {
124:                 _flow.mint(address(this), _required - _balanceOf);

```



## Discussion

**sherlock-admin2**

The protocol team fixed this issue in the following PRs/commits:
https://github.com/Velocimeter/v4-contracts/pull/16

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Velocimeter |
| Report Date | N/A |
| Finders | eeyore, Audinarey, Ch\_301, Sentryx, mike-watson, bbl4de, Ruhum |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2024-06-velocimeter-judging/issues/168
- **Contest**: https://app.sherlock.xyz/audits/contests/442

### Keywords for Search

`vulnerability`

