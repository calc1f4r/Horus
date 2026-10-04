---
# Core Classification
protocol: Vader Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 5245
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2021-11-vader-protocol-contest
source_link: https://code4rena.com/reports/2021-11-vader
github_link: https://github.com/code-423n4/2021-11-vader-findings/issues/31

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
  - oracle
  - liquid_staking
  - bridge
  - cdp
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - WatchPug
  - TomFrenchBlockchain
---

## Vulnerability Title

[H-05] LPs of VaderPoolV2 can manipulate pool reserves to extract funds from the reserve.

### Overview


This bug report details a vulnerability in the "VaderPoolV2.burn" code, which allows an LP (liquidity provider) to exploit the impermanent loss protection feature to drain the reserve. By manipulating the pool's reserves, an LP can artificially create a huge amount of impermanent loss and receive compensation from the reserve for it. The attack involves the LP being an LP for a reasonable period of time, flashloaning a huge amount of one of the pool's assets, trading against the pool to unbalance it, removing their liquidity, receiving compensation from the reserve, and then re-adding their liquidity back to the pool. After a year, any large LP is incentivised and able to perform this attack. To mitigate this issue, a manipulation-resistant oracle should be used for the relative prices of the pool's assets.

### Original Finding Content

_Submitted by TomFrenchBlockchain, also found by WatchPug_

#### Impact

Impermanent loss protection can be exploited to drain the reserve.

#### Proof of Concept

In `VaderPoolV2.burn` we calculate the current losses that the LP has made to impermanent loss.

<https://github.com/code-423n4/2021-11-vader/blob/3a43059e33d549f03b021d6b417b7eeba66cf62e/contracts/dex-v2/pool/VaderPoolV2.sol#L237-L269>

These losses are then refunded to the LP in VADER tokens from the reserve

<https://github.com/code-423n4/2021-11-vader/blob/3a43059e33d549f03b021d6b417b7eeba66cf62e/contracts/dex-v2/router/VaderRouterV2.sol#L208-L227>

This loss is calculated by the current reserves of the pool so if an LP can manipulate the pool's reserves they can artificially engineer a huge amount of IL in order to qualify for a payout up to the size of their LP position.

<https://github.com/code-423n4/2021-11-vader/blob/3a43059e33d549f03b021d6b417b7eeba66cf62e/contracts/dex/math/VaderMath.sol#L73-L93>

The attack is then as follows.

1.  Be an LP for a reasonable period of time (IL protection scales linearly up to 100% after a year)
2.  Flashloan a huge amount of one of the pool's assets.
3.  Trade against the pool with the flashloaned funds to unbalance it such that your LP position has huge IL.
4.  Remove your liquidity and receive compensation from the reserve for the IL you have engineered.
5.  Re-add your liquidity back to the pool.
6.  Trade against the pool to bring it back into balance.

The attacker now holds the majority of their flashloaned funds (minus slippage/swap fees) along with a large fraction of the value of their LP position in VADER paid out from the reserve. The value of their LP position is unchanged. Given a large enough LP position, the IL protection funds extracted from the reserve will exceed the funds lost to swap fees and the attacker will be able to repay their flashloan with a profit.

This is a high risk issue as after a year any large LP is incentivised and able to perform this attack.

#### Recommended Mitigation Steps

Use a manipulation resistant oracle for the relative prices of the pool's assets (TWAP, etc.)



### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Vader Protocol |
| Report Date | N/A |
| Finders | WatchPug, TomFrenchBlockchain |

### Source Links

- **Source**: https://code4rena.com/reports/2021-11-vader
- **GitHub**: https://github.com/code-423n4/2021-11-vader-findings/issues/31
- **Contest**: https://code4rena.com/contests/2021-11-vader-protocol-contest

### Keywords for Search

`vulnerability`

