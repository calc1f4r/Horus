---
# Core Classification
protocol: Coinbase
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 40939
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/e0617560-04c7-4591-8e64-31c642408403
source_link: https://cdn.cantina.xyz/reports/cantina_coinbase_nov2023.pdf
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
  - Liam Eastwood
  - Anurag Jain
  - Jonatas Martins
---

## Vulnerability Title

Sanity check on Refund destination is missing 

### Overview

See description below for full details.

### Original Finding Content

## Transfers.sol

## Description
For an intent to be valid, `_intent.refundDestination` should not be `address(0)`. The same check could be placed in this function.

## Recommendation
Add a new check to revert on incorrect refund destination:
```solidity
if (_intent.refundDestination == address(0)) {
    revert NullRefundDestination(); // define this new event
}
```

## Coinbase
Related to the issue "refundDestination cannot be configured", this is okay since the refund destination is purely informational. If it's the zero address, then the merchant should assume the sender address is okay to send a refund to. We'll make this clear once we start using that field in our product (we currently don't surface it). Nothing needed for this one.

## Cantina Managed
Acknowledged.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Coinbase |
| Report Date | N/A |
| Finders | Liam Eastwood, Anurag Jain, Jonatas Martins |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_coinbase_nov2023.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/e0617560-04c7-4591-8e64-31c642408403

### Keywords for Search

`vulnerability`

