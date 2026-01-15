---
# Core Classification
protocol: Exponent Generic Standard
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 53212
audit_firm: OtterSec
contest_link: https://www.exponent.finance/income
source_link: https://www.exponent.finance/income
github_link: https://github.com/exponent-finance/exponent-core

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
  - Ajay Shankar Kunapareddy
  - Robert Chen
---

## Vulnerability Title

Improper Handling of Negative Fluctuation

### Overview


The code has a problem with handling negative changes in exchange rates when comparing the new rate to the current index. This is due to an error in the way the Pyth price feed is used to retrieve the latest price in the Utils::get_index function. The current logic allows for negative changes above the confidence interval, which should be ignored. A fix for this issue has been implemented in patch #1915.

### Original Finding Content

## Issue Summary

The issue lies in the way the code handles negative fluctuations in the exchange rate when comparing the `new_exchange_rate` to the `current_index`. Specifically, when utilizing the Pyth price feed to retrieve the latest price in `Utils::get_index`, the check for ignoring negative fluctuations within the confidence interval is incorrect. Negative fluctuations that are within the confidence interval should be ignored, but the current logic accepts negative fluctuations even if they are above the confidence interval.

## Code Snippet

```rust
pub fn get_index<'a>(meta: &SyMeta, remaining_accounts: &'a [AccountInfo]) -> Result<Number> {
    match meta.interface_type {
        InterfaceType::Pyth => {
            [...]
            // The price account has very small negative fluctuations of less than 2 price units
            // because of publishers that post slightly outdated indices.
            // Ignore negative fluctuations as long as they are within confidence interval,
            // which is very tight for redemption index feeds.
            if new_exchange_rate < current_index
                && current_index.checked_sub(&new_exchange_rate).unwrap() > conf_interval
            {
                return Ok(current_index);
            }
            Ok(new_exchange_rate)
            [...]
        }
    }
}
```

## Remediation

Update the comparison to ensure that negative fluctuations are below the confidence interval.

## Patch

Resolved in #1915.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Exponent Generic Standard |
| Report Date | N/A |
| Finders | Ajay Shankar Kunapareddy, Robert Chen |

### Source Links

- **Source**: https://www.exponent.finance/income
- **GitHub**: https://github.com/exponent-finance/exponent-core
- **Contest**: https://www.exponent.finance/income

### Keywords for Search

`vulnerability`

