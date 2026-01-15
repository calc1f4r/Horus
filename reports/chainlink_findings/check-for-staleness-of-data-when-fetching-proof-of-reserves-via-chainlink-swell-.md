---
# Core Classification
protocol: Swell Barracuda
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31983
audit_firm: Cyfrin
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
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
finders_count: 2
finders:
  - Dacian
  - Carlitox477
---

## Vulnerability Title

Check for staleness of data when fetching Proof of Reserves via Chainlink `Swell ETH PoR` Oracle

### Overview

See description below for full details.

### Original Finding Content

**Description:** `RepricingOracle::_assertRepricingSnapshotValidity` [uses](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/RepricingOracle.sol#L329-L331) the `Swell ETH PoR` Chainlink Proof Of Reserves Oracle to fetch an off-chain data source for Swell's current reserves.

The Oracle `Swell ETH PoR` is [listed](https://docs.chain.link/data-feeds/proof-of-reserve/addresses?network=ethereum&page=1#networks) on Chainlink's website as having a heartbeat of `86400` seconds (check the "Show More Details" box in the top-right corner of the table), however [no staleness check](https://medium.com/SwellNetwork/chainlink-oracle-defi-attacks-93b6cb6541bf#99af) is implemented by `RepricingOracle`:
```solidity
// @audit no staleness check
(, int256 externallyReportedV3Balance, , , ) = AggregatorV3Interface(
  ExternalV3ReservesPoROracle
).latestRoundData();
```

**Impact:** If the `Swell ETH PoR` Chainlink Proof Of Reserves Oracle has stopped functioning correctly, `RepricingOracle::_assertRepricingSnapshotValidity` will continue processing with stale reserve data as if it were fresh.

**Recommended Mitigation:** Implement a staleness check and if the Oracle is stale, either revert or skip using it as the code currently does [if the oracle is not set](https://github.com/SwellNetwork/v3-contracts-lst/tree/a95ea7942ba895ae84845ab7fec1163d667bee38/contracts/implementations/RepricingOracle.sol#L325-L327).

For multi-chain deployments ensure that a [correct staleness check is used for each feed](https://medium.com/SwellNetwork/chainlink-oracle-defi-attacks-93b6cb6541bf#fb78) as the same feed can have different heartbeats on different chains.

Consider adding an off-chain bot that periodically checks if the Oracle has become stale and if it has, raises an internal alert for the team to investigate.

**Swell:** Fixed in commit [84a6517](https://github.com/SwellNetwork/v3-contracts-lst/commit/84a65178c31222d80559f6fd5f1b4c60f9249016).

**Cyfrin:**
Verified.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cyfrin |
| Protocol | Swell Barracuda |
| Report Date | N/A |
| Finders | Dacian, Carlitox477 |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

