---
# Core Classification
protocol: Blueberry Update
chain: everychain
category: uncategorized
vulnerability_type: liquidation

# Attack Vector Details
attack_type: liquidation
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 18503
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/69
source_link: none
github_link: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/117

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
  - liquidation
  - missing-logic

protocol_categories:
  - lending
  - leveraged_farming
  - options_vault

# Audit Details
report_date: unknown
finders_count: 3
finders:
  - cducrest-brainbot
  - HonorLt
  - 0x52
---

## Vulnerability Title

M-9: Issue 290 from previous contest has not been fully addressed by fixes

### Overview


This bug report is about an issue from a previous contest that has not been fully addressed by the fixes. The issue is that users may be liquidated without the chance to repay their debt. MEV bots are typically used to liquidate positions, so even if a user tries to pay off their debt on the same block that repay is enabled, they will still be liquidated due to frontrunning. The impact of this is that users who become liquidatable during a repay pause will still be unable to save their position. The code snippet mentioned in the report is BlueBerryBank.sol#L487-L548. The recommendation given is to put a timer that prevents liquidations for some amount of time after repayment has been resumed, so that users can fairly repay their position.

### Original Finding Content

Source: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/117 

## Found by 
0x52, HonorLt, cducrest-brainbot
## Summary

[Issue 290](https://github.com/sherlock-audit/2023-02-blueberry-judging/issues/290) from the previous contest points out that users may be liquidated without the chance to repay their debt. Liquidate was changed to only be allowed when repayment was allowed. While this does address some of the problem this will still fail to protect users who become liquidatable during the period of time that repay has been disabled.

MEV bots are typically used to liquidate positions since it is always more profitable to liquidate the vault even if a user tries to pay off their debt on the same black that repay is enabled, they will still be liquidated because of frontrunning.

## Vulnerability Detail

See summary.

## Impact

Users who become liquidatable during a repay pause will still be unable to save their position

## Code Snippet

[BlueBerryBank.sol#L487-L548](https://github.com/sherlock-audit/2023-04-blueberry/blob/main/blueberry-core/contracts/BlueBerryBank.sol#L487-L548)

## Tool used

Manual Review

## Recommendation

When repay is paused and then resumed, put a timer that prevents liquidations for some amount of time after (i.e. 4 hours) so that users can fairly repay their position after repayment has been resumed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Sherlock |
| Protocol | Blueberry Update |
| Report Date | N/A |
| Finders | cducrest-brainbot, HonorLt, 0x52 |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2023-04-blueberry-judging/issues/117
- **Contest**: https://app.sherlock.xyz/audits/contests/69

### Keywords for Search

`Liquidation, Missing-Logic`

