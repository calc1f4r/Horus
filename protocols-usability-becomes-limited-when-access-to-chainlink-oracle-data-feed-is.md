---
# Core Classification
protocol: Vaultka
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 37035
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
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
  - Zokyo
---

## Vulnerability Title

Protocol’s Usability Becomes Limited When Access To Chainlink Oracle Data Feed Is Blocked

### Overview


This bug report is about a medium severity issue in the function getLatestData in a smart contract called VaultkaV2GMXHandler.sol. This function takes the address of a token as input, queries a chainlink aggregator for the token's price, and returns the price in the correct decimal precision. However, there is a problem with this function because it relies on a chainlink multisig, which can block access to price feeds at any time. This can cause the function to fail and potentially deny service to users. The recommendation is to add a fallback logic in case access to the chainlink oracle data feed is denied.

### Original Finding Content

**Severity** - Medium

**Status** - Acknowledge

**Description**

The function getLatestData inside VaultkaV2GMXHandler.sol at L373 takes the address of the token as input , queries the chainlink aggregator to fetch the price and returns the price in correct decimal precision.
As https://blog.openzeppelin.com/secure-smart-contract-guidelines-the-dangers-of-price-oracles/ mentions, it is possible that Chainlink’s multisigs can immediately block access to price feeds at will. When this occurs, executing latestRoundData reverts , which causes denial of service if the  function getLatestData gets called to fetch the price of the token.

**Recommendation**:

The logic for getting the token's price (inside getLatestData ) from the Chainlink oracle data feed should be placed in the try block while some fallback logic when the access to the Chainlink oracle data feed is denied should be placed in the catch block.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Vaultka |
| Report Date | N/A |
| Finders | Zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-11-09-Vaultka.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

