---
# Core Classification
protocol: Cedro Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37532
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro Finance.md
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
  - Zokyo
---

## Vulnerability Title

Chainlink `basePrice` can be non-positive

### Overview

See description below for full details.

### Original Finding Content

**Severity**: Low

**Status**: Resolved

**Description**

In Contract Oracle.sol, the method `getPriceFromChainlink(...)` fetches assets prices from chainlink as follows:

```solidity
(
           uint80 roundID,
           int256 basePrice,
           /*uint256 startedAt*/,
           uint256 timeStamp,
           uint80 answeredInRound
       ) =
        AggregatorV3Interface(
           aggregator[_symbol]
       ).latestRoundData();


       if (basePrice == 0) revert ChainlinkMalfunction(TAG, _symbol); 
```
Here `basePrice` is of type int256 meaning it can be a negative value as well. Checking it for just equal to 0 can lead to prices being negative.

**Recommendation**:
Update the above check as follows:
```solidity
if (basePrice <= 0) revert ChainlinkMalfunction(TAG, _symbol);
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Cedro Finance |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro Finance.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

