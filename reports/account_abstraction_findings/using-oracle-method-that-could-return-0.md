---
# Core Classification
protocol: Boba Network
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57677
audit_firm: Zokyo
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba Network.md
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
  - zokyo
---

## Vulnerability Title

Using oracle method that could return 0

### Overview


A bug has been found in the Boba Deposit Paymaster contract. The function "getTokenValueOfEth" is not working properly and is causing issues with the application. The function uses oracles to retrieve values and token decimals, but the chosen oracle, BobaStraw, is not functioning correctly. It is recommended to use the function "latestRoundData" instead and to check for fresh data by verifying the updatedAt and answeredInRound values. This issue has been resolved.

### Original Finding Content

**Description**

In contract Boba Deposit Paymaster, function "getTokenValueOfEth" is translating a given value amount of ethereum into the underlying token amount, for that the business logic is using oracles to query for values and different token decimals, oracles will be chosen by the admin of the contract however we expect that most preferred oracles will be BobaStraw, as BobaStraw is a fork of chainlink as it is saying in it's documentation, we noticed that the used function to query the oracles is the function "latestAnswer" which based on it's implementation does not revert if the price returned it's staled or if it can not retrieve the price it will simply return 0 which will break all the logic of the application resulting in a token cost of and and free transactions.

**Recommendation**

Use function "latestRoundData" instead of "latestAnswer" and ensure you are receiving fresh data from it by sanity checking updatedAt and answeredInRound returned values.

**Re-audit comment**

Resolved

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Zokyo |
| Protocol | Boba Network |
| Report Date | N/A |
| Finders | zokyo |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-08-07-Boba Network.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

