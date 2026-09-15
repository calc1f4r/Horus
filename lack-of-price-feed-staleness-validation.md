---
# Core Classification
protocol: Datachain - App for Liquidity
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 58926
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/datachain-app-for-liquidity/b8c4b08a-4456-4ab9-a381-d738d1ba3f0b/index.html
source_link: https://certificate.quantstamp.com/full/datachain-app-for-liquidity/b8c4b08a-4456-4ab9-a381-d738d1ba3f0b/index.html
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
  - Hamed Mohammadi
  - Ibrahim Abouzied
  - Danny Aksenov
---

## Vulnerability Title

Lack of Price Feed Staleness Validation

### Overview


This bug report discusses an issue with the TokenPriceOracle contract, which retrieves price data from Chainlink price feeds. The problem is that the contract does not have checks in place to ensure that the price data is up-to-date. This could lead to outdated prices being used in important operations if there are delays or problems with the price feed. The client has marked this issue as "Fixed" and provided an explanation for the fix. They suggest validating the "updatedAt" and "answeredInRound" values and using multiple oracles for more reliable data. The affected files are TokenPriceOracle.sol and StableTokenPriceOracle.sol.

### Original Finding Content

**Update**
Marked as "Fixed" by the client. Addressed in: `990dadbc16696c96a58e8779ef90e7c72b029034`. The client provided the following explanation:

> We introduced pool-level expiration checks with a buffer using updateAt (answeredInRound appeared to be deprecated).

**File(s) affected:**`src/TokenPriceOracle.sol`, `src/StableTokenPriceOracle.sol`

**Description:** The `TokenPriceOracle` contract retrieves price data from `Chainlink` price feeds but lacks validation checks for stale or outdated price data. This could lead to the usage of outdated prices in critical operations if the price feed experiences delays or issues.

**Recommendation:** Validate the `updatedAt` and `answeredInRound` values returned from `latestRoundData()`. Consider using multiple oracles if redundancy and reliably fresh data is of high importance.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Datachain - App for Liquidity |
| Report Date | N/A |
| Finders | Hamed Mohammadi, Ibrahim Abouzied, Danny Aksenov |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/datachain-app-for-liquidity/b8c4b08a-4456-4ab9-a381-d738d1ba3f0b/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/datachain-app-for-liquidity/b8c4b08a-4456-4ab9-a381-d738d1ba3f0b/index.html

### Keywords for Search

`vulnerability`

