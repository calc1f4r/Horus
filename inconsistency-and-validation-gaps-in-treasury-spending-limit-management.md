---
# Core Classification
protocol: Primex Finance
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59052
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html
source_link: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html
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
finders_count: 4
finders:
  - Jennifer Wu
  - Andy Lin
  - Adrian Koegl
  - Hytham Farah
---

## Vulnerability Title

Inconsistency and Validation Gaps in Treasury Spending Limit Management

### Overview

See description below for full details.

### Original Finding Content

**Update**
In the commits `c80e9ed` and `42f4e7a`, we reviewed that most recommended validations are applied. The `isSpenderExist` validation is applied in other commits but already shown in those two commits. The only validation missing is `minTimeBetweenTransfers` and we assume that the team would like to have the ability to have it be zero.

The `setMaxSpendingLimit` has been changed from a medium to a large time-lock along with the mentioned commit(s), although this change is not directly related to the fix.

**File(s) affected:**`Treasury.sol`

**Description:** The current structure of the `Treasury.setMaxSpendingLimit()` and `Treasury.decreaseLimits()` functions, crucial for managing the treasury spending, exhibit inconsistencies and lack the necessary validation checks.

The `setMaxSpendingLimit()` function allows the `Treasury` to add a new spender address with spending limits or update existing limits. This function does not validate the `_newSpendingLimits` used and but the function is locked behind a `MEDIUM_TIMELOCK_ADMIN`. Although the function name implies modifying the maximum spending limits for a spender, the implementation allows any data in `SpendingInfo.limits` to be updated for new and existing spenders.

The `Treasury.decreaseLimits()` function allows `Treasury` to update the spending limits of existing spenders. This function validates that the new limits are decreased and time durations are increased. However, the function does not validate the existence of the spender address. This lack of validation could allow for unintentional increases in the time duration for non-existent spenders in the `spenders` mapping.

The following input validations are recommended, but not limited to:

1.   When adding or updating spending limits for a spender address,
    1.   `maxTotalAmount` should exceed zero,
    2.   `maxAmountPerTransfer` should exceed zero,
    3.   `maxPercentPerTransfer` should be less than `WAD` or reasonably bounded,
    4.   `minTimeBetweenTransfers` should exceed zero or reasonably bounded,
    5.   `maxAmountDuringTimeFrame` should exceed zero or reasonably bounded.

2.   When decreasing spending limits for a spender address,
    1.   `isSpenderExist` should be validated,

**Recommendation:** We recommend introducing more input validations when adding a new spender address or updating existing spending limits. Furthermore, depending on the treasury's use case, consider adding a function to deactivate existing spenders and track the total spendings of spenders.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Primex Finance |
| Report Date | N/A |
| Finders | Jennifer Wu, Andy Lin, Adrian Koegl, Hytham Farah |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/primex-finance/179ad629-f166-493b-ad06-16ebf80054af/index.html

### Keywords for Search

`vulnerability`

