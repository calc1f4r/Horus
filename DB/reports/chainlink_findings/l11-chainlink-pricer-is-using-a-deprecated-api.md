---
# Core Classification
protocol: Opyn Gamma Protocol Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 11242
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/opyn-gamma-protocol-audit/
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
  - dexes
  - cdp
  - services
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

[L11] Chainlink pricer is using a deprecated API

### Overview

See description below for full details.

### Original Finding Content

The [Chainlink Pricer](https://github.com/opynfinance/GammaProtocol/pull/309/files) is currently using multiple functions from a [deprecated Chainlink API](https://docs.chain.link/docs/deprecated-aggregatorinterface-api-reference#gettimestamp) such as `latestAnswer()` in L61, `getTimestamp()` in L74. These functions might suddenly stop working if Chainlink stop supporting deprecated APIs.


Consider refactoring these to use the latest Chainlink API.

### Metadata

| Field | Value |
|-------|-------|
| Impact | LOW |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Opyn Gamma Protocol Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/opyn-gamma-protocol-audit/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

