---
# Core Classification
protocol: Beefy Zap Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 32754
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/beefy-zap-audit-1
github_link: none

# Impact Classification
severity: high
impact: security_vulnerability
exploitability: 0.00
financial_impact: high

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

External Call to Permit2 Allows Stealing Users' Tokens

### Overview


This bug report discusses a vulnerability in the BeefyZapRouter contract that allows an attacker to steal tokens from another user during an order execution. This is possible by making an external call to the Permit2 contract using a valid order/signature pair from a different user. The suggested solution is to disallow any external calls to the Permit2 contract in both steps and relaying executions. This issue has been resolved in a recent update to the BeefyZapRouter contract.

### Original Finding Content

During an order execution, it is possible to [make arbitrary external calls](https://github.com/beefyfinance/beefy-zap/blob/addd5741a520b10924f1f26cc45208ff5fa88139/contracts/zaps/BeefyZapRouter.sol#L137) to any `stepTarget` except the token manager. A vulnerability arises when setting `stepTarget` equal to the `Permit2` address, which allows an attacker to make a call from the router to `Permit2` using a valid order/signature pair from another benign user.


This results in the transfer of all tokens from the benign user to the router during the attacker's order execution, enabling them to steal all the tokens from the order.


Consider disallowing any external calls to `Permit2` in both steps and relaying executions.


***Update:** Resolved in [pull request #6](https://github.com/beefyfinance/beefy-zap/pull/6) at commit [6ba7a7e](https://github.com/beefyfinance/beefy-zap/pull/6/commits/6ba7a7e176b423bd0159e69b65778dcb2378633c). External calls to the `Permit2` contract have been prohibited.*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | Beefy Zap Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/beefy-zap-audit-1
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

