---
# Core Classification
protocol: Thala
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 48064
audit_firm: OtterSec
contest_link: https://www.thalalabs.xyz/
source_link: https://www.thalalabs.xyz/
github_link: https://github.com/ThalaLabs/thala-modules

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
finders_count: 4
finders:
  - Akash Gurugunti
  - Robert Chen
  - Ajay Kunapareddy
  - OtterSec
---

## Vulnerability Title

Configurable Simple Oracle Updater

### Overview

See description below for full details.

### Original Finding Content

## Oracle Module Overview

The oracle module employs a straightforward oracle that saves the price of a coin in a resource. The price of a coin, frequently updated by a protocol bot, may be utilized as a backup in the event of a failure of the Pyth or Switchboard oracles.

## Resource Updater

The resource updater, responsible for updating the coin price in the resource, is statically set in the move configuration file and is fixed at compile time.

## Remediation

Implement a configurable simple oracle updater address instead. The manager will then be able to update the address in the case of losing the updater private key.

## Patch

Fixed in `778e6ee` by implementing `configure_simple_oracle`.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OtterSec |
| Protocol | Thala |
| Report Date | N/A |
| Finders | Akash Gurugunti, Robert Chen, Ajay Kunapareddy, OtterSec |

### Source Links

- **Source**: https://www.thalalabs.xyz/
- **GitHub**: https://github.com/ThalaLabs/thala-modules
- **Contest**: https://www.thalalabs.xyz/

### Keywords for Search

`vulnerability`

