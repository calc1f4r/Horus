---
# Core Classification
protocol: Ethereum Credit Guild
chain: everychain
category: uncategorized
vulnerability_type: chain_reorganization_attack

# Attack Vector Details
attack_type: chain_reorganization_attack
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 30221
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-12-ethereumcreditguild
source_link: https://code4rena.com/reports/2023-12-ethereumcreditguild
github_link: https://github.com/code-423n4/2023-12-ethereumcreditguild-findings/issues/1253

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
  - chain_reorganization_attack

# Audit Details
report_date: unknown
finders_count: 2
finders:
  - EV\_om
  - Ward
---

## Vulnerability Title

[M-01] No check for sequencer uptime can lead to dutch auctions failing or executing at bad prices

### Overview


The `AuctionHouse` contract has a bug that can cause auctions to fail or execute at unfavorable prices. This is because there is no check for sequencer uptime, which can lead to issues if there is a network outage. This can result in a loss for the protocol and the slashing of all users with weight on the term. To fix this, it is recommended to integrate an external uptime feed or implement a mechanism to restart auctions if there are no bids. The severity of this bug is debated, with some suggesting it is low due to the low likelihood of a network outage, while others argue it should be medium as it can still result in loss and slashing for users.

### Original Finding Content


The `AuctionHouse` contract implements a Dutch auction mechanism to recover debt from collateral. However, there is no check for sequencer uptime, which could lead to auctions failing or executing at unfavorable prices.

The current deployment parameters allow auctions to succeed without a loss to the protocol for a duration of 10m 50s. If there's no bid on the auction after this period, the protocol has no other option but to take a loss or forgive the loan. This could have serious consequences in the event of a network outage, as any loss results in the slashing of all users with weight on the term.

Network outages and large reorgs happen with relative frequency. For instance, Arbitrum suffered an hour-long outage just two weeks ago ([source](https://github.com/ArbitrumFoundation/docs/blob/50ee88b406e6e5f3866b32d147d05a6adb0ab50e/postmortems/15\_Dec\_2023.md)).

### Proof of Concept

Consider the following scenario:

1. A loan is called and an auction is initiated.
2. The network experiences an outage, causing the sequencer to go offline.
3. The auction fails to receive any bids within the 10m 50s window due to the outage.
4. The protocol is forced to take a loss (if there's still a bid after the `midPoint` and before the auction ends) or forgive the loan, both leading to the complete slashing of all users with weight on the term.

### Recommended Mitigation Steps

To mitigate this issue, consider integrating an external uptime feed such as [Chainlink's L2 Sequencer Feeds](https://docs.chain.link/data-feeds/l2-sequencer-feeds). This would allow the contract to invalidate an auction if the sequencer was ever offline during its duration. Alternatively, implement a mechanism to restart an auction if it has received no bids.

**[eswak (Ethereum Credit Guild) acknowledged, but disagreed with severity and commented](https://github.com/code-423n4/2023-12-ethereumcreditguild-findings/issues/1253#issuecomment-1898857129):**
 > Acknowledging this, we definitely don't want to add a dependency on an oracle to run the liquidations, so maybe another fix would be to define auction durations in number of blocks. I think basing auctions on time is semantically correct because it depends on market conditions (that are based on time) and when the sequencer resumes the conditions that triggered the auction might not hold anymore. The `forgive()` path at the end of the auction could be used to unstick the situation at the smart contract level, and the governance can organize an orderly fix of the situation when the sequencer resumes.
> 
> Given the likelihood, I think it should be low severity, especially since we know auctions have to be longer on L2s than on mainnet (liquidity potentially needs to bridge, etc), so the chance that a downtime large enough relative to the auction duration will happen is pretty low.

**[TrungOre (judge) commented](https://github.com/code-423n4/2023-12-ethereumcreditguild-findings/issues/1253#issuecomment-1917487929):**
 > In my opinion, if an auction is still active when the sequencer is down, it may cause a loss of assets (collateral) for the borrower. Although governance's measures can help mitigate the situation when the sequencer resumes, loss and slashing in this lending term will be inevitable in such cases. So I think medium severity is appropriate for this issue, but I'm open to other feedback.

***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Ethereum Credit Guild |
| Report Date | N/A |
| Finders | EV\_om, Ward |

### Source Links

- **Source**: https://code4rena.com/reports/2023-12-ethereumcreditguild
- **GitHub**: https://github.com/code-423n4/2023-12-ethereumcreditguild-findings/issues/1253
- **Contest**: https://code4rena.com/reports/2023-12-ethereumcreditguild

### Keywords for Search

`Chain Reorganization Attack`

