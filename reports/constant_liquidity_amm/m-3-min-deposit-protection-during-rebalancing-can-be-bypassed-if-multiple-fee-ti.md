---
# Core Classification
protocol: Arrakis
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20739
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/86
source_link: none
github_link: https://github.com/sherlock-audit/2023-06-arrakis-judging/issues/28

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
  - cergyk
---

## Vulnerability Title

M-3: Min deposit protection during rebalancing can be bypassed if multiple fee tiers

### Overview


This bug report is about an issue (M-3) found in the Arrakis vault code which implements a slippage protection during rebalancing. The issue is that when multiple feeTiers are used, the slippage protection does not protect against manipulation. This means that a malicious user (Alice) can front-run and back-run a rebalance operation by Bob (the operator) to make a profit at Bob's expense. This is possible because Bob's rebalance operation does not check the deposited amounts in aggregate when grouped by fee tiers. The impact of this issue is that Bob makes an unfortunate rebalance to the profit of a sandwich. The recommendation given is to check deposited amounts in aggregate but grouped by fee tiers.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-06-arrakis-judging/issues/28 

## Found by 
cergyk
## Summary
Arrakis vault implements a slippage protection during rebalancing, but it does not protect when multiple feeTiers are used.

## Vulnerability Detail
The slippage protection used here:
https://github.com/sherlock-audit/2023-06-arrakis/blob/main/v2-core/contracts/ArrakisV2.sol#L408-L409

can be used to check that liquidity is added around a given price (acts like a slippage protection), when used on one pool.

However when aggregated on multiple pools as it is done here (over same tokens but multiple fee tiers), it does not protect the user, as pools can be imbalanced in different directions, and funds can be provided in the same proportion but provide liquidity at a worse price,

Example:

Arrakis vault handles the price range 1200-2000 on WETH-USDC in fee tiers [0.3%, 0.5%], price of WETH sits at 1600.

Alice sees that Bob the operator tries to rebalance the pool and thus provides liquidity on both ranges

Alice front runs Bob transaction, driving the price of WETH-USDC on fee tier 0.3% to 1200, and on fee tier 0.5% to 2000.

Bob executes his operation, and provides bigger amounts of WETH and USDC to provide same liquidity (worse prices), and so the slippage checks out.

Alice back runs the operation and makes a nice profit.

Please note that in the setup using `SimpleManager`, price deviation is checked on every minting pool:
https://github.com/sherlock-audit/2023-06-arrakis/blob/main/v2-manager-templates/contracts/SimpleManager.sol#L189-L194

So the sandwiching is limited by the deviation parameter (1%). This issue still holds, since maybe Bob wanted to enforce a stricter deviation for his rebalance (0.5%) using this check, and fails to do so.

## Impact
Bob makes an unfortunate rebalance to the profit of a sandwich.

## Code Snippet

## Tool used

Manual Review

## Recommendation
Check deposited amounts in aggregate but grouped by fee tiers. 




## Discussion

**kassandraoftroy**

For me this issue is a valid medium and not a duplicate of #164 since it is about rebalance() not addLiquidity() (so does not have the proper checks to sniff out manipulation when adding liquidity on multiple fee tiers simultaneously).

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Arrakis |
| Report Date | N/A |
| Finders | cergyk |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-06-arrakis-judging/issues/28
- **Contest**: https://app.sherlock.xyz/audits/contests/86

### Keywords for Search

`vulnerability`

