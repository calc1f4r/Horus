---
# Core Classification
protocol: blex.io
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 60061
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/blex-io/215a1fca-04f3-49f0-aa2a-9f3be6f89fdd/index.html
source_link: https://certificate.quantstamp.com/full/blex-io/215a1fca-04f3-49f0-aa2a-9f3be6f89fdd/index.html
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
finders_count: 4
finders:
  - Zeeshan Meghji
  - Cameron Biniamow
  - Roman Rohleder
  - Jonathan Mevs
---

## Vulnerability Title

Invalid Future Price May Be Used

### Overview


The Blex team has acknowledged an issue with their price updater server. The problem is related to the function that checks the timestamp for when the price is updated. This function allows for future timestamps to be used, which can cause incorrect prices to be set. This could lead to the protocol making incorrect decisions and potentially leaving the protocol in debt. The team recommends replacing the current check with a stricter one to prevent future timestamps from being used.

### Original Finding Content

**Update**
The Blex team acknowledged the issue. The team indicated that they use `_maxTimeDeviation` to perform a time deviation check between the price updater server and `block.timestamp`. We advise that `_maxTimeDeviation` should be a reasonably small value.

**File(s) affected:**`./contracts/oracle/FastPriceFeed.sol`

**Description:** The internal function `_setLastUpdatedValues()` performs a few important checks on the `_timestamp` for which the price is updated. In particular, two checks that attempt to ensure that the `_timestamp` falls within the `_maxTimeDeviation` on either side of the current time. However, one of these checks allows for future `_timestamp` values to be used:

```
require(
    _timestamp < block.timestamp + _maxTimeDeviation,
    "FastPriceFeed: _timestamp exceeds allowed range"
);
```

The check would only fail if `_timestamp` is more than `_maxTimeDeviation` seconds in the future. However, it never makes sense to set a price in the future as it is not possible to reliably predict the price in advance. Thus, any `_timestamp` value in the future should be disallowed. If an off-chain bug in the price updater results in an incorrect price being set for the future, the protocol may use the wrong prices for collateral and debt assets.

As a result, the protocol could fail to liquidate unhealthy positions or prematurely liquidate healthy positions, leaving the protocol in debt.

**Recommendation:** Replace the `_timestamp < block.timestamp + _maxTimeDeviation` check with `_timestamp <= block.timestamp`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | blex.io |
| Report Date | N/A |
| Finders | Zeeshan Meghji, Cameron Biniamow, Roman Rohleder, Jonathan Mevs |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/blex-io/215a1fca-04f3-49f0-aa2a-9f3be6f89fdd/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/blex-io/215a1fca-04f3-49f0-aa2a-9f3be6f89fdd/index.html

### Keywords for Search

`vulnerability`

