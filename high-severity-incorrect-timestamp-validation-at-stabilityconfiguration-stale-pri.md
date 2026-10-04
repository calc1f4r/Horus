---
# Core Classification
protocol: Part 2
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 49966
audit_firm: Codehawks
contest_link: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl
source_link: none
github_link: https://github.com/Cyfrin/2025-01-zaros-part-2

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
  - 0xsnoweth
---

## Vulnerability Title

High Severity - Incorrect Timestamp Validation at `StabilityConfiguration` (Stale Price Reports) 

### Overview

See description below for full details.

### Original Finding Content

## Summary

The timestamp validation logic in` StabilityConfiguration.sol` incorrectly verifies Chainlink price reports, allowing stale or expired data to be accepted. This occurs due to missing checks against the report's `validUntilTimestamp` and improper validity window enforcement.

## Vulnerability Details

The `StabilityConfiguration::verifyOffchainPrice` function checks `block.timestamp > validFromTimestamp + maxVerificationDelay` but neglects two critical validations:

1. Does not verify against Chainlink's validUntilTimestamp expiration time

2. Fails to ensure (validUntil - validFrom) <= maxVerificationDelay

This allows two dangerous scenarios:

1. Expired Reports Accepted: If validUntilTimestamp has passed but validFrom + maxDelay hasn't, expired data is used

2. Overly Long Validity Windows: Reports with validity periods exceeding maxVerificationDelay are permitted

Code References:

```javascript

// StabilityConfiguration.sol
if (block.timestamp > premiumReport.validFromTimestamp + self.maxVerificationDelay) {
    revert Errors.DataStreamReportExpired();
}
```

Proof of Concept:

Consider a report with:

`validFromTimestamp = 1000`

`validUntilTimestamp = 1500`

`maxVerificationDelay = 1000`

At `block.timestamp = 1600:`

Current check passes: `1600 <= 1000+1000 (2000)`

1. Actual validity expired at 1500
2. The protocol would accept a report that has been invalid for 100 blocks.

## Impact

Traders could be liquidated based on stale prices

Incorrect profit/loss calculations for positions

Potential arbitrage opportunities draining protocol funds

Systemic risk to USDz stablecoin peg maintenance

## Tools Used

Manual code analysis

Chainlink documentation review

Timestamp manipulation testing

## Recommendations

```javascript
if (
    block.timestamp > premiumReport.validUntilTimestamp ||
    (premiumReport.validUntilTimestamp - premiumReport.validFromTimestamp) > self.maxVerificationDelay
) {
    revert Errors.DataStreamReportExpired();
}
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Codehawks |
| Protocol | Part 2 |
| Report Date | N/A |
| Finders | 0xsnoweth |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/Cyfrin/2025-01-zaros-part-2
- **Contest**: https://codehawks.cyfrin.io/c/cm60h7a380000k66h6knt2vtl

### Keywords for Search

`vulnerability`

