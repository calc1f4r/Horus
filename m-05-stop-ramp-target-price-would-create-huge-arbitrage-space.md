---
# Core Classification
protocol: Boot Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 973
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-boot-finance-contest
source_link: https://code4rena.com/reports/2021-11-bootfinance
github_link: https://github.com/code-423n4/2021-11-bootfinance-findings/issues/208

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
  - privacy

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - jonah1005
---

## Vulnerability Title

[M-05] Stop ramp target price would create huge arbitrage space.

### Overview


This bug report is about a vulnerability in the Stop Ramp Target Price which could potentially create a huge arbitrage space. This would allow an attacker to set up a bot once a proposal to stop the Ramp Target Price has passed. The bug report includes a proof of concept, which shows how the precision multiplier is set and how an attacker can use it to gain profits. The recommended mitigation steps include ramping the token precision multipliers as the aPrecise is ramped. This would slow down the arbitrage space and distribute the profits evenly to lpers.

### Original Finding Content

## Handle

jonah1005


## Vulnerability details

## Stop ramp target price would create huge arbitrage space.
## Impact
`stopRampTargetPrice` would set the `tokenPrecisionMultipliers` to `originalPrecisionMultipliers[0].mul(currentTargetPrice).div(WEI_UNIT);`
Once the `tokenPrecisionMultipliers` is changed, the price in the AMM pool would change. Arbitrager can sandwich `stopRampTargetPrice` to gain profit.

Assume the decision is made in the DAO, an attacker can set up the bot once the proposal to `stopRampTargetPrice` has passed. I consider this is a medium-risk issue.

## Proof of Concept
The `precisionMultiplier` is set here:
[Swap.sol#L661-L666](https://github.com/code-423n4/2021-11-bootfinance/blob/main/customswap/contracts/Swap.sol#L661-L666)

We can set up a mockSwap with extra `setPrecisionMultiplier` to check the issue.
```solidity
    function setPrecisionMultiplier(uint256 multipliers) external {
        swapStorage.tokenPrecisionMultipliers[0] = multipliers; 
    }
```

```python
print(swap.functions.getVirtualPrice().call())
swap.functions.setPrecisionMultiplier(2).transact()
print(swap.functions.getVirtualPrice().call())

## output log:
## 1000000000000000000
## 1499889859738721606
```
## Tools Used
None
## Recommended Mitigation Steps
Dealing with the target price with multiplier precision seems clever as we can reuse most of the existing code. However, the precision multiplier should be an immutable parameter. Changing it after the pool is setup would create multiple issues. This function could be implemented in a safer way IMHO.

A quick fix I would come up with is to ramp the `tokenPrecisionMultipliers` as the `aPrecise` is ramped. As the `tokenPrecision` is slowly increased/decreased, the arbitrage space would be slower and the profit would (probably) distribute evenly to lpers.

Please refer to `_getAPreceise`'s implementation
[SwapUtils.sol#L227-L250](https://github.com/code-423n4/2021-11-bootfinance/blob/main/customswap/contracts/SwapUtils.sol#L227-L250)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Boot Finance |
| Report Date | N/A |
| Finders | jonah1005 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-bootfinance
- **GitHub**: https://github.com/code-423n4/2021-11-bootfinance-findings/issues/208
- **Contest**: https://code4rena.com/contests/2021-11-boot-finance-contest

### Keywords for Search

`vulnerability`

