---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 19481
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
source_link: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
github_link: none

# Impact Classification
severity: low
impact: security_vulnerability
exploitability: 0.00
financial_impact: low

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Sigma Prime
---

## Vulnerability Title

Oracle Reporting Delays Can Unfairly Impact Less Sophisticated Users

### Overview

See description below for full details.

### Original Finding Content

## Description

The LidoOracle contract is responsible for reporting the state of Eth2 to the Lido system, and directly controls the amount of stETH in circulation. Because the LidoOracle can only report once per frame (day by default), there can be a sizeable delay before the Lido contracts see any dumps in balance due to slashing events. 

As such, more sophisticated “whales” (with their own view of the Eth2 state) can sell their stETH before the balance changes are visible on-chain, thus transferring their penalties and much of the risk in owning stETH onto unsuspecting third parties. 

This delay may make stETH valuation more difficult, exaggerating price fluctuations which could be taken advantage of. In a hypothetical scenario, stETH has some consistent value proportional to its associated Eth2 ETH. Should a balance drop occur, stETH is no longer one-to-one with its backed ETH for the duration of the oracle delay. Should the market be aware of this, in order to keep the value of the staked ETH consistent, the stETH price would artificially drop for this duration. 

Because node operators are fairly trusted and any slashing events should be rare, this has been deemed a low security risk.

## Recommendations

While the timeliness of oracle reporting can be improved, much of the potential for abuse is associated with uneven knowledge of the Eth2 state. It is not possible to entirely remove oracle reporting delays, so education and communication can provide a sufficient, “due-diligence” mitigation. 

Such a mitigation could include clear documentation explaining the risks associated, advising careful stETH purchases when balance decreases are pending, as well as a recommended communication platform that can notify users when such a balance decrease is expected. By providing this status notification, Lido can “even the playing field” and minimize market panic in the event of a slashing. This communication can also be helpful because the slashing penalties are not immediately applied to the balance. Thus, additional balance decreases should be expected for the 36 days following a slashing event.

To reduce market fluctuations due to inconsistent balance information, consider implementing a “flux monitoring” oracle solution, where the oracles should report more frequently than once-per-day in the event of large balance fluctuations. This can have added gas savings benefits, where oracles may not need to report as often.

In an extreme case, it may be profitable to front-run trades while the oracle reporting transaction is in the mempool.

See [here](https://benjaminion.xyz/eth2-annotated-spec/phase0/beacon-chain/#epochs_per_slashings_vector) for additional information. 

ChainLink provides some similar functionality with their “FluxMonitor” [here](https://chainlinkgod.medium.com/scaling-chainlink-in-2020-371ce24b4f31).

## Resolution

The Lido team acknowledges the issue and plans to implement the following mitigations:

- A comprehensive dashboard to provide real-time status information to stakers.
- Educate Oracle operators to proactively notify the DAO should they detect an unusual situation.

Any changes to the reporting protocol can be implemented as upgrades to the LidoOracle contracts.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/lido/lido/review.pdf

### Keywords for Search

`vulnerability`

