---
# Core Classification
protocol: Origin OETH Integration Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 33091
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/origin-oeth-integration-audit
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

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - OpenZeppelin
---

## Vulnerability Title

Data feeds may be outdated

### Overview


The bug report is about a discrepancy between the recommended validation process for prices returned by Chainlink's feeds and the actual validation process used in two specific contracts, OracleRouterBase and OETHOracleRouter. This discrepancy could potentially cause issues with the pricing of OUSD and OETH tokens. However, the bug has been resolved in a recent pull request.

### Original Finding Content

[Chainlink's documentation](https://docs.chain.link/data-feeds/#monitoring-data-feeds) recommends validating that prices returned by their feeds are recent and fall within reasonable bounds. The `price` function of the [`OracleRouterBase`](https://github.com/OriginProtocol/origin-dollar/blob/508921bd39f988fa61b60cea372b910725ff7bd0/contracts/contracts/oracle/OracleRouter.sol#L40) and the [`OETHOracleRouter`](https://github.com/OriginProtocol/origin-dollar/blob/508921bd39f988fa61b60cea372b910725ff7bd0/contracts/contracts/oracle/OracleRouter.sol#L148) contracts do not validate these properties directly, although the vault [independently requires](https://github.com/OriginProtocol/origin-dollar/blob/508921bd39f988fa61b60cea372b910725ff7bd0/contracts/contracts/vault/VaultCore.sol#L696-L697) the price to be within 30% of the expected value. In addition, consider confirming the [`updatedAt` parameter](https://docs.chain.link/data-feeds/api-reference#latestrounddata) is suitably recent to ensure users can mint and redeem OUSD and OETH tokens at a reasonable market price.


***Update:** Resolved in [pull request #1491](https://github.com/OriginProtocol/origin-dollar/pull/1491) at commit [9cc9626](https://github.com/OriginProtocol/origin-dollar/pull/1491/commits/9cc9626d6be1e2bf0798786fad3047f04cda7c60).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Origin OETH Integration Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/origin-oeth-integration-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

