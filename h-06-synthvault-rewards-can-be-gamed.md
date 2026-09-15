---
# Core Classification
protocol: Spartan Protocol
chain: everychain
category: uncategorized
vulnerability_type: twap

# Attack Vector Details
attack_type: twap
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 491
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-07-spartan-protocol-contest
source_link: https://code4rena.com/reports/2021-07-spartan
github_link: https://github.com/code-423n4/2021-07-spartan-findings/issues/166

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 3.5

# Context Tags
tags:
  - twap

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
  - cmichel
---

## Vulnerability Title

[H-06] SynthVault rewards can be gamed

### Overview


This bug report is about an exploit in the `SynthVault._deposit` function of a system. The exploit allows a user to manipulate the spot price of a pool to inflate their weight, which would allow them to claim a large share of rewards. The cost of the attack depends on the pool's liquidity and the profit depends on the reserve. It could be profitable under certain circumstances and the recommended mitigation steps are to track a TWAP price of the synth, store the deposited synths, and compute the weight and total weight on the fly based on the TWAP and deposit amount.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

## Vulnerability Details

The `SynthVault._deposit` function adds `weight` for the user that depends on the spot value of the deposit synth amount in `BASE`.
This spot price can be manipulated and the cost of manipulation is relative to the pool's liquidity.
However, the reward (see `calcReward`) is measured in BASE tokens unrelated to the pool.
Therefore, if the pool's liquidity is low and the reward reserve is high, the attack can be profitable:

1. Manipulate the pool spot price of the `iSYNTH(_synth).LayerONE()` pool by dripping a lot of `BASE` into it repeatedly (sending lots of smaller trades is less costly due to the [path-independence of the continuous liquidity model](https://docs.thorchain.org/thorchain-finance/continuous-liquidity-pools)). This increases the `BASE` per `token` price.
2. Call `SynthVault.depositForMember` and deposit a _small_ amount of synth token. The `iUTILS(_DAO().UTILS()).calcSpotValueInBase(iSYNTH(_synth).LayerONE(), _amount)` will return an inflated weight due to the price.
3. Optionally drip more `BASE` into the pool and repeat the deposits
4. Drip back `token` to the pool to rebalance it

The user's `weight` is now inflated compared to the deposited / locked-up amount and they can claim a large share of the rewards.

## Impact
The cost of the attack depends on the pool's liquidity and the profit depends on the reserve.
It could therefore be profitable under certain circumstances.

## Recommended Mitigation Steps
Track a TWAP price of the synth instead, store the deposited synths instead, and compute the weight & total weight on the fly based on the TWAP * deposit amount instead of at the time of deposit.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 3.5/5 |
| Audit Firm | Code4rena |
| Protocol | Spartan Protocol |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-07-spartan
- **GitHub**: https://github.com/code-423n4/2021-07-spartan-findings/issues/166
- **Contest**: https://code4rena.com/contests/2021-07-spartan-protocol-contest

### Keywords for Search

`TWAP`

