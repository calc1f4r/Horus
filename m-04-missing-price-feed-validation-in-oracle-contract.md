---
# Core Classification
protocol: Hyperhyper_2025-03-30
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57747
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Hyperhyper-security-review_2025-03-30.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-04] Missing price feed validation in oracle contract

### Overview


This bug report is about a vulnerability found in the `Oracle` contract's `_getLastPrice` function. This function retrieves price data from oracle price feeds without performing critical validation checks. This means that stale or invalid price data could be used in the protocol, which could have a medium impact and likelihood. The report recommends implementing comprehensive price feed validation in the function to prevent this issue.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `Oracle` contract's `_getLastPrice` function retrieves price data from oracle price feeds without performing critical validation checks, which could lead to stale or invalid price data being used in the protocol.

Link: https://github.com/Hyperhyperfi/protocol/blob/212acfdcd4066334ff5ea06ce46b0bbca7ca212f/src/core/oracle/Oracle.sol#L96-L101

```solidity
    function _getLastPrice(address token) internal view returns (uint256 price, uint256 timestamp) {
        (, int256 answer, /* uint256 startedAt */, uint256 updatedAt,) = tokenOracle[token].latestRoundData();

        price = answer.toUint256();
        timestamp = updatedAt;
    }
```

This vulnerability exists in the following areas:

- Staleness Check:
  - The function does not verify if the price data is fresh by comparing the `updatedAt` timestamp with the current `block.timestamp`.
  - Stale price data could be used for critical protocol operations.
- Price Validity:
  - No validation of the answer value to ensure it's not going to go below `minAnswer` defined by the `breaker`.
- L2-Specific Concerns:
  - When deployed on L2 networks, the contract lacks sequencer uptime validation (To be validated).

## Recommendations

Implement comprehensive price feed validation in the `_getLastPrice` function.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Hyperhyper_2025-03-30 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Hyperhyper-security-review_2025-03-30.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

