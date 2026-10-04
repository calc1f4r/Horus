---
# Core Classification
protocol: Biconomy
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 46524
audit_firm: Cantina
contest_link: https://cantina.xyz/portfolio/be510b38-8e1c-4815-bde1-d276b3fa7b36
source_link: https://cdn.cantina.xyz/reports/cantina_biconomy_november2024.pdf
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
  - dexes
  - bridge
  - cdp
  - services
  - yield_aggregator

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Chinmay Farkya
---

## Vulnerability Title

In Nexus:checkERC7739Support() only the last validator is checked to determine if the smart account supports ERC7739 

### Overview


The report discusses a bug in the Nexus.sol file, specifically in the isValidSignature() function. This function is responsible for checking if the smart account supports ERC7739, by looping over all installed validators and returning true if any of them support 7739 flows. However, the bug causes the logic to only check for support from the last validator in the list, as the while loop used does not increment and only runs one iteration. The recommendation is to add a getNext() method to fetch the corresponding mapping value of an entry and behave as an increment operation inside the while loop. This will ensure that the loop goes through the entire list of validators. The bug has been fixed in PR 216 by Biconomy and Cantina Managed. The risk of this bug is considered low.

### Original Finding Content

## Context
**File:** Nexus.sol  
**Lines:** L336-L350

## Description
The `isValidSignature() → checkERC7739Support()` flow in `Nexus.sol` is meant to determine if the smart account supports ERC7739. Nexus achieves this by looping over all the installed validators and returning true if any of the validators show support for 7739 flows.

However, the current logic only checks for one validator (i.e., the last entry in the sentinel list). This is due to the implementation using a while loop that starts from the sentinel entry but never increments the loop, resulting in only one iteration being executed before the loop ends.

## Recommendation
To resolve this issue, add the `getNext()` method from `SentinelList.sol#L54` to fetch the corresponding mapping value of an entry. This method will act as an increment operation within the while loop, allowing it to iterate over the complete list of validators.

## Status
- **Biconomy:** Fixed in PR 216.
- **Cantina Managed:** Fixed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Cantina |
| Protocol | Biconomy |
| Report Date | N/A |
| Finders | Chinmay Farkya |

### Source Links

- **Source**: https://cdn.cantina.xyz/reports/cantina_biconomy_november2024.pdf
- **GitHub**: N/A
- **Contest**: https://cantina.xyz/portfolio/be510b38-8e1c-4815-bde1-d276b3fa7b36

### Keywords for Search

`vulnerability`

