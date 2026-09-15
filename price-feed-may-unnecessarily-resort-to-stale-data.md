---
# Core Classification
protocol: Ethereum Reserve Dollar (ERD)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60136
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
source_link: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
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
finders_count: 3
finders:
  - Ibrahim Abouzied
  - Rabib Islam
  - Hytham Farah
---

## Vulnerability Title

Price Feed May Unnecessarily Resort to Stale Data

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> We use the oracle that liquity used.

**File(s) affected:**`PriceFeed.sol`

**Description:** At `PriceFeed.sol#265`, it is required that both Chainlink and Tellor are working in order for the price to be updated. This means that if Chainlink is restored while Tellor is not, the feed will continue to use the "last good price" instead of proceeding with the latest Chainlink price. The vice versa case is also true: if Tellor is restored while Chainlink is not, the feed will continue to use the "last good price" instead of proceeding with the latest Tellor price. Hence stale data will end up being preferred to fresh data.

A similar situation occurs at `PriceFeed.sol#234`, where if Chainlink becomes operational at the same time as Tellor becomes unreliable, fresh Chainlink data will not be used.

**Recommendation:** Rework the logic so that fresh data is always used when it can reliably be sourced from at least Chainlink.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Ethereum Reserve Dollar (ERD) |
| Report Date | N/A |
| Finders | Ibrahim Abouzied, Rabib Islam, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/ethereum-reserve-dollar-erd/d2c63484-d071-4479-ab8d-d3267f272253/index.html

### Keywords for Search

`vulnerability`

