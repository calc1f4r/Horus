---
# Core Classification
protocol: Lumin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27237
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Lumin.md
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
  - Pashov
---

## Vulnerability Title

[M-03] Price feed oracle data validation is missing

### Overview


This bug report is about validating the price feed data in `PriceFeedProxyChainlink`. When the code doesn't revert when `intPrice == 0`, and price staleness is not checked, it can lead to unfair loans/liquidations. The `GRACE_PERIOD` after a sequencer was down is also not waited.

To fix this issue, the code should be changed to `if (intPrice <= 0) { revert ImplausiblePrice(); }`, and the timestamp value of the `latestRoundData` call should be checked to make sure it hasn't been longer than the heartbeat interval for the price feed (plus 10-30 minutes buffer period). Partially fixed, excluding the price staleness check.

### Original Finding Content

**Severity**

**Impact:**
High, as it can possibly result in unfair liquidations

**Likelihood:**
Low, as it only happens in specific rare conditions

**Description**

There are multiple problems when validating the price feed data in `PriceFeedProxyChainlink`:

- the code doesn't revert when `intPrice == 0`
- price staleness is not checked
- the `GRACE_PERIOD` after a sequencer was down is not waited

Using an incorrect price can be detrimental for the protocol as it can lead to unfair loans/liquidations.

**Recommendations**

For the sequencer `GRACE_PERIOD` make sure to follow the [Chainlink docs](https://docs.chain.link/data-feeds/l2-sequencer-feeds#example-code). Also iplement the following change:

```diff
- if (intPrice < 0) {
+ if (intPrice <= 0) {
    revert ImplausiblePrice();
}
```

Finally, check the timestamp value of the `latestRoundData` call and make sure it hasn't been longer than the heartbeat interval for the price feed (plus 10-30 minutes buffer period).

**Discussion**

**pashov:** Partially fixed, excluding the price staleness check.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Lumin |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-09-01-Lumin.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

