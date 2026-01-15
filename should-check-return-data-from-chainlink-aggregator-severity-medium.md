---
# Core Classification
protocol: Coinlend
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20930
audit_firm: AuditOne
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-29-Coinlend.md
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
  - AuditOne
---

## Vulnerability Title

Should check return data from chainlink aggregator Severity: Medium

### Overview


This bug report is about the Coinlend.sol contract, which fetches the asset price from a Chainlink aggregator using the latestRoundData function. The issue is that there are no checks on roundID, meaning that stale prices could put funds at risk. Chainlink's documentation states that the function does not error if no answer has been reached but returns 0, causing an incorrect price fed to the PriceOracle. This introduces risk to the system, as the external oracle could become outdated or fail to be maintained, resulting in outdated data being fed to the index price calculations of the liquidity.

The recommendation is to add checks on the return data with proper revert messages if the price is stale or the round is incomplete. This would help to ensure that the system is using the most up to date data and that funds are not put at risk.

### Original Finding Content

**Description:**

 The latestRoundData function in the contract Coinlend.sol fetches the asset price from a Chainlink aggregator using the latestRoundData function. However, there are no checks on roundID.

Stale prices could put funds at risk. According to Chainlink's documentation, This function does not error if no answer has been reached but returns 0, causing an incorrect price fed to the PriceOracle. The external Chainlink oracle, which provides index price information to the system, introduces risk inherent to any dependency on third-party data sources. For example, the oracle could fall behind or otherwise fail to be maintained, resulting in outdated data being fed to the index price calculations of the [liquidity.](https://github.com/code-423n4/2021-08-notional-findings/issues/18)

**Recommendations:** 

Consider to add checks on the return data with proper revert messages if the price is stale or the round is incomplete.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | AuditOne |
| Protocol | Coinlend |
| Report Date | N/A |
| Finders | AuditOne |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-06-29-Coinlend.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

