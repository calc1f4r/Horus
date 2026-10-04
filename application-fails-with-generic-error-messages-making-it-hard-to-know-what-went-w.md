---
# Core Classification
protocol: Open Dollar - dApp
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 59515
audit_firm: Quantstamp
contest_link: https://certificate.quantstamp.com/full/open-dollar-d-app/f0ff4333-535d-4de6-96e0-8573623c18bf/index.html
source_link: https://certificate.quantstamp.com/full/open-dollar-d-app/f0ff4333-535d-4de6-96e0-8573623c18bf/index.html
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
finders_count: 2
finders:
  - Pavel Shabarkin
  - Mostafa Yassin
---

## Vulnerability Title

Application Fails with Generic Error Messages Making It Hard to Know What Went Wrong

### Overview

See description below for full details.

### Original Finding Content

**Update**
Marked as "Acknowledged" by the client. The client provided the following explanation:

> The Open Dollar application’s back end is composed completely of Solidity smart contracts. Calling functions in the application usually involves delegatecall and proxy contracts, making it easy for a failure to occur when estimating the gas cost of the transaction, but making it difficult to debug these errors without using advanced developer tools. The Open Dollar team continues to create strong front-end validation to prevent errors on the smart contract level from occurring.

**Description:** Occasionally, the application will return a generic error to the user stating that the transaction failed. This does not provide the user with any knowledge about what went wrong; this negatively affects the user experience.

**Recommendation:** Consider returning meaningful errors to the user.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Quantstamp |
| Protocol | Open Dollar - dApp |
| Report Date | N/A |
| Finders | Pavel Shabarkin, Mostafa Yassin |

### Source Links

- **Source**: https://certificate.quantstamp.com/full/open-dollar-d-app/f0ff4333-535d-4de6-96e0-8573623c18bf/index.html
- **GitHub**: N/A
- **Contest**: https://certificate.quantstamp.com/full/open-dollar-d-app/f0ff4333-535d-4de6-96e0-8573623c18bf/index.html

### Keywords for Search

`vulnerability`

