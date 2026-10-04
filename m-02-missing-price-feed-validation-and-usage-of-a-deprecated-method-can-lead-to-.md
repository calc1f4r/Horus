---
# Core Classification
protocol: Bloom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20596
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-05-01-Bloom.md
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

[M-02] Missing price feed validation and usage of a deprecated method can lead to 0 price

### Overview


This bug report is about a potential problem with the `SwapFacility` method in Chainlink price feeds. The issue is that the `latestAnswer` NatSpec says it will return 0 if no answer has been reached, which could lead to miscalculations in the rate of `underlyingToken` to `billyToken`, resulting in a loss of funds. The impact of this bug is high as it would mess up the swap calculations, however, the likelihood of it occurring is low as it requires a malfunctioning price feed. The recommendation is to use `latestRoundData` instead to query a price feed, which includes better verification information.

### Original Finding Content

**Impact:**
High, as using a 0 price would mess the swap calculations

**Likelihood:**
Low, as it requires a malfunctioning price feed

**Description**

The `_getTokenPrices` method in `SwapFacility` makes use of the `latestAnswer` method from Chainlink price feeds. The problem is that the NatSpec of `latestAnswer` says this:

> @dev #[deprecated] Use latestRoundData instead. This does not error if no
> answer has been reached, it will simply return 0. Either wait to point to
> an already answered Aggregator or use the recommended latestRoundData
> instead which includes better verification information.```

So currently it is possible that `latestAnswer` returns 0 and the code operates with zero price, leading to miscalculations in the rate of `underlyingToken` to `billyToken` which will lead to a loss of funds.

**Recommendations**

As pointed out in the comment, use `latestRoundData` instead to query a price feed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Bloom |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-05-01-Bloom.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

