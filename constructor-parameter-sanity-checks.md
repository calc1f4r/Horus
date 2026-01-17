---
# Core Classification
protocol: Global Messaging Token Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 12001
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/global-messaging-token-audit-865e6a821cd8/
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

protocol_categories:
  - liquid_staking
  - cdp
  - services
  - payments
  - oracle

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Constructor parameter sanity checks

### Overview

See description below for full details.

### Original Finding Content

Consider performing sanity checks to validate `GMToken`’s [constructor parameters](https://github.com/MercuryProtocol/global-messaging-token-contracts/blob/d0765cbd0732453832455dae0e2cf892da1ab572/contracts/Tokens/GMToken.sol#L99-L102). Check that `_startBlock &lt; _endBlock`.


***Update:** Fixed in the latest version.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Global Messaging Token Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/global-messaging-token-audit-865e6a821cd8/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

