---
# Core Classification
protocol: Hubble
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 1518
audit_firm: Code4rena
contest_link: https://code4rena.com/contests/2022-02-hubble-contest
source_link: https://code4rena.com/reports/2022-02-hubble
github_link: https://github.com/code-423n4/2022-02-hubble-findings/issues/46

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
  - derivatives
  - liquidity_manager
  - staking_pool

# Audit Details
report_date: unknown
finders_count: 10
finders:
  - csanuragjain
  - pauliax
  - cccz
  - leastwood
  - WatchPug
---

## Vulnerability Title

[M-01] Liquidations can be run on the bogus Oracle prices

### Overview


This bug report concerns an issue in the Oracle.sol contract which could allow a malicious user to liquidate a healthy position if the price feed is manipulated or there is any malfunction based volatility on the market. The issue occurs in the Oracle.getUnderlyingPrice function and is used in liquidation triggers providing isLiquidatable and _getLiquidationInfo functions. The recommended mitigation steps include adding a non-zero Oracle price check, possibly adding an additional Oracle feed information usage to control that the price is fresh, and constructing a mitigation mechanics for price spikes. This could involve tracking both current and TWAP prices, and condition all state changing actions, including liquidations, on the current price being within a threshold of the TWAP one. Another option is to introduce a time delay between liquidation request and actual liquidation. The Chainlink documentation can provide more information on the implementation of these mitigation steps.

### Original Finding Content

_Submitted by hyh, also found by 0x1f8b, cccz, csanuragjain, defsec, hubble, leastwood, pauliax, WatchPug, and ye0lde_

If the price feed is manipulated in any way or there is any malfunction based volatility on the market, a malicious user can use this to liquidate a healthy position.

An attacker can setup a monitoring of the used Oracle feed and act on observing a price outbreak (for example, zero price, which is usually a subject to filtration), liquidating the trader position which is perfectly healthy otherwise, obtaining the collateral with a substantial discount at the expense of the trader.

The same is for a flash crash kind of scenario, i.e. a price outbreak of any nature will allow for non-market liquidation by an attacker, who has the incentives to setup such a monitoring and act on such an outbreak, knowing that it will not be smoothed or filtered out, allowing a liquidation at a non-market price that happen to be printed in the Oracle feed

### Proof of Concept

Oracle.getUnderlyingPrice just passes on the latest Oracle answer, not checking it anyhow:

<https://github.com/code-423n4/2022-02-hubble/blob/main/contracts/Oracle.sol#L24-L35>

It is then used in liquidation triggers providing isLiquidatable and \_getLiquidationInfo functions:

<https://github.com/code-423n4/2022-02-hubble/blob/main/contracts/MarginAccount.sol#L249>

<https://github.com/code-423n4/2022-02-hubble/blob/main/contracts/MarginAccount.sol#L465>

### Recommended Mitigation Steps

Add a non-zero Oracle price check, possibly add an additional Oracle feed information usage to control that the price is fresh. Please consult the Chainlink for that as OCR introduction might have changed the state of the art approach (i.e. whether and how to use latestRoundData returned data):

<https://docs.chain.link/docs/off-chain-reporting/>

Regarding any price spikes it is straightforward to construct a mitigation mechanics for such cases, so the system will be affected by sustainable price movements only.

As price outrages provide a substantial attack surface for the project it's worth adding some complexity to the implementation.

One of the approaches is to track both current and TWAP prices, and condition all state changing actions, including liquidations, on the current price being within a threshold of the TWAP one. If the liquidation margin level is conservative enough and TWAP window is small enough this is safe for the overall stability of the system, while providing substantial mitigation mechanics by allowing state changes on the locally calm market only.

Another approach is to introduce time delay between liquidation request and actual liquidation. Again, conservative enough margin level plus small enough delay keeps the system safe, while requiring that market conditions allow for liquidation both at request time and at execution time provides ample filtration against price feed outbreaks

**[atvanguard (Hubble) confirmed](https://github.com/code-423n4/2022-02-hubble-findings/issues/46)**

**[moose-code (judge) decreased severity from High to Medium](https://github.com/code-423n4/2022-02-hubble-findings/issues/46)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Hubble |
| Report Date | N/A |
| Finders | csanuragjain, pauliax, cccz, leastwood, WatchPug, 0x1f8b, hyh, hubble, ye0lde, defsec |

### Source Links

- **Source**: https://code4rena.com/reports/2022-02-hubble
- **GitHub**: https://github.com/code-423n4/2022-02-hubble-findings/issues/46
- **Contest**: https://code4rena.com/contests/2022-02-hubble-contest

### Keywords for Search

`vulnerability`

