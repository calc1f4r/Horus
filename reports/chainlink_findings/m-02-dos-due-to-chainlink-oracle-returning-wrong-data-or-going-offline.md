---
# Core Classification
protocol: Ouroboros_2024-12-06
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 45950
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2024-12-06.md
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
  - Pashov Audit Group
---

## Vulnerability Title

[M-02] DoS due to Chainlink oracle returning wrong data or going offline

### Overview


The Chainlink oracle price feed has a high impact bug that can cause the `EthPriceFeed.fetchEthPrice()` function to fail, resulting in incorrect data or the system going offline. This can have severe consequences, such as causing the system to become uncollateralized or users losing their collateral. The current solution to prevent this is for the guardian to manually reset the system, but this is not ideal as it requires quick action, needs to be repeated after every interaction, and introduces a centralization risk. It is recommended to use a fallback oracle in case of failure or extreme price movements to prevent these issues.

### Original Finding Content

## Severity

**Impact:** High

**Likelihood:** Low

## Description

Chainlink oracle price feed can return wrong data or go offline in extreme cases, which will provoke the `EthPriceFeed.fetchEthPrice()` function to revert. This function is called to execute the main actions of the system, such as redeeming collateral, opening a position, adding collateral, closing a position, claiming escrow, and liquidating a position.

The impact of transaction reverting is especially severe in the case of liquidations, which might cause the system to be uncollateralized, and adding collateral, which might cause users to lose their collateral when the price feed gets back online.

In order to prevent this, the system relies on the guardian calling the `resetBreaker` function to manually provide the new price and set the oracle status to the working state. However, this is not ideal, as:

- Requires the guardian to act quickly after the oracle goes offline.
- Until the oracle goes back online, the process has to be repeated after every interaction with the system, as every call will change the oracle status again to not working.
- Introduces a centralization vector.

Another issue is that price movements greater than 50% are considered invalid, which prevents the system from reacting quickly to extreme price movements.

## Recommendations

Use a fallback oracle to query the price in case the main oracle fails or the price movement is too high.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Ouroboros_2024-12-06 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Ouroboros-security-review_2024-12-06.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

