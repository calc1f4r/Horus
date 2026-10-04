---
# Core Classification
protocol: Balmy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46442
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/d365c977-e13a-41e2-84e3-67083ecbc362
source_link: https://cdn.cantina.xyz/reports/antina_balmy_november2024.pdf
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
finders_count: 2
finders:
  - Blockdev
  - ladboy233
---

## Vulnerability Title

User can pass in zero underlying token amount and non-zero reward amount to bypass the fee accumulation 

### Overview


This bug report discusses an issue with a protocol that charges a performance fee on a base underlying asset and a reward token. The problem occurs when a user tries to withdraw an amount between 0 and 100. In this case, the fee for the reward token is skipped because no fee is charged when the underlying token is 0. The report suggests a fix for this issue and mentions that it has already been addressed in a pull request.

### Original Finding Content

## Context
(No context files were provided by the reviewer)

## Description
If the strategy has token A as base underlying asset, and token B as reward token, the protocol wants to charge performance fee both on the yield part of the underlying asset and the reward token balance.

However, if a user passes in a withdraw amount [0, 100], the withdrawal fee (see `ExternalFees.sol#L207`) for the reward token will be skipped because when the first token (underlying token) is 0, no fee will be charged nor accumulated.

```solidity
(, uint256[] memory currentBalances) = _fees_underlying_totalBalances();
for (uint256 i; i < tokens.length; ++i) {
    // If there is nothing being withdrawn, we can skip fee update, since balance didn't change
    if (toWithdraw[0] == 0) continue;
    if (toWithdraw[i] == 0) continue;
}
```

## Recommendation
Balmy: Fixed in PR 131.

Cantina Managed: Fix looks good.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Balmy |
| Report Date | N/A |
| Finders | Blockdev, ladboy233 |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/antina_balmy_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/d365c977-e13a-41e2-84e3-67083ecbc362

### Keywords for Search

`vulnerability`

