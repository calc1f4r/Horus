---
# Core Classification
protocol: Florence Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27264
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-10-01-Florence Finance.md
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
  - Pashov
---

## Vulnerability Title

[L-01] Missing Arbitrum Sequencer availability check

### Overview

See description below for full details.

### Original Finding Content

The `getFundingTokenExchangeRate` method in `LoanVault` makes use of Chainlink price feeds by calling the `latestRoundData` method. While there are sufficient validations for the price feed answer, a check is missing for the L2 sequencer availability which has to be there since the protocol is moving from Ethereum to Arbitrum. In case the L2 Sequencer is unavailable the protocol will be operating with a stale price and also when the sequencer is back up then all of queued transactions will be executed on Arbitrum before new ones can be done. This can result in the `LoanVault::getFundingTokenExchangeRate` using a stale price, which means that a user might receive more or less shares from the `LoanVault` than he should have had. Still, since all of the funding requests are first approved off-chain, the probability of this happening is much lower. For a fix you can follow the [Chainlink docs](https://docs.chain.link/data-feeds/l2-sequencer-feeds) to add a check for sequencer availability.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Florence Finance |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-10-01-Florence Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

