---
# Core Classification
protocol: ReyaNetwork-August
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 41128
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-August.md
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

[M-03] Confidence interval of Pyth price is not validated

### Overview


The PythOffchainLookupNode is not properly checking the confidence interval of the Pyth price, which can lead to untrusted prices being accepted. This is a high impact bug with a low likelihood of occurring. To fix this, the `minConfidenceRatio` value should be added as a parameter, global configuration, or constant in the contract. It's important to note that a confidence interval of 0 should still be considered a valid price.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

`PythOffchainLookupNode.process` does not validate the confidence interval of the Pyth price.

As stated in the [Pyth documentation](https://docs.pyth.network/price-feeds/best-practices#confidence-intervals), it is important to check this value to prevent the contract from accepting untrusted prices.

## Recommendations

```diff
+       if (latestPrice.conf > 0 && (latestPrice.price / int64(latestPrice.conf) < minConfidenceRatio)) {
+           revert LowConfidencePyth(latestPrice.price, latestPrice.conf, oracleAdaptersProxy);
+       }
```

The `minConfidenceRatio` value could be an additional parameter for Pyth nodes, a global configuration or a constant in the contract.

Note that a confidence interval of 0 means no spread in price, so should be considered as a valid price.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | ReyaNetwork-August |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/ReyaNetwork-security-review-August.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

