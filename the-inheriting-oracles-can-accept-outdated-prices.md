---
# Core Classification
protocol: Elara Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59159
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/elara-finance/ceaf2e43-2883-4f4f-bd80-20dc354abb46/index.html
source_link: https://certificate.quantstamp.com/full/elara-finance/ceaf2e43-2883-4f4f-bd80-20dc354abb46/index.html
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
  - Gereon Mendler
  - Julio Aguilar
  - Valerian Callens
---

## Vulnerability Title

The Inheriting Oracles Can Accept Outdated Prices

### Overview


The client has marked a bug as "Fixed" in the contract code. The bug was related to the `maxDelayTime` variable not being initialized in the constructor, which could result in outdated price information being delivered by the `API3Oracle`, `ChainlinkOracle`, and `PythOracle` implementations. The recommendation is to initialize this variable to a non-zero value in the constructor and follow best practices for integrating these oracles.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `12cbe0a9f0efaa2dfe8a2577e33102a40802f584`. The client provided the following explanation:

> We set maxDelayTime when deploying the contract, rather than initializing it in the constructor. We have currently set maxDelayTime to one month on our deployed contracts on Zircuit testnet. When deploying on the Zircuit mainnet, we will ensure that maxDelayTime is greater than the heartbeat of the oracle price feed. (e.g. 1 month)

**File(s) affected:**`API3Oracle.sol`, `ChainlinkOracle.sol`, `PythOracle.sol`

**Description:** The `API3Oracle`, `ChainlinkOracle`, and `PythOracle` implementations are at risk of accepting outdated prices because the `maxDelayTime` variable is not initialized during construction. As a result, this variable could remain unset for an indefinite period, potentially causing these oracles to deliver outdated price information.

**Recommendation:** We recommend initializing `maxDelayTime` to a non-zero value in the constructor. Also, for more information about integrating these Oracles, see the following:

*   Pyth oracles, keep an eye on the best practices described here: https://docs.pyth.network/price-feeds/best-practices
*   API3 oracles, keep an eye on the best practices described here: https://docs.api3.org/explore/dapis/security-considerations.html
*   Chainlink oracles, keep an eye on the best practices described here: https://docs.chain.link/data-feeds/developer-responsibilities

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Elara Finance |
| Report Date | N/A |
| Finders | Gereon Mendler, Julio Aguilar, Valerian Callens |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/elara-finance/ceaf2e43-2883-4f4f-bd80-20dc354abb46/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/elara-finance/ceaf2e43-2883-4f4f-bd80-20dc354abb46/index.html

### Keywords for Search

`vulnerability`

