---
# Core Classification
protocol: EigenLayer
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53562
audit_firm: SigmaPrime
contest_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
source_link: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
github_link: none

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
  - Sigma Prime
---

## Vulnerability Title

Completing Queued Withdrawal Can Result In Revert When sharesToWithdraw Is Zero

### Overview

See description below for full details.

### Original Finding Content

## Description

The _completeQueuedWithdrawal() function does not handle scenarios where `sharesToWithdraw = 0`, which can cause issues with ERC-20 tokens that do not support zero-value transfers.

When `receiveAsTokens = true`, the `StrategyManager.withdrawSharesAsTokens()` function is called to withdraw tokens from the strategy. This poses a problem for ERC-20 implementations that explicitly prohibit zero-value transfers, as `sharesToWithdraw = 0` in cases where the operator is fully slashed during the withdrawal delay period.

```solidity
DelegationManager.sol::_completeQueuedWithdrawal()
// @audit this is zero when prevSlashingFactors[i] is zero
uint256 sharesToWithdraw = SlashingLib.scaleForCompleteWithdrawal({
    scaledShares: withdrawal.scaledShares[i],
    slashingFactor: prevSlashingFactors[i]
});
if (receiveAsTokens) {
    // @audit this will revert for tokens that do not support zero-value transfers
    // if sharesToWithdraw = 0
    shareManager.withdrawSharesAsTokens({
        staker: withdrawal.staker,
        strategy: withdrawal.strategies[i],
        token: tokens[i],
        shares: sharesToWithdraw
    });
}
```

When `receiveAsTokens = false`, the `StrategyManager.addShares()` function is called to add shares back to the strategy. However, the `StrategyManager._addShares()` function does not allow for zero-value shares to be added, and hence will also revert.

The actual impact is rated high, as it would cause the staker’s tokens in other strategies associated with the queued withdrawal to be permanently stuck. However, the likelihood of this issue is rated low, as it requires an ERC-20 token that does not support zero-value transfers and the operator to become fully slashed during the cooldown period.

This issue is rated as informational severity in the report, as it was discovered by the EigenLayer team during the engagement.

## Recommendations

Consider adding a check to ensure `sharesToWithdraw != 0` before performing the withdrawal. If `sharesToWithdraw = 0`, the withdrawal should be completed without withdrawing any tokens.

## Resolution

The EigenLayer team has added a check to skip calling `SharesManager` if `sharesToWithdraw = 0` as recommended above. This issue has been resolved in PR #1019.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | SigmaPrime |
| Protocol | EigenLayer |
| Report Date | N/A |
| Finders | Sigma Prime |

### Source Links

- **Source**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf
- **GitHub**: N/A
- **Contest**: https://github.com/sigp/public-audits/blob/master/reports/eigenlayer/Sigma_Prime_Layr_Labs_EigenLayer_Slashing_Security_Assessment_Report_v2_0.pdf

### Keywords for Search

`vulnerability`

