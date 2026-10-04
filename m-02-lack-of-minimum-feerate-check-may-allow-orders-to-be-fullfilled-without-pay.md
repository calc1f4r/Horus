---
# Core Classification
protocol: FactcheckDotFun
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 57708
audit_firm: Kann
contest_link: none
source_link: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/FactcheckDotFun.md
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
  - Kann
---

## Vulnerability Title

[M-02] Lack of Minimum feeRate check may allow orders to be fullfilled without paying any fees

### Overview


The settleMatchedOrders function in the backend allows for the settlement of matched orders that were created and matched off-chain. However, there is a bug where the contract does not enforce a minimum fee rate, allowing for orders with extremely low fee rates (e.g. 1 wei) to be matched and settled. This can result in users bypassing protocol fees, which undermines the protocol's revenue and fairness. This bug can also be exploited by malicious or careless matching, leading to widespread abuse of low-fee orders. To fix this issue, the team recommends introducing a minFeeRate variable that can be configured by protocol administrators and enforced during order validation. The team has acknowledged this bug and is working on a solution.

### Original Finding Content

## Severity

Medium

## Description

The settleMatchedOrders function allows the backend to settle matched orders that
were created and matched off-chain. While the contract enforces an upper bound for feeRate, it does
not enforce a minimum feerate.
This omission allows orders with extremely low feeRate values(e.g.,1wei)to be matched and settled.
As aresult, users can effectively bypass protocol fees altogether, undermining protocol revenue and
fairness.
Since order matching is handled off-chain and executed on-chain by an address with the BACK
END_ROLE, malicious or careless matching could lead to widespread abuse of low-fee orders.

## Recommendation

Introduce a minFeeRate variable, configurable by protocol administrators, and
enforce it during order validation to ensure all orders pay at least a minimum protocol fee:

```solidity
require(order.feeRate >= minFeeRate, "Fee rate below minimum allowed");
```

## Team Response

Acknowledged

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Kann |
| Protocol | FactcheckDotFun |
| Report Date | N/A |
| Finders | Kann |

### Source Links

- **Source**: https://github.com/Kann-Audits/Kann-Audits/blob/main/reports/md-format/private-audits-reports/FactcheckDotFun.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

