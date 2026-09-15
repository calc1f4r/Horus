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
solodit_id: 53471
audit_firm: Hexens
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2023-04-14-Lido.md
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
  - Hexens
---

## Vulnerability Title

[LID-21] Withdrawals accrued rewards are not distributed among stakers

### Overview


The PositiveTokenRebaseLimiter is a function that calculates rewards and shares for withdrawal requests. However, there is a bug where the ratio used to calculate shares to be burned does not take into account any rewards accrued during the processing of the request. This means that rewards will not be divided among active stakers and could lead to profitable strategies for depositing after a large withdrawal. To fix this, it is recommended to immediately remove the ETH and shares from the total pool, and slowly add them back in afterwards. This has been fixed.

### Original Finding Content

**Severity:** Medium

**Path:** PositiveTokenRebaseLimiter.sol

**Description:**

The PositiveTokenRebaseLimiter calculates the rewards to be taken from the vaults and the amount of shares to be burned for withdrawal requests.

OracleReportSanityChecker initialises the PositiveTokenRebaseLimiter with the total pooled ETH and total shares at the moment of the oracle report. The shares to be burned are then calculated with a ratio of the total ETH in the withdrawal requests against the total pooled ETH.

For example:
```
sharesBurnLimit = (totalWithdrawalRequestETH / totalPooledETH) * totalShares
```
However, this total pooled ETH includes rewards that have been accrued during the processing of the withdrawal request, also the ETH in the withdrawal requests cannot be larger than the ETH value from when the requests were created which therefore will not include any rewards that would have been accrued.

As a result, the ratio that is calculated will never be higher than the current share rate and the shares that will be burned will always be less than the shares that have been locked during withdrawal request creation.

This means that any rewards accrued by the withdrawers will not be divided among the stakers that were active during the processing of the withdrawal request. Instead, the burning of the shares is postponed and the rewards will be divided among stakers that are active later.

This could give rise to profitable strategies were depositing after the finalisation of a large withdrawal gives higher APR.
```
TokenRebaseLimiterData memory tokenRebaseLimiter = PositiveTokenRebaseLimiter.initLimiterState(
    getMaxPositiveTokenRebase(),
    _preTotalPooledEther,
    _preTotalShares
);
```

**Remediation:**  If the distribution of the accrued rewards of withdrawal requests among stakers after finalisation of a withdrawal requests is not desired, then we would recommend to change this logic.

One possible solution could be to immediately remove the ETH from the total pooled ETH and the shares from the total shares. This would not impact the share rate and any subsequent rewards will be divided only among active shares. 

In the less likely scenario where the share rate drops after a withdrawal request, the withdrawer would only be able to claim the lower ETH amount after finalisation, just like now. The remaining ETH could be (slowly) added back to the total pooled ETH (or potentially used for finalisation of other withdrawal requests).

This solution is just to give an idea, any implementation would have to be reviewed thoroughly again.

**Status:**  Fixed



- - -

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
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

