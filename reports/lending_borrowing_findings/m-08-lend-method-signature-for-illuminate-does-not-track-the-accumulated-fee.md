---
# Core Classification
protocol: Illuminate
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 25292
audit_firm: Code4rena
contest_link: https://code4rena.com/reports/2022-06-illuminate
source_link: https://code4rena.com/reports/2022-06-illuminate
github_link: https://github.com/code-423n4/2022-06-illuminate-findings/issues/208

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
  - cdp
  - yield
  - yield_aggregator
  - cross_chain

# Audit Details
report_date: unknown
finders_count: 0
finders:
---

## Vulnerability Title

[M-08] Lend method signature for illuminate does not track the accumulated fee

### Overview


A bug has been reported in the Illuminate lending method which prevents it from tracking the fees[u] after each transaction. This means that the admin cannot withdraw the fees using the withdrawFee method and has to wait at least 3 days to receive the fees through the withdraw method.

To mitigate this issue, it is recommended to add the amount of fee after each transaction into fees[u], like other lending methods. This can be done by adding the following line of code: fees[u] += calculateFee(a);

This bug has been confirmed by sourabhmarathe of Illuminate.

### Original Finding Content

_Submitted by Kumpa, also found by cccz, cryptphi, hansfriese, jah, kenzo, kirk-baird, Metatron, pashov, and poirots_

Normally the amount of fees after `calculateFee` should be added into `fees[u]` so that the admin could withdraw it through `withdrawFee`. However, illuminate ledning does not track `fees[u]`. Therefore, the only way to get fees back is through `withdraw` which admin needs to wait at least 3 days before receiving the fees.

### Recommended Mitigation Steps

Add the amount of fee after each transaction into `fees[u]` like other lending method.\
for example: `  fees[u] += calculateFee(a); `

**[sourabhmarathe (Illuminate) confirmed](https://github.com/code-423n4/2022-06-illuminate-findings/issues/208)**



***



### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Code4rena |
| Protocol | Illuminate |
| Report Date | N/A |
| Finders | N/A |

### Source Links

- **Source**: https://code4rena.com/reports/2022-06-illuminate
- **GitHub**: https://github.com/code-423n4/2022-06-illuminate-findings/issues/208
- **Contest**: https://code4rena.com/reports/2022-06-illuminate

### Keywords for Search

`vulnerability`

