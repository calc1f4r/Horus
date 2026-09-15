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
solodit_id: 46443
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

Potential read-only entrancy pattern if external protocol read the share state from the Earn- Vault 

### Overview


This bug report is about a potential vulnerability in the code for the Vault#withdraw function. The code updates the state after an external call, which could potentially lead to a reentrancy attack. This type of attack has been seen before in other projects and the report recommends implementing a read-only reentrancy check to prevent it. The bug has been fixed in a recent pull request and has been deemed low risk.

### Original Finding Content

## Security Assessment Report

## Context
(No context files were provided by the reviewer)

## Description
In the `Vault#withdraw` function, the code updates the state after an external call (see `Earn-Vault.sol#L293`):

```solidity
withdrawalTypes = strategy.withdraw({
  positionId: positionId,
  tokens: tokensToWithdraw,
  toWithdraw: withdrawn,
  recipient: recipient
});
// slither-disable-next-line unused-return
(, uint256[] memory balancesAfterUpdate) = strategy.totalBalances();
_updateAccounting({
```

The withdraw function and all functions in Vault are certainly guarded by a `nonReentrant` modifier; this pattern is set up for read-only reentrancy.

- Sentiment's hackmd shows an example of such a hack caused by balancer read-only reentrancy.
- Quillaudits also shows an example of such a hack caused by curve read-only reentrancy.

## Recommendation
At least if there is any external integration that reads share values from the earn vault, they should be aware that this read-only reentrancy vector exists.

Balancer adds a read-only reentrancy check (see `VaultReentrancyLib.sol#L19`) when calling the view-related function; a similar pattern can be followed.

### Status
- **Balmy**: Fixed in PR 78.
- **Cantina Managed**: Fix looks good.

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

