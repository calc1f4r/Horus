---
# Core Classification
protocol: Convergent
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 47154
audit_firm: OtterSec
contest_link: https://convergent.so/
source_link: https://convergent.so/
github_link: https://github.com/Convergent-Finance/v1-contracts

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
  - Kevin Chow
  - Robert Chen
---

## Vulnerability Title

Extended Utilization Of Stale Data

### Overview


This bug report discusses an issue with the PriceFeedState::update function, which currently always returns the last good price. However, if both oracles are broken or untrusted, there is a risk that this price may be outdated. This can lead to incorrect or sub-optimal decisions being made by the system. The report suggests implementing fallback actions when both oracles are broken, such as pausing trading and alerting users. The issue has been acknowledged by the Convergent team and a patch is being worked on. 

### Original Finding Content

## Current State of PriceFeed

Currently, `PriceFeedState::update` returns the `last_good_price` every time. However, if the `last_good_price` is returned when both oracles are broken or untrusted, there is a risk that this price might be outdated. Thus, if the oracles are down for an extended period and the system continues to utilize the last good price, the system may rely on this price long after the failure. Over time, the market price may diverge significantly from this stale value, resulting in incorrect or sub-optimal decisions based on the outdated price.

> _price_feed_state.rs_ untrusted
> [...]
> // --- CASE 5: Using Pyth, Chainlink is untrusted ---
> Status::UsingPythChainlinkUntrusted => {
> // If Pyth breaks, now both oracles are untrusted
> if is_pyth_broken(pyth_price_message) {
> self.set_status(Status::BothOraclesUntrusted);
> return Ok(self.last_good_price);
> }
> // If Pyth is frozen, return last good price (no status change)
> if is_pyth_frozen(pyth_price_message) {
> return Ok(self.last_good_price);
> }
> [...]
> }

## Remediation

Instead of relying solely on `last_good_price`, implement fallback actions when both oracles are broken. These actions may involve pausing trading and alerting users.

## Patch

Acknowledged by the Convergent team.  
© 2024 Otter Audits LLC. All Rights Reserved. 11/19

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Convergent |
| Report Date | N/A |
| Finders | Kevin Chow, Robert Chen |

### Source Links

- **Source**: https://convergent.so/
- **GitHub**: https://github.com/Convergent-Finance/v1-contracts
- **Contest**: https://convergent.so/

### Keywords for Search

`vulnerability`

