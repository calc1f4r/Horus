---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 495
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-spartan-protocol-contest
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/38

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
  - dexes
  - cdp
  - services
  - yield_aggregator
  - rwa

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - jonah1005
---

## Vulnerability Title

[H-10] Hijack token pool by burning liquidity token

### Overview


This bug report is about a vulnerability in Pool that allows users to burn liquidity tokens without withdrawing them. This allows the hacker to mutate the pool's rate to a point that no one can get any liquidity token anymore, even if they deposit tokens. The liquidity tokens are calculated using a formula which uses the variable `P`, which stands for `totalSupply` of the current Pool. If `P` is too small (e.g, 1) then all the units would be rounding to 0. Hackers can create a Pool and burn their liquidity and set `totalSupply` to 1, making them the only person who owns the Pool's liquidity. The bug report includes a proof of concept which shows that if a user deposits 1M tokens to a pool where `totalSupply` equals 1, the user will not receive any liquidity tokens. The recommended mitigation step is to remove the `burn` function or restrict it to privileged users only.

### Original Finding Content

_Submitted by jonah1005_

`Pool` allows users to burn lp tokens without withdrawing the tokens. This allows the hacker to mutate the pools' rate to a point that no one can get any lp token anymore (even if depositing token).

The liquidity tokens are calculated at `Utils:calcLiquidityUnits`
```solidity
// units = ((P (t B + T b))/(2 T B)) * slipAdjustment
// P * (part1 + part2) / (part3) * slipAdjustment
uint slipAdjustment = getSlipAdustment(b, B, t, T);
uint part1 = t*(B);
uint part2 = T*(b);
uint part3 = T*(B)*(2);
uint _units = (P * (part1 + (part2))) / (part3);
return _units * slipAdjustment / one;  // Divide by 10**18
```
where `P` stands for `totalSupply` of current Pool. If `P` is too small (e.g, 1) then all the units would be rounding to 0.

Since any person can create a `Pool` at `PoolFactory`, hackers can create a Pool and burn his lp and set `totalSupply` to 1. He will be the only person who owns the Pool's lp from now on. [Pool's burn logic](https://github.com/code-423n4/2021-07-spartan/blob/e2555aab44d9760fdd640df9095b7235b70f035e/contracts/Pool.sol#L146) and [Utils' lp token formula](https://github.com/code-423n4/2021-07-spartan/blob/e2555aab44d9760fdd640df9095b7235b70f035e/contracts/Utils.sol#L80).

Here's a script of a user depositing 1M token to a pool where `totalSupply` equals 1

```solidity
dai_pool.functions.burn(init_amount-1).transact()
print('total supply', dai_pool.functions.totalSupply().call())
dai.functions.transfer(dai_pool.address, 1000000 * 10**18).transact()
dai_pool.functions.addForMember(user).transact()
print('lp received from depositing 1M dai: ', dai_pool.functions.balanceOf(user).call())
```

Output:
```solidity
total supply 1
lp received from depositing 1M dai:  0
```

Recommend removing `burn` or restrict it to privileged users only.

**[verifyfirst (Spartan) confirmed](https://github.com/code-423n4/2021-07-spartan-findings/issues/38#issuecomment-883855367):**
 > We agree to this issue and will restrict access to burn in the pool contract.
> We have already proposed adding a 1 week withdraw coolOff for all users per pool from the genesis of creation. Users can only add liquidity within this period.



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | jonah1005 |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/38
- **Contest**: https://code4rena.com/contests/2021-07-spartan-protocol-contest

### Keywords for Search

`vulnerability`

