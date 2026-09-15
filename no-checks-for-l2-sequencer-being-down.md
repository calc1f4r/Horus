---
# Core Classification
protocol: Bima
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 38436
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-27-cyfrin-bima-v2.0.md
github_link: none

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
  - Dacian
---

## Vulnerability Title

No checks for L2 Sequencer being down

### Overview


This bug report highlights an issue with two smart contracts, `PriceFeed.sol` and `StorkOracleWrapper`, which do not have a check in place to test if the L2 Sequencer is down. This can lead to inaccurate pricing data and potential loss of funds for users or the protocol. The recommended solution is to implement a check for the L2 Sequencer, as demonstrated in Chainlink's documentation. However, Stork's documentation does not provide a similar solution at this time. 

### Original Finding Content

**Description:** Neither `PriceFeed.sol` (which is designed to work with Chainlink) nor `StorkOracleWrapper` (which has been created to allow `PriceFeed` to work with Stork Oracles) implement a check to test whether the L2 Sequencer is currently down.

When using Chainlink or other oracles with L2 chains like Arbitrum, smart contracts should [check whether the L2 Sequencer is down](https://medium.com/Bima-Labs/chainlink-oracle-defi-attacks-93b6cb6541bf#0faf) to avoid stale pricing data that appears fresh.

**Impact:** Code can execute with prices that don’t reflect the current pricing resulting in a potential loss of funds for users or the protocol.

**Recommended Mitigation:** Chainlink’s official documentation provides an [example](https://docs.chain.link/data-feeds/l2-sequencer-feeds#example-code) implementation of checking L2 sequencers. Stork's publicly available documentation does not provide any such feed.

**Bima:**
Acknowledged; Stork Oracle does not have an API for the L2 Sequencer status check at this time.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Bima |
| Report Date | N/A |
| Finders | Dacian |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-27-cyfrin-bima-v2.0.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

