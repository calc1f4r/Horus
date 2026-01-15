---
# Core Classification
protocol: Open Dollar - Smart Contract Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59518
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/open-dollar-smart-contract-audit/202828fa-eb09-4d33-beab-c1ebee11ebd1/index.html
source_link: https://certificate.quantstamp.com/full/open-dollar-smart-contract-audit/202828fa-eb09-4d33-beab-c1ebee11ebd1/index.html
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
finders_count: 3
finders:
  - Nikita Belenkov
  - Ibrahim Abouzied
  - Mostafa Yassin
---

## Vulnerability Title

Missing Checks for Sequencer Uptime when Fetching Chainlink Prices

### Overview


This bug report is about a function called `ChainlinkRelayer.latestRoundData()` which is used to get the latest price of an asset from Chainlink price feeds. The issue is that when the protocol is deployed on Arbitrum, it is important to check the sequencer's uptime before getting the price data. If the sequencer is down, there is a risk of using incorrect or old prices. To avoid this, it is recommended to use an example code provided in the Chainlink documentation to check the sequencer's uptime before getting the price data. This bug has been fixed in a recent update and the recommended fix can be found in the `contracts/oracles/ChainlinkRelayer.sol` file in the `open-dollar/od-relayer` repository.

### Original Finding Content

**Update**
The Oracle system has been moved to a different repository, and the suggested fix has been added. Fixed in commit `a1a8ef1402716a230b12d9e0f3cacd75cb64b1d8` in `open-dollar/od-relayer`.

**File(s) affected:**`contracts/oracles/ChainlinkRelayer.sol`

**Description:** The `ChainlinkRelayer.latestRoundData()` function fetches the latest price of an asset from Chainlink price feeds. However, as the protocol is intended to be deployed on Arbitrum, checking the sequencer's uptime before querying price data is crucial. If the sequencer is down, there is a chance of using an incorrect or stale price. Please refer to the [Chainlink L2 Sequencer Uptime Feeds](https://docs.chain.link/data-feeds/l2-sequencer-feeds) document for more details.

**Recommendation:** Consider checking the sequencer's uptime feed to avoid using stale prices. An [example code](https://docs.chain.link/data-feeds/l2-sequencer-feeds#example-code) can be found in the Chainlink official documentation

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Open Dollar - Smart Contract Audit |
| Report Date | N/A |
| Finders | Nikita Belenkov, Ibrahim Abouzied, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/open-dollar-smart-contract-audit/202828fa-eb09-4d33-beab-c1ebee11ebd1/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/open-dollar-smart-contract-audit/202828fa-eb09-4d33-beab-c1ebee11ebd1/index.html

### Keywords for Search

`vulnerability`

