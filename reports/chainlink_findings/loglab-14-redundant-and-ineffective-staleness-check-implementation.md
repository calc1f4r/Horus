---
# Core Classification
protocol: Basisos
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62404
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-11-25-BasisOS.md
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
  - Hexens
---

## Vulnerability Title

[LOGLAB-14] Redundant and ineffective staleness check implementation

### Overview

See description below for full details.

### Original Finding Content

**Severity:** Low

**Path:** src/oracle/LogarithmOracle.sol#L110-115

**Description:** The `LogarithmOracle` uses Chainlink data feeds to fetch assets prices. This oracle exposes the `latestRoundData` function to return pricing data.

There is a staleness check, the first part of which is redundant.
```
uint256 heartbeatDuration = _getLogarithmOracleStorage().heartbeatDurations[address(priceFeed)];
if (block.timestamp > timestamp && block.timestamp - timestamp > heartbeatDuration) {
    revert Errors.PriceFeedNotUpdated(asset, timestamp, heartbeatDuration);
}
```
The condition `block.timestamp - timestamp > heartbeatDuration` is sufficient to check for staleness. The additional condition `block.timestamp > timestamp` is redundant and adds no value. Furthermore, in unlikely cases where the price feed occasionally returns incorrect data (e.g., a `timestamp` value greater than `block.timestamp`), the staleness check does not revert as expected. This could result in inconsistent or invalid behavior, as the check fails to handle such edge cases properly.

**Remediation:**  Consider deleting redundant check.

**Status:** Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Basisos |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2024-11-25-BasisOS.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

