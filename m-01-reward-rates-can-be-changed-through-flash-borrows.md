---
# Core Classification
protocol: Based Loans
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3993
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-04-based-loans-contest
source_link: https://code4rena.com/reports/2021-04-basedloans
github_link: https://github.com/code-423n4/2021-04-basedloans-findings/issues/33

# Impact Classification
severity: medium
impact: security_vulnerability
exploitability: 1.00
financial_impact: medium

# Scoring
quality_score: 5
rarity_score: 0

# Context Tags
tags:

protocol_categories:
  - liquid_staking
  - bridge
  - services
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-01] Reward rates can be changed through flash borrows

### Overview


This bug report concerns a vulnerability in the rewards per market system of a platform. The vulnerability allows a large holder to manipulate the rewards by depositing lots of collateral, taking out a huge borrow in the market, updating the rewards, and then unwinding the position. The vulnerability is exploited by miners who can run flash-loan-like attacks by first sending a borrow tx, then the refreshCompSpeeds transaction, and then the repay of the borrow. The attacker is then able to receive increased rewards which are stolen from other users. The recommended mitigation steps for this vulnerability are to make the function admin-only or to use a time-weighted total borrow system similar to Uniswap's price oracles.

### Original Finding Content


The rewards per market are proportional to their `totalBorrows` which can be changed by a large holder who deposits lots of collateral, takes out a huge borrow in the market, updates the rewards, and then unwinds the position.
They'll only pay gas fees as the borrow / repay can happen in the same block.

The `Comptroller.refreshCompSpeeds` function only checks that the single transaction is called from an EOA, but miners (or anyone if a miner offers services like flash bundles for flashbots) can still run flash-loan-like attacks by first sending a borrow tx increasing the totalBorrows, then the `refreshCompSpeeds` transaction, and then the repay of the borrow, as miners have full control over the transaction order of the block.

The new rate will then persist until the next call to `refreshCompSpeeds`.

Attackers have an incentive to drive up the rewards in markets they are a large supplier/borrower in.

The increased rewards that the attacker receives are essentially stolen from other legitimate users.

Recommend making it an admin-only function or use a time-weighted total borrow system similar to Uniswap's price oracles.

**[ghoul-sol (Based Loans) confirmed](https://github.com/code-423n4/2021-04-basedloans-findings/issues/33#issuecomment-835539656):**

> Restricting `Comptroller.refreshCompSpeeds` function to admin only would centralize an ability to update speeds. A better solution may be a bot that keeps track of markets utilizations and updates speeds when needed. That will also give a way to community to participate.
>
> Also, higher rewards would mean that all participants are getting them and that would bring even more liquidity to the given market and decrease attackers earnings. Attacker could keep moving the liquidity from market to market but everyone would follow quite quickly. If that actually happens, admin has a way to stop the rewards and make `refreshCompSpeeds` admin-only function as last resolution because comptroller is using proxy pattern.

<br /><br />



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 5/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Based Loans |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2021-04-basedloans
- **GitHub**: https://github.com/code-423n4/2021-04-basedloans-findings/issues/33
- **Contest**: https://code4rena.com/contests/2021-04-based-loans-contest

### Keywords for Search

`vulnerability`

