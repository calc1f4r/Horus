---
# Core Classification
protocol: Venus Protocol
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20781
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2023-05-venus
source_link: https://code4rena.com/reports/2023-05-venus
github_link: https://github.com/code-423n4/2023-05-venus-findings/issues/122

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
  - lanrebayode77
  - SaeedAlipoor01988
---

## Vulnerability Title

[M-12] Fix utilization rate computation

### Overview


This bug report is about the `BaseJumpRateModelV2.sol#L131.utilizationRate()` function which is designed to return a value between 0 and 1e18. However, the system does not guarantee that reserves never exceed cash, which can lead to the function returning a value above 1. The recommended mitigation step for this bug is to make the utilization rate computation return 1 if reserves > cash. This bug is of the type Math.

### Original Finding Content


The `BaseJumpRateModelV2.sol#L131.utilizationRate()` function can return a value above 1 and not between [0, BASE].

### Proof of Concept

In the `BaseJumpRateModelV2.sol#L131.utilizationRate()` function, cash and borrows and reserves values get used to calculate the utilization rate between [0, 1e18]. Reserves are currently unused but it will be used in the future.

     */
    function utilizationRate(
        uint256 cash,
        uint256 borrows,
        uint256 reserves
    ) public pure returns (uint256) {
        // Utilization rate is 0 when there are no borrows
        if (borrows == 0) {
            return 0;
        }

        return (borrows * BASE) / (cash + borrows - reserves);
    }

If the borrow value is 0, then the function will return 0, but in this function, the scenario where the value of reserves exceeds cash is not handled. The system does not guarantee that reserves never exceed cash. The reserves grow automatically over time, so it might be difficult to avoid this entirely.

If reserves > cash (and borrows + cash - reserves > 0), the formula for `utilizationRate` above gives a utilization rate above 1.

### Recommended Mitigation Steps

Make the utilization rate computation return 1 if reserves > cash.

### Assessed type

Math

**[chechu (Venus) confirmed](https://github.com/code-423n4/2023-05-venus-findings/issues/122#issuecomment-1560092307)**
***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Venus Protocol |
| Report Date | N/A |
| Finders | lanrebayode77, SaeedAlipoor01988 |

### Source Links

- **Source**: https://code4rena.com/reports/2023-05-venus
- **GitHub**: https://github.com/code-423n4/2023-05-venus-findings/issues/122
- **Contest**: https://code4rena.com/reports/2023-05-venus

### Keywords for Search

`vulnerability`

