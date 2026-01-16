---
# Core Classification
protocol: Brava Labs
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53569
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf
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
  - Sigma Prime
---

## Vulnerability Title

Protocol Fees Can Block Further Deposits

### Overview


This bug report discusses an issue with the accounting system that can cause deposits to fail on the Brava platform. The problem occurs when accrued fees owed to Brava are removed before processing a deposit, which can lead to an overflow revert and ultimately a failed deposit. This issue can also occur during the slippage control process. The report recommends two solutions - either changing the accounting flow to record the share balance after fees have been processed, or regularly using the fee taking bot to keep accrued fees at a small proportion compared to user deposits. The issue has been resolved by adjusting the share balance calculations in AcrossSupply. However, it should be noted that the share balance calculations in other protocols may not accurately represent the size of a user's deposit, but these protocols have not been altered. 

### Original Finding Content

## Description

Due to system accounting, it is possible for the payment of accrued fees to Brava to cause further deposits to fail. 

When supplying assets, accrued fees owed to Brava are first removed before processing the deposit. As this occurs after taking the initial share balance, it is possible that the overall share balance may decrease after a deposit, for example, if a user has not interacted with the protocol in a long time, such as 1 year. If the share balance decreases, then the accounting on line [79] will cause an overflow revert, which in turn will cause the deposit to fail.

This revert can also occur as part of the slippage control in AcrossSupply with the check on line [80]:

```
require(
    shares >= _inputData.minSharesReceived,
    Errors.Action_InsufficientSharesReceived(
        protocolName(),
        uint8(actionType()),
        shares,
        _inputData.minSharesReceived
    )
);
```

This check is intended to prevent a supply issuing too few shares for a deposit and so is more likely to occur than the previously mentioned overflow. 

Note, while only Across can revert due to this issue, the other protocols are affected by this for the accounting aspect only. Other protocols do not revert, but the sharesBefore and sharesAfter emitted by their events do not accurately represent the deposit size.

## Recommendations

- Alter the accounting flow such that the share balance is recorded after fees have been processed, but before the supply or withdrawal action occurs.
- Alternatively, ensure regular use of the fee taking bot, so that accrued fees are always proportionally very small compared to user deposits.

## Resolution

The share balance calculations in AcrossSupply have been adjusted to remove the potential for protocol fee payment to cause an overflow revert. 

The Brava team have noted that the delta of sharesBefore and sharesAfter emitted by events is not intended to represent the size of a user’s deposit and so other contracts have not been altered.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | Brava Labs |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/brava/report.pdf

### Keywords for Search

`vulnerability`

