---
# Core Classification
protocol: Mellow Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1148
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-mellow-protocol-contest
source_link: https://code4rena.com/reports/2021-12-mellow
github_link: https://github.com/code-423n4/2021-12-mellow-findings/issues/46

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
  - services
  - yield_aggregator
  - cross_chain
  - options_vault

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - cmichel
---

## Vulnerability Title

[M-01] User deposits don’t have min. return checks

### Overview


This bug report describes a vulnerability in the `LPIssuer.deposit` function which can lead to users receiving a different amount of LP tokens than they expected. This can happen when a strategist frontruns the user’s deposit and rebalances the vault tokens, changing the tvl for each vault token. The user’s deposit amount is then calculated based on the new tvl, leading to them receiving a smaller LP amount than they expected. 

For example, if a user deposits an equal amount of two tokens A and B, expecting to get 50% of the supply, but the strategist rebalances the tokens to equal tvl, the user will only receive 33.3% of the total supply. 

The impact of this vulnerability is that users can get rekt when depositing, as the received LP amount is unpredictable and leads to a trade using a very different balanced token mix than they intended. 

To mitigate this vulnerability, it is recommended to add a minimum return amount check and accept a function parameter that can be chosen by the user indicating their expected LP amount for their deposit token amounts, then check that the actually minted LP token amount is above this parameter.

### Original Finding Content

## Handle

cmichel


## Vulnerability details

The `LPIssuer.deposit` first computes _balanced amounts_ on the user's defined `tokenAmounts`.
The idea is that LP tokens give the same percentage share of each vault tokens' tvl, therefore the provided amounts should be _balanced_, meaning, the `depositAmount / tvl` ratio should be equal for all vault tokens.

But the strategist can frontrun the user's deposit and rebalance the vault tokens, changing the tvl for each vault token which changes the rebalance.
This frontrun can happen accidentally whenever the strategist rebalances

## POC
There's a vault with two tokens A and B, tvls are `[500, 1500]`

- The user provides `[500, 1500]`, expecting to get 50% of the share supply (is minted 100% of old total supply).
- The strategist rebalances to `[1000, 1000]`
- The user's balanceFactor is `min(500/1000, 1500/1000) = 1/2`, their balancedAmounts are thus `tvl * balanceFactor = [500, 500]`, the `1000` excess token B are refunded. In the end, they only received `500/(1000+500) = 33.3%` of the total supply but used up all of their token A which they might have wanted to hold on to if they had known they'd only get 33.3% of the supply.

## Impact
Users can get rekt when depositing as the received LP amount is unpredictable and lead to a trade using a very different balanced token mix that they never intended.

## Recommended Mitigation Steps
Add minimum return amount checks.
Accept a function parameter that can be chosen by the user indicating their _expected LP amount_ for their deposit `tokenAmounts`, then check that the actually minted LP token amount is above this parameter.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Mellow Protocol |
| Report Date | N/A |
| Finders | cmichel |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-mellow
- **GitHub**: https://github.com/code-423n4/2021-12-mellow-findings/issues/46
- **Contest**: https://code4rena.com/contests/2021-12-mellow-protocol-contest

### Keywords for Search

`vulnerability`

