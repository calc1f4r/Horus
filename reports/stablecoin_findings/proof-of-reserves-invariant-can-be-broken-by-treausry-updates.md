---
# Core Classification
protocol: vusd-stablecoin
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 61775
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
source_link: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
github_link: none

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
  - Paul Clemson
  - Leonardo Passos
  - Tim Sigl
---

## Vulnerability Title

Proof of Reserves Invariant Can Be Broken by Treausry Updates

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> Planned to fix it in future release of treasury contract

**File(s) affected:**`VUSD.sol`

**Description:** Description: From the VUSD documentation, it says:

> VUSD is open source, designed for simplicity and security, peg stability, self-sustaining, backed by over-collateralized, yield-generating cryptocurrencies. VUSD is fully auditable on-chain, with real-time proof of reserves available at all times.

Having a proof of reserve means that all VUSD should be backed by at least the corresponding amount in USD, as given the collateral assets in the treasury.

This invariant, however, is not enforced in `VUSD.updateTreasury()`. Hence, a malicious governor may set a new treasury with no matching reserve to back the value of all the VUSD in circulation.

**Recommendation:** In the `updateTreasury()` function, check that the new treasury holds enough collateral to back the value of all the VUSD current supply.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | vusd-stablecoin |
| Report Date | N/A |
| Finders | Paul Clemson, Leonardo Passos, Tim Sigl |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/vusd-stablecoin/f4e8fad4-3c79-4e7b-b0f3-260ef5f0acf6/index.html

### Keywords for Search

`vulnerability`

