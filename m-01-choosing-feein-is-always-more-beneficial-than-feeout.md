---
# Core Classification
protocol: Kekotron
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 31473
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Kekotron-security-review.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-01] Choosing FeeIn is always more beneficial than FeeOut

### Overview


This bug report discusses an issue where users are able to choose between two fee options, FeeIn and FeeOut, when making a swap. However, it has been found that choosing FeeIn always results in fewer fees for the user, and the difference becomes more significant as the size of the swap increases. This is because FeeIn means less funds are being swapped, resulting in less loss due to slippage. While this may seem beneficial for both the user and the protocol, it is also more beneficial for the FeeReceiver. The report suggests considering options such as only having one default fee option, adjusting the formula to make the two options identical, or leaving it as is and acknowledging the small difference.

### Original Finding Content

**Severity**

**Impact:** Low, the difference is very small for the majority of swaps

**Likelihood:** High, FeeIn can be chosen on every swap

**Description**

Users can choose between `FeeIn` (fee on tokenIn-amountIn), or choose `FeeOut` (fee on tokenOut-amountOut). If both alternatives are calculated it always happens that choosing `FeeIn` always results in fewer fees (the user receives more net amountOut).

Technically it happens because FeeIn means less funds to swap, and less loss due to slippage in the end.
The difference between the two options is becoming larger when the size of the swap grows (more slippage).

The difference between options is 0.5% for a swap of 100% of reserves, and 0.09% for 10% of reserves.

But, `FeeIn` is also more beneficial for FeeReceiver as the fee is taken before slippage and DEX fees.

As a result, `FeeIn` is always financially better for both the protocol and the user.

**Recommendations**

Consider some of the options:

1. leaving only FeeIn or only FeeOut as a default setup
2. adjust the formula so that the two options are identical
3. leaving as it is (and acknowledging the difference as neglectable)

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Kekotron |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Kekotron-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

