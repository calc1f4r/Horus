---
# Core Classification
protocol: OpenTrade
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47891
audit_firm: OtterSec
contest_link: https://www.open-trade.io/
source_link: https://www.open-trade.io/
github_link: https://github.com/tomniermann/ot-perimeter-protocol

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

# Scoring
quality_score: 0
rarity_score: 0

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - Nicholas R. Putra
  - Robert Chen
  - OtterSec
---

## Vulnerability Title

Incorrect Timestamp Calculation

### Overview


This bug report discusses an issue with the calculateSchedule function in the Loan contract. This function is important for determining timestamps that mark different phases in the loan process. However, there is a vulnerability in the formula used to calculate the earlyRedeemRequestClosingTimestamp, which is the deadline for requesting early redemption of assets from the loan. The issue is caused by a redundant operation that subtracts the transferInWindowDurationDays from itself. To fix this, the formula should be changed to add the transferInWindowDurationDays to the transferOutWindowDurationDays. This bug has been fixed in a recent patch.

### Original Finding Content

## Vulnerability Report: calculateSchedule in Loan

The function `calculateSchedule` within the Loan contract is crucial for determining and configuring several critical timestamps that delineate different phases within the loan life cycle.

### Affected File
- **Location:** `contracts/Loan.sol`
- **Language:** Solidity

### Function Definition
```solidity
function calculateSchedule() internal {
    [...]
    earlyRedeemRequestClosingTimestamp =
        accrualStartTimestamp +
        (settings.durationDays -
        settings.transferInWindowDurationDays -
        settings.transferInWindowDurationDays) *
        (1 days);
    [...]
}
```

### Description of the Vulnerability
The vulnerability emerges from the calculation of `earlyRedeemRequestClosingTimestamp` within `calculateSchedule`. This timestamp represents the deadline for requesting early redemption of assets from the loan. 

The issue arises from the flawed formula utilized for calculations. Specifically, it subtracts `transferInWindowDurationDays` from itself, as shown in the code snippet above, resulting in a redundant operation and assigning an incorrect value to the timestamp.

### Remediation
Change the formula used for the calculation of `earlyRedeemRequestClosingTimestamp` so that `transferInWindowDurationDays` is added to `transferOutWindowDurationDays`.

Updated function definition:

```solidity
function calculateSchedule() internal {
    [...]
    earlyRedeemRequestClosingTimestamp =
        accrualStartTimestamp +
        (settings.durationDays -
        settings.transferInWindowDurationDays -
        settings.transferOutWindowDurationDays) *
        (1 days);
    [...]
}
```

### Patch
- **Fixed in commit:** 6249748.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | OpenTrade |
| Report Date | N/A |
| Finders | Nicholas R. Putra, Robert Chen, OtterSec |

### Source Links

- **Source**: https://www.open-trade.io/
- **GitHub**: https://github.com/tomniermann/ot-perimeter-protocol
- **Contest**: https://www.open-trade.io/

### Keywords for Search

`vulnerability`

