---
# Core Classification
protocol: COSMOS Fundraiser Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 12114
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/cosmos-fundraiser-audit-7543a57335a4/
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

protocol_categories:
  - liquid_staking
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

Usage of blockchain.info API

### Overview


Blockchain.info is a service that has had issues in the past, and its nodes don't recognize OP_RETURN outputs as standard. To reduce the risk of fundraiser problems due to third-party service issues, the COSMOS team recommends running your own nodes of insight-api or bitcoin-abe and connecting to those. Insight-api and bitcoin-abe are both open-source software packages available on GitHub.

### Original Finding Content

blockchain.info has had problems in the past, and [as the COSMOS team mentions on this note](https://gist.github.com/mappum/428dc46afba73b2bf8c38f65272704d2#notes), their nodes don’t recognize OP\_RETURN outputs as standard. Consider running your own nodes of [insight-api](https://github.com/bitpay/insight-api) or [bitcoin-abe](https://github.com/bitcoin-abe/bitcoin-abe) and connecting to those, to reduce the risk of fundraiser problems because of third party problems.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | COSMOS Fundraiser Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/cosmos-fundraiser-audit-7543a57335a4/
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

