---
# Core Classification
protocol: Lido
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53467
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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
  - Hexens
---

## Vulnerability Title

[LID-20] Share rate can be negatively influenced due to shares burn limit

### Overview


A bug has been found in the PositiveTokenRebaseLimiter, which is responsible for limiting the increase of the StETH share rate in the positive direction. This bug affects the calculation of the shares burn limit, resulting in a conservative limit amount. This means that fewer shares are burned while the full ETH amount is locked for withdrawal claiming. This leads to a decrease in the share rate, resulting in discounted StETH and a temporary higher APR. This bug has been fixed by removing a specific calculation in the code.

### Original Finding Content

**Severity:** High

**Path:** PositiveTokenRebaseLimiter.sol:getSharesToBurnLimit#L119-L136

**Description:**

The PositiveTokenRebaseLimiter is responsible for limiting the increase of the StETH share rate in the positive direction. For example, if a lot of rewards come in from one oracle report, then the limiter would return how much ETH can be taken from the WithdrawalVault such that the share rate does not increase above the configured threshold.

In the testing environment, the default positive token rebase limit is set at 0.05%.

The PositiveTokenRebaseLimiter is also responsible for calculating the shares burn limit. For example, when a batch of withdrawal requests get finalised, the locked StETH shares have to be burned such that the withdrawer’s rewards get distributed among the stakers.

However, the calculation of the shares burn limit is skewed and will result in a conservative limit amount. 

First, Lido calls `smoothTokenRebase` on the OracleReportSanityChecker to calculate limits considering rewards and withdrawals.

This function first calculates the rewards limit, then it calls `raiseLimit` on the PositiveTokenRebaseLimiter with the total amount of ETH for finalisation of the withdrawal requests. This raises the limit for the full ETH amount to be locked for withdrawal claiming.

But instead of returning the corresponding share amount, `getSharesToBurnLimit` will use the following `x / (1 + x)` formula:

```
rebaseLimit = requestedETH / totalETH
sharesBurnLimit = totalShares * (rebaseLimit / (1 + rebaseLimit))
```

Less shares are burned, while the full ETH amount is locked for withdrawal claiming. As a result, the share rate decreases.

Taking the 0.05% standard rebase limit into account, the effects start to show at a batch of withdrawal requests containing ETH of 2% of the total pooled ETH. However, if there are also consensus/execution layer rewards claimed in the same oracle report (this consume some/all of the 0.05% standard limit), then the effects could start to show at any withdrawal amount.

The share rate would lower, resulting in discounted StETH. The burning remaining shares are postponed to be burned at a later oracle report, resulting in a temporary higher APR.

Due to this bug, it becomes profitable to perform large withdrawals, buy shares at a discounted rate and earn more APR.

```
function getSharesToBurnLimit(TokenRebaseLimiterData memory _limiterState)
    internal
    pure
    returns (uint256 maxSharesToBurn)
{
    if (_limiterState.rebaseLimit == UNLIMITED_REBASE) {
        return _limiterState.totalShares;
    }

    uint256 remainingRebase = _limiterState.rebaseLimit - _limiterState.accumulatedRebase;
    maxSharesToBurn = (
        _limiterState.totalShares * remainingRebase
    ) / (LIMITER_PRECISION_BASE + remainingRebase);
}
```

**Remediation:**  We would recommend to remove the remainingRebase from the denominator in PositiveTokenRebaseLimiter.sol:getSharesToBurnLimit (L119-136).

**Status:**  Fixed

- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Hexens |
| Protocol | Lido |
| Report Date | N/A |
| Finders | Hexens |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

