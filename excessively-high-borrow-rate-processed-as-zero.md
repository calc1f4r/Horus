---
# Core Classification
protocol: NUTS Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 62697
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Pike/README.md#3-excessively-high-borrow-rate-processed-as-zero
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
  - MixBytes
---

## Vulnerability Title

Excessively High Borrow Rate Processed as Zero

### Overview


This bug report talks about an issue in the `accrueInterest` function, which checks for a maximum borrow rate. If the computed rate exceeds this maximum, the function updates a timestamp and returns early, treating the rate as zero without notifying anyone. This can lead to incorrect financial calculations and make it difficult to detect abnormal rates. The recommendation is to revert the transaction and prompt for investigation instead of silently ignoring the issue. It is also suggested to make the maximum rate configurable to stay aligned with the current interest rate model.

### Original Finding Content

##### Description
This issue has been identified within the `accrueInterest` function, which checks whether the computed borrow rate exceeds `borrowRateMaxMantissa`. If it does, the function updates `accrualBlockTimestamp` and returns early:

```solidity
if (IInterestRateModel(address(this)).getBorrowRate(
    getCash(), snapshot.totalBorrow, snapshot.totalReserve
) > $.borrowRateMaxMantissa) {
    $.accrualBlockTimestamp = currentBlockTimestamp;
    return;
}
```

This effectively treats any excessively high borrow rate as zero interest accrual without notifying users or developers. Consequently, if the interest rate model malfunctions or market conditions become abnormal, the protocol silently applies no interest instead of alerting stakeholders. Additionally, `borrowRateMaxMantissa` is only set in the constructor and may not align with changing interest rate models over time.

The issue is classified as **medium** severity because it leads to inaccurate financial calculations and hinders prompt detection of anomalous or erroneous borrow rate conditions.

##### Recommendation
We recommend reverting the transaction if the computed borrow rate exceeds the maximum threshold, prompting immediate investigation rather than silently ignoring it. For example:

```solidity!
if (IInterestRateModel(address(this)).getBorrowRate(
    getCash(), snapshot.totalBorrow, snapshot.totalReserve
) > $.borrowRateMaxMantissa) {
    revert PTokenError.ExcessiveBorrowRate();
}
```

Additionally, consider making `borrowRateMaxMantissa` configurable by an authorized administrator so that it remains aligned with the current interest rate model.


### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | NUTS Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/NUTS%20Finance/Pike/README.md#3-excessively-high-borrow-rate-processed-as-zero
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

