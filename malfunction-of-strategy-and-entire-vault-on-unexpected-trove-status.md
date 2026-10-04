---
# Core Classification
protocol: Yearn Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 28428
audit_firm: MixBytes
contest_link: none
source_link: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/Liquity%20Stability%20Pool/README.md#2-malfunction-of-strategy-and-entire-vault-on-unexpected-trove-status
github_link: none

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
finders_count: 1
finders:
  - MixBytes
---

## Vulnerability Title

Malfunction of strategy and entire vault on unexpected trove status

### Overview


This bug report is about a *liquity trove* which can be in one of several states: *nonExistent, active, closedByOwner, closedByLiquidation, closedByRedemption*. When the *trove* is in a state different than *active*, any call to *ajdustTrove()* will fail. The bug report highlights that the strategy does not implement proper handling of trove state, which can cause the trove to be in an unexpected state. This can be caused by liquidation, full collaterial redemption and manual closing by a privileged user.

The *_deposit()* function is expected to be in two states: *zero* (which is *nonExistent*) and other (which is *active, closedByOwner, closedByLiquidation, closedByRedemption*). However, only *active* state is valid for *adjustTrove*, other three states will cause a revert. The *liquidatePosition()* function does not handle the trove state either, which will cause a revert on the *adjustTrove()* call. This can break the harvest() and withdraw() functions, making the strategy broken and preventing any withdrawals from the vault.

To fix this issue, it is recommended to handle the state of the trove properly.

### Original Finding Content

##### Description
A *liquity trove* can be in one of several states: *nonExistent, active, closedByOwner, closedByLiquidation, closedByRedemption*. When the *trove* is in state different than *active*, any call to *ajdustTrove()* will fail. Unfortunately, the strategy does not implement proper handling of trove state. There is some scenarios that will cause trove to be in unexpected state: trove liquidation, full collaterial redemption and trove manual *[closing](https://github.com/orbxball/liquity-stability-pool/blob/c3fa76af0a4e2d5fd7132b8e24361d5b7439a75d/contracts/Strategy.sol#L374)* by priveleged user.

The [*_deposit()*](https://github.com/orbxball/liquity-stability-pool/blob/c3fa76af0a4e2d5fd7132b8e24361d5b7439a75d/contracts/Strategy.sol#L216) function is expected only two states: *zero* (which is *nonExistent*) and other (which is *active, closedByOwner, closedByLiquidation, closedByRedemption*). However, only *active* state is valid for *[adjustTrove](https://github.com/orbxball/liquity-stability-pool/blob/c3fa76af0a4e2d5fd7132b8e24361d5b7439a75d/contracts/Strategy.sol#L237)*, other three states will cause revert.

The *[liquidatePosition()](https://github.com/orbxball/liquity-stability-pool/blob/c3fa76af0a4e2d5fd7132b8e24361d5b7439a75d/contracts/Strategy.sol#L307)* function does not handle trove state. When trove is in any state except *active*, *liquidatePosition()* will revert on *[adjustTrove()](https://github.com/orbxball/liquity-stability-pool/blob/c3fa76af0a4e2d5fd7132b8e24361d5b7439a75d/contracts/Strategy.sol#L322)* call. This will break harvest() and withdraw() functions so strategy will become broken and should be manually removed from the vault to prevent blocking of any withdrawal from it.

##### Recommendation
It is recommended to handle state of the trove properly.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | MixBytes |
| Protocol | Yearn Finance |
| Report Date | N/A |
| Finders | MixBytes |

### Source Links

- **Source**: https://github.com/mixbytes/audits_public/blob/master/Yearn%20Finance/Liquity%20Stability%20Pool/README.md#2-malfunction-of-strategy-and-entire-vault-on-unexpected-trove-status
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

