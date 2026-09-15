---
# Core Classification
protocol: Nexus_2024-11-29
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 44987
audit_firm: Pashov Audit Group
contest_link: none
source_link: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
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

[M-01] LayerZero Fee refunds cannot be processed

### Overview


This bug report is about three contracts, `DepositUSD`, `DepositETHBera`, and `DepositUSDBera`, that are supposed to receive refunds for excess fees in a messaging protocol called LayerZero. However, these contracts are unable to receive the refunds and cause an error when they are sent. The report suggests adding a `receive()` function to these contracts to fix the issue.

### Original Finding Content

## Severity

**Impact:** Medium

**Likelihood:** Medium

## Description

The `DepositUSD`, `DepositETHBera`, and `DepositUSDBera` contracts are intended to serve as the refund address for LayerZero, the messaging protocol responsible for paying fees in the native gas token. However, these contracts are unable to receive these refunds, causing a revert when excess fees are sent.

Although the `DepositUSD`, `DepositETHBera`, and `DepositUSDBera` contracts act as implementation contracts, the refunds are transferred to the Proxy contract. The standard [ERC1697Proxy](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/proxy/ERC1967/ERC1967Proxy.sol) implements the fallback function to forward all calls, making a delegate call to the implementation contract.

Therefore, it is expected that the implementation contract should provide functionality to receive native gas transfers.

## Recommendation

Consider adding `receive()` functions to the `DepositUSD`, `DepositETHBera`, and `DepositUSDBera` contracts if these contracts are intended to receive users' refund excess fees.

### Metadata

| Field | Value |
|-------|-------|
| Impact | MEDIUM |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | Pashov Audit Group |
| Protocol | Nexus_2024-11-29 |
| Report Date | N/A |
| Finders | Pashov Audit Group |

### Source Links

- **Source**: https://github.com/pashov/audits/blob/master/team/md/Nexus-security-review_2024-11-29.md
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

