---
# Core Classification
protocol: Nabla
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36531
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nabla-security-review.md
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

[M-01] Pyth oracle price is not validated properly

### Overview


Severity: High

Impact: This bug can cause the contract to accept invalid or untrusted prices.

Likelihood: Low

Description: The function `PythAdapter.getAssetPrice` does not check the values for `price`, `conf`, and `expo`, which can lead to the contract accepting incorrect prices. This is especially concerning for the `conf` value, which is used to determine the confidence interval of the price. If this value is not validated, the contract may accept untrusted prices.

Recommendations: The code needs to be updated to include validation for the `price`, `conf`, and `expo` values. The suggested changes include checking for a negative or zero `price` and ensuring that the `expo` value is not less than -18. Additionally, the code should also check if the `conf` value is greater than 0 and if the `price` divided by the `conf` value is less than a specified minimum confidence ratio. These changes will help prevent the contract from accepting invalid or untrusted prices.

### Original Finding Content

**Severity**

**Impact:** High

**Likelihood:** Low

**Description**

`PythAdapter.getAssetPrice` does not perform input validation on the `price`, `conf`, and `expo` values, which can lead to the contract accepting invalid or untrusted prices.

It is especially important to validate the confidence interval, as stated in the [Pyth documentation](https://docs.pyth.network/price-feeds/best-practices#confidence-intervals), to prevent the contract from accepting untrusted prices.

**Recommendations**

```diff
-       (int64 price, int32 expo) = (
+       (int64 price, uint64 conf, int32 expo) = (
            pythStructsPrice.price,
+           pythStructsPrice.conf,
            pythStructsPrice.expo
        );

+       if (price <= 0 || expo < -18) {
+           revert("PA:getAssetPrice:INVALID_PRICE");
+       }
+
+       if (conf > 0 && (price / int64(conf) < MIN_CONFIDENCE_RATIO)) {
+           revert("PA:getAssetPrice:UNTRUSTED_PRICE");
+       }
```

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nabla |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nabla-security-review.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

