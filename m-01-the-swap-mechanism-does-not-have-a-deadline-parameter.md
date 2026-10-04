---
# Core Classification
protocol: Bloom
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 20595
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-05-01-Bloom.md
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
  - Pashov
---

## Vulnerability Title

[M-01] The swap mechanism does not have a deadline parameter

### Overview


This bug report is about a transaction deadline mechanism for swap mechanisms. If a user sets a low gas fee for a transaction, it can remain pending in the mempool for a long time. If the average gas fees drop low enough for the transaction to be executed, the price of the assets may have changed drastically, resulting in a big slippage or maximum allowed one. This is especially worse when there is no slippage. 

Therefore, it is recommended to add a `deadline` timestamp parameter to the `SwapFacility::_swap` method and revert the transaction if the expiry has passed. This would help prevent the user from receiving a value that is much lower than what they expected.

### Original Finding Content

**Impact:**
High, as the swap might forcefully result in a big slippage (or maximum allowed one)

**Likelihood:**
Low, as it requires special conditions

**Description**

Swap mechanisms should implement a transaction deadline mechanism, due to the following attack vector:

1. Alice wants to execute a swap, sets slippage to 10% and sends a transaction to the mempool, but with a very low gas fee
2. Miners/validators see the transaction but the fe is not attractive, so the transaction is stale and pending for a long time
3. After a week (let's say) the average gas fees drop low enough for the miners/validators to execute the transaction but the price of the assets has changed drastically
4. Now the value Alice receives is much lower and possibly close to the max slippage she set.

The effects are even worse when there is no slippage as it is the current case in the protocol.

**Recommendations**

Add a `deadline` timestamp parameter to the `SwapFacility::_swap` method and revert the transaction if the expiry has passed.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Bloom |
| Report Date | N/A |
| Finders | Pashov |

### Source Links

- **Source**: https://github.com/solodit/solodit_content/blob/main/reports/Pashov/2023-05-01-Bloom.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

