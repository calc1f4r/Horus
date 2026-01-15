---
# Core Classification
protocol: Fluid Protocol (Hydrogen Labs)
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46905
audit_firm: OtterSec
contest_link: https://fluidprotocol.xyz/
source_link: https://fluidprotocol.xyz/
github_link: https://github.com/Hydrogen-Labs/fluid-protocol

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
finders_count: 3
finders:
  - James Wang
  - Alpha Toure
  - Renato Eugenio Maria Marziano
---

## Vulnerability Title

Code Maturity

### Overview

See description below for full details.

### Original Finding Content

## Issues and Remediation

## 1. Incorrect Constant for Seconds in a Year

CommunityIssuance is incorrectly utilizing **31,104,000 seconds** as the number of seconds in a year for the `ONE_YEAR_IN_SECONDS` constant, which is approximately five days too short. This miscalculation may result in time-sensitive actions, such as reward distribution or contract transitions, being triggered earlier than intended, leading to less predictable issuance and distribution behaviors.

## 2. Allowing Less Stringent Minimum Requirements

Utilizing `>=` in `require_at_least_min_net_debt` and `require_at_least_mcr` will make the protocol slightly less strict, allowing borrowers to meet the minimum required debt or collateral ratio, instead of exceeding it by a small margin.

```sway
fn require_at_least_min_net_debt(_net_debt: u64) {
    require(
        _net_debt > MIN_NET_DEBT,
        "Borrow Operations: net debt must be greater than 0",
    );
}

fn require_at_least_mcr(icr: u64) {
    require(
        icr > MCR,
        "Borrow Operations: Minimum collateral ratio not met",
    );
}
```

## 3. TIMEOUT Constant in Oracle

In Oracle, the `TIMEOUT` constant (the period after which data fetched from the Pyth or Redstone oracles is considered stale) is currently set to four hours. However, Pyth provides real-time price updates with a high frequency, potentially every **400 milliseconds** (approximately **0.4 seconds**). This implies that Pyth price data may be refreshed multiple times per second. Redstone also provides fresh price data every few minutes. Thus, the `TIMEOUT` value may result in the utilization of outdated data for hours, even though new and more accurate prices are available.

## Remediation

1. Update the constant to the correct number of seconds in a year (**31,536,000**).
2. Modify the check in `require_at_least_min_net_debt` and `require_at_least_mcr` to utilize `>=` instead of `>`.
3. Reduce the `TIMEOUT` value to a shorter interval so that the system can ensure it uses fresher, more accurate prices from the oracles.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Fluid Protocol (Hydrogen Labs) |
| Report Date | N/A |
| Finders | James Wang, Alpha Toure, Renato Eugenio Maria Marziano |

### Source Links

- **Source**: https://fluidprotocol.xyz/
- **GitHub**: https://github.com/Hydrogen-Labs/fluid-protocol
- **Contest**: https://fluidprotocol.xyz/

### Keywords for Search

`vulnerability`

