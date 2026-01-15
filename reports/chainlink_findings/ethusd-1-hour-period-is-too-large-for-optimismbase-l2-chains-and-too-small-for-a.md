---
# Core Classification
protocol: Beanstalk: The Finale
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36230
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/clw9e11e4001gdv0iigjylx5n
source_link: none
github_link: https://github.com/Cyfrin/2024-05-beanstalk-the-finale

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

protocol_categories:
  - yield
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 4
finders:
  - Bauchibred
  - holydevoti0n
  - T1MOH
  - Uno
---

## Vulnerability Title

ETH/USD 1 hour period is too large for Optimism/Base L2 Chains and too small for Arbitrum/Avalanche leading to consuming stale price data.

### Overview

See description below for full details.

### Original Finding Content

## Summary

This is not considered Known Issue.

The stale period 1 hours is too large for Optimism and Base chains, leading to consuming stale price data.\
On the other hand, that period is too small for Arbitrum and Avalanche chains.

## Vulnerability Details

After the Previous Audit (Beanstalk Part 1) The Beanstalk will update CHAINLINK\_TIMEOUT to 1 hour instead of 4 hours but its still an issue after\
the migration to L2 Chains Optimism/Base/Avalanche/Arbitrum etc..

in previous audit a chainlink oracle Vulnerability was submitted and validated as Medium the bug was:

> The `LibChainlinkOracle` library utilizes a `CHAINLINK_TIMEOUT` constant set to `14400` seconds (4 hours). This duration is four times longer than the `Chainlink` heartbeat that is `3600` seconds (1 hour), potentially introducing a significant delay in recognizing stale or outdated price data.

link to previous audit (Beanstalk Part 1):\
<https://codehawks.cyfrin.io/c/2024-02-Beanstalk-1/results?t=report&lt=contest&sc=reward&sj=reward&page=1>



This was on ethereum mainnet but after migration to L2, CHAINLINK\_TIMEOUT must be changed to fit the targeted L2.

Beanstalk will migrate to L2 Optimism or Base or Avalanche etc... and these chains has different ETH/USD heartbeats:

1. On Ethereum, the oracle will update the price data [every \~1 hour](https://data.chain.link/feeds/ethereum/mainnet/eth-usd).
2. On Optimism, the oracle will update the price data [every \~20 minutes](https://data.chain.link/feeds/optimism/mainnet/eth-usd).
3. On Base, the oracle will update the price data [every \~20 minutes](https://data.chain.link/feeds/base/base/eth-usd).
4. On Arbitrum, the oracle will update the price data [every \~24 hours](https://data.chain.link/arbitrum/mainnet/crypto-usd/eth-usd).
5. On Avalanche, the oracle will update the price data [every \~24 hours](https://data.chain.link/feeds/avalanche/mainnet/eth-usd).

On some chains such as Optimism Base, 1 hour considered too large for the stale period, causing to return stale price data.\
And on other chains such as Arbitrum Avalanche 1 hour considered too small.

## Impact

A `CHAINLINK_TIMEOUT` that is significantly longer than the heartbeat can lead to scenarios where the `LibChainlinkOracle`\
library accepts outdated price. &#x20;

## Tools Used

Previous Audits: <https://github.com/Cyfrin/2023-07-foundry-defi-stablecoin/issues/961>

## Recommendations

Consider to set the right heartbeat for the targeted L2.

1. &#x20;On Optimism, the oracle will update the price data [every \~20 minutes](https://data.chain.link/feeds/optimism/mainnet/eth-usd).
2. On Base, the oracle will update the price data [every \~20 minutes](https://data.chain.link/feeds/base/base/eth-usd).
3. On Arbitrum, the oracle will update the price data [every \~24 hours](https://data.chain.link/arbitrum/mainnet/crypto-usd/eth-usd).
4. On Avalanche, the oracle will update the price data [every \~24 hours](https://data.chain.link/feeds/avalanche/mainnet/eth-usd).

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Beanstalk: The Finale |
| Report Date | N/A |
| Finders | Bauchibred, holydevoti0n, T1MOH, Uno |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2024-05-beanstalk-the-finale
- **Contest**: https://codehawks.cyfrin.io/c/clw9e11e4001gdv0iigjylx5n

### Keywords for Search

`vulnerability`

