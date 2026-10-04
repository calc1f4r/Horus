---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: economic
vulnerability_type: lending_pool

# Attack Vector Details
attack_type: lending_pool
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1239
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-12-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-12-vader
github_link: https://github.com/code-423n4/2021-12-vader-findings/issues/55

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.80
financial_impact: high

# Scoring
quality_score: 4
rarity_score: 3

# Context Tags
tags:
  - lending_pool
  - flash_loan

protocol_categories:
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - TomFrenchBlockchain
  - hyh
---

## Vulnerability Title

[H-06] LPs of VaderPoolV2 can manipulate pool reserves to extract funds from the reserve.

### Overview


This bug report is about a vulnerability in the VaderPoolV2 code that can be exploited to drain the reserve. The vulnerability allows an LP to manipulate the pool's reserves to artificially engineer a huge amount of impermanent loss, which can then be refunded from the reserve in VADER tokens. This is done by flashloaning a huge amount of one of the pool's assets, trading against the pool to unbalance it, removing the liquidity and receiving compensation from the reserve for the IL, re-adding the liquidity, and then trading against the pool to bring it back into balance. After a year any large LP is incentivised and able to perform this attack and drain reserve funds. To mitigate this issue, it is recommended to use a manipulation resistant oracle for the relative prices of the pool's assets.

### Original Finding Content

## Handle

TomFrenchBlockchain


## Vulnerability details

(Resubmission as the form crashed apologies if this is a duplicate)

## Impact
Impermanent loss protection can be exploited to drain the reserve.

## Proof of Concept
In `VaderPoolV2.burn` we calculate the current losses that the LP has made to impermanent loss.

https://github.com/code-423n4/2021-12-vader/blob/fd2787013608438beae361ce1bb6d9ffba466c45/contracts/dex-v2/pool/VaderPoolV2.sol#L265-L296

These losses are then refunded to the LP in VADER tokens from the reserve.

https://github.com/code-423n4/2021-12-vader/blob/fd2787013608438beae361ce1bb6d9ffba466c45/contracts/dex-v2/router/VaderRouterV2.sol#L220

This loss is calculated by the current reserves of the pool so if an LP can manipulate the pool's reserves they can artificially engineer a huge amount of IL in order to qualify for a payout up to the size of their LP position.

https://github.com/code-423n4/2021-12-vader/blob/fd2787013608438beae361ce1bb6d9ffba466c45/contracts/dex/math/VaderMath.sol#L72-L92

The attack is then as follows.
1. Be an LP for a reasonable period of time (IL protection scales linearly up to 100% after a year)
2. Flashloan a huge amount of one of the pool's assets.
3. Trade against the pool with the flashloaned funds to unbalance it such that your LP position has huge IL.
4. Remove your liquidity and receive compensation from the reserve for the IL you have engineered.
5. Re-add your liquidity back to the pool.
6. Trade against the pool to bring it back into balance.

The attacker now holds the majority of their flashloaned funds (minus slippage/swap fees) along with a large fraction of the value of their LP position in VADER paid out from the reserve. The value of their LP position is unchanged. Given a large enough LP position, the IL protection funds extracted from the reserve will exceed the funds lost to swap fees and the attacker will be able to repay their flashloan with a profit.

This is a high risk issue as after a year any large LP is incentivised and able to perform this attack and drain reserve funds.

## Recommended Mitigation Steps

Use a manipulation resistant oracle for the relative prices of the pool's assets (TWAP, etc.)

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 4/5 |
| Rarity Score | 3/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | TomFrenchBlockchain, hyh |

### Source Links

- **Source**: https://code4rena.com/reports/2021-12-vader
- **GitHub**: https://github.com/code-423n4/2021-12-vader-findings/issues/55
- **Contest**: https://code4rena.com/contests/2021-12-vader-protocol-contest

### Keywords for Search

`Lending Pool, Flash Loan`

