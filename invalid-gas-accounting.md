---
# Core Classification
protocol: ZK Stack VM1.5 Diff Audit
chain: everychain
category: uncategorized
vulnerability_type: unknown

# Attack Vector Details
attack_type: unknown
affected_component: smart_contract

# Source Information
source: solodit
solodit_id: 36566
audit_firm: OpenZeppelin
contest_link: none
source_link: https://blog.openzeppelin.com/zk-stack-vm1.5-diff-audit
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

Invalid Gas Accounting

### Overview


There is a problem with the bootloader code that is causing transactions to fail when using a paymaster and consuming pubdata. This is due to the order in which parameters are being passed, causing an incorrect estimation of pubdata cost and gas limit. The issue has been identified and a solution has been proposed in a recent pull request.

### Original Finding Content

The bootloader reverses the [last two parameters](https://github.com/matter-labs/era-contracts/blob/705a4c8946c1ddbd50dbc637010e6223b3865dab/system-contracts/bootloader/bootloader.yul#L1599-L1600) when calling `ZKSYNC_NEAR_CALL_callPostOp`. This causes the [pubdata allowance check](https://github.com/matter-labs/era-contracts/blob/705a4c8946c1ddbd50dbc637010e6223b3865dab/system-contracts/bootloader/bootloader.yul#L2340) to significantly overestimate the pubdata cost and underestimate the gas limit. Consequently, transactions that specify a paymaster and consume pubdata would likely fail this check, incorrectly reverting the `postTransaction` changes.


Consider correcting the parameter order.


***Update:** Resolved in [pull request \#316](https://github.com/matter-labs/era-contracts/pull/316).*

### Metadata

| Field | Value |
|-------|-------|
| Impact | HIGH |
| Quality Score | 0/5 |
| Rarity Score | 0/5 |
| Audit Firm | OpenZeppelin |
| Protocol | ZK Stack VM1.5 Diff Audit |
| Report Date | N/A |
| Finders | OpenZeppelin |

### Source Links

- **Source**: https://blog.openzeppelin.com/zk-stack-vm1.5-diff-audit
- **GitHub**: N/A
- **Contest**: N/A

### Keywords for Search

`vulnerability`

