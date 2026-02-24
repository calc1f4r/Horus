---
# Core Classification
protocol: GMX
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 27181
audit_firm: Guardian Audits
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-10-24-GMX.md
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.20
financial_impact: high

# Scoring
quality_score: 1
rarity_score: 1

# Context Tags
tags:

# Audit Details
report_date: unknown
finders_count: 1
finders:
  - Guardian Audits
---

## Vulnerability Title

GLOBAL-2 | Delay Limit Success

### Overview


This bug report is about a vulnerability found in the GMX exchange. The vulnerability is related to the try/catch block in each handler not catching any errors related to a Panic exception or custom revert. This vulnerability allows for a number of bugs and exploits on the exchange. For example, a user could create a LimitIncrease order that exceeds the max reserved usd, which would cause the order to revert but remain in the order store. This would enable the user to deposit enough reserves later when conditions are favorable, allowing them to execute the order and close their position for a risk free profit.

The recommendation for this vulnerability is to utilize catch (bytes memory lowLevelData) to catch Panic exceptions and custom reverts. The GMX team has implemented this recommendation.

### Original Finding Content

**Description - [PoC1](https://github.com/GuardianAudits/GMX/blob/af740b1972788f429219d1381183c68b244e00d8/test/guardianTestSuite/testPOCS.js#L522) [PoC2](https://github.com/GuardianAudits/GMX/blob/af740b1972788f429219d1381183c68b244e00d8/test/guardianTestSuite/testPOCS.js#L841)**


The try/catch block in each handler does not catch any errors related to a [Panic exception](https://docs.soliditylang.org/en/v0.8.16/control-structures.html#panic-via-assert-and-error-via-require) or custom revert. This enables a number of bugs and exploits on the exchange.

Most notably, It is possible to create a `LimitIncrease` order that exceeds the max reserved usd, therefore reverting on execution but remaining in the order store, then when conditions are favorable the user can deposit enough reserves so their order gets executed.

Consider the following scenario:
- The current price of ETH is $2,000
- User A creates a `LimitIncrease` long order for ETH at $2,000 in block 100 with usd size larger than allowable
- User A’s order reverts due to insufficient reserves but remains in the order store
- 20 blocks later ether is now $2,100
- User A deposits enough reserves to execute their `LimitIncrease`
- The `LimitIncrease` long order now executes with the prices from block 101
- User A closes their position making risk free profit

**Recommendation**

Utilize `catch (bytes memory lowLevelData)` to catch Panic exceptions and custom reverts.

**Resolution**

GMX Team: The recommendation was implemented.

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 1/5 |
| Rarity Score | 1/5 |
| Audit Firm | Guardian Audits |
| Protocol | GMX |
| Report Date | N/A |
| Finders | Guardian Audits |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Guardian Audits/2022-10-24-GMX.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

