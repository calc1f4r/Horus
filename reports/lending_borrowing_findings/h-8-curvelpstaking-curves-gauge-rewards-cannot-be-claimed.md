---
# Core Classification
protocol: Sentiment
chain: everychain
category: logic
vulnerability_type: business_logic

# Attack Vector Details
attack_type: business_logic
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 3356
audit_firm: Sherlock
contest_link: https://app.sherlock.xyz/audits/contests/1
source_link: none
github_link: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/502-H

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.60
financial_impact: high

# Scoring
quality_score: 3
rarity_score: 3

# Context Tags
tags:
  - business_logic

protocol_categories:
  - liquid_staking
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - WATCHPUG
---

## Vulnerability Title

H-8: `CurveLPStaking` Curve's gauge rewards cannot be claimed

### Overview


This bug report is about an issue found by WatchPug during an audit of Sentiment's CurveLPStakingController. The issue is that the controller does not support the `claim_rewards()` function, and both `deposit()` and `withdraw()` are using the default value (`false`) for the `_claim_rewards` parameter. This means that Curve's gauge rewards cannot be claimed. The code snippet provided in the report can be found at https://github.com/sentimentxyz/controller/blob/be4a7c70ecef788ca9226b46ff108ddd9001b14e/src/curve/CurveLPStakingController.sol#L20-L24. The recommendation was to consider supporting `claim_rewards(address,address)` or using `deposit(uint256,address,bool)` and `withdraw(uint256,address,bool)` to support claim rewards when deposit() or withdraw(). Sentiment Team fixed the controller as recommended to claim gauge rewards and moved gauge token oracle into a separate contract instead. Lead Senior Watson confirmed the fix.

### Original Finding Content

Source: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/502-H 
## Found by 
WATCHPUG

## Summary

Note: This issue is a part of the extra scope added by Sentiment AFTER the audit contest. This scope was only reviewed by WatchPug and relates to these three PRs:

1. [Lending deposit cap](https://github.com/sentimentxyz/protocol/pull/234)
2. [Fee accrual modification](https://github.com/sentimentxyz/protocol/pull/233)
3. [CRV staking](https://github.com/sentimentxyz/controller/pull/41)

Curve's gauge rewards cannot be claimed.

## Vulnerability Detail

The sole goal of `CurveLPStakingController` is to stake and earn rewards from Curve's gauge system.

However, it doesn't support `claim_rewards()`, and both `deposit()` or `withdraw()` are using the default value (`false`) for `_claim_rewards` parameter.

## Impact

Curve's gauge rewards cannot be claimed.

## Code Snippet
https://github.com/sentimentxyz/controller/blob/be4a7c70ecef788ca9226b46ff108ddd9001b14e/src/curve/CurveLPStakingController.sol#L20-L24

```solidity
/// @notice deposit(uint256)
bytes4 constant DEPOSIT = 0xb6b55f25;

/// @notice withdraw(uint256)
bytes4 constant WITHDRAW = 0x2e1a7d4d;
```

## Tool used

Manual Review

## Recommendation

Consider supporting claim_rewards(address,address) or using deposit(uint256,address,bool) and withdraw(uint256,address,bool) to support claim rewards when deposit() or withdraw().

## Sentiment Team
Fixed controller as recommended to claim gauge rewards and moved gauge token oracle into a separate contract instead. PR [here](https://github.com/sentimentxyz/oracle/pull/42).

## Lead Senior Watson
Confirmed fix.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 3/5 |
| Rarity Score | 3/5 |
| Audit Firm | Sherlock |
| Protocol | Sentiment |
| Report Date | N/A |
| Finders | WATCHPUG |

### Source Links

- **Source**: N/A
- **GitHub**: https://github.com/sherlock-audit/2022-08-sentiment-judging/tree/main/502-H
- **Contest**: https://app.sherlock.xyz/audits/contests/1

### Keywords for Search

`Business Logic`

